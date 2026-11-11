# Order 9 attempt 2: packages installed, original image pull interrupted

Date: 2026-11-07, Asia/Shanghai.
Authorization: "Proceed to order 9. Try to fix the connection issues."
Status: **failed** at the combined installer's GPU-check stage. Its package and runtime steps passed.

The verified curl cache supplied all four exact packages to APT.
APT installed version 1.20.1-1 for every package, with no upgrades or removals.
Docker accepted its NVIDIA runtime configuration and restarted successfully.
The native Docker Hub image stream was slow.
The agent loaded the same pinned image through verified range downloads and Docker's archive interface.
The original image-pull client was then canceled. The combined installer returned exit code 130.

One diagnostic template referenced the image's absent optional Config.Volumes field.
The image itself was available through its correct pinned digest.
The final check uses the full image JSON and handles optional fields correctly.

Read the [attempt 2 evidence](../reference/order-09-nvidia-toolkit-attempt-02-2026-11-07.json) and [log](../validation/order-09-installation-attempt-02-2026-11-07.log).
The [image receipt](../reference/order-09-ubuntu-image-transfer-2026-11-07.json) records every verified digest and the successful import.
Continue through [attempt 3](2026-11-07-order-09-nvidia-toolkit-attempt-03.md) for the GPU-only check.
Do not reinstall packages or restart Docker to repeat that check.
