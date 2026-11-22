"""Codex PreToolUse guard for direct Git, glab, and recursive deletion commands."""

import json
import os
import re
import sys
from urllib.parse import parse_qsl, unquote


GITLAB_UNKNOWN = (
    "Could not verify this GitLab API call. Use a REST endpoint with documented glab flags."
)
GITLAB_WRITE = (
    "This GitLab write is outside the hook's permitted board, issue, label, and retry operations. "
    "Read current state and show the exact target and proposed change for manual review."
)
GITLAB_DELETE = "GitLab deletion is blocked. Review the resource and run any intended deletion manually."

# Preserve encoded namespace slashes inside the locator. Match the actual route
# structure so a similar path such as jobs/123/erase cannot qualify as a retry.
GITLAB_SLUG = r"[A-Za-z0-9_][A-Za-z0-9_.-]*"
GITLAB_LOCATOR = rf"{GITLAB_SLUG}(?:%2[fF]{GITLAB_SLUG})*"
PROJECT = rf"projects/(?:{GITLAB_LOCATOR}|:id|:fullpath)"
GROUP = rf"groups/(?:{GITLAB_LOCATOR}|:group)"
BOARD_SCOPE = rf"(?:{PROJECT}|{GROUP})"
ID = r"[1-9][0-9]*"
GITLAB_WRITE_ROUTES = {
    "POST": re.compile(
        rf"{BOARD_SCOPE}/(?:boards(?:/{ID}/lists)?|labels)"
        rf"|{PROJECT}/(?:issues(?:/{ID}/notes)?|(?:jobs|pipelines)/{ID}/retry)"
    ),
    "PUT": re.compile(
        rf"{BOARD_SCOPE}/(?:boards/{ID}(?:/lists/{ID})?|labels/{ID})"
        rf"|{PROJECT}/issues/{ID}"
    ),
}


# Keep quoted words together, and handle common pipelines and redirections.
REDIRECTION = r"(?P<redirect>\d*(?:>>?|<)&?)"
POSIX_LEXER = re.compile(
    r"(?P<comment>\#[^\n]*)|(?P<separator>[;&|()\n])|" + REDIRECTION
    + r'''|(?P<word>(?:'[^']*'|"(?:\\.|[^"\\])*"|\\[\s\S]|[^\s'";&|()<>\\])+)'''
)
WINDOWS_LEXER = re.compile(
    r"(?P<comment>\#[^\n]*)|(?P<separator>[;&|()\n])|" + REDIRECTION
    + r'''|(?P<word>(?:'(?:''|[^'])*'|"(?:`.|[^"`])*"|`[\s\S]|[^\s'";&|()<>`])+)'''
)
POSIX_PARTS = re.compile(r"""'([^']*)'|"((?:\\.|[^"\\])*)"|\\([\s\S])|([^'"\\]+)""")
WINDOWS_PARTS = re.compile(r"""'((?:''|[^'])*)'|"((?:`.|[^"`])*)"|`([\s\S])|([^'"`]+)""")


def shell_words(command, windows):
    """Yield words for each simple command in a shell tool call."""
    lexer, parts = (
        (WINDOWS_LEXER, WINDOWS_PARTS) if windows else (POSIX_LEXER, POSIX_PARTS)
    )
    words = []
    redirect_target = False
    for token in lexer.finditer(command):
        if token.lastgroup == "separator":
            if words:
                yield words
                words = []
            redirect_target = False
        elif token.lastgroup == "redirect":
            redirect_target = True
        elif token.lastgroup == "word":
            if redirect_target:
                redirect_target = False
                continue
            value = []
            for part in parts.finditer(token.group()):
                single, double, escaped, bare = part.groups()
                if single is not None:
                    value.append(single.replace("''", "'") if windows else single)
                elif double is not None:
                    value.append(re.sub(r"`(.)" if windows else r'\\(["\\$`])', r"\1", double))
                elif escaped is not None:
                    if escaped != "\n":
                        value.append(escaped)
                else:
                    value.append(bare)
            word = "".join(value)
            if word or token.group() in {"''", '\"\"'}:
                words.append(word)
    if words:
        yield words


def executable(word):
    return re.split(r"[/\\]", word)[-1].lower().removesuffix(".exe")


def option(args, *names):
    return any(arg.split("=", 1)[0] in names for arg in args)


def short_option(args, letter):
    return any(re.fullmatch(r"-[a-zA-Z]+", arg) and letter in arg[1:] for arg in args)


def clean_is_preview(flags):
    dry_run = False
    args = iter(flags)
    for arg in args:
        name, equals, _ = arg.partition("=")
        if name == "--exclude":
            if not equals:
                next(args, None)
        elif arg.startswith("--"):
            if arg == "--dry-run":
                dry_run = True
            elif arg not in {"--force", "--quiet"}:
                # Reject interactive mode, negations and abbreviated options.
                return False
        elif arg.startswith("-"):
            letters, exclude, pattern = arg[1:].partition("e")
            if set(letters) - set("dfnqxX"):
                return False
            if exclude and not pattern:
                next(args, None)
            dry_run = dry_run or "n" in letters
    return dry_run


