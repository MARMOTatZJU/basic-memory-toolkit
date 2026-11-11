# Order 13 attempt 1: installer path failure

Date: 2026-11-07, Asia/Shanghai.
Authorization: "proceed to order 13".
Status: **failed**. A corrected second attempt follows the same authorized scope.

## Execution and result

The exact source commit and 190 publisher archives passed verification.
The Dockerfile built Pybars3 0.9.7 and PyMeta3 0.5.1 offline through Setuptools 83.0.0 and pip 26.2.2.
The complete 190-wheel export passed. No network access was enabled for either installation step.

From the installation bundle in Ubuntu WSL2, the Windows owner used the existing WSL root identity to run:

```bash
python3 scripts/build-application.py --run-id 20261107-order13-attempt01 --attempt 1
```

The application stage reached uv pip install through /opt/bm-python/bin/python.
uv failed to create the websockets command script through a relative path that traversed the interpreter symlink.
The selected wheel contained no external RECORD paths or bundled .data/scripts entries.
The installer exited with code 2. Docker build and the helper exited with code 1.
The application image tag was not created. The failed RUN layer did not become a completed image.
Earlier foundations and verified archives remained available.

## Preserved artifacts and recovery

| Element | Entry point | Purpose |
| --- | --- | --- |
| Exact failed Dockerfile | [attempt-01 Dockerfile](../reference/order-13-attempt-01.dockerfile) | Original installer path and successful wheel stages. |
| Failure evidence | [attempt-01 JSON](../reference/order-13-application-attempt-01-2026-11-07.json) | Commands, preflight, archive recovery, failure, and original staging path. |
| Failure log | [attempt-01 log](../validation/order-13-application-attempt-01-2026-11-07.log) | Full offline wheel and application build output. |
| Active input | [Dockerfile](../docker/basic-memory.dockerfile) | Corrected canonical prefix for UV_PROJECT_ENVIRONMENT and application installer commands. |
| Next attempt | [attempt 2](2026-11-07-order-13-application-attempt-02.md) | Corrected build and its current result. |

The failed context was /home/ydxu_/basic-memory-installation-assets/.staging/order13-gr31eft8.
The exact Dockerfile and results were preserved before that redundant temporary context was removed.
The 190 original archives remained in the preflight cache for the retry. BuildKit retained the successful wheel stage.
The correction uses /opt/uv/python/cpython-3.13.18-linux-x86_64-gnu for installation.
The stable /opt/bm-python alias remains available for runtime commands.

Read the [Order 13 guide](../docs/order-13-application.md) before a repeat.
Complete only Order 13. Stop before Order 14.
