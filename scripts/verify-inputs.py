#!/usr/bin/env python3
import hashlib,json,sys
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
assert (v/'proprietary/kernel').stat().st_size==5547183
assert (root/f'patches/g81/lineage-{version}/series.json').is_file()
print('G81_'+version+'_INPUTS_VERIFIED='+str(len(records)))
