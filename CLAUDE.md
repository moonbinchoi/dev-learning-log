## Course PDFs

Read course material from `courses/*/docs/*.md`, which mirror `courses/*/pdf/*.pdf` by file name. Open a `.pdf` only through the pdf-to-markdown skill.

## Lessons

`/mattpocock-skills:teach` uses `lecture/<track>/` as its teaching workspace, not the repo root; `lecture/TRACKS.md` lists the tracks. Before teaching, adding course material, or creating a track, follow `docs/learning/operating-rules.md`. Prepare each lesson in its own session with `/prepare-lesson <track>` before teaching it.

Project-local reference notes live in `knowledge/`; before writing or grading a topic one of them covers, read `knowledge/index.md` and the matching note.

## Git

The root repo has one branch, `main`. `projects/*` are independent repos: start project work in that folder, not with `--worktree` from the root.

Commit when you report finished work or finish a lesson's wrap-up (`docs/learning/operating-rules.md` rule 7). Keep a list of the files this session changed with write tools and commands, write paths file by file, and handle only that list:

1. Run `git status --short` for the list. Leave changes outside it alone, including other sessions' staged files.
2. Compare `git diff HEAD -- <paths>` with what you wrote. If a file has changes you did not write, or you cannot tell (context compaction), leave it out and ask the user.
3. Show the user the file list and the message, then wait. Without confirmation, do not commit.
4. Run `git add -A -- <paths>`.
5. Immediately run `git commit -m "<message>" -- <paths>`. Write the message in Korean.

If a git command fails on `index.lock`, keep the lock file, retry up to 3 times, 5 seconds apart, then tell the user.

Restore one file with `git restore --source=<commit> -- <path>`. If the file has uncommitted changes, ask the user first. If the file does not exist in that commit, this deletes it, so tell the user first.

Unless the user names the command, do not run these in the root repo: pathless `git add` or `git commit` (including `-a`), branch switches, `git stash`, `git reset --hard`, `git rebase`, pathless `git restore`, `git checkout -- .`, `git clean`. They mix or destroy other sessions' work. `*.pdf` and `.scratch/` are not in git, so `git clean -x` loses them for good.

## Agent skills

### Issue tracker

Issues live as local markdown files under `docs/issues/<feature>/`. See `docs/agents/issue-tracker.md`.

### Triage labels

Default five canonical labels (needs-triage, needs-info, ready-for-agent, ready-for-human, wontfix). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: one `CONTEXT.md` + `docs/adr/` at the repo root. See `docs/agents/domain.md`.
