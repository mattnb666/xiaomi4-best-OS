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
if [[ -d .repo ]]; then
  if [[ ! -f .repo/bestos-source.json ]]; then
    echo 'Existing unmanaged/incomplete repo workspace; inspect manually, do not overwrite.' >&2; exit 1
  fi
  python3 - <<'CHECK'
import json, subprocess, xml.etree.ElementTree as ET
from pathlib import Path
expected={'url':'https://android.googlesource.com/platform/manifest','tag':'android-10.0.0_r47'}
if json.loads(Path('.repo/bestos-source.json').read_text()) != expected:
    raise SystemExit('Workspace marker mismatch')
url=subprocess.check_output(['git','-C','.repo/manifests','remote','get-url','origin'],text=True).strip()
root=ET.parse('.repo/manifest.xml').getroot()
default=root.find('default')
if url != expected['url'] or default is None or default.get('revision') != 'refs/tags/'+expected['tag']:
    raise SystemExit('Manifest source/revision mismatch; inspect before syncing')
if Path('.repo/local_manifests').exists():
    raise SystemExit('Local manifests present; review before automatic sync')
CHECK
else
  if [[ -n $(ls -A) ]]; then echo 'Choose an empty source directory.' >&2; exit 1; fi
  repo init -u https://android.googlesource.com/platform/manifest -b android-10.0.0_r47 --depth=1
  python3 - <<'MARK'
import json
from pathlib import Path
Path('.repo/bestos-source.json').write_text(json.dumps({'url':'https://android.googlesource.com/platform/manifest','tag':'android-10.0.0_r47'})+'\n')
MARK
fi
repo sync -c -j2 --no-clone-bundle --no-tags --fail-fast
repo manifest -r -o bestos-aosp10-pinned.xml
printf '%s\n' '源码同步结束并导出固定 revision 清单；尚未加入 cancro 设备构建目标，未编译 ROM。'
