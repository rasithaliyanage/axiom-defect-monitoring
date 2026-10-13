# .claude

Claude Code configuration for this project.

`settings.local.json` holds this machine's local settings, chiefly permission grants. It is intended
to be personal and unshared.

**It is not currently either.** The file is tracked in git and is absent from `.gitignore`, and the
committed copy carries a permission grant naming a path on a different contributor's machine. Until
it is untracked and ignored, treat it as a shared file. Resolving that is a deliberate change —
`git rm --cached .claude/settings.local.json` plus a `.gitignore` entry — and it removes the file
from other working trees, so it belongs to whoever owns this repository's git hygiene, not to a
drive-by edit.

Project-wide Claude Code settings, if they become necessary, belong in `settings.json` in this
directory and are committed. None exist yet, because no build, test, or run commands exist to grant
permissions for.

Engineering instructions for Claude Code are not kept here. They are in `CLAUDE.md` at the repository
root, where they are read automatically and stay visible to human reviewers.
