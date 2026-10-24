"""Download the user-selected stock ROM in validated HTTP ranges; never flash."""
import concurrent.futures, hashlib, json, pathlib, subprocess, time, tarfile
ROOT = pathlib.Path(__file__).resolve().parents[1]
DEST = ROOT / 'downloads/stock-rom'
NAME = 'cancro_images_V10.1.1.0.MXDCNFI_20181010.0000.00_6.0_cn_911b6abc33.tgz'
URL = 'https://cdnorg.d.miui.com/V10.1.1.0.MXDCNFI/' + NAME
SIZE = 1212837378
CHUNK = 4 * 1024 * 1024
PARTS = DEST / (NAME + '.chunks')
PARTS.mkdir(parents=True, exist_ok=True)
def fetch(i):
    start = i * CHUNK
    end = min(SIZE, start + CHUNK) - 1
    part = PARTS / ('%04d.part' % i)
    header = PARTS / ('%04d.headers' % i)
    if part.exists() and part.stat().st_size == end-start+1 and header.exists():
        if ('content-range: bytes %d-%d/%d' % (start,end,SIZE)) in header.read_text().lower():
            return i
    for attempt in range(4):
        r = subprocess.run(['curl','--fail','--silent','--show-error','-L','--connect-timeout','20','--max-time','180','--range','%d-%d' % (start,end),'-D',str(header),URL,'-o',str(part)],capture_output=True,text=True)
        if r.returncode == 0 and part.stat().st_size == end-start+1 and ('content-range: bytes %d-%d/%d' % (start,end,SIZE)) in header.read_text().lower():
            return i
        time.sleep(attempt+1)
    raise RuntimeError('Range %d failed: %s' % (i,r.stderr[-200:]))
count = (SIZE + CHUNK - 1) // CHUNK
completed = 0
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
    for future in concurrent.futures.as_completed([pool.submit(fetch,i) for i in range(count)]):
        future.result(); completed += 1
        print(json.dumps({'completed_chunks':completed,'total_chunks':count}),flush=True)
assembled = DEST / (NAME + '.assembling')
sha=hashlib.sha256(); md5=hashlib.md5()
with assembled.open('wb') as out:
    for i in range(count):
        data=(PARTS / ('%04d.part' % i)).read_bytes();out.write(data);sha.update(data);md5.update(data)
assert assembled.stat().st_size == SIZE
# Read every archive member to verify decompression before declaring completion.
import gzip
with gzip.open(assembled,'rb') as stream:
    while stream.read(8*1024*1024): pass
with tarfile.open(assembled,'r:gz') as archive:
    inventory=[{'name':m.name,'bytes':m.size,'type':m.type.decode('ascii','replace')} for m in archive.getmembers()]
final=DEST/NAME
assembled.replace(final)
report={'source_page':'https://xiaomirom.com/download/mi-3-mi-4-mi-4-lte-ct-cancro-stable-V10.1.1.0.MXDCNFI/','download_url':URL,'bytes':SIZE,'sha256':sha.hexdigest(),'md5':md5.hexdigest(),'publisher_checksum':'not provided on source page','gzip_verified':True,'members':inventory}
(DEST/'stock-rom-inspection.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':'complete','path':str(final),'sha256':sha.hexdigest(),'members':len(inventory)}),flush=True)
