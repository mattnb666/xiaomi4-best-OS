#!/usr/bin/env bash
# Run inside Ubuntu/WSL2, using its Linux filesystem, not /mnt/c.
set -euo pipefail
bestos_tools_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
if [[ $(uname -s) != Linux || $(uname -m) != x86_64 ]]; then
  echo '需要 Linux x86_64（可使用 Ubuntu / WSL2）。' >&2; exit 1
fi
command -v repo >/dev/null || { echo '请先安装 repo。' >&2; exit 1; }
command -v python3 >/dev/null || { echo '请先安装 python3。' >&2; exit 1; }
bestos_source_dir=${1:-"$HOME/bestos/aosp10"}
mkdir -p "$bestos_source_dir"
cd "$bestos_source_dir"
case "$PWD" in /mnt/*) echo '请使用 WSL Linux 文件系统内的路径。' >&2; exit 1;; esac
# Project planning reserve, not a claim about an exact Android 10 requirement.
python3 - <<'PY'
import shutil,sys
free=shutil.disk_usage('.').free
if free < 200 * 1024**3:
    sys.exit('当前可用空间 %.1f GiB；本项目首次同步预留至少 200 GiB，编译前仍须重新检查。' % (free/1024**3))
PY
python3 "$bestos_tools_dir/preflight.py" --source-parent "$PWD" --network
if [[ -e .repo/manifest.xml ]]; then
  echo '已有 repo 工作区；为避免改变现有分支，请在该目录手动检查后继续同步。' >&2; exit 1
fi
repo init -u https://android.googlesource.com/platform/manifest -b android-10.0.0_r47 --depth=1
repo sync -c -j2 --no-clone-bundle --no-tags --fail-fast
repo manifest -r -o bestos-aosp10-pinned.xml
printf '%s\n' '源码同步结束并导出固定 revision 清单；尚未加入 cancro 设备构建目标，未编译 ROM。'
