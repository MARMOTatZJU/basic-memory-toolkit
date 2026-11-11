# Basic Memory installation bundle

**Installation control:** perform only the operation that the user explicitly selects.
After that operation, report its result and stop.

Start with [QUICK-START.md](QUICK-START.md) for setup, note/search examples, MCP access, and daily operation.

Use [ENTRY-POINTS.md](ENTRY-POINTS.md) for detailed image identities, script contracts, configuration ownership, storage, and recovery.

## Current state and resume point

Updated: 2026-11-07, Asia/Shanghai.
Latest completed dependency: **Order 15, embedding model, passed**.
All planned dependencies are available. Persistent deployment and Basic Memory acceptance remain pending.
The pinned **nomic-embed-text:v1.5** model uses F16 weights and returned **768 finite values** through Ollama 0.40.15.
Ollama reported the model in GPU memory. Actual runner mappings confirmed CUDA Runtime **12.8.90** and cuBLAS **12.8.5.5**.
The RTX 5090 Laptop GPU retained Windows driver **572.84**.

**Embedding choice:** Basic Memory remains on Nomic v1.5. A separate
multilingual-E5-small channel is recorded only as a future companion-index
TODO for multilingual stores. Its 384-dimensional vectors must remain separate
from Nomic's 768-dimensional vectors; only ranked results may be fused.
Nomic v2 is not selected. Read the
[companion embedding TODO](docs/companion-multilingual-embeddings-todo.md).

Use the [Order 15 guide](docs/order-15-model.md), [completed result](records/2026-11-07-order-15-model-attempt-01.md), and [runtime evidence](reference/order-15-model-runtime-2026-11-07.json).
The native model store is `/home/ydxu_/basic-memory-installation-assets/models/ollama/nomic-embed-text/v1.5/0a109f422b47/store`.
The home cache contains **572 verified files plus index.json**, with full source, version, size, and SHA-256 records.
The temporary model container and storage were removed. Container and volume inventories are empty.
Basic Memory **1.0.0** and the pinned Ollama image remain available.

**GPU smoke tests:** both passed. The five-minute run produced **58,176 embeddings in 300.12 seconds**.
NVIDIA utilization peaked at **53%**, with **725 MiB** of device memory in use.
All test containers and temporary files are removed. The cleanup recovery is documented in the [result](records/2026-11-07-gpu-smoke-attempt-02.md).
Use the [monitoring guide](docs/gpu-monitoring.md) for Windows Task Manager and WSL nvidia-smi.

**Remaining work:** runtime settings, persistent storage, service startup, and application acceptance.
Read the [remaining installation steps](docs/remaining-installation-steps.md).
The next deployment operation is **runbook Step 6: runtime configuration**, awaiting explicit instruction.
No persistent service has started. Existing-corpus retrieval passed on disposable copies after documented adaptations. MCP and persistent-service acceptance remain untested.
Read the [checkpoint](docs/installation-status.md) after any interruption.

**Existing database test, 2026-11-10:** all 480 Markdown records were indexed. After copy-only repairs, all 1,528 legacy graph edges matched. GPU batch 128 reached 265 vectors/second in the controlled trial. Retrieval quality remains mixed. Original files are unchanged, and temporary Docker resources are removed. Read the [compatibility report](docs/database-compatibility.md) and [operation record](records/2026-11-10-database-compatibility.md).

**Existing database repair, 2026-11-11:** the four Notion YAML aliases are now
expanded in place, both derived indexes are current, and all 1,528 authored
edges pass container verification. The established E5 vectors remained valid
after a projection-equivalence proof. Read the
[current repair result](docs/database-in-place-fix.md) and
[operation record](records/2026-11-11-database-in-place-fix.md).

## Entry points for independent operation

Open Ubuntu WSL2 and enter the bundle directory:

```bash
cd /mnt/d/Documents/Projects/AICodingWorkspace/basic-memory-toolkit/basic-memory-installation
```

Use Windows PowerShell when a row explicitly names Windows.
Each row below is a separate entry point. Do not execute the table as one sequence.

