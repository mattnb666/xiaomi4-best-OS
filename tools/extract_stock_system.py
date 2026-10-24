"""Extract an EXT image without mounting or running any contained programs."""
import sys,stat,json,hashlib
from pathlib import Path
# Standard installed package preferred; local analysis environment fallback.
if Path('/private/tmp/bestos-extfs').is_dir():
    sys.path.insert(0,'/private/tmp/bestos-extfs')
from dissect.extfs import ExtFS
root=Path(__file__).resolve().parents[1]/'downloads/stock-rom/analysis'
out=root/'system-files';out.mkdir(exist_ok=True);records=[]
with (root/'system.raw.img').open('rb') as f:
 fs=ExtFS(f)
 def walk(node,path):
  for child in node.iterdir():
   name=child.filename
   if name in ('.','..'):continue
   assert '/' not in name and name not in ('','..')
   p=path/name
   if child.filetype==stat.S_IFDIR:walk(child,p)
   else:
    rec={'path':'/system/'+p.as_posix(),'bytes':child.size,'mode':oct(child.inode.i_mode),'uid':child.inode.i_uid,'gid':child.inode.i_gid}
    if child.filetype==stat.S_IFREG:
     dest=out/p;dest.parent.mkdir(parents=True,exist_ok=True);h=hashlib.sha256()
     with child.open() as src,dest.open('wb') as dst:
      while True:
       data=src.read(1024*1024)
       if not data:break
       dst.write(data);h.update(data)
     rec['sha256']=h.hexdigest()
    elif child.filetype==stat.S_IFLNK:rec['symlink_target']=child.link
    else:rec['not_materialized']=True
    records.append(rec)
 walk(fs.root,Path())
(root/'system-file-manifest.json').write_text(json.dumps(records,indent=2)+'\n')
print('Extracted regular files:',sum('sha256' in r for r in records),'recorded entries:',len(records))
