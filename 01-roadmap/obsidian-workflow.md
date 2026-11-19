# Obsidian workflow — useful defaults, portable content

## Entry and navigation

Open [[00-start-here]], then [[master-plan]] or [[practice-catalog]]. Use core Search/Quick Switcher, backlinks, outline and file navigation. Lab READMEs intentionally repeat a filename; use qualified wikilinks or relative Markdown links, not an ambiguous `[[README]]`.

The learning system uses ordinary Markdown tables/checklists and optional collapsed hint files. It does not require query scripts, a custom dashboard language, a code-execution plugin or a task database to function.

## Templates and daily notes

Core Templates continues to use `99-templates/`. Choose concept, lab, project, evidence or review according to the note's job. Core Daily Notes creates `06-journal/YYYY/YYYY-MM-DD-dddd.md` (weekday in the filename) from `daily`; weekly reviews use `journal-weekly` at `06-journal/YYYY/YYYY-Www.md`, where `W47` means week 47. See [[00-journal]]. Earlier root-level dated files remain preserved rather than moved without context.

Record artifact paths, actual check results, assistance and a next action. Do not auto-tick progress because a file was generated or a reference passed. [[learning-evidence]] is deliberately empty until you produce your own evidence.

## Plugin decision

No additional community plugin was necessary for the implemented workflow. Existing Excalidraw 2.28.1, Excalidraw Extras 0.1.0 and Math+ 0.7.0 installations were retained. This is an inventory, not a claim that every line of those plugins was security-audited or their UI reverified.

Core file recovery, templates, daily notes, bookmarks, properties and existing navigation features are sufficient for this first system. Existing Sync/Publish settings were not newly enabled or connected to any account. No vault content was uploaded by a new integration.

A spaced-repetition plugin may be useful later if manual review becomes burdensome; choose it only after checking current maintenance, compatibility, source, privacy, storage portability and actual review needs. Plugins execute with significant user access, not a guaranteed sandbox. More plugins are not evidence of better learning.

## Reload and verification

Reload Obsidian (or the relevant core plugin) to pick up daily-note configuration changes if needed. On-disk JSON/link checks do not prove a UI behavior was observed. Confirm Daily Notes creates the next note under `06-journal/YYYY/` as `YYYY-MM-DD-dddd.md` and Templates offers the new template files; report any app-specific problem rather than claiming it was tested automatically.

Disable a core feature through Settings → Core plugins; disable a community plugin through Settings → Community plugins. Preserve its data before removing its directory. For rollback, review the original .obsidian configuration from the snapshot using [[vault-maintenance]].
