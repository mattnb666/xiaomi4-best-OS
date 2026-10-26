#!/usr/bin/env bash
set -euo pipefail
if [[ $(uname -s) != Linux || $(uname -m) != x86_64 ]]; then
  echo 'This setup requires Linux x86_64.' >&2; exit 1
fi
. /etc/os-release
if [[ ${ID:-} != ubuntu || ${VERSION_ID:-} != 22.04 ]]; then
  echo 'Prepared for Ubuntu 22.04. Review dependencies before using another distro.' >&2; exit 1
fi
# Baseline host tools, not a validated Android 10 or cancro toolchain.
sudo apt-get update
sudo apt-get install -y git curl ca-certificates gnupg python3 repo \
  build-essential flex bison zip unzip rsync bc cpio xz-utils file \
  zlib1g-dev libc6-dev-i386 lib32z1-dev lib32stdc++6 libelf-dev libssl-dev \
  libxml2-utils xsltproc fontconfig libgl1-mesa-dev device-tree-compiler
repo version
printf '%s\n' 'Baseline dependencies installed. Run preflight before source sync.'
