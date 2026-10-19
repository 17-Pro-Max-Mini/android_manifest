#!/usr/bin/env python3
import hashlib,json,sys,subprocess,xml.etree.ElementTree as ET
from pathlib import Path
version=sys.argv[1];root=Path(sys.argv[2]).resolve()
assert version in ('15.1','17.1')
v=root/'vendor/alps/g81';d=root/'device/alps/g81'
records=json.loads((v/'release-inputs/files.json').read_text())
for name,expected in records.items():
    f=v/name;assert f.is_file(),f
    h=hashlib.sha256()
    with f.open('rb') as stream:
        for block in iter(lambda:stream.read(4*1024*1024),b''):h.update(block)
    assert h.hexdigest()==expected,'Input hash differs: '+name
if version=='17.1':assert (d/'prebuilt').resolve()==v/'device-prebuilts'
assert (v/'proprietary/vendor.img').stat().st_size==419430400
expected_image={'15.1':'95a5dfaaaa9f3db8d5d5cf37fae1f21b28027dafd910c815c3068162c7892f9e',
                '17.1':'9d4bee1e55a3a274e7e06ea8685c77bf2a260466e1a3c148edb8f414d68350b8'}[version]
assert records['proprietary/vendor.img']==expected_image,'Wrong Android-version vendor image'
assert (v/'proprietary/kernel').stat().st_size==5547183
assert (root/f'patches/g81/lineage-{version}/series.json').is_file()
manifest=ET.parse(Path(__file__).resolve().parents[1]/f'manifests/g81-{version}-locked.xml')
for rel in ['device/alps/g81','vendor/alps/g81','patches/g81']:
    item=manifest.getroot().find(f"project[@path='{rel}']")
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root/rel,text=True).strip()
    assert head==item.get('revision'),'Wrong repository revision: '+rel
    status=subprocess.check_output(['git','status','--porcelain','--untracked-files=normal'],cwd=root/rel,text=True)
    assert not status,'Unrecorded repository changes: '+rel
print('G81_'+version+'_INPUTS_VERIFIED='+str(len(records)))
