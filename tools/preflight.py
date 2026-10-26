"""Read-only Linux/source-host checks. Optional network probes; no credentials read."""
import argparse, json, platform, shutil, subprocess, tempfile
from pathlib import Path

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--source-parent', type=Path, default=Path.home())
    p.add_argument('--network', action='store_true')
    args = p.parse_args()
    parent = args.source_parent.expanduser().resolve()
    if not parent.is_dir(): p.error('--source-parent must be an existing directory')
    report = {'platform': platform.system(), 'arch': platform.machine(),
              'free_gib': round(shutil.disk_usage(parent).free / 1024**3, 1),
              'tools': {n: bool(shutil.which(n)) for n in ['git','repo','python3','make','gcc','curl','dtc']}}
    # Temporary probe leaves no permanent source files.
    with tempfile.TemporaryDirectory(prefix='bestos-check-', dir=parent) as d:
        f = Path(d)/'case'; f.write_text('probe')
        report['case_sensitive'] = not (Path(d)/'CASE').exists()
    report['windows_mount'] = str(parent).startswith('/mnt/')
    if Path('/proc/meminfo').exists():
        report['memory_kib'] = {line.split(':')[0]: int(line.split()[1]) for line in
            Path('/proc/meminfo').read_text().splitlines() if line.startswith(('MemTotal:', 'SwapTotal:'))}
    if args.network:
        report['network'] = {}
        for name, url in [('manifest','https://android.googlesource.com/platform/manifest'),
                          ('repo','https://gerrit.googlesource.com/git-repo')]:
            try:
                r = subprocess.run(['git','ls-remote',url,'HEAD'], capture_output=True, timeout=30)
                report['network'][name] = r.returncode == 0 and bool(r.stdout.strip())
            except (subprocess.TimeoutExpired, FileNotFoundError): report['network'][name] = False
    report['sync_preflight_pass'] = (report['platform']=='Linux' and report['arch']=='x86_64'
        and report['free_gib']>=200 and report['case_sensitive'] and not report['windows_mount']
        and all(report['tools'][n] for n in ['git','repo','python3'])
        and all(report.get('network',{}).values()))
    report['note'] = 'Does not verify Windows host volume space, complete compiler compatibility or device support.'
    print(json.dumps(report, indent=2))
    return 0 if report['sync_preflight_pass'] else 1

if __name__ == '__main__': raise SystemExit(main())