| Operation | Entry point | Prerequisites and effects |
| --- | --- | --- |
| Operate the repaired databases | [Current in-place repair result](docs/database-in-place-fix.md) | Agent entry points, runtime filter, serial import, current counts, and machine evidence. |
| Review the optional multilingual companion design | [Companion embedding TODO](docs/companion-multilingual-embeddings-todo.md) | Future E5 channel alongside BM's unchanged Nomic v1.5 index; no current installation action. |
| Test existing database compatibility | [Container test procedure](docs/database-compatibility.md#repeat-and-resume) | Read/search/graph checks on copies, GPU benchmarks, and explicit cleanup. Original folders are mounted read-only. |
| Find detailed technical entry points | [ENTRY-POINTS.md](ENTRY-POINTS.md) | Image identities and archives, every active script/configuration, effects, privileges, outputs, and recovery routes. |
| Start using the selected installation | [Quick start](QUICK-START.md) | First deployment, verification, notes, search, MCP, and daily commands. Persistent deployment remains pending in the saved records. |
| Read the dependency order | [installation-plan.md](installation-plan.md) | Names and versions for each dependency. |
| Review unfinished installation work | [Remaining steps](docs/remaining-installation-steps.md) | Current file and Docker-state audit. Runtime configuration is the next selected operation. |
| Recover the current position | [Current checkpoint](docs/installation-status.md) | Read before repeating a command or after a reboot. |
| Review the connection recovery | [Connection impact](docs/connection-troubleshooting.md#impact-on-the-installation) | NVIDIA installation passed through a verified official raw GitHub route. The original Pages domain still fails. |
| Check the driver in WSL | `/usr/lib/wsl/lib/nvidia-smi --query-gpu=name,driver_version --format=csv,noheader` | Read-only. Current observed result: 572.84. |
| Check the driver in Windows PowerShell | `nvidia-smi --query-gpu=name,driver_version --format=csv,noheader` | Read-only. Use NVIDIA Control Panel if the command is unavailable. |
| Review the selected driver baseline | [Detailed Order 3 guide](docs/nvidia-driver.md) | CUDA 12.8 is selected. Retain 572.84 for initial testing. |
| Recheck Order 5 systemd | `systemctl is-system-running` and [Order 5 result](records/2026-11-07-order-05-systemd-attempt-01.md) | Read-only. Expected: running, PID 1 systemd, no failed units. |
| Explain or recheck Order 6 | [Prerequisite guide](docs/order-06-prerequisites.md) | Lists the three packages, exact versions, HTTPS checks, current failure, and repeat commands. |
| Diagnose the NVIDIA connection | [Connection recovery guide](docs/connection-troubleshooting.md) | Inspect Clash routing and upstream connectivity. Includes Windows, WSL, DNS, and TLS checks. No CA addition is indicated. |
| Check saved files | `python3 scripts/validate-bundle.py` | Python 3.11 or later. Writes the local static report. |
| Resolve Docker socket permission denied | `sudo docker images` and [Docker access guide](docs/docker-access.md) | Group access is now fixed and verified. Existing terminals need newgrp docker. The guide records its root-level permissions. |
| Read host prerequisites | `bash scripts/preflight.sh` | Reads host, GPU, and tool versions. Installs no software. |
| Follow an installation operation | [Runbook](docs/runbook.md) | Details each operation, effects, prerequisites, and expected checks. |
| Inspect completed Order 7 | `sudo docker version`, `sudo containerd --version`, and [result](records/2026-11-07-order-07-docker-engine-attempt-01.md) | Expected: Docker 29.9.3, containerd 2.4.2, active and enabled services. |
| Reinstall or repair Order 7 when selected | `sudo bash scripts/install-docker.sh` and [Order 7 guide](docs/order-07-docker-engine.md) | Changes the repository, packages, and services. Order 7 is already complete. This is not an Order 8 installer. |
| Inspect completed Order 8 | `docker buildx version`, `docker compose version`, and `sudo docker buildx inspect default` | Read-only inspection. Expected: Buildx 0.38.1, Compose 5.7.0, default builder running. See the [guide](docs/order-08-docker-plugins.md) for configuration validation. |
| Reinstall or repair Order 8 when selected | `sudo bash scripts/install-docker-plugins.sh` and [Order 8 guide](docs/order-08-docker-plugins.md) | Order 8 is complete. A repeat refreshes APT metadata and checks the pinned plugin packages. |
| Reinstall or repair Order 9 when selected | `sudo bash scripts/install-nvidia-toolkit.sh --repository-route raw-github` and [Order 9 guide](docs/order-09-nvidia-toolkit.md) | Order 9 is complete. A repeat changes packages and runtime configuration, restarts Docker, and runs the GPU check. |
| Recover a slow GPU test image pull | [Order 9 image transfer](docs/order-09-nvidia-toolkit.md#slow-docker-hub-image-transfer) | Fetches the pinned Ubuntu image through verified curl transfers. Docker import requires root. |
| Inspect completed Order 9 | `nvidia-ctk --version` and [Order 9 guide](docs/order-09-nvidia-toolkit.md) | Read package and runtime state. Expected toolkit CLI 1.20.1. |
| Repeat only GPU visibility when selected | `sudo bash scripts/check-nvidia-gpu.sh` | Requires the cached pinned Ubuntu image. Runs and removes one container with --pull=never. |
| Verify the reusable download folder | `python3 /home/ydxu_/basic-memory-installation-assets/verify-assets.py` | Read-only SHA-256, size, and complete-index check. No administrator access required. |
| Archive completed downloads | `sudo python3 scripts/save-download-assets.py --asset-dir /home/ydxu_/basic-memory-installation-assets --owner ydxu_` | Copies authenticated APT archives and cached test images. Writes the home README and index. See the [download guide](docs/downloaded-assets.md). |
| Rebuild Order 10 when selected | `sudo python3 scripts/build-native-runtime.py` and [Order 10 guide](docs/order-10-native-runtime.md) | Order 10 is complete. A repeat builds only the native target, checks libraries, and archives reusable output. |
| Rebuild Order 11 when selected | `sudo python3 scripts/build-python-runtime.py` and [Order 11 guide](docs/order-11-python-runtime.md) | Order 11 is complete. A repeat uses verified source caches, builds only python-runtime, verifies the result, and indexes archives. |
| Rebuild Order 12 when selected | `sudo python3 scripts/build-build-backends.py` and [Order 12 guide](docs/order-12-build-backends.md) | Order 12 is complete. A repeat uses the saved lock and cached wheels, checks a fixture build, and archives the image. |
| Prepare local runtime settings | [Configuration example](config/runtime.env.example) and runbook Step 6 | Create `config/runtime.env` if absent. Set UID, GID, note path, port, and project. |
| Build the application image | `sudo bash scripts/build.sh` | Order 13 is complete. A selected rebuild requires Docker, Git, host Python 3, and verified caches. Archives and checks the image without starting services. |
| Report the current image download | `python3 scripts/download-progress.py` | Read-only local progress, verified range sizes, and archive readiness. No network request. |
| Install Order 14 inference image | `sudo python3 scripts/install-ollama-image.py` and [Order 14 guide](docs/order-14-ollama.md) | Order 14 is complete. A selected repeat imports the cached image, probes CUDA readiness, and archives results. No model or persistent service. |
| Install or verify Order 15 when selected | `sudo python3 scripts/install-embedding-model.py` and [Order 15 guide](docs/order-15-model.md) | Order 15 passed. A selected repeat reuses the cache, checks one disposable GPU embedding, removes the container, and archives new evidence. |
| Check the downloaded model files | `python3 scripts/check-embedding-assets.py --store PATH` and [Order 15 guide](docs/order-15-model.md#entry-points-and-prerequisites) | Read-only. No root required. Checks full manifest and blob hashes, format, license, and declared dimensions. |
| Run a selected temporary GPU smoke test | [Test guide](docs/gpu-smoke-test.md) and `python3 scripts/run-gpu-smoke.py --duration 300 --batch-size 32 --run-id NEW_ID` | Both runs passed. A selected repeat requires a new run identifier. Use Docker group access or sudo; see the guide. |
| Start the complete deployment | `sudo bash scripts/start.sh` | Separately selected runbook Step 8. Creates the note directory, starts Ollama, pulls the model, and starts Basic Memory. Use the Order 15 guide for cached-model import. |
| Check running services and embeddings | `sudo bash scripts/verify.sh` | Runbook Step 9. Requires running services. Sends an embedding request and checks GPU residency. |
| Complete application acceptance | [Acceptance procedure](docs/validation-and-open-items.md) | Retrieval, MCP, file watching, persistence, and restore checks remain separate. |
| Record a result or failure | [Step record template](records/TEMPLATE.md) | Record exact commands, changes, evidence, and the next action. |

The startup helper combines several actions.
If the user selects only one startup action, use that command from the [runbook](docs/runbook.md).
The Dockerfile passed its complete image checks. Service startup and application acceptance remain pending.

## Resume after an interruption or failure

1. Open this README again.
2. Read the checkpoint and the latest operation record.
3. Check the recorded package versions, file paths, and partial changes.
4. Confirm the prerequisites for the exact next action.
5. Perform only that selected action.
6. Save its result and update the checkpoint before another operation.

A failed operation can leave packages, configuration, images, or volumes in place.
Use its recorded partial state before repeating it.
Do not run every installer again to recover an unknown state.

After a driver update and reboot, return to the driver guide and check Windows and WSL versions.
Do not use a successful `nvidia-smi` result as evidence of successful model inference.

## Runtime status entry point

After Docker and runtime settings exist, inspect the selected deployment through:

```bash
sudo docker compose --project-name basic-memory-installation \
  --project-directory "$PWD" \
  --env-file config/versions.env \
  --env-file config/runtime.env \
  -f docker/compose.yaml ps
```

Use the same prefix with `logs --tail=100` to inspect service logs.
A later `stop` action preserves named volume data.
The command `down -v` deletes named volume data. It is not a normal stop command.
The future MCP endpoint is `http://127.0.0.1:8000/mcp` unless the configured host port changes.

## Maintain the entry points after every operation

Keep this README usable without the chat history.
Update its current state, exact next action, command entry points, and file index before each installation handoff.
Update the checkpoint and save a dated operation record, including failed or partial attempts.

Index every reusable document, script, configuration file, asset, and result file below.
Give each element a purpose and an invocation or reader entry point.
Record external installers, images, models, containers, volumes, and persistent paths in the operation record and relevant inventories.
Link those records from this README.
Describe private data locations by path and purpose. Keep private note contents and credentials out of the public index.

The validator checks that every reusable bundle file has a documented README row.
Its file scan excludes Git metadata, Python bytecode caches, the private `data/`
content directory, and generated `validation/` output. Compact reusable
validation baselines are indexed under
[`basic-memory-database-workspace-essential-assets/reference-baselines/runtime-validation/`](../basic-memory-database-workspace-essential-assets/reference-baselines/runtime-validation/).
New runtime reports and operation records must have README entries.
The conditional file `config/runtime.env` is documented below even before it exists.

The local `validation/` directory contains regenerated checks, raw logs, and
temporary run evidence. It can be Git-ignored. Historical validation links in
this document are local evidence references and can be absent from a clean
clone; use the essential-assets baseline index for durable comparison data.

## Complete file index

| File | Purpose | Entry point or use |
| --- | --- | --- |
| [ENTRY-POINTS.md](ENTRY-POINTS.md) | Detailed durable reference for images, scripts, configuration, storage, evidence, and recovery. | Consult before selecting, modifying, restoring, or repeating an operation. |
| [QUICK-START.md](QUICK-START.md) | Concise first-deployment and daily-use guide for the selected complete runtime. | Start here for configuration, service commands, note/search examples, MCP, and recovery links. |
| [README.md](README.md) | Bundle entry points, current state, and complete file index. | Start here after each interruption or restart. |
| [AGENTS.md](AGENTS.md) | User-controlled installation and documentation maintenance rules. | Read before any installation operation. |
| [installation-plan.md](installation-plan.md) | Dependency order, locations, and proposed versions. | Use the dependency order to select the next authorized operation. |
| [.gitignore](.gitignore) | Exclusions for private runtime configuration, data, and generated caches. | Used by Git if the bundle is tracked. |
| [docs/installation-status.md](docs/installation-status.md) | Current focus, operation status, and exact resume instructions. | Read before selecting or repeating an operation. |
| [docs/nvidia-driver.md](docs/nvidia-driver.md) | Order 3 explanation, version checks, package selection, and later update procedure. | Includes Windows and WSL commands for the selected CUDA 12.8 baseline. |
| [docs/runbook.md](docs/runbook.md) | Full sequence, prerequisites, effects, and operating commands. | Follow only the selected runbook step. |
| [docs/requirements-and-decisions.md](docs/requirements-and-decisions.md) | Requested scope and selected architecture. | Review before changing deployment choices. |
| [docs/dependencies.md](docs/dependencies.md) | All direct Python requirements, extras, versions, and lock distinctions. | Review application package changes here. |
| [docs/gpu-runtime.md](docs/gpu-runtime.md) | GPU runtime placement, model identity, API settings, and inference limits. | Use before model configuration or GPU tests. |
| [docs/companion-multilingual-embeddings-todo.md](docs/companion-multilingual-embeddings-todo.md) | Future optional multilingual-E5 companion design, isolation rules, and acceptance gates. | Review before proposing a second semantic index; it does not change the current Nomic v1.5 deployment. |
| [docs/host-observations.md](docs/host-observations.md) | Historical host inspection and command results. | Compare with fresh observations before installation. |
| [docs/validation-and-open-items.md](docs/validation-and-open-items.md) | Acceptance procedure, pending checks, and evidence limits. | Use to decide whether an operation passed. |
| [docs/sources-and-provenance.md](docs/sources-and-provenance.md) | First-party sources, local evidence, and reference provenance. | Check a claim or revisit version research. |
| [records/README.md](records/README.md) | Index of operation records and preparation evidence. | Open to locate the latest attempt. |
| [records/TEMPLATE.md](records/TEMPLATE.md) | Result, artifact, verification, and resume record template. | Copy for each authorized attempt. |
| [config/versions.env](config/versions.env) | Application, package, model, and image pins. | Loaded by the shell helpers. |
| [config/runtime.env.example](config/runtime.env.example) | UID, GID, notes path, MCP port, and project settings. | Copy during runbook Step 6, then edit. |
| [config/build-constraints.txt](config/build-constraints.txt) | Pinned application build backends. | Consumed during the image build. |
| [scripts/preflight.sh](scripts/preflight.sh) | Reads the host, GPU, and available tools. | bash scripts/preflight.sh |
| [scripts/install-docker.sh](scripts/install-docker.sh) | Installs Order 7 Engine, CLI, and containerd, then starts their system services. | sudo bash scripts/install-docker.sh |
| [scripts/install-nvidia-toolkit.sh](scripts/install-nvidia-toolkit.sh) | Installs GPU container support, restarts Docker, and checks GPU visibility. | sudo bash scripts/install-nvidia-toolkit.sh |
| [scripts/build.sh](scripts/build.sh) | Exports the pinned Git release and builds the application image. | sudo bash scripts/build.sh |
| [scripts/start.sh](scripts/start.sh) | Creates the note path, starts services, downloads the model, and checks its identity. | sudo bash scripts/start.sh. This combines several actions. |
| [scripts/verify.sh](scripts/verify.sh) | Checks the running image, embeddings, and GPU residency. | sudo bash scripts/verify.sh |
| [scripts/common.sh](scripts/common.sh) | Shared paths, version loading, prerequisite checks, and Compose invocation. | Sourced by helpers. It is not an installer entry point. |
| [scripts/validate-bundle.py](scripts/validate-bundle.py) | Checks file indexing, documentation links, syntax, snapshots, and dependency coverage. | python3 scripts/validate-bundle.py |
| [docker/basic-memory.dockerfile](docker/basic-memory.dockerfile) | Tested complete application image, source-wheel stage, and direct managed Python installation. | Built by scripts/build.sh using its prepared context. |
| [docker/compose.yaml](docker/compose.yaml) | Two-service deployment, GPU reservation, ports, and persistent storage. | Used by startup and verification helpers. |
| [docker/container-entrypoint.sh](docker/container-entrypoint.sh) | Registers the selected local project before starting MCP. | Runs automatically inside the future application container. |
| [docker/check-runtime.py](docker/check-runtime.py) | Checks installed versions, native imports, SQLite, and Python layout. | Runs during image build and scripts/verify.sh. |
| [docker/check-embedding.py](docker/check-embedding.py) | Checks an embedding request, dimensions, and reported GPU residency. | Runs inside the application container through scripts/verify.sh. |
| [reference/host-observations.json](reference/host-observations.json) | Machine-readable initial host observations. | Historical evidence, not a live status probe. |
| [reference/driver-inspection-2026-11-07.json](reference/driver-inspection-2026-11-07.json) | Read-only notebook and driver inspection, with update candidates. | Evidence for the current driver discussion. |
| [reference/image-identities.json](reference/image-identities.json) | Registry digests and model identity metadata. | Compare image identity before build or startup. |
| [reference/snapshot-manifest.json](reference/snapshot-manifest.json) | Reference source identities, derivation, and SHA-256 checksums. | Validated by scripts/validate-bundle.py. |
| [reference/basic-memory-1.0.0/pyproject.toml](reference/basic-memory-1.0.0/pyproject.toml) | Unchanged release manifest. | Source for declared requirements and extras. |
| [reference/basic-memory-1.0.0/uv.lock](reference/basic-memory-1.0.0/uv.lock) | Unchanged universal release lock. | Source for dependency versions and environment markers. |
| [reference/basic-memory-1.0.0/LICENSE](reference/basic-memory-1.0.0/LICENSE) | Upstream release license. | Retained with the reference metadata. |
| [reference/dependencies/declared-dependencies.csv](reference/dependencies/declared-dependencies.csv) | Original audit of declared requirements. | Reference for the declaration inventory. |
| [reference/dependencies/direct-dependencies.csv](reference/dependencies/direct-dependencies.csv) | Grouped direct requirements and locked versions. | Compare selected application features. |
| [reference/dependencies/expected-application-versions.json](reference/dependencies/expected-application-versions.json) | Expected package versions for image checks. | Read by docker/check-runtime.py. |
| [reference/dependencies/locked-packages.csv](reference/dependencies/locked-packages.csv) | Full inventory regenerated from the saved universal lock. | Preserves every package version and its markers. |
| [reference/dependencies/historical-locked-packages-2026-11-04.csv](reference/dependencies/historical-locked-packages-2026-11-04.csv) | Unchanged earlier dependency audit. | Historical traceability, including version alternatives. |
| [validation/static-checks.json](validation/static-checks.json) | Latest local file validation result. | Regenerated by scripts/validate-bundle.py. |
| [docs/order-06-prerequisites.md](docs/order-06-prerequisites.md) | Order 6 scope, package roles, versions, results, and independent repeat commands. | Current entry point for download prerequisites and the NVIDIA HTTPS issue. |
| [records/2026-11-07-order-05-systemd-attempt-01.md](records/2026-11-07-order-05-systemd-attempt-01.md) | Authorized Order 5 result and repeat commands. | Passed systemd check, no host changes. |
| [records/2026-11-07-order-06-prerequisites-attempt-01.md](records/2026-11-07-order-06-prerequisites-attempt-01.md) | Authorized Order 6 package and endpoint results. | Packages passed. NVIDIA GitHub Pages TLS issue remains open. |
| [reference/order-05-systemd-2026-11-07.json](reference/order-05-systemd-2026-11-07.json) | Machine-readable systemd commands, versions, and results. | Evidence for the Order 5 record. |
| [reference/order-06-prerequisites-2026-11-07.json](reference/order-06-prerequisites-2026-11-07.json) | Package versions, tool checks, and HTTPS endpoint outcomes. | Evidence for the Order 6 record. |
| [docs/connection-troubleshooting.md](docs/connection-troubleshooting.md) | TLS and proxy diagnosis, certificate decision, and independent recovery sequence. | Current entry point for the NVIDIA connection failure. |
| [records/2026-11-07-order-06-tls-attempt-02.md](records/2026-11-07-order-06-tls-attempt-02.md) | Read-only TLS, DNS, Windows, and proxy diagnostic result. | Connection remains unresolved. Inspect the client route before a repair. |
| [reference/order-06-tls-diagnosis-2026-11-07.json](reference/order-06-tls-diagnosis-2026-11-07.json) | Sanitized diagnostic evidence, observed fake-range DNS, and handshake outcomes. | Evidence for diagnostic attempt 2. |
| [records/2026-11-07-order-06-strict-route-attempt-03.md](records/2026-11-07-order-06-strict-route-attempt-03.md) | Connectivity retest after user-reported strict-route activation. | Latest result. NVIDIA TLS still fails in Windows and WSL. |
| [reference/order-06-strict-route-retest-2026-11-07.json](reference/order-06-strict-route-retest-2026-11-07.json) | DNS, HTTPS endpoint outcomes, and TLS handshake evidence for attempt 3. | Evidence for the strict-route retest. |
| [docs/order-07-docker-engine.md](docs/order-07-docker-engine.md) | Order 7 scope, exact versions, privileges, installation commands, and recovery. | Completed Order 7 guide and independent inspection commands. |
| [records/2026-11-07-order-07-docker-engine-attempt-01.md](records/2026-11-07-order-07-docker-engine-attempt-01.md) | Completed Docker installation result, artifact index, and resume point. | Order 7 passed. Read before any requested repair. |
| [reference/order-07-docker-engine-2026-11-07.json](reference/order-07-docker-engine-2026-11-07.json) | Package pins, metadata checks, privileges, and installation evidence. | Machine-readable record of Order 7. |
| [validation/order-07-installation-2026-11-07.log](validation/order-07-installation-2026-11-07.log) | Captured Docker installer and successful container verification output. | Inspect installation progress or failure. |
| [scripts/install-docker-plugins.sh](scripts/install-docker-plugins.sh) | Installs pinned Order 8 Buildx and Compose packages with a guarded APT simulation. | sudo bash scripts/install-docker-plugins.sh |
| [docs/order-08-docker-plugins.md](docs/order-08-docker-plugins.md) | Order 8 scope, versions, installation commands, checks, and recovery. | Installation, inspection, and repeat entry points for completed Order 8. |
| [records/2026-11-07-order-08-docker-plugins-attempt-01.md](records/2026-11-07-order-08-docker-plugins-attempt-01.md) | Authorized plugin installation attempt and independent resume point. | Read before repeating a partial operation. |
| [reference/order-08-docker-plugins-2026-11-07.json](reference/order-08-docker-plugins-2026-11-07.json) | Planned pins, preflight, package changes, and verification evidence. | Machine-readable record for Order 8. |
| [validation/order-08-installation-2026-11-07.log](validation/order-08-installation-2026-11-07.log) | Captured Order 8 installer and verification output. | Inspect the completed installation and scoped checks. |
| [scripts/check-nvidia-repository.py](scripts/check-nvidia-repository.py) | Verifies the NVIDIA key fingerprint, signed index checksum, and four exact package pins. | python3 scripts/check-nvidia-repository.py reference/nvidia-repository 1.20.1-1 |
| [scripts/check-nvidia-gpu.sh](scripts/check-nvidia-gpu.sh) | Runs and removes one pinned Ubuntu container to check GPU visibility. | sudo bash scripts/check-nvidia-gpu.sh. Requires the NVIDIA runtime. |
| [docs/order-09-nvidia-toolkit.md](docs/order-09-nvidia-toolkit.md) | Order 9 route, versions, prerequisites, installation, inspection, and recovery. | Read before toolkit installation or a repeat. |
| [records/2026-11-07-order-09-nvidia-toolkit-attempt-01.md](records/2026-11-07-order-09-nvidia-toolkit-attempt-01.md) | Authorized Order 9 result, artifacts, limits, and resume instruction. | Read the current attempt before repeating a command. |
| [reference/order-09-nvidia-toolkit-2026-11-07.json](reference/order-09-nvidia-toolkit-2026-11-07.json) | Order 9 starting state, package changes, commands, and runtime results. | Machine-readable toolkit installation evidence. |
| [reference/order-09-connection-2026-11-07.json](reference/order-09-connection-2026-11-07.json) | Canonical failures, fixed-IP failure, and official raw GitHub success. | Connection diagnosis and selected route evidence. |
| [reference/nvidia-repository/gpgkey.asc](reference/nvidia-repository/gpgkey.asc) | Unchanged NVIDIA public APT signing key. | Input for the repository verifier. Not a CA certificate. |
| [reference/nvidia-repository/InRelease](reference/nvidia-repository/InRelease) | Unchanged signed NVIDIA amd64 repository metadata. | Verified by check-nvidia-repository.py and APT. |
| [reference/nvidia-repository/Packages](reference/nvidia-repository/Packages) | Unchanged package index with exact package hashes. | Its SHA-512 checksum is authenticated by InRelease. |
| [reference/nvidia-repository/nvidia-container-toolkit.list](reference/nvidia-repository/nvidia-container-toolkit.list) | Unchanged upstream repository definition. | Provenance for the canonical source. The selected host route uses official raw GitHub. |
| [reference/nvidia-repository/verification.json](reference/nvidia-repository/verification.json) | Signature, key fingerprint, index digests, and selected package hashes. | Snapshot verification result. |
| [validation/order-09-installation-2026-11-07.log](validation/order-09-installation-2026-11-07.log) | Order 9 installer and runtime verification output. | Read for progress, failure diagnosis, or review. |
| [scripts/cache-nvidia-packages.py](scripts/cache-nvidia-packages.py) | Downloads official NVIDIA packages with curl and verifies signed SHA-256 and SHA-512 digests. | Called by the Order 9 installer before APT installation. Writes the selected package cache. |
| [reference/order-09-nvidia-toolkit-attempt-01-2026-11-07.json](reference/order-09-nvidia-toolkit-attempt-01-2026-11-07.json) | Preserved first attempt, interrupted before dpkg installation. | Read to recover the repository and package-cache partial state. |
| [records/2026-11-07-order-09-nvidia-toolkit-attempt-02.md](records/2026-11-07-order-09-nvidia-toolkit-attempt-02.md) | Second attempt result for verified curl caching and APT installation. | Preserved interrupted package-installation attempt. Use attempt 3 for the completed result. |
| [validation/order-09-installation-attempt-02-2026-11-07.log](validation/order-09-installation-attempt-02-2026-11-07.log) | Second Order 9 installer and scoped verification output. | Preserved package installation and interrupted native image pull. |
| [scripts/fetch-ubuntu-smoke-image.py](scripts/fetch-ubuntu-smoke-image.py) | Fetches the pinned Ubuntu GPU test image with curl and verifies every manifest and blob digest. | See the Order 9 guide. Optional --load uses Docker archive import and checks the pinned reference. |
| [reference/order-09-ubuntu-image-transfer-2026-11-07.json](reference/order-09-ubuntu-image-transfer-2026-11-07.json) | Verified Ubuntu image descriptors, archive identity, import result, and digest inspection. | Receipt for the faster Docker Hub transfer route. Contains no registry token. |
| [reference/order-09-nvidia-toolkit-attempt-02-2026-11-07.json](reference/order-09-nvidia-toolkit-attempt-02-2026-11-07.json) | Preserved second attempt after package installation and runtime setup. | Historical interrupted image-pull and diagnostic evidence. |
| [records/2026-11-07-order-09-nvidia-toolkit-attempt-03.md](records/2026-11-07-order-09-nvidia-toolkit-attempt-03.md) | Completed Order 9 GPU visibility result, artifacts, and independent resume. | Latest completed installation result. |
| [validation/order-09-gpu-attempt-03-2026-11-07.log](validation/order-09-gpu-attempt-03-2026-11-07.log) | GPU-only check, standard Docker device request, and final service and image inspection. | Both GPU visibility commands returned exit code 0. |
| [scripts/save-download-assets.py](scripts/save-download-assets.py) | Archives authenticated session packages, public metadata, and cached test images under the WSL home. | sudo python3 scripts/save-download-assets.py --asset-dir /home/ydxu_/basic-memory-installation-assets --owner ydxu_ |
| [scripts/verify-download-assets.py](scripts/verify-download-assets.py) | Standalone verifier for every indexed home asset hash and size, including unindexed-file detection. | python3 scripts/verify-download-assets.py /home/ydxu_/basic-memory-installation-assets |
| [docs/downloaded-assets.md](docs/downloaded-assets.md) | Home asset layout, ownership, package and image reuse, verification, and refresh commands. | Main entry point for reuse on another installation. |
| [reference/downloaded-assets-2026-11-07.json](reference/downloaded-assets-2026-11-07.json) | Snapshot of all home asset paths, versions, sources, sizes, hashes, and verification. | External asset inventory. The live home index remains authoritative for later updates. |
| [docker/prepare-native-packages.sh](docker/prepare-native-packages.sh) | Authenticates Ubuntu metadata and downloads exact native package pins with their required dependencies. | Runs inside the Dockerfile native-downloads stage. |
| [docker/check-native-runtime.sh](docker/check-native-runtime.sh) | Verifies native package versions, the certificate bundle, library dependencies, and the Order 10 boundary. | Runs in the disposable native image verification container. |
| [scripts/build-native-runtime.py](scripts/build-native-runtime.py) | Builds and archives only Order 10 targets and extends the WSL home asset index. | sudo python3 scripts/build-native-runtime.py |
| [docs/order-10-native-runtime.md](docs/order-10-native-runtime.md) | Order 10 scope, versions, stages, actions, prerequisites, checks, and recovery. | Independent entry point for native foundation installation. |
| [records/2026-11-07-order-10-native-runtime-attempt-01.md](records/2026-11-07-order-10-native-runtime-attempt-01.md) | Authorized Order 10 attempt and exact resume point. | Completed native foundation result and next operation. |
| [reference/order-10-native-runtime-2026-11-07.json](reference/order-10-native-runtime-2026-11-07.json) | Order 10 preflight, executed commands, image identities, versions, assets, and verification. | Machine-readable installation and archive evidence. |
| [validation/order-10-native-runtime-2026-11-07.log](validation/order-10-native-runtime-2026-11-07.log) | Captured native build, package download, export, and verification output. | Completed build and verification output. |
| [.dockerignore](.dockerignore) | Excludes private runtime configuration, data, and generated operation records from a direct Docker build context. | Applied by Docker when the bundle directory is the context. |
| [scripts/fetch-uv-image.py](scripts/fetch-uv-image.py) | Downloads the digest-pinned official uv image, verifies every blob, and optionally imports its OCI archive. | Used by the Order 11 builder. Archive and receipt output paths are explicit arguments. |
| [scripts/download-python-archive.py](scripts/download-python-archive.py) | Downloads the selected standalone Python archive and verifies its published SHA-256 checksum. | Used by the Order 11 builder with a WSL-home cache directory. |
| [docker/check-python-runtime.py](docker/check-python-runtime.py) | Verifies uv, CPython, SQLite features, native library loading, and direct installation without an application venv. | Runs during the Python image build and in a disposable runtime check. |
| [scripts/build-python-runtime.py](scripts/build-python-runtime.py) | Builds and archives only Order 11, using verified source assets and the commented Dockerfile. | sudo python3 scripts/build-python-runtime.py |
| [docs/order-11-python-runtime.md](docs/order-11-python-runtime.md) | Order 11 scope, exact artifacts, entry points, checks, archives, and recovery. | Independent procedure for the Python foundation. |
| [records/2026-11-07-order-11-python-runtime-attempt-01.md](records/2026-11-07-order-11-python-runtime-attempt-01.md) | Authorized Order 11 result and partial-state record. | Completed Python foundation result and next operation. |
| [reference/order-11-python-runtime-2026-11-07.json](reference/order-11-python-runtime-2026-11-07.json) | Order 11 pins, preflight, transfer recovery, executed commands, versions, image identity, and validation. | Machine-readable Python foundation evidence. |
| [validation/order-11-python-runtime-2026-11-07.log](validation/order-11-python-runtime-2026-11-07.log) | Captured Python foundation build, installation, and verification output. | Inspect before repeating a failed or interrupted build. |
| [config/build-backend-overlaps.txt](config/build-backend-overlaps.txt) | Constrains backend packages shared with the saved application runtime lock. | Read by the backend resolver to prevent incompatible shared versions. |
| [config/build-backends.lock](config/build-backends.lock) | Complete exact backend dependency resolution with SHA-256 archive hashes. | Used for offline backend installation with required hashes. |
| [scripts/prepare-build-backend-assets.py](scripts/prepare-build-backend-assets.py) | Resolves selected backends and downloads target-compatible wheels verified against PyPI and lock hashes. | Called by the backend builder when the wheel cache is missing. |
| [docker/check-build-backends.py](docker/check-build-backends.py) | Verifies installed backend versions and builds a disposable wheel through the dynamic-version plugin. | Runs during the image build and a disposable runtime verification. |
| [scripts/build-build-backends.py](scripts/build-build-backends.py) | Builds only Order 12, verifies its result, and indexes reusable wheels and image output. | sudo python3 scripts/build-build-backends.py |
| [docs/order-12-build-backends.md](docs/order-12-build-backends.md) | Order 12 scope, input lock, construction, verification, reuse, and recovery. | Independent procedure for backend installation. |
| [records/2026-11-07-order-12-build-backends-attempt-01.md](records/2026-11-07-order-12-build-backends-attempt-01.md) | First backend build failure and correction. | Historical attempt; use the completed second attempt to resume. |
| [reference/order-12-build-backends-2026-11-07.json](reference/order-12-build-backends-2026-11-07.json) | Order 12 preflight, commands, installed versions, functional check, image identity, and archives. | Machine-readable backend foundation evidence. |
| [validation/order-12-build-backends-2026-11-07.log](validation/order-12-build-backends-2026-11-07.log) | Captured backend image build, installation, and verification output. | Inspect before repeating a failed or interrupted operation. |
| [records/2026-11-07-order-12-build-backends-attempt-02.md](records/2026-11-07-order-12-build-backends-attempt-02.md) | Completed backend image, exact versions, functional checks, archive identities, and stop point. | Latest Order 12 result; stop before Order 13. |
| [reference/order-12-build-backends-attempt-01-2026-11-07.json](reference/order-12-build-backends-attempt-01-2026-11-07.json) | Unchanged evidence for the first backend build failure. | Historical managed-prefix protection failure. |
| [validation/order-12-build-backends-attempt-01-2026-11-07.log](validation/order-12-build-backends-attempt-01-2026-11-07.log) | Unchanged output from the first failed backend build. | Read with the first attempt record. |
| [reference/order-12-attempt-01.dockerfile](reference/order-12-attempt-01.dockerfile) | Exact Dockerfile from the failed first backend build. | Historical input; the active Dockerfile contains the correction. |
| [scripts/prepare-application-assets.py](scripts/prepare-application-assets.py) | Selects target-compatible dependencies from the unchanged release lock and verifies downloaded archives. | Called by the Order 13 builder with a WSL-home directory. |
| [scripts/build-application.py](scripts/build-application.py) | Builds only the application image, verifies all runtime versions and CLI identity, and archives inputs and output. | sudo python3 scripts/build-application.py. Also called by scripts/build.sh. |
| [docker/prepare-application-wheels.py](docker/prepare-application-wheels.py) | Verifies locked archives and builds source-only dependency wheels offline in a Dockerfile stage. | Runs in application-wheels before application installation. |
| [docs/order-13-application.md](docs/order-13-application.md) | Order 13 scope, exact source, entry points, effects, verification, cache, and recovery. | Independent application-image installation procedure. |
| [records/2026-11-07-order-13-application-attempt-01.md](records/2026-11-07-order-13-application-attempt-01.md) | First application build failure, successful source wheel preparation, and canonical-prefix correction. | Historical attempt; read the second attempt for current state. |
| [reference/order-13-application-2026-11-07.json](reference/order-13-application-2026-11-07.json) | Order 13 preflight, commands, image identity, installed package versions, CLI checks, and archive receipt. | Machine-readable current application-image result. |
| [validation/order-13-application-2026-11-07.log](validation/order-13-application-2026-11-07.log) | Captured application wheel preparation, image build, and verification output. | Inspect before repeating a failed build. |
| [docs/docker-access.md](docs/docker-access.md) | Completed socket-access correction, immediate commands, and activation of persistent docker group membership. | Use when a normal Docker command cannot access /var/run/docker.sock. |
| [records/2026-11-07-docker-access-attempt-01.md](records/2026-11-07-docker-access-attempt-01.md) | Authorized Docker group membership change and fresh WSL access verification. | Completed permission correction; run newgrp docker in an older terminal. |
| [reference/docker-access-2026-11-07.json](reference/docker-access-2026-11-07.json) | Before/after groups, unchanged socket mode, authorization, and successful fresh-process image listing. | Machine-readable Docker access result. |
| [records/2026-11-07-order-13-application-attempt-02.md](records/2026-11-07-order-13-application-attempt-02.md) | Application build retry using the canonical managed prefix, verification, artifacts, and stop point. | Completed Order 13 result; stop before Order 14. |
| [reference/order-13-attempt-01.dockerfile](reference/order-13-attempt-01.dockerfile) | Exact Dockerfile from the first failed application image build. | Historical symlink-path input; use the active Dockerfile for rebuilds. |
| [reference/order-13-application-attempt-01-2026-11-07.json](reference/order-13-application-attempt-01-2026-11-07.json) | Unchanged first-attempt execution evidence and failure. | Historical application install path failure. |
| [validation/order-13-application-attempt-01-2026-11-07.log](validation/order-13-application-attempt-01-2026-11-07.log) | Unchanged output from the successful wheel stage and failed first application installation. | Read with the first attempt record. |
| [reference/dependencies/installed-application-versions.csv](reference/dependencies/installed-application-versions.csv) | Every installed application-image distribution, version, role, and exact image identity. | Verified inventory of 192 distributions from Order 13. |
| [scripts/fetch-ollama-image.py](scripts/fetch-ollama-image.py) | Downloads the pinned official Ollama image through resumable checked ranges and verifies every manifest, config, and layer digest. | Called by the Order 14 installer with a WSL-home transfer directory. |
| [scripts/install-ollama-image.py](scripts/install-ollama-image.py) | Imports and verifies only Order 14, probes the selected CUDA runtime, and archives reusable image and metadata. | sudo python3 scripts/install-ollama-image.py. |
| [docker/check-ollama-runtime.py](docker/check-ollama-runtime.py) | Inventories image libraries and tests CUDA 12.8 version, device access, memory operations, and cuBLAS availability. | Runs in a disposable Ollama container with an archived Python interpreter mounted read-only. |
| [docs/order-14-ollama.md](docs/order-14-ollama.md) | Order 14 pins, entry points, image transfer, CUDA checks, effects, artifacts, and recovery. | Independent Ollama image installation procedure. |
| [records/2026-11-07-order-14-ollama-attempt-01.md](records/2026-11-07-order-14-ollama-attempt-01.md) | Authorized Order 14 state, exact commands, results, and stop point. | Completed Order 14 result; stop before Order 15. |
| [reference/order-14-ollama-2026-11-07.json](reference/order-14-ollama-2026-11-07.json) | Order 14 preflight, commands, image identities, transfer, GPU/library checks, and archive receipt. | Machine-readable current Order 14 result. |
| [reference/order-14-cuda-libraries-2026-11-07.json](reference/order-14-cuda-libraries-2026-11-07.json) | Actual inference-image libraries, OS package versions, GPU identity, and CUDA readiness results. | Generated by the disposable CUDA probe. |
| [validation/order-14-ollama-2026-11-07.log](validation/order-14-ollama-2026-11-07.log) | Captured image transfer/import and CUDA verification output. | Inspect before resuming an interrupted or failed image installation. |
| [scripts/download-progress.py](scripts/download-progress.py) | Reports checked image ranges, partial transfer bytes, and final archive readiness from local files. | python3 scripts/download-progress.py. Works after installation through the completed asset receipt. |
| [reference/dependencies/ollama-libraries.csv](reference/dependencies/ollama-libraries.csv) | Every packaged shared-library path, filename version, version scope, selected-backend flag, and image digest. | 113 entries from the verified inference image. |
| [reference/dependencies/ollama-os-packages.csv](reference/dependencies/ollama-os-packages.csv) | Exact installed Ubuntu package versions in the inference image. | 123 package versions tied to the pinned manifest. |
| [scripts/fetch-embedding-model.py](scripts/fetch-embedding-model.py) | Verified, resumable model download through Windows or WSL curl. | Called by the Order 15 installer; see docs/order-15-model.md. |
| [scripts/check-embedding-assets.py](scripts/check-embedding-assets.py) | Native model manifest, blob hashes, GGUF metadata, and license checks. | python3 scripts/check-embedding-assets.py --store PATH; no inference or root required. |
| [docker/check-embedding-runtime.py](docker/check-embedding-runtime.py) | Disposable OpenAI-compatible embedding and actual CUDA runner check. | Run only through the Order 15 installer inside its temporary container. |
| [scripts/install-embedding-model.py](scripts/install-embedding-model.py) | Scoped Order 15 cache registration, disposable GPU check, and evidence. | sudo python3 scripts/install-embedding-model.py; see the Order 15 guide. |
| [docs/order-15-model.md](docs/order-15-model.md) | Order 15 scope, prerequisites, operation, reuse, and verification. | Read before repeating model installation or restoring its native cache. |
| [records/2026-11-07-order-15-model-attempt-01.md](records/2026-11-07-order-15-model-attempt-01.md) | Authorized Order 15 operation result and resume boundary. | Read with its linked machine evidence. |
| [reference/order-15-model-2026-11-07.json](reference/order-15-model-2026-11-07.json) | Order 15 command history, status, model identity, and asset verification. | Machine-readable operation evidence; current state is authoritative. |
| [reference/order-15-model-metadata-2026-11-07.json](reference/order-15-model-metadata-2026-11-07.json) | Model hashes, F16 format, GGUF metadata, dimensions, and context. | Read the status before using this evidence. |
| [reference/order-15-model-runtime-2026-11-07.json](reference/order-15-model-runtime-2026-11-07.json) | Disposable embedding dimensions, GPU placement, and CUDA runner mappings. | Read the status; this is separate from Basic Memory acceptance. |
| [validation/order-15-model-2026-11-07.log](validation/order-15-model-2026-11-07.log) | Exact model operation command and output history. | Read after a failure or interrupted model verification. |
| [validation/order-15-ollama-server-2026-11-07.log](validation/order-15-ollama-server-2026-11-07.log) | Sanitized disposable Ollama server and GPU runner log. | Inspect alongside the model runtime evidence. |
| [docker/run-gpu-smoke.py](docker/run-gpu-smoke.py) | Repeated public embedding batches for a bounded GPU workload. | Called only inside the temporary smoke container after user confirmation. |
| [scripts/run-gpu-smoke.py](scripts/run-gpu-smoke.py) | Temporary GPU container, sustained inference, telemetry, results, and cleanup. | Use the selected duration and a new run identifier after explicit authorization. |
| [docs/gpu-smoke-test.md](docs/gpu-smoke-test.md) | GPU smoke test scope, results, monitor entry point, repeat command, and cleanup recovery. | Read before a separately selected repeat. Both recorded tests passed. |
| [records/2026-11-07-gpu-smoke-attempt-01.md](records/2026-11-07-gpu-smoke-attempt-01.md) | Authorized temporary GPU smoke-test operation record and resume point. | Read with docs/gpu-smoke-test.md and the operation record. |
| [validation/gpu-smoke/20261107-smoke01/commands.log](validation/gpu-smoke/20261107-smoke01/commands.log) | Exact smoke-test commands and public workload progress. | Read with docs/gpu-smoke-test.md and the operation record. |
| [smoke01 GPU samples](../basic-memory-database-workspace-essential-assets/reference-baselines/runtime-validation/gpu-smoke/20261107-smoke01/gpu-samples.csv) | One-second NVIDIA timestamp, name, driver, GPU utilization, memory, and power samples. | Reusable baseline moved to essential assets. |
| [validation/gpu-smoke/20261107-smoke01/inputs/config/versions.env](validation/gpu-smoke/20261107-smoke01/inputs/config/versions.env) | Exact executed smoke-test input. | Read with docs/gpu-smoke-test.md and the operation record. |
| [validation/gpu-smoke/20261107-smoke01/inputs/docker/check-embedding-runtime.py](validation/gpu-smoke/20261107-smoke01/inputs/docker/check-embedding-runtime.py) | Exact executed smoke-test input. | Read with docs/gpu-smoke-test.md and the operation record. |
| [validation/gpu-smoke/20261107-smoke01/inputs/docker/run-gpu-smoke.py](validation/gpu-smoke/20261107-smoke01/inputs/docker/run-gpu-smoke.py) | Exact executed smoke-test input. | Read with docs/gpu-smoke-test.md and the operation record. |
| [validation/gpu-smoke/20261107-smoke01/inputs/scripts/run-gpu-smoke.py](validation/gpu-smoke/20261107-smoke01/inputs/scripts/run-gpu-smoke.py) | Exact executed smoke-test input. | Read with docs/gpu-smoke-test.md and the operation record. |
| [smoke01 result](../basic-memory-database-workspace-essential-assets/reference-baselines/runtime-validation/gpu-smoke/20261107-smoke01/result.json) | Smoke-test status, dimensions, GPU placement, timings, and cleanup. | Reusable baseline moved to essential assets. |
| [docs/gpu-monitoring.md](docs/gpu-monitoring.md) | Explain Task Manager engine figures and inspect NVIDIA execution through WSL counters. | Read with docs/gpu-smoke-test.md and the linked operation record. |
| [records/2026-11-07-gpu-smoke-attempt-02.md](records/2026-11-07-gpu-smoke-attempt-02.md) | Authorized five-minute temporary test, launcher recovery, result, and resume point. | Read with docs/gpu-smoke-test.md and the linked operation record. |
| [validation/gpu-smoke/20261107-smoke01/ollama-server.log](validation/gpu-smoke/20261107-smoke01/ollama-server.log) | Sanitized temporary server and CUDA runner diagnostics. | Read with docs/gpu-smoke-test.md and the linked operation record. |
| [smoke01 telemetry summary](../basic-memory-database-workspace-essential-assets/reference-baselines/runtime-validation/gpu-smoke/20261107-smoke01/telemetry-summary.json) | Device-wide utilization, memory, and power statistics with measurement scope. | Reusable baseline moved to essential assets. |
| [validation/gpu-smoke/20261107-smoke02/commands.log](validation/gpu-smoke/20261107-smoke02/commands.log) | Exact smoke-test commands and public workload progress. | Read with docs/gpu-smoke-test.md and the linked operation record. |
| [smoke02 GPU samples](../basic-memory-database-workspace-essential-assets/reference-baselines/runtime-validation/gpu-smoke/20261107-smoke02/gpu-samples.csv) | NVIDIA device timestamp, name, driver, utilization, memory, and power each second. | Reusable baseline moved to essential assets. |
| [validation/gpu-smoke/20261107-smoke02/inputs/config/versions.env](validation/gpu-smoke/20261107-smoke02/inputs/config/versions.env) | Exact executed smoke-test input. | Read with docs/gpu-smoke-test.md and the linked operation record. |
| [validation/gpu-smoke/20261107-smoke02/inputs/docker/check-embedding-runtime.py](validation/gpu-smoke/20261107-smoke02/inputs/docker/check-embedding-runtime.py) | Exact executed smoke-test input. | Read with docs/gpu-smoke-test.md and the linked operation record. |
| [validation/gpu-smoke/20261107-smoke02/inputs/docker/run-gpu-smoke.py](validation/gpu-smoke/20261107-smoke02/inputs/docker/run-gpu-smoke.py) | Exact executed smoke-test input. | Read with docs/gpu-smoke-test.md and the linked operation record. |
| [validation/gpu-smoke/20261107-smoke02/inputs/scripts/run-gpu-smoke.py](validation/gpu-smoke/20261107-smoke02/inputs/scripts/run-gpu-smoke.py) | Exact executed smoke-test input. | Read with docs/gpu-smoke-test.md and the linked operation record. |
| [smoke02 result](../basic-memory-database-workspace-essential-assets/reference-baselines/runtime-validation/gpu-smoke/20261107-smoke02/result.json) | Timed GPU smoke-test result, dimensions, placement, library maps, and cleanup. | Reusable baseline moved to essential assets. |
| [validation/gpu-smoke/20261107-smoke02-launch.json](validation/gpu-smoke/20261107-smoke02-launch.json) | Failed Windows WSL entry and recovery through existing Docker group access. | Read with docs/gpu-smoke-test.md and the linked operation record. |
| [validation/gpu-smoke/20261107-smoke02/cleanup-recovery.json](validation/gpu-smoke/20261107-smoke02/cleanup-recovery.json) | Scoped temporary-cache ownership recovery, exact commands, and final result. | Read with docs/gpu-smoke-test.md and the relevant operation record. |
| [validation/gpu-smoke/20261107-smoke02/ollama-server.log](validation/gpu-smoke/20261107-smoke02/ollama-server.log) | Sanitized temporary server and CUDA runner diagnostics. | Read with docs/gpu-smoke-test.md and the relevant operation record. |
| [validation/gpu-smoke/20261107-smoke02/post-cleanup-gpu.csv](validation/gpu-smoke/20261107-smoke02/post-cleanup-gpu.csv) | NVIDIA counters after complete test cleanup. | Read with docs/gpu-smoke-test.md and the relevant operation record. |
| [validation/gpu-smoke/20261107-smoke02/recovery/cleanup.py](validation/gpu-smoke/20261107-smoke02/recovery/cleanup.py) | Exact one-time smoke02 cache recovery; already executed and not a general repeat entry point. | Read with docs/gpu-smoke-test.md and the relevant operation record. |
| [validation/gpu-smoke/20261107-smoke02/recovery/inputs/scripts/run-gpu-smoke.py](validation/gpu-smoke/20261107-smoke02/recovery/inputs/scripts/run-gpu-smoke.py) | Follow-up host helper fix for future cleanup; separate from timed-run inputs. | Read with docs/gpu-smoke-test.md and the relevant operation record. |
| [smoke02 telemetry summary](../basic-memory-database-workspace-essential-assets/reference-baselines/runtime-validation/gpu-smoke/20261107-smoke02/telemetry-summary.json) | Device-wide utilization, memory, and power statistics with measurement scope. | Reusable baseline moved to essential assets. |
| [docs/remaining-installation-steps.md](docs/remaining-installation-steps.md) | Audited unfinished runtime configuration, storage, service startup, acceptance, and separate open issues. | Read before selecting runbook Step 6 or another remaining operation. |
| [validation/gpu-smoke/20261107-smoke02/home-cache-verification.json](validation/gpu-smoke/20261107-smoke02/home-cache-verification.json) | Complete 572-file home-cache hash, size, and index check after recovered test cleanup. | All files passed. Read with the five-minute smoke-test result. |
| [docs/database-compatibility.md](docs/database-compatibility.md) | Compatibility procedure, findings, or operation record. | See the compatibility report for use and limitations. |
| [records/2026-11-10-database-compatibility.md](records/2026-11-10-database-compatibility.md) | Compatibility procedure, findings, or operation record. | See the compatibility report for use and limitations. |
| [docs/database-in-place-fix.md](docs/database-in-place-fix.md) | Current in-place database repair result and durable entry points. | Use before operating either repaired database. |
| [records/2026-11-11-database-in-place-fix.md](records/2026-11-11-database-in-place-fix.md) | Authorized in-place repair actions, result, cleanup, and next boundary. | Current database repair operation record. |
| [scripts/run-database-compatibility.py](scripts/run-database-compatibility.py) | Reusable compatibility test or reporting entry point. | See the compatibility report for use and limitations. |
| [scripts/summarize-database-compatibility.py](scripts/summarize-database-compatibility.py) | Reusable compatibility test or reporting entry point. | See the compatibility report for use and limitations. |
| [docker/test-database-compatibility.py](docker/test-database-compatibility.py) | Reusable compatibility test or reporting entry point. | See the compatibility report for use and limitations. |
| [docker/test-database-retrieval.py](docker/test-database-retrieval.py) | Reusable compatibility test or reporting entry point. | See the compatibility report for use and limitations. |
| [docker/reindex-compatibility-serial.py](docker/reindex-compatibility-serial.py) | Reusable compatibility test or reporting entry point. | See the compatibility report for use and limitations. |
| [compatibility batch tuning](../basic-memory-database-workspace-essential-assets/reference-baselines/runtime-validation/database-compatibility/2026-11-10/batch-tuning.json) | Provider batch and concurrency baseline. | Reusable baseline moved to essential assets. |
| [validation/compatibility/2026-11-10/container-stats.jsonl](validation/compatibility/2026-11-10/container-stats.jsonl) | Empty CPU-series capture retained as failed measurement evidence. | See the compatibility report for use and limitations. |
| [compatibility frontmatter repair](../basic-memory-database-workspace-essential-assets/reference-baselines/runtime-validation/database-compatibility/2026-11-10/copy-frontmatter-repair.json) | Copy-only YAML-alias repair invariant. | Reusable repair baseline moved to essential assets. |
| [compatibility CUDA libraries](../basic-memory-database-workspace-essential-assets/reference-baselines/runtime-validation/database-compatibility/2026-11-10/cuda-libraries.txt) | Tested inference-image CUDA library inventory. | Reusable runtime baseline moved to essential assets. |
| [compatibility CUDA runner](../basic-memory-database-workspace-essential-assets/reference-baselines/runtime-validation/database-compatibility/2026-11-10/cuda-runner.txt) | Selected CUDA runner evidence. | Reusable runtime baseline moved to essential assets. |
| [validation/compatibility/2026-11-10/embedding-requests.jsonl](validation/compatibility/2026-11-10/embedding-requests.jsonl) | Existing-database compatibility evidence. | See the compatibility report for use and limitations. |
| [compatibility frontmatter diagnostics](../basic-memory-database-workspace-essential-assets/reference-baselines/runtime-validation/database-compatibility/2026-11-10/frontmatter-diagnostics.json) | Original parser-compatibility diagnostic summary. | Reusable diagnostic baseline moved to essential assets. |
| [compatibility GPU samples](../basic-memory-database-workspace-essential-assets/reference-baselines/runtime-validation/database-compatibility/2026-11-10/gpu.csv) | Device samples from the database compatibility workload. | Reusable performance baseline moved to essential assets. |
| [validation/compatibility/2026-11-10/lifecycle.jsonl](validation/compatibility/2026-11-10/lifecycle.jsonl) | Existing-database compatibility evidence. | See the compatibility report for use and limitations. |
| [compatibility metrics summary](../basic-memory-database-workspace-essential-assets/reference-baselines/runtime-validation/database-compatibility/2026-11-10/metrics-summary.json) | GPU-phase statistics and request-overlap summary. | Reusable performance baseline moved to essential assets. |
| [validation/compatibility/2026-11-10/phases.jsonl](validation/compatibility/2026-11-10/phases.jsonl) | Existing-database compatibility evidence. | See the compatibility report for use and limitations. |
| [compatibility pre-repair audit](../basic-memory-database-workspace-essential-assets/reference-baselines/runtime-validation/database-compatibility/2026-11-10/pre-repair-audit.json) | Baseline record, edge, and runtime observations. | Reusable comparison baseline moved to essential assets. |
| [compatibility main result](../basic-memory-database-workspace-essential-assets/reference-baselines/runtime-validation/database-compatibility/2026-11-10/result.json) | Runtime import, identity, timing, and integrity result. | Reusable comparison baseline moved to essential assets. |
| [compatibility retrieval result](../basic-memory-database-workspace-essential-assets/reference-baselines/runtime-validation/database-compatibility/2026-11-10/retrieval.json) | Read, search, ranking, graph, and original-integrity checks. | Reusable retrieval baseline moved to essential assets. |
| [compatibility serial-index result](../basic-memory-database-workspace-essential-assets/reference-baselines/runtime-validation/database-compatibility/2026-11-10/serial-index-repair.json) | Serial SQLite file-index result. | Reusable workaround baseline moved to essential assets. |
| `config/runtime.env` | Local runtime configuration, created during runbook Step 6. It does not yet exist. | Loaded by startup, verification, and Compose commands. Keep private credentials out of shared records. |

## References and validation limits

The original [code report](../basic-memory-code/code-report/) and [source checkout](../basic-memory-database-workspace/vendor/basic-memory/) remain in the toolkit.
The selected application is Basic Memory 1.0.0 at commit `c9bd187b83baba549d5cd16bacc180f8023d51c8`.
The build helper exports that commit without changing the source checkout.

The [static report](validation/static-checks.json) covers local files, syntax, snapshots, and dependency and index coverage.
It does not establish Docker build, driver update, model inference, or application acceptance.
PyYAML and Docker enable additional validation checks when available.

Observed helper versions: host Python 3.12.3 and Git 2.43.0.
The application uses its separate uv-managed interpreter inside Docker.
Writing status: STE-aligned. Official dictionary verification and independent human review remain pending.
