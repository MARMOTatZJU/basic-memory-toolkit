# Order 10 attempt 1: native runtime foundation

## Identity and authorization

Date: 2026-11-07, Asia/Shanghai. Status: **passed**.
Authorization: "Proceed to order 10".
The user also required Dockerfile-based rebuilds and informative comments for every build instruction.
Run identifier: 20261107-order10-attempt01.

## Starting state

Docker Engine and CLI were 29.9.3. The pinned Ubuntu 24.04 amd64 image was already cached.
The native image tag was absent. Container and volume inventories were empty.
The asset folder already contained the completed Orders 7 through 9 downloads.
WSL root access used the Windows owner's existing Ubuntu-24.04 root entry point.

## Execution

Working directory: `/mnt/d/Documents/Projects/AICodingWorkspace/basic-memory-toolkit/basic-memory-installation`.
The entry point was:

```bash
sudo python3 scripts/build-native-runtime.py --run-id 20261107-order10-attempt01
```

The agent invoked the same script through the documented Windows WSL root entry point.
The script built only native-runtime and exported native-assets from the shared Dockerfile.
Ubuntu metadata was authenticated by APT. The download stage obtained 33.7 MB of indices and 3.2 MB of package archives.
The runtime installed 12 new packages and reinstalled two existing GCC libraries at their same selected versions.
No package was upgraded or removed inside the image.
The installation stage used --no-download and the exact authenticated archives from the download stage.

The [log](../validation/order-10-native-runtime-2026-11-07.log) contains build and package output.
The [machine evidence](../reference/order-10-native-runtime-2026-11-07.json) records every command and exit code.
The native image build, export, verification, and archive steps returned exit code 0.

## Downloaded package inventory

The first five selected packages and their required dependencies are all preserved by name and exact version.

| Package | Exact version |
| --- | --- |
| ca-certificates | 20260816ubuntu0.24.04.2 |
| libgcc-s1 | 14.2.0-4ubuntu2~24.04.1 |
| libgomp1 | 14.2.0-4ubuntu2~24.04.1 |
| libgssapi-krb5-2 | 1.20.1-6ubuntu2.10 |
| libk5crypto3 | 1.20.1-6ubuntu2.10 |
| libkeyutils1 | 1.6.3-3build1 |
| libkrb5-3 | 1.20.1-6ubuntu2.10 |
| libkrb5support0 | 1.20.1-6ubuntu2.10 |
| libldap2 | 2.6.10+dfsg-0ubuntu0.24.04.1 |
| libpq5 | 16.15-0ubuntu0.24.04.1 |
| libsasl2-2 | 2.1.28+dfsg1-5ubuntu3.1 |
| libsasl2-modules-db | 2.1.28+dfsg1-5ubuntu3.1 |
| libstdc++6 | 14.2.0-4ubuntu2~24.04.1 |
| openssl | 3.0.13-0ubuntu3.16 |

These are container packages. The WSL host package inventory hash was unchanged.

## Image and artifact index

| Element | Identity or path | Purpose and entry point |
| --- | --- | --- |
| Native image tag | local/basic-memory-native:ubuntu24.04-20261107 | Dockerfile native-runtime target. Inspect through docker image inspect. |
| Immutable native image identity | sha256:6079012aa6493ec37942670211927e8187ad39dd4afe43958d2629cd1be08d09 | Exact tested local image manifest. |
| Base image | ubuntu:24.04@sha256:78d4744ead1f5b19b04d0df558ab182a5300903900755e515b2ca4d10eb2044d | Recorded Ubuntu amd64 foundation. |
| Native image archive | /home/ydxu_/basic-memory-installation-assets/images/basic-memory-native/ubuntu24.04/linux-amd64/native-6079012aa649.oci.tar | Restore with docker image load. SHA-256: 2e402d1a9097c71f2f5e5282e4794f4be408859477f3c9b376ee1c7f998b7b50. |
| Package archives | /home/ydxu_/basic-memory-installation-assets/packages/order-10/ | Fourteen authenticated packages, under amd64 or all as appropriate. |
| Build and repository evidence | /home/ydxu_/basic-memory-installation-assets/metadata/order-10/20261107-order10-attempt01/ | Original Dockerfile, preparation helper, package plan, base inventory, signed indices, public key, package hashes, image metadata, and library check output. |
| Annotated Dockerfile | Content-addressed .dockerfile under the same metadata folder | Preserves comments for all 49 instructions. The command sequence matches the successfully built source. |
| Source Dockerfile | [basic-memory.dockerfile](../docker/basic-memory.dockerfile) | Authoritative image construction. Contains native and later application stages. |
| Build inputs and checks | [README file index](../README.md#complete-file-index) | Native preparation script, library checker, builder, context exclusions, guides, and results. |
| Reusable asset index | /home/ydxu_/basic-memory-installation-assets/index.json | Every archived file's version, purpose, source, size, and SHA-256 digest. |

The home folder now contains 31 package archives and three image archives.
Its 77 indexed files passed hash, size, and completeness checks. The index itself is the 78th file.
The disposable native verification container was removed. Container and volume inventories remained empty.
The temporary build context was removed after its reusable content was archived.
BuildKit retains its normal build cache in Docker's daemon storage.

## Verification and limits

All five selected package pins matched.
The CA certificate bundle was present and nonempty.
The libpq, libgomp, libstdc++, and libgcc dependency chains resolved without a missing library.
The native-only image contained neither uv nor Python 3.
The later uv image stage was not downloaded or built by this target.
No service restart, host package installation, application startup, model download, or GPU inference occurred.

After the successful build, the user requested comments for every Dockerfile command.
All 49 instructions received adjacent comments, with longer explanations for compound steps.
Removing comments and blank lines gives the same instruction sequence as the successfully built Dockerfile.
The evidence records the instruction hash and annotated source hash. No rebuild was needed for this documentation change.
The original build input and annotated source are both preserved.

Direct package pins and the base digest are fixed. Repository-selected transitive versions can change during a fresh rebuild.
The saved complete image archive preserves the exact tested result.
The final application stages still require separate testing under the later authorized orders.

## Independent resume and rebuild

Order 10 is complete. No repeat is required.
Use the [Order 10 guide](../docs/order-10-native-runtime.md) for the exact Dockerfile target, context, argument, and rebuild commands.
Use the [download guide](../docs/downloaded-assets.md) before copying or loading cached assets on another installation.
The next dependency is Order 11: uv 0.13.7 and CPython 3.13.18.
Await explicit user instruction before that operation.

## Documentation handoff

The README, checkpoint, dependency plan, record index, runbook, and validation notes contain the completed result.
All reusable bundle files and external assets are indexed.
The local static report distinguishes this successful native image build from the pending complete application image build.
