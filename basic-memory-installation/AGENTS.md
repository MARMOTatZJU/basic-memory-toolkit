# Installation control

The user requires installation one step at a time under explicit instruction.

- Execute only the installation step that the user explicitly authorizes.
- After that step, report its result and stop before the next installation step.
- Do not infer permission from the existence of a plan, Dockerfile, or script.
- Do not automatically install packages, update drivers, configure services, build images, download models, or start containers.
- Do not run several installation scripts together unless the user explicitly authorizes that combined action.
- File saving and local static checks are separate from installation. The user authorized those tasks in this conversation.
- Keep proposed versions, source checks, host observations, static validation, and runtime acceptance clearly distinguished.
- Preserve existing notes and application state. Use disposable notes for explicitly authorized acceptance tests.

Start future work with `installation-plan.md` and `docs/validation-and-open-items.md`.
The prepared assets are drafts until the required runtime checks pass.

## Continuous documentation and independent resume

- Keep README.md as the main user entry point throughout the installation.
- Before each handoff, update its current state, next action, operation commands, and complete file index.
- Index and document every new or changed reusable file, including result files and failed-attempt records.
- State the purpose, prerequisites, working directory, shell, inputs, outputs, privileges, effects, and verification for each operational entry point.
- Put longer procedures in a linked guide. The README must identify the correct guide and executable entry point.
- Maintain docs/installation-status.md with the last completed action, partial changes, current versions, and exact resume instruction.
- Save each authorized attempt through records/TEMPLATE.md. Link its result from records/README.md and README.md.
- Record external installer, image, model, container, volume, and persistent path identities in the appropriate operation record and inventory.
- Document private data directories by path and purpose. Exclude credentials, serial numbers, private notes, and full transcripts from public records.
- After file changes, run scripts/validate-bundle.py and resolve missing index entries before the handoff.
- Keep unexecuted operations and untested assets marked clearly. Documentation maintenance does not authorize an installation action.

## Download asset storage

Prefer the intended user's WSL home for reusable downloaded assets and image staging.
Keep the asset folder structured and include a README, complete index, versions, sources, sizes, and checksums.
Keep repository documentation in this bundle and record the external asset root here.
Verify cached assets before reuse or migration. Preserve interrupted-attempt evidence separately.

## Image construction and rebuilds

Keep image construction in the saved Dockerfile and versioned build inputs.
Document the exact target, context, version arguments, and rebuild command.
Keep every referenced helper indexed so users can modify or rebuild the image independently.

Document every Dockerfile instruction with an adjacent concise comment.
Use longer explanations for commands that perform more work. Keep comments outside instruction arguments.
