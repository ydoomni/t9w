# Project Instructions

## Purpose and compatibility

- This repository is a New Recruit data repository for a custom Warhammer Fantasy ruleset.
- Keep the primary `.gst` and faction `.cat` files in the repository root so New Recruit can discover them.
- Use the public WHFB 6th Definitive Edition repository only as an implementation reference for BattleScribe/New Recruit XML structure, catalogue organization, constraints, modifiers, conditions, shared entries, shared rules, categories, and force organization.
- Never assume this project uses the same rules, values, profiles, equipment, or army restrictions as the reference repository.

## Rule authority

Rules are authoritative in this order:

1. The user's latest explicit override.
2. User-provided Errata, FAQ, or Balance Patch.
3. User-provided Army Book or Army List.
4. User-provided Core Rulebook.
5. Other sources explicitly designated by the user.

- When sources conflict, use the higher-priority source and, within the same priority, the newer source.
- The user's supplied rules are the only authority for game content. Do not invent missing rules or silently import content from reference data.
- Do not alter verified correct data without a rule source or an explicit user request.
- Record unresolved ambiguity in `RULE_QUESTIONS.md`, leave a narrowly scoped TODO where useful, and continue with unambiguous work.

## Change discipline

- Read this file before every project task.
- Inspect the existing structure and `git status` before editing.
- Prefer the smallest coherent change. Understand existing structures before broad changes.
- Preserve existing filenames, directory layout, object IDs, and public references unless a change is necessary.
- Do not regenerate an existing ID merely to tidy XML. Generate a new unique ID only for a new object.
- Before deleting an object, search all catalogues and the game system for references to its ID.
- Keep every `id` unique across the repository data set.
- Keep each catalogue's `gameSystemId`, catalogue links, and target references correct.
- Put genuinely cross-faction content in the system catalogue; keep faction-only content in that faction's catalogue.
- Encode enforceable rules using native constraints, modifiers, condition groups, category links, entry links, and profile links. Do not use descriptive text as a substitute for machine validation when New Recruit can validate the rule.
- Record unavoidable text-only implementations and their reasons in `IMPLEMENTATION_NOTES.md`.

## Sources and copyright

- Record important unit, profile, cost, composition, equipment, magic item, and special-rule sources in `SOURCES.md` with document title, version, page or section, and source type where available.
- Mark user changes as House Rule, Community Rule, Balance Patch, or User Override as appropriate.
- Do not copy complete copyrighted rulebooks, scans, or long passages into this public repository.
- Store only the data, rule names, short descriptions, citations, and original implementation notes needed by New Recruit.

## Required validation

After every data change, run the repository validation tests. At minimum verify:

- every `.gst` and `.cat` is well-formed XML;
- no duplicate IDs exist;
- every internal `targetId` and relevant reference resolves;
- every catalogue uses the correct `gameSystemId` and can reference the game system;
- catalogue links resolve correctly;
- point costs and constraint values are valid numbers;
- obvious minimum/maximum constraint conflicts are absent;
- modifiers reference valid targets and fields.

Do not report a data change complete while validation errors remain unless the error is explicitly documented as a blocked rule question.

## Git workflow

- Use a dedicated branch for substantial implementation work.
- Make logical commits with descriptive messages that state the implemented behavior.
- Do not overwrite or merge directly into `main` without explicit user authorization and completed validation.
- Never discard unrelated user changes.

## Delivery report

For each substantial work round, report changed files, implemented rules and units, constraints/modifiers, tests and results, remaining TODOs and ambiguities, suggested New Recruit checks, and branch/commit status.
