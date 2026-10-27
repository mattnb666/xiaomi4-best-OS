#!/usr/bin/env bash
# Explicit stages: no flash commands and no invented build target.
set -euo pipefail
bestos_root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
bestos_mode=${1:-help}
case "$bestos_mode" in
  help|--help|-h)
    printf '%s\n' 'Usage: bash start-bestos.sh prepare|sync|all|check [source-directory]' \
      'prepare: install Ubuntu 22.04 baseline dependencies' \
      'sync: preflight and download Android 10 r47 (can resume matching workspace)' \
      'all: prepare then sync; does NOT compile an unported ROM' \
      'check: read-only host check (apart from temporary filesystem probe)' \
      'Logs: out/environment/'; exit 0;;
  prepare|sync|all|check) ;;
  *) echo 'Unknown stage. Use --help.' >&2; exit 2;;
esac
if [[ $(uname -s) != Linux || $(uname -m) != x86_64 ]]; then
  echo 'Requires Linux x86_64. Read docs/linux-start.md.' >&2; exit 1
fi
if [[ $EUID == 0 ]]; then echo 'Run as a normal user; installer requests sudo when needed.' >&2; exit 1; fi
bestos_dest=${2:-"$HOME/bestos/aosp10"}
mkdir -p "$bestos_root/out/environment"
bestos_log="$bestos_root/out/environment/$(date +%Y%m%d-%H%M%S)-$$-$bestos_mode.log"
exec > >(tee -a "$bestos_log") 2>&1
trap 'echo "Stage failed; inspect log. No build success is implied."' ERR
if [[ -r /proc/meminfo ]]; then
  bestos_ram=$(awk '/^MemTotal:/ {print $2}' /proc/meminfo)
  if (( bestos_ram < 8000000 )); then
    echo 'Low RAM: source preparation only; full AOSP build is not recommended on this host.'
  fi
fi
if [[ $bestos_mode == prepare || $bestos_mode == all ]]; then
  bash "$bestos_root/tools/setup_ubuntu.sh"
fi
if [[ $bestos_mode == check ]]; then
  python3 "$bestos_root/tools/preflight.py" --source-parent "$bestos_root" --network
elif [[ $bestos_mode == sync || $bestos_mode == all ]]; then
  bash "$bestos_root/tools/sync_aosp10.sh" "$bestos_dest"
fi
printf '%s\n' "Finished stage: $bestos_mode" 'No cancro ROM compiled. Next: docs/linux-start.md'
