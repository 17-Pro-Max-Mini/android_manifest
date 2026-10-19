# G81 — LineageOS 17.1

Reproducible source/input preservation for MT6580 G81 (384x854, 1 GiB).
Use **lineage-17.1** in device, vendor, patches and manifest repositories.
The 15.1 port is the historical Android 8.1 environment; the currently used
phone runs 17.1. Preserving both does not mean both were freshly flashed today.

## Fresh setup on Linux / ext4

Install git, git-lfs, repo, python3 and the Android host dependencies. Allocate
200 GiB+ for each full source/output tree. 15.1 builds in the retained Ubuntu
20.04 / JDK8 container; 17.1 uses the source-pinned JDK9 selected by Soong, not
the host's Java 8. Host OpenJDK11 and libncurses5 were installed on the tested
Ubuntu22.04 machine. See [restore/setup details](docs/RESTORE.md).

```sh
git clone -b lineage-17.1 https://github.com/17-Pro-Max-Mini/android_manifest.git
cd android_manifest
./g81-build sync 17.1 /absolute/ext4/g81-17.1
./g81-build check 17.1 /absolute/ext4/g81-17.1
G81_BUILD_JOBS=28 ./g81-build build 17.1 /absolute/ext4/g81-17.1
```

All project SHAs, including the matching G81 repositories, are pinned in the
release XML. Sync initializes a **new** tree; it does not reset an old dirty
checkout. Preserve local work before manually synchronizing an existing tree.
Both versions use LFS vendor inputs. The build command does not flash a device.

## Verification boundaries

Input hashes and forward/reverse patch tests are checked separately from
compilation and hardware tests. Read the release verification report for the
actual commands/results. A graph-only or Ninja -n test is not a full ROM build.
The pinned vendor image is the supported binary input; a fully stock-to-vendor
regeneration pipeline and an open-source kernel replacement are not claimed.