def git_denial(args):
    # Skip Git's global options before identifying the subcommand.
    while args and args[0].startswith("-"):
        name = args[0].split("=", 1)[0]
        takes_value = name in {"-C", "-c", "--git-dir", "--work-tree",
                               "--namespace", "--super-prefix", "--config-env"}
        args = args[2:] if takes_value and "=" not in args[0] else args[1:]
    if not args:
        return None
    action, *values = args
    if values in (["-h"], ["--help"]):
        return None
    flags = values[:values.index("--")] if "--" in values else values
    force = option(flags, "--force") or short_option(flags, "f")

    if action == "push" and (
        force or option(flags, "--force-with-lease", "--force-if-includes",
                        "--delete", "--mirror", "--prune") or short_option(flags, "d")
        or any(arg.startswith("+") or (arg.startswith(":") and len(arg) > 1)
               for arg in values)
    ):
        return "Git push can overwrite or delete remote refs. Review the target and push normally."
    if action == "clean" and not clean_is_preview(flags):
        return "Git clean can permanently delete untracked files. Preview with git clean -n."
    if action == "reset" and option(flags, "--hard", "--merge", "--keep"):
        return "Git reset can change tracked files. Inspect git status and preserve your changes first."
    if action == "restore" and (
        not (option(flags, "--staged") or short_option(flags, "S"))
        or option(flags, "--worktree") or short_option(flags, "W")
    ):
        return "Git restore would replace working tree files. Inspect git diff or unstage only."
    checkout_paths = action == "checkout" and (
        "--" in values or "." in values
        or option(flags, "--ours", "--theirs", "--merge", "--pathspec-from-file")
        or any(flag in flags for flag in ("-2", "-3"))
        or (sum(not arg.startswith("-") for arg in flags) >= 2 and not short_option(flags, "b"))
    )
    if action in {"checkout", "switch"} and (
        force or option(flags, "--discard-changes") or short_option(flags, "B")
        or short_option(flags, "C") or checkout_paths
    ):
        return "Git checkout or switch can discard changes or overwrite a branch. Inspect git status first."
    if action == "branch" and (
        (force and not option(flags, "--list"))
        or any(short_option(flags, flag) for flag in "DMC")
    ):
        return "This Git branch command can overwrite or delete a ref. Review the branch and its commits."
    if action in {"filter-branch", "filter-repo", "update-ref"}:
        return "This Git command directly rewrites history or refs. Review and run it manually."
    if (
        action == "stash" and values[:1] in (["drop"], ["clear"])
        or action == "reflog" and values[:1] in (["delete"], ["drop"], ["expire"])
        or action == "worktree" and values[:1] == ["remove"] and force
        or action == "rm" and force
        or action == "tag" and (force or option(flags, "--delete") or short_option(flags, "d"))
        or action == "gc" and "--prune=now" in flags
        or action == "prune"
    ):
        return "This Git command can permanently discard saved work. Review and run it manually."
    return None


def glab_api_denial(args):
    methods, endpoints = [], []
    fields = False
    paginate = False
    arg_iter = iter(args)
    for arg in arg_iter:
        if arg == "--":
            endpoints.extend(arg_iter)
            break
        if not arg.startswith("-"):
            endpoints.append(arg)
            continue
        flag, equals, value = arg.partition("=")
        if not flag.startswith("--"):
            # pflag accepts clusters of booleans followed by a value flag,
            # e.g. -iXGET and -ifstate=open.
            short = flag[1:].lstrip("ih")
            if not short:
                continue
            flag, attached = short[0], short[1:]
            if attached:
                value = attached + (equals + value if equals else "")
                equals = "="
        if flag == "--paginate":
            paginate = True
            continue
        if flag in {"--silent", "--include", "--help"}:
            continue
        if flag in {"--input", "--form"}:
            return "GitLab request bodies must use visible -f or -F fields for permitted writes."
        if flag not in {"X", "F", "f", "H", "--method", "--field", "--raw-field",
                        "--hostname", "--header", "--output", "--placeholder"}:
            return GITLAB_UNKNOWN
        value = value if equals else next(arg_iter, "")
        if not value or (not equals and value.startswith("-")):
            return GITLAB_UNKNOWN
        if flag in {"X", "--method"}:
            methods.append(value.upper())
        elif flag in {"F", "f", "--field", "--raw-field"}:
            fields = True
            if value.partition("=")[0].split("[", 1)[0].strip().lower() == "_method":
                return "GitLab HTTP method overrides are blocked. Use --method."
        elif flag in {"H", "--header"} and value.partition(":")[0].strip().lower() in {
            "x-http-method", "x-http-method-override", "x-method-override",
        }:
            return "GitLab HTTP method overrides are blocked. Use --method."
    if "DELETE" in methods:
        return GITLAB_DELETE
    if len(methods) > 1:
        return "Use a single explicit GitLab HTTP method."
    if not endpoints and args in ([], ["--help"], ["-h"]):
        return None
    if len(endpoints) != 1 or not re.match(r"^/?[A-Za-z0-9]", endpoints[0]):
        return GITLAB_UNKNOWN
    path, _, query = endpoints[0].partition("?")
    decoded_path = unquote(path).strip("/").lower()
    if decoded_path == "graphql" or decoded_path.endswith("/graphql"):
        return "Use GitLab REST GET for this lookup. GraphQL can submit mutations through POST."
    if any(key.split("[", 1)[0].strip().lower() == "_method" for key, _ in parse_qsl(query)):
        return "GitLab HTTP method overrides are blocked. Use --method."
    if fields and not methods:
        return "GitLab fields default to POST. Use explicit GET for a lookup or POST for a permitted write."
    method = methods[0] if methods else "GET"
    if method in {"GET", "HEAD"}:
        return None
    route = GITLAB_WRITE_ROUTES.get(method)
    if route and not paginate and route.fullmatch(path.removeprefix("/").removesuffix("/")):
        return None
    return GITLAB_WRITE


