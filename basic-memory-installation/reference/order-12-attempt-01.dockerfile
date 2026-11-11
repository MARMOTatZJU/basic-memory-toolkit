# Dependency Order 10 builds native-runtime and exports native-assets.
# Dependency Order 11 builds python-runtime; Order 12 builds build-backends. The application stage remains pending.
# Use Docker Engine's bundled frontend to avoid a separate Dockerfile frontend download.

# Select the versioned uv tool image for the later Python installation stage.
ARG BM_UV_IMAGE=ghcr.io/astral-sh/uv:0.13.7@sha256:c7db1d63057f268a8b6da8af9077850a60461f98d23db23c676a82089a050c91
# Pin the Ubuntu 24.04 amd64 base by digest so every stage starts from the recorded image.
ARG BM_BASE_IMAGE=ubuntu:24.04@sha256:78d4744ead1f5b19b04d0df558ab182a5300903900755e515b2ca4d10eb2044d

# Create the package download stage from the pinned Ubuntu base. Its authenticated files feed both installation and archive export.
FROM ${BM_BASE_IMAGE} AS native-downloads
# Select the exact CA bundle package version used by the native foundation.
ARG BM_CA_CERTIFICATES_VERSION=20260816ubuntu0.24.04.2
# Keep libgomp1, libstdc++6, and libgcc-s1 on the same selected GCC runtime version.
ARG BM_NATIVE_GCC_VERSION=14.2.0-4ubuntu2~24.04.1
# Select the PostgreSQL client library required by the application's pure Python Psycopg package.
ARG BM_LIBPQ_VERSION=16.15-0ubuntu0.24.04.1
# Add the versioned helper that prepares the authenticated native package cache and its provenance records.
COPY docker/prepare-native-packages.sh /usr/local/libexec/prepare-native-packages.sh
# Authenticate Ubuntu repository metadata, then download the five selected package pins and their required dependencies.
# Retain complete package archives, signed indices, the public repository key, package records, and the simulated installation plan.
# The native-runtime stage installs these same downloaded files. The native-assets stage exports them for later reuse.
RUN bash /usr/local/libexec/prepare-native-packages.sh

