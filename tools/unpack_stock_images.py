"""Read-only stock image conversion and boot component extraction."""
from pathlib import Path
import struct,json,gzip,hashlib
root=Path(__file__).resolve().parents[1]/'downloads/stock-rom'
images=next((root/'extracted').glob('*/images'))
out=root/'analysis';out.mkdir(exist_ok=True)
with (images/'system.img').open('rb') as src,(out/'system.raw.img').open('wb') as dst:
 h=src.read(28);magic,major,minor,fh,ch,bs,blocks,count,checksum=struct.unpack('<I4H4I',h)
 assert magic==0xed26ff3a and major==1 and fh>=28 and ch>=12
 src.read(fh-28)
 for _ in range(count):
  header=src.read(ch);typ,res,n,total=struct.unpack('<2H2I',header[:12]);payload=total-ch;size=n*bs
  if typ==0xcac1:
   assert payload==size
   remaining=size
   while remaining:
    data=src.read(min(remaining,1024*1024));assert data;dst.write(data);remaining-=len(data)
  elif typ==0xcac2:
   assert payload==4;word=src.read(4);buf=word*(min(size,1024*1024)//4)
   for offset in range(0,size,len(buf)):dst.write(buf[:min(len(buf),size-offset)])
  elif typ==0xcac3:assert payload==0;dst.seek(size,1)
  elif typ==0xcac4:assert payload==4;src.read(4)
  else:raise ValueError(hex(typ))
 assert dst.tell()==blocks*bs;dst.truncate()
b=(images/'boot.img').read_bytes();assert b[:8]==b'ANDROID!'
v=struct.unpack_from('<10I',b,8);ks,ka,rs,ra,ss,sa,tags,page,dt,unused=v
align=lambda n:(n+page-1)//page*page
parts={'kernel':b[page:page+ks],'ramdisk.gz':b[page+align(ks):page+align(ks)+rs]}
dt_start=page+align(ks)+align(rs)+align(ss)
parts['dt.img']=b[dt_start:dt_start+dt]
assert len(parts['dt.img'])==dt
boot=out/'boot';boot.mkdir(exist_ok=True)
for name,data in parts.items():(boot/name).write_bytes(data)
report={'kernel_size':ks,'ramdisk_size':rs,'second_size':ss,'page_size':page,'dt_size_field':dt,'cmdline_offset_observed':60,'cmdline':b[60:572].split(b'\0')[0].decode(errors='replace'),'components':{n:hashlib.sha256(d).hexdigest() for n,d in parts.items()}}
cpio=gzip.decompress(parts['ramdisk.gz']);(boot/'ramdisk.cpio').write_bytes(cpio)
rdir=boot/'ramdisk';rdir.mkdir(exist_ok=True);pos=0;entries=[]
while pos+110<=len(cpio):
 h=cpio[pos:pos+110];assert h[:6] in (b'070701',b'070702');fields=[int(h[6+i*8:14+i*8],16) for i in range(13)];mode=fields[1];size=fields[6];namelen=fields[11]
 name=cpio[pos+110:pos+110+namelen-1].decode();pos=(pos+110+namelen+3)&~3;data=cpio[pos:pos+size];pos=(pos+size+3)&~3
 if name=='TRAILER!!!':break
 p=Path(name);assert not p.is_absolute() and '..' not in p.parts
 entries.append({'path':name,'mode':oct(mode),'bytes':size,'symlink_target':data.decode(errors='replace') if mode&0o170000==0o120000 else None})
 if mode&0o170000==0o100000:
  dest=rdir/p;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
report['ramdisk_entries']=entries;(out/'boot-inspection.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='ramdisk_entries'},indent=2));print('raw system bytes',blocks*bs)
