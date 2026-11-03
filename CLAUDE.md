## Course PDFs

Read course material from `courses/*/docs/*.md`, which mirror `courses/*/pdf/*.pdf` by file name. Open a `.pdf` only through the pdf-to-markdown skill.

## Lessons

`/mattpocock-skills:teach` uses `lecture/<track>/` as its teaching workspace, not the repo root; `lecture/TRACKS.md` lists the tracks. Before teaching, adding course material, or creating a track, follow `docs/learning/operating-rules.md`.

Project-local reference notes live in `knowledge/`; before writing or grading a topic one of them covers, read `knowledge/index.md` and the matching note.

## Agent skills

### Issue tracker

Issues live as local markdown files under `docs/issues/<feature>/`. See `docs/agents/issue-tracker.md`.

### Triage labels

Default five canonical labels (needs-triage, needs-info, ready-for-agent, ready-for-human, wontfix). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: one `CONTEXT.md` + `docs/adr/` at the repo root. See `docs/agents/domain.md`.
