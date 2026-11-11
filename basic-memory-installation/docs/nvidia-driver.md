# Order 3: NVIDIA Windows driver

Checked: 2026-11-07, Asia/Shanghai.
Status: explanation and read-only inspection. No driver installation or download occurred.
This dependency is Order 3 in the plan and Step 2 in the runbook.

## Is an upgrade necessary?

**CUDA 12.8 is now the selected version in the documentation.**
Retain driver **572.84** for the first authorized inference test. No driver upgrade is planned for this selection.
The earlier plan proposed a newer driver for the CUDA 13 route. That proposal is not a universal installation prerequisite.

| Runtime route | Evidence | Conclusion |
| --- | --- | --- |
| Ollama CUDA 12.8 | NVIDIA lists Windows driver 572.61 or later for CUDA 12.8 Update 1. Installed 572.84 exceeds that version. | A source-supported candidate for testing without a driver upgrade. |
| RTX 5090 on the CUDA 12 runner | Ollama 0.40.15's Linux CUDA 12 build includes compute architecture 120. | RTX 5090 hardware alone does not force a CUDA 13 choice. |
| Ollama CUDA 13 | NVIDIA lists driver family 580 or later as the general CUDA 13 requirement. | Installed 572.84 does not meet this route's driver requirement. |

Sources: [CUDA 12.8 Update 1 release notes](https://docs.nvidia.com/cuda/archive/12.8.1/cuda-toolkit-release-notes/index.html), [Ollama CUDA build presets](https://raw.githubusercontent.com/ollama/ollama/v0.40.15/llama/server/CMakePresets.json), and [CUDA compatibility](https://docs.nvidia.com/deploy/cuda-compatibility/minor-version-compatibility.html).

Ollama's [release Dockerfile](https://raw.githubusercontent.com/ollama/ollama/v0.40.15/Dockerfile) supplies CUDA 12.8 and CUDA 13.0 runners.
The selected embedding model does not require us to select CUDA 13.
The original compatibility assessment used release metadata and driver requirements.
Order 15 subsequently passed actual model inference with driver 572.84, GPU residency, and CUDA 12.8 mappings.
See the [Order 15 result](../records/2026-11-07-order-15-model-attempt-01.md).

At the later authorized inference test, inspect Ollama's active runner, model residency, and logs.
A successful `nvidia-smi` command alone does not complete that test.
If a failure occurs, diagnose it before attributing the failure to the driver.
Upgrade if the selected runtime requires a newer driver, a confirmed driver fault requires a fix, or the user selects maintenance.
A general maintenance update remains a separate decision from the minimum driver needed for this installation.
No model download, CUDA runner change, driver change, or test is authorized by this documentation update.

## Purpose and placement

The Windows NVIDIA display driver controls the laptop GPU.
It also supplies the CUDA driver interface that WSL uses through `libcuda.so`.
GPU applications inside later Docker containers use that host interface.
Install the display driver on Windows.
Do not install a Linux NVIDIA display driver in WSL2. It can overwrite the mapped driver interface.
Source: [NVIDIA CUDA on WSL](https://docs.nvidia.com/cuda/wsl-user-guide/).

The driver, CUDA Toolkit, CUDA runtime, cuDNN, and NVIDIA Container Toolkit have different roles.

| Element | Location in this design | Role |
| --- | --- | --- |
| NVIDIA display driver | Windows | Controls the GPU and supplies the WSL CUDA driver interface. |
| WSL GPU interface | Supplied through Windows and WSL | Makes the Windows GPU accessible to Linux applications. |
| NVIDIA Container Toolkit | Later installation inside the WSL Docker host | Exposes GPU devices and driver libraries to containers. |
| CUDA runtime libraries | Ollama image | Execute the selected model backend. |
| CUDA development toolkit and cuDNN installed on the host | No separate installation selected | Unnecessary for the selected prebuilt embedding path. |

This driver step does not install Docker, uv, a CUDA Toolkit, cuDNN, Ollama, or Basic Memory.

## Observed state and version choice

| Item | Result |
| --- | --- |
| Manufacturer and reported family | MECHREVO, YAOSHI Series |
| GPU | NVIDIA GeForce RTX 5090 Laptop GPU |
| Driver | 572.84 |
| Windows release and build | 25H2, 26200.9711 |
| Original proposed driver pin | 595.79 WHQL |
| Newer candidate found during this review | NVIDIA Studio 621.14 WHQL, released 2026-11-04 |
| Installation decision | CUDA 12.8 selected in documentation. Retain 572.84 for initial testing. No update executed. |

The current driver already exposes the GPU to WSL.
The CUDA 13 runner needs a newer driver family. NVIDIA lists family 580 as the general CUDA 13 minimum.
This is a compatibility condition, not proof of successful model inference.
Source: [NVIDIA CUDA compatibility](https://docs.nvidia.com/deploy/cuda-compatibility/minor-version-compatibility.html).

The 595.79 entry was a proposed compatibility baseline. It was not a claim that this version was the latest release.
NVIDIA lists 621.14 for Windows and the RTX 5090 Laptop GPU.
Review the notebook OEM package first, as NVIDIA recommends for notebooks.
Sources: [NVIDIA Studio 621.14](https://www.nvidia.com/en-us/drivers/details/283967/) and [MECHREVO downloads](https://www.mechrevo.com/cn/downloads).

For this compute-focused setup, Studio is a reasonable preference. This is a deployment recommendation, not a CUDA requirement.
NVIDIA describes Studio releases around creative application reliability and Game Ready releases around new games.
Source: [NVIDIA driver selection](https://www.nvidia.com/en-in/geforce/drivers/).

The generic YAOSHI Series identifier does not determine the exact retail model.
Select the matching notebook model on MECHREVO's site.
If the OEM lookup needs a serial number, enter it directly on the OEM site. Do not copy it into public records.

## Check the version yourself

### In WSL

Run:

```bash
/usr/lib/wsl/lib/nvidia-smi --query-gpu=name,driver_version --format=csv,noheader
```

The observed output was:

```text
NVIDIA GeForce RTX 5090 Laptop GPU, 572.84
```

For the full status display, run:

```bash
/usr/lib/wsl/lib/nvidia-smi
```

Read the `Driver Version` field. A newer utility can label the corresponding field `KMD Version`.
The `CUDA Version` or `CUDA UMD Version` field describes driver support.
It does not establish that a CUDA Toolkit is installed.
Source: [NVIDIA System Management Interface](https://docs.nvidia.com/deploy/nvidia-smi/index.html).

### In Windows PowerShell

Run:

```powershell
nvidia-smi --query-gpu=name,driver_version --format=csv,noheader
```

If Windows cannot locate the command, use NVIDIA Control Panel.
Open **Help > System Information** and read **Driver version**.
Use the NVIDIA release version, such as 572.84, when comparing with the installation plan.
A Windows Device Manager version can use another numbering format.

## Proposed procedure after package selection

The following actions are instructions for a later user-selected operation.
No action in this procedure has run.

1. Record the current driver version and the notebook's exact model.
2. Review the matching OEM driver and the NVIDIA notebook package.
3. Select the exact package and version before changing the driver pin.
4. Download the Windows notebook package from its official source.
5. Record the package filename, source URL, and SHA-256 hash.
6. Check the installer's Windows signature and publisher.
7. Save active work before the driver update.
8. Connect the notebook to its power supply.
9. Run the Windows installer only after the user selects that action.
10. Follow the installer's restart instructions.
11. After the restart, open this bundle's README again.
12. Check the version in Windows.
13. Check the version in WSL.
14. Record both results and update the installation checkpoint.
15. Stop before the next installation operation.

The driver update can interrupt the display, GPU work, WSL, and this application session.
Keep the README and checkpoint paths available before the update.

Optional Windows package checks, after downloading an installer:

```powershell
$bmDriverInstaller = 'C:\path\to\the-downloaded-driver.exe'
Get-FileHash -Algorithm SHA256 -LiteralPath $bmDriverInstaller
Get-AuthenticodeSignature -LiteralPath $bmDriverInstaller |
    Format-List Status, StatusMessage, SignerCertificate
```

Use the actual filename instead of the example path.
Check that the signature status is valid and the signer matches the official publisher.
A recorded hash identifies the selected file. It does not replace signature verification.

## Acceptance and failure handling

The driver step passes when the selected version appears in Windows and WSL without a driver initialization error.
Confirm normal display operation after the restart.
Record any version difference or WSL error before proceeding.

This check establishes driver access. Docker visibility and GPU inference remain later acceptance steps.
If the update fails, retain the exact installer error and any partial changes in the step record.
If Windows works but WSL fails, inspect Windows driver status first.
Do not install a Linux NVIDIA display driver as a WSL repair.
Review a return to the notebook's previous supported package only under a separate user instruction.

## Immediate next action

Check the current version through either command above.
The user selected CUDA 12.8 in the documentation. Retain 572.84 for later authorized testing.
The 595.79 value retained in the saved configuration is historical optional upgrade metadata. It is not selected for this route.
Actual runner selection and inference verification remain later operations.
See the [checkpoint](installation-status.md) and [README](../README.md) for independent resume entry points.