def glab_without_repo_flags(args):
    remaining = []
    flags = iter(args)
    for arg in flags:
        if arg == "--":
            remaining.extend(flags)
            break
        if arg in {"-R", "--repo"}:
            next(flags, None)
        elif not arg.startswith(("-R", "--repo=")):
            remaining.append(arg)
    return remaining


def glab_denial(args):
    if args[:1] == ["api"]:
        return glab_api_denial(args[1:])
    args = glab_without_repo_flags(args)
    if len(args) < 2:
        return None
    command, action, *values = args
    if values in (["-h"], ["--help"]):
        return None
    if command in {"ci", "pipe", "pipeline"}:
        if action == "retry" and not (len(values) == 1 and re.fullmatch(ID, values[0])):
            return "Use glab ci retry with one numeric job ID. Inspect that job and its trace first."
        if action == "view":
            return "Use glab ci get, glab ci trace, or REST GET. The interactive view can cancel or run jobs."
        if action in {"cancel", "run", "run-trig", "run-trigger", "erase", "play", "trigger"}:
            return "Only targeted GitLab CI retries are permitted. Use read commands to inspect the pipeline."
    if (command, action) == ("schedule", "run"):
        return "Starting a scheduled GitLab pipeline is outside the retry policy."
    if action in {"delete", "remove", "archive", "transfer", "revoke", "unregister", "erase", "prune"}:
        return GITLAB_DELETE
    return None


def command_denial(command, windows, depth=0):
    """Check common shell wrappers without evaluating the command."""
    if depth >= 8:
        return "The command has too many nested shell wrappers to check. Run a direct command."
    for words in shell_words(command, windows):
        while words and (
            words[0] in {"if", "then", "else", "elif", "do", "!", "{", "command",
                         "builtin", "exec", "env", "sudo", "nohup", "."}
            or re.match(r"^[A-Za-z_]\w*=", words[0])
        ):
            words = words[1:]
        if not words:
            continue
        program, args = executable(words[0]), words[1:]
        result = None
        if program == "git":
            result = git_denial(args)
        elif program == "glab":
            result = glab_denial(args)
        elif program in {"bash", "sh", "zsh", "dash", "pwsh", "powershell", "cmd"}:
            markers = {"-c", "-command", "/c"} if program in {"pwsh", "powershell", "cmd"} else {"-c", "-lc"}
            for index, arg in enumerate(args[:-1]):
                if arg.lower() in markers:
                    native = program in {"pwsh", "powershell", "cmd"}
                    script = " ".join(args[index + 1:]) if native else args[index + 1]
                    result = command_denial(script, native, depth + 1)
                    break
        elif program in {"rm", "remove-item", "ri", "rmdir", "rd", "del", "erase"}:
            recursive = (option(args, "--recursive", "-R") or short_option(args, "r")
                         or "-recurse" in [arg.lower() for arg in args]
                         or "/s" in [arg.lower() for arg in args])
            git_metadata = any(".git" in re.split(r"[/\\]", arg.lower()) for arg in args)
            preview = windows and "-whatif" in [arg.lower() for arg in args]
            if (git_metadata or recursive) and not preview:
                result = "This deletion can erase Git metadata or a directory tree. Review the paths and run it manually."
        if result:
            return result
    return None


def main():
    try:
        payload = json.load(sys.stdin)
        command = payload["tool_input"]["command"]
        if not isinstance(command, str):
            raise TypeError("command must be a string")
        reason = command_denial(command, os.name == "nt")
    except (KeyError, TypeError, ValueError):
        reason = "Could not read the Codex shell hook input. Check the installed hook before retrying."
    if reason:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }}))


if __name__ == "__main__":
    main()
