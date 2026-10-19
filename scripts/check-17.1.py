#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,sys
root=Path(sys.argv[1]).resolve()
assert (root/'device/alps/g81/health/HealthService.cpp').is_file()
assert (root/'device/alps/g81/overlay/packages/apps/Settings/res/values/themes.xml').is_file()
vendor=root/'vendor/alps/g81'
assert (root/'device/alps/g81/prebuilt').resolve()==vendor/'device-prebuilts'
records=json.loads((vendor/'release-inputs/files.json').read_text())
for name,expected in records.items():
    f=vendor/name;assert f.is_file(),f
    h=hashlib.sha256()
    with f.open('rb') as stream:
        for data in iter(lambda:stream.read(1024*1024),b''):h.update(data)
    assert h.hexdigest()==expected,'Input differs: '+name
assert (root/'device/alps/g81/prebuilt/vendor.img').resolve()==vendor/'proprietary/vendor.img'
assert b'/sys/class/power_supply/battery/batt_vol' in (root/'device/alps/g81/health/HealthService.cpp').read_bytes()
device=(root/'device/alps/g81/device.mk').read_text()
assert '$(TARGET_COPY_OUT_ROOT)/vendor_file_contexts' in device
print('G81_INPUTS_VERIFIED='+str(len(records)))
