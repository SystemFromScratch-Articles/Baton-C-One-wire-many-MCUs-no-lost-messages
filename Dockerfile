# syntax=docker/dockerfile:1.7
#
# Build and test environment of the article: Zephyr SDK (ARM Cortex-M only),
# west and the Python packages of the Zephyr build and twister.
# Based on https://github.com/AntonVynohradov/Zephyr-SmartFusion2-workspace,
# updated for Zephyr 4.5: Python 3.12+ (Debian trixie) and Zephyr SDK 1.0.
#
# SPDX-License-Identifier: Apache-2.0

FROM debian:trixie-slim

ARG DEBIAN_FRONTEND=noninteractive
ARG WEST_VERSION=1.5.0
ARG ZEPHYR_SDK_VERSION=1.0.1

ENV \
    ZEPHYR_SDK_INSTALL_DIR=/opt/zephyr-sdk \
    ZEPHYR_TOOLCHAIN_VARIANT=zephyr \
    VIRTUAL_ENV=/opt/venv \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    CCACHE_DIR=/ccache \
    PATH=/opt/venv/bin:/opt/zephyr-sdk/gnu/arm-zephyr-eabi/bin:${PATH}

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates ccache cmake device-tree-compiler file g++ gcc git gperf \
        make ninja-build python3 python3-dev python3-pip python3-venv wget xz-utils \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv "${VIRTUAL_ENV}" \
    && pip install "west==${WEST_VERSION}"

# Minimal SDK (host tools, CMake package) plus the ARM toolchain only. From
# SDK 1.0 the GNU toolchains live under gnu/.
RUN set -eux; \
    base="https://github.com/zephyrproject-rtos/sdk-ng/releases/download/v${ZEPHYR_SDK_VERSION}"; \
    cd /tmp; \
    wget -q "${base}/sha256.sum" \
        "${base}/zephyr-sdk-${ZEPHYR_SDK_VERSION}_linux-x86_64_minimal.tar.xz" \
        "${base}/toolchain_gnu_linux-x86_64_arm-zephyr-eabi.tar.xz"; \
    grep -E "_linux-x86_64_minimal|gnu_linux-x86_64_arm-zephyr-eabi" sha256.sum \
        | sha256sum -c -; \
    mkdir -p "${ZEPHYR_SDK_INSTALL_DIR}/gnu"; \
    tar -xJf "zephyr-sdk-${ZEPHYR_SDK_VERSION}_linux-x86_64_minimal.tar.xz" \
        --strip-components=1 -C "${ZEPHYR_SDK_INSTALL_DIR}"; \
    tar -xJf toolchain_gnu_linux-x86_64_arm-zephyr-eabi.tar.xz \
        -C "${ZEPHYR_SDK_INSTALL_DIR}/gnu"; \
    rm -f /tmp/*.tar.xz /tmp/sha256.sum; \
    cmake -P "${ZEPHYR_SDK_INSTALL_DIR}/cmake/zephyr_sdk_export.cmake"

RUN mkdir -p /ccache \
    && ccache --set-config=max_size=2G \
    && ccache --set-config=compression=true

WORKDIR /workspace
CMD ["/bin/bash"]
