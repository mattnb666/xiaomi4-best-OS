"""Create a portable snapshot; excludes duplicate outputs and download caches."""
from pathlib import Path
import hashlib,json,tarfile
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'out/migration'
OUT.mkdir(parents=True,exist_ok=True)
rows=[]
def selected(p):
 rel=p.relative_to(ROOT)
 return not (rel.parts[0] in ('out','.git','.repo') or '__pycache__' in rel.parts
     or any(x.endswith('.chunks') for x in rel.parts)
     or p.name=='.DS_Store' or p.name.startswith('.env')
     or p.suffix in ('.partial','.part','.pem','.pk8'))
files=sorted(p for p in ROOT.rglob('*') if p.is_file() and selected(p))
for p in files:
 h=hashlib.sha256()
 with p.open('rb') as f:
  while data:=f.read(4*1024*1024):h.update(data)
 rows.append({'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':h.hexdigest()})
manifest=OUT/'workspace-manifest.json'
manifest.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
archive=OUT/'bestOS-workspace.tar.gz'
with tarfile.open(str(archive)+'.partial','w:gz',compresslevel=1) as tar:
 for p in files:tar.add(p,arcname='bestOS/'+p.relative_to(ROOT).as_posix(),recursive=False)
 tar.add(manifest,arcname='bestOS/workspace-manifest.json')
Path(str(archive)+'.partial').replace(archive)
# Verify each archived byte stream against the source inventory.
expected={ 'bestOS/'+r['path']:r for r in rows }
with tarfile.open(archive,'r:gz') as tar:
 for m in tar:
  if m.name not in expected:continue
  h=hashlib.sha256()
  with tar.extractfile(m) as f:
   while data:=f.read(4*1024*1024):h.update(data)
  r=expected.pop(m.name)
  if r['bytes']!=m.size or r['sha256']!=h.hexdigest():raise RuntimeError(m.name)
assert not expected
h=hashlib.sha256()
with archive.open('rb') as f:
 while data:=f.read(4*1024*1024):h.update(data)
(OUT/'SHA256SUMS').write_text(h.hexdigest()+'  '+archive.name+'\n')
print(json.dumps({'archive':str(archive),'files':len(rows),'bytes':archive.stat().st_size,'sha256':h.hexdigest(),'verified':True}),flush=True)
