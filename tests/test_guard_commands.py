"""Regression tests for the Codex shell guard. Commands are inspected, never run."""

import runpy
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "repository/.codex/hooks/guard_commands.py"
command_denial = runpy.run_path(str(SCRIPT))["command_denial"]


class GitLabGuardTests(unittest.TestCase):
    def test_board_and_ci_work_is_allowed(self):
        commands = (
            "glab api --hostname gitlab.example -XGET -f 'scope[]=failed' "
            "--paginate projects/42/pipelines/123/jobs",
            "glab api projects/42/jobs/456/trace",
            "glab ci status -R group/project",
            "glab ci trace 456",
            "glab api --method POST projects/:fullpath/boards -f 'name=Team Kanban'",
            "glab api -iXPOST groups/:group/boards/7/lists -F label_id=9",
            "glab api -XPOST groups/parent%2fteam/labels -f name=Ready -f 'color=#000000'",
            "glab api -XPUT projects/42/boards/7 -f 'name=Board A'",
            "glab api -XPUT groups/42/boards/7/lists/20?position=2",
            "glab api -XPUT projects/42/labels/9 -f new_name=Review",
            "glab api -XPOST projects/42/issues -f 'title=Follow up'",
            "glab api -XPUT projects/42/issues/12 -f add_labels=Review -f remove_labels=Ready",
            "glab api -XPOST projects/42/issues/12/notes -f 'body=Reviewed'",
            "glab api --method=POST projects/:id/jobs/456/retry",
            "glab api projects/group%2Fproject/pipelines/123/retry -X POST",
            "glab ci retry 456 -R group/project",
            "glab ci --repo group/project retry 456",
        )
        for command in commands:
            with self.subTest(command=command):
                self.assertIsNone(command_denial(command, windows=False))

    def test_deletion_and_unverified_writes_are_denied(self):
        commands = (
            "glab api -XDELETE projects/42/boards/7/lists/20",
            "glab api projects/42/jobs/456/artifacts --method=DELETE",
            "glab api -XGET -XDELETE projects/42/issues/12",
            "glab api -XPOST projects/42/jobs/456/erase",
            "glab api -XPOST projects/42/pipelines/123/cancel",
            "glab api -XPOST projects/42/jobs/456/play",
            "glab api -XPOST projects/42/pipeline -f ref=main",
            "glab api -XPOST projects/42/archive",
            "glab api -XPUT projects/42 -F visibility=public",
            "glab api -XPUT projects/42/labels/9/promote",
            "glab api -XPOST projects/42/issues/12/move -F to_project_id=2",
            "glab api projects/42/boards -f name=Kanban",
            "glab api -XPOST graphql -f 'query=mutation { x }'",
            "glab api -XPOST projects/42/boards --input payload.json",
            "glab api -XPOST projects/42/boards --form name=Kanban",
            "glab api -XPOST projects/42/boards --paginate -f name=Kanban",
            "glab api -H 'X-HTTP-Method-Override: DELETE' projects/42/boards/7",
            "glab api -XPOST projects/42/boards -f _method=DELETE",
            "glab api -XPUT 'projects/42/boards/7?%5Fmethod=DELETE' -f name=Kanban",
            "glab api -XPOST projects/42/jobs/456%2Ferase/retry",
            "glab api -XPOST projects/42/pipelines/123/retry/../cancel",
            'glab api -XPOST "projects/42/jobs/$JOB_ID/retry"',
            "glab ci retry",
            "glab ci retry lint",
            "glab ci view",
            "glab ci run",
            "glab ci trigger list",
            "glab schedule run 42",
            "glab pipeline --repo group/project cancel 123",
            "glab pipe -Rgroup/project delete 123",
            "glab repo archive group/project",
            "glab repo prune group/project",
        )
        for command in commands:
            with self.subTest(command=command):
                self.assertIsNotNone(command_denial(command, windows=False))

    def test_powershell_gitlab_commands(self):
        program = r'& "C:\Program Files\GitLab\glab.exe"'
        self.assertIsNone(command_denial(f"{program} api projects/42/jobs/456/retry -X POST", windows=True))
        self.assertIsNotNone(command_denial(f"{program} api projects/42/jobs/456/erase -X POST", windows=True))

    def test_destructive_git_and_file_guards_still_apply(self):
        self.assertIsNone(command_denial("git clean -nd && git push origin topic", windows=False))
        for command in ("git reset --hard", "git push --force-with-lease", "git clean -fd", "rm -r .git"):
            with self.subTest(command=command):
                self.assertIsNotNone(command_denial(command, windows=False))


if __name__ == "__main__":
    unittest.main()
