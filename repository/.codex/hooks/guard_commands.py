"""Codex PreToolUse guard for direct Git, glab, and recursive deletion commands."""

import json
import os
import re
import sys
from urllib.parse import unquote


GITLAB_WRITE = (
    "GitLab API writes require manual execution. Read current state with REST GET "
    "and show the exact host, target, method, and proposed change."
)
GITLAB_UNKNOWN = (
    "Could not verify a read-only GitLab API call. Use a literal REST endpoint "
    "with GET or HEAD and documented flags."
)
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
        if flag in {"--paginate", "--silent", "--include", "--help"}:
            continue
        if flag in {"--input", "--form"}:
            return GITLAB_WRITE
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
        elif flag in {"H", "--header"} and value.partition(":")[0].strip().lower() in {
            "x-http-method", "x-http-method-override", "x-method-override",
        }:
            return GITLAB_WRITE
    if any(method not in {"GET", "HEAD"} for method in methods) or (fields and not methods):
        return GITLAB_WRITE
    if not endpoints and args in ([], ["--help"], ["-h"]):
        return None
    if len(endpoints) != 1 or not re.match(r"^/?[A-Za-z0-9]", endpoints[0]):
        return GITLAB_UNKNOWN
    path = unquote(endpoints[0]).split("?", 1)[0].rstrip("/").lower()
    if path == "graphql" or path.endswith("/graphql"):
        return "Use GitLab REST GET for this lookup. GraphQL can submit mutations through POST."
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
            if args[:1] == ["api"]:
                result = glab_api_denial(args[1:])
            elif len(args) >= 2 and args[1] in {
                "delete", "remove", "archive", "transfer", "revoke",
            }:
                result = "This GitLab CLI operation can remove remote resources. Review and run it manually."
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
