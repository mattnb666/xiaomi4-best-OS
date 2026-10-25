"""Package local extracted firmware and supplied APK; never execute or flash them."""
from pathlib import Path
import gzip, hashlib, json, shutil, tarfile
ROOT = Path(__file__).resolve().parents[1]
STOCK = ROOT / 'downloads/stock-rom'
ANALYSIS = STOCK / 'analysis'
OUT = ROOT / 'out/github-assets'
OUT.mkdir(parents=True, exist_ok=True)
def archive(name, entries):
    dest = OUT / name
    with tarfile.open(str(dest) + '.partial', 'w:gz', compresslevel=1) as tar:
        for source, target in entries:
            tar.add(source, arcname=target, recursive=True)
    Path(str(dest) + '.partial').replace(dest)
    with tarfile.open(dest, 'r:gz') as tar:
        for member in tar:
            if member.isfile():
                with tar.extractfile(member) as src:
                    while src.read(1024 * 1024): pass
    print('Validated archive:', name, flush=True)
images = next((STOCK / 'extracted').glob('*/images'))
archive('cancro-stock-images.tar.gz', [(images, 'images')])
archive('cancro-system-files.tar.gz', [(ANALYSIS / 'system-files', 'system-files'), (ANALYSIS / 'system-file-manifest.json', 'system-file-manifest.json'), (ANALYSIS / 'driver-candidates.json', 'driver-candidates.json')])
archive('cancro-boot-components.tar.gz', [(ANALYSIS / 'boot', 'boot'), (ANALYSIS / 'boot-inspection.json', 'boot-inspection.json')])
# The raw image is reproducible from the sparse system.img in the images archive;
# avoid transferring a duplicate expanded image.
shutil.copyfile(ROOT / 'vendor/bestos/prebuilt/MTManager/MTManager.apk', OUT / 'MTManager-clone-2.26.8.apk')
records = []
for name in ['cancro-stock-images.tar.gz', 'cancro-system-files.tar.gz', 'cancro-boot-components.tar.gz', 'MTManager-clone-2.26.8.apk']:
    p = OUT / name
    h = hashlib.sha256()
    with p.open('rb') as f:
        while chunk := f.read(1024 * 1024): h.update(chunk)
    records.append({'file': name, 'bytes': p.stat().st_size, 'sha256': h.hexdigest()})
(OUT / 'SHA256SUMS').write_text(''.join(f"{r['sha256']}  {r['file']}\n" for r in records))
(OUT / 'asset-manifest.json').write_text(json.dumps(records, indent=2) + '\n')
print(json.dumps(records, indent=2), flush=True)
