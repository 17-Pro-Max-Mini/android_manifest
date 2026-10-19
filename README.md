# G81 — LineageOS 17.1 / Android 10

Daily-use source snapshot: **g81-17.1-20261019**. Existing `main`, `lineage-15.1`
and TWRP branches are retained; this branch describes the Android 10 port.
Read [the tested status and remaining issues](docs/STATUS-20261019.md).

## Repositories
| Project | Branch | Contents |
|---|---|---|
| android_device_alps_g81 | lineage-17.1 | device configuration, overlays, native helper sources |
| android_patches_g81 | lineage-17.1 | exact patches for 12 upstream projects |
| proprietary_vendor_alps_g81 | lineage-17.1 (private) | pinned vendor image, kernel and required device prebuilts; Git LFS |
| android_manifest | lineage-17.1 | upstream SHA lock, integration lock and build entry point |

Upstream is LineageOS-Revived. `manifests/lineage-17.1-upstream.xml` pins every
exported upstream project. `releases/20261019.xml` additionally pins the G81
device/vendor/patch repositories. An upstream-local commit is exported as a
patch against its real upstream parent, not as an unreachable manifest SHA.

## Reproduce sources
Use Linux/ext4, Git, Git LFS, repo, Python 3, and authenticated SSH access to the
existing private vendor repository. Build with OpenJDK 11 and normal Android 10
host dependencies. The tested host was Ubuntu 22.04; old legacy Java 8 build
instructions in other branches do not apply here. A fresh source/output tree
needs substantially more disk than an incremental build (budget 200 GiB+).

```sh
git clone -b lineage-17.1 https://github.com/17-Pro-Max-Mini/android_manifest.git
cd android_manifest
./g81-17.1 sync /path/on/ext4/g81-lineage-17.1
./g81-17.1 check /path/on/ext4/g81-lineage-17.1
G81_BUILD_JOBS=28 ./g81-17.1 build /path/on/ext4/g81-lineage-17.1
```

The script does not flash a phone or format partitions. `--check` verifies
patch applicability or already-applied result hashes without resetting local
work. Proprietary binaries stay in the existing private repository; no device
logs, NVRAM/nvdata or personal user data are published.

The public device tree's `prebuilt` symlink resolves into the private vendor
checkout at the expected repo layout. The private image is the cumulative,
tested Android 10 vendor input, not the unmodified Oreo stock vendor.

This publication freezes a working runtime and its source/input changes.
Patch apply/reverse and fresh repository checkout/input verification are
tested separately from a full build or clean flash. Those tests are recorded
explicitly in the status document rather than implied by a release tag.