# Create an empty export stage whose filesystem contains reusable packages and build provenance.
FROM scratch AS native-assets
# Export all downloaded native package archives, including required dependencies, into the Order 10 asset folder.
COPY --from=native-downloads /var/cache/apt/archives/*.deb /packages/order-10/amd64/
# Export the package plan, baseline inventory, public key, source definition, package records, and checksums.
COPY --from=native-downloads /native-evidence/ /metadata/order-10/
# Retain the authenticated repository indices so saved package hashes can be traced to their original metadata.
COPY --from=native-downloads /var/lib/apt/lists/ /metadata/order-10/apt-lists/

# Start the deployable native foundation from the clean pinned base, separate from the download stage.
FROM ${BM_BASE_IMAGE} AS native-runtime
# Select the exact CA bundle package version used by the native foundation.
ARG BM_CA_CERTIFICATES_VERSION=20260816ubuntu0.24.04.2
# Keep libgomp1, libstdc++6, and libgcc-s1 on the same selected GCC runtime version.
ARG BM_NATIVE_GCC_VERSION=14.2.0-4ubuntu2~24.04.1
# Select the PostgreSQL client library required by the application's pure Python Psycopg package.
ARG BM_LIBPQ_VERSION=16.15-0ubuntu0.24.04.1
# Expose the selected base reference inside this stage for its provenance label.
ARG BM_BASE_IMAGE
# Identify this intermediate runtime image and record its exact Ubuntu base reference.
LABEL org.opencontainers.image.title="Basic Memory native runtime foundation" \
    org.opencontainers.image.base.name="${BM_BASE_IMAGE}"
# Mount the authenticated package archives and repository indices read-only from the download stage.
# Copy them into APT's writable cache locations and install the exact native package versions without another package download.
# Reinstall the selected GCC libraries even when the base already contains those versions.
# Remove repository indices and package archives from the runtime layer after installation. Portable copies remain available through native-assets.
RUN --mount=type=bind,from=native-downloads,source=/var/cache/apt/archives,target=/mnt/native-packages \
    --mount=type=bind,from=native-downloads,source=/var/lib/apt/lists,target=/mnt/native-lists \
    cp /mnt/native-packages/*.deb /var/cache/apt/archives/ \
    && cp -a /mnt/native-lists/. /var/lib/apt/lists/ \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-download --no-install-recommends --reinstall \
        ca-certificates="${BM_CA_CERTIFICATES_VERSION}" \
        libpq5="${BM_LIBPQ_VERSION}" \
        libgomp1="${BM_NATIVE_GCC_VERSION}" \
        libstdc++6="${BM_NATIVE_GCC_VERSION}" \
        libgcc-s1="${BM_NATIVE_GCC_VERSION}" \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*.deb

# Make the versioned uv and uvx binaries available to the later application stage.
FROM ${BM_UV_IMAGE} AS uv
# Extend the verified native foundation with uv and managed CPython for dependency Order 11.
FROM native-runtime AS python-runtime
# Require the selected uv executable version during interpreter validation.
ARG BM_UV_VERSION=0.13.7
# Select the exact CPython patch release, independent of the host interpreter.
ARG BM_PYTHON_VERSION=3.13.18
# Pin the standalone build used by uv's managed Python installer.
ARG BM_PYTHON_BUILD=20261026
# Identify the exact downloaded archive mounted during the offline installation step.
ARG BM_PYTHON_ARCHIVE_NAME=cpython-3.13.18+20261026-x86_64-unknown-linux-gnu-install_only_stripped.tar.gz
# Authenticate the archive against its recorded publisher checksum before uv reads it.
ARG BM_PYTHON_ARCHIVE_SHA256=df15fe60d3ff55bf9dcf25824b5572756bb8816ff93865a273d3301d7066a8b7
# Require the selected SQLite library version in the managed interpreter.
ARG BM_EXPECTED_SQLITE_VERSION=3.53.1
# Identify this intermediate image and its selected Python and uv versions.
LABEL org.opencontainers.image.title="Basic Memory uv-managed Python foundation" \
    org.opencontainers.image.python.version="${BM_PYTHON_VERSION}" \
    org.opencontainers.image.uv.version="${BM_UV_VERSION}"
# Install uv and uvx from the digest-pinned official tool image.
COPY --from=uv /uv /uvx /usr/local/bin/
# Record managed interpreter locations, stable installation prefix, and exact validation expectations.
# Keep bytecode writes disabled and output unbuffered for later image checks.
ENV UV_PYTHON_INSTALL_DIR=/opt/uv/python \
    UV_PYTHON_PREFERENCE=only-managed \
    UV_PYTHON_CPYTHON_BUILD=${BM_PYTHON_BUILD} \
    UV_PROJECT_ENVIRONMENT=/opt/bm-python \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    BM_EXPECTED_PYTHON_VERSION=${BM_PYTHON_VERSION} \
    BM_EXPECTED_UV_VERSION=${BM_UV_VERSION} \
    BM_EXPECTED_PYTHON_BUILD=${BM_PYTHON_BUILD} \
    BM_EXPECTED_PYTHON_ARCHIVE_SHA256=${BM_PYTHON_ARCHIVE_SHA256} \
    BM_EXPECTED_SQLITE_VERSION=${BM_EXPECTED_SQLITE_VERSION}
# Preserve the authenticated archive identity inside the image for runtime inspection.
COPY python-archive.json /opt/installation/python-archive.json
# Verify the mounted standalone archive, then let uv install it through its supported local mirror.
# Disable build-step networking so this operation uses only the prepared archive and the pinned uv image.
# Resolve the actual managed prefix and expose it through the stable /opt/bm-python symlink.
RUN --network=none --mount=type=bind,source=python-archives,target=/opt/python-archives \
    echo "${BM_PYTHON_ARCHIVE_SHA256}  /opt/python-archives/${BM_PYTHON_BUILD}/${BM_PYTHON_ARCHIVE_NAME}" | sha256sum --check - \
    && UV_PYTHON_INSTALL_MIRROR=file:///opt/python-archives \
       uv python install "cpython-${BM_PYTHON_VERSION}-linux-x86_64-gnu" \
    && bm_python="$(uv python find "cpython-${BM_PYTHON_VERSION}-linux-x86_64-gnu")" \
    && ln -s "$("$bm_python" -c 'import sys; print(sys.prefix)')" /opt/bm-python
# Select the managed Python binaries for subsequent image instructions and container commands.
ENV PATH=/opt/bm-python/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
# Add the focused Order 11 validator as a versioned image build input.
COPY docker/check-python-runtime.py /opt/installation/check-python-runtime.py
# Check exact versions, FTS5, extension loading, native libraries, and the direct managed prefix.
# These checks use temporary in-memory data and require no application package or network access.
RUN --network=none python /opt/installation/check-python-runtime.py

# Add the exact application build backends to the verified managed Python prefix for dependency Order 12.
FROM python-runtime AS build-backends
# Identify the build-tool foundation independently from the complete application image.
LABEL org.opencontainers.image.title="Basic Memory application build backend foundation"
# Preserve the full backend dependency resolution, including archive hashes, for deterministic offline installation.
COPY config/build-backends.lock /opt/installation/build-backends.lock
# Keep the two selected backend pins beside their complete resolved dependency lock.
COPY config/build-constraints.txt /opt/installation/build-constraints.txt
# Include exact selected wheel identities for installed-version and provenance checks.
COPY backend-wheel-inventory.json /opt/installation/backend-wheel-inventory.json
# Include the version, prefix, dependency, and disposable wheel-build verification procedure.
COPY docker/check-build-backends.py /opt/installation/check-build-backends.py
# Mount only verified local wheels and require their hashes when installing into the existing managed prefix.
# Disable networking and package-index access so installation uses the saved wheel set exclusively.
# Check dependency consistency and build a disposable fixture wheel to verify Hatchling's dynamic-version plugin.
RUN --network=none --mount=type=bind,source=build-wheels,target=/opt/build-wheels \
    uv pip install --python /opt/bm-python/bin/python --no-index --find-links /opt/build-wheels \
        --only-binary :all: --require-hashes --requirement /opt/installation/build-backends.lock \
    && uv pip check --python /opt/bm-python/bin/python \
    && python /opt/installation/check-build-backends.py

# Extend the prepared native, Python, and backend foundations during the later application installation order.
FROM build-backends AS basic-memory

# Set the release version used by image labels, package version generation, and runtime checks.
ARG BM_VERSION=1.0.0
# Record the source commit. The build helper exports this same commit into the source directory.
ARG BM_COMMIT=c9bd187b83baba549d5cd16bacc180f8023d51c8
# Select the exact CPython version that uv will install in the container.
ARG BM_PYTHON_VERSION=3.13.18
# Set the SQLite version that the later interpreter and application checks must confirm.
ARG BM_EXPECTED_SQLITE_VERSION=3.53.1
# Select the exact CA bundle package version used by the native foundation.
ARG BM_CA_CERTIFICATES_VERSION=20260816ubuntu0.24.04.2
# Keep libgomp1, libstdc++6, and libgcc-s1 on the same selected GCC runtime version.
ARG BM_NATIVE_GCC_VERSION=14.2.0-4ubuntu2~24.04.1
# Select the PostgreSQL client library required by the application's pure Python Psycopg package.
ARG BM_LIBPQ_VERSION=16.15-0ubuntu0.24.04.1
# Select the container user ID used for application state and mounted note ownership.
ARG BM_APP_UID=1000
# Select the matching container group ID for application and note permissions.
ARG BM_APP_GID=1000
# Attach release, commit, and upstream source metadata to the final application image.
LABEL org.opencontainers.image.title="Basic Memory complete runtime" \
    org.opencontainers.image.version="${BM_VERSION}" \
    org.opencontainers.image.revision="${BM_COMMIT}" \
    org.opencontainers.image.source="https://github.com/basicmachines-co/basic-memory"

# Set application build constraints, release version generation, and expected package identity for later checks.
ENV UV_BUILD_CONSTRAINT=/opt/installation/build-constraints.txt \
    UV_DYNAMIC_VERSIONING_BYPASS=${BM_VERSION} \
    BM_EXPECTED_VERSION=${BM_VERSION}

# Supply exact build-backend constraints for the application package installation.
COPY config/build-constraints.txt /opt/installation/build-constraints.txt
# Provide the audited package-version inventory used to validate the completed image.
COPY reference/dependencies/expected-application-versions.json /opt/installation/expected-application-versions.json
# Include the native runtime validator and the separate embedding verification helper.
COPY docker/check-runtime.py docker/check-embedding.py /opt/installation/
# Install the startup script that registers the configured local project before starting the service.
COPY docker/container-entrypoint.sh /usr/local/bin/basic-memory-entrypoint
# Copy the clean source commit exported by the build helper into the application directory.
COPY source/ /app/
# Run dependency installation and the application from the exported project directory.
WORKDIR /app
# Require a consistent release lock, include all application extras, and omit development dependencies.
# Use the verified in-container build backends without a temporary build environment.
# Install the source as a regular package into the selected Python environment.
# Check dependency consistency, package identity, native imports, SQLite features, and the intended Python layout.
# Make the startup script executable. Any failed check stops this application image build.
RUN uv sync --locked --all-extras --no-dev --no-editable --no-build-isolation --python /opt/bm-python/bin/python \
    && uv pip check --python /opt/bm-python/bin/python \
    && python /opt/installation/check-runtime.py \
    && chmod 0755 /usr/local/bin/basic-memory-entrypoint

# Reuse the configured group and user IDs when present, or create accounts for those IDs.
# Create the application state and note directories with ownership matching the selected container account.
# This prepares writable paths for later persistent storage and the note bind mount.
RUN (getent group "${BM_APP_GID}" || groupadd --gid "${BM_APP_GID}" bmgroup) \
    && (getent passwd "${BM_APP_UID}" || useradd --uid "${BM_APP_UID}" --gid "${BM_APP_GID}" --create-home bmuser) \
    && install -d -m 0755 -o "${BM_APP_UID}" -g "${BM_APP_GID}" /var/lib/basic-memory /notes
# Set persistent state and note locations, then apply the selected local configuration flags.
ENV BASIC_MEMORY_CONFIG_DIR=/var/lib/basic-memory \
    BASIC_MEMORY_HOME=/notes \
    BASIC_MEMORY_AUTO_UPDATE=false \
    BASIC_MEMORY_FORCE_LOCAL=true
# Run the service with the configured user and group IDs so file ownership follows the selected note account.
USER ${BM_APP_UID}:${BM_APP_GID}
# Document the container's MCP service port. The Compose configuration controls the actual host port mapping.
EXPOSE 8000
# Allow a startup grace period, then periodically check that the service accepts a TCP connection on port 8000.
# MCP operations, retrieval, and GPU execution require the separate acceptance checks.
HEALTHCHECK --interval=30s --timeout=5s --start-period=120s --retries=5 \
    CMD ["python", "-c", "import socket; socket.create_connection(('127.0.0.1', 8000), 3).close()"]
# Register the selected local project through the startup script, then execute the service command.
ENTRYPOINT ["/usr/local/bin/basic-memory-entrypoint"]
# Start the MCP server with streamable HTTP on container port 8000 and the /mcp endpoint.
CMD ["basic-memory", "mcp", "--transport", "streamable-http", "--host", "0.0.0.0", "--port", "8000", "--path", "/mcp"]
