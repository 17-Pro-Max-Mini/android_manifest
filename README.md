# G81 Android build manifest

This is the single supported entry point for reproducible G81 builds. It keeps
the upstream Android manifests authoritative, adds the G81 repositories as
local manifests, builds in a pinned Ubuntu 20.04 container, applies the public
patch series, validates partition artifacts, and exports a SHA-pinned manifest
for every release.

## Repository names and branches

| Repository | Visibility | Branches |
| --- | --- | --- |
| `android_manifest` | public | `main` |
| `android_device_alps_g81` | public | `lineage-15.1`, `twrp-8.1` |
| `android_patches_g81` | public | `lineage-15.1` |
| `mtk_bootlogo_g81` | public | `main` |
| `proprietary_vendor_alps_g81` | private, Git LFS | `lineage-15.1`, `twrp-8.1` |
| `stock_firmware_g81` | private, Git LFS | `main` |

`stock_firmware_g81` is a recovery archive. It is deliberately absent from
the LineageOS and TWRP manifests and is not an input to either build.

The build script defaults to the published `17-Pro-Max-Mini` organization.
Override the public or private fetch roots only when using a mirror:

```bash
export G81_PUBLIC_FETCH=https://github.com/17-Pro-Max-Mini
export G81_PRIVATE_FETCH=ssh://git@github.com/17-Pro-Max-Mini
export G81_BUILD_ROOT=/path/to/ext4/G81
```

`G81_PRIVATE_FETCH` is optional during source inspection, but both builds need
the private vendor checkout. Git credentials remain in the host Git/SSH setup;
the scripts do not store tokens.

The host needs Docker Engine, Git, a POSIX shell, and an ext4 build volume with
at least 150 GiB free. The container supplies the legacy Android toolchain,
`repo`, Git LFS, Java 8, image tools, and build dependencies. The scripts use
the current user's numeric UID/GID, write only below `G81_BUILD_ROOT`, and
never flash a connected device.

## Build workflow

```bash
./g81 setup
./g81 sync lineage
./g81 build lineage
./g81 validate lineage
./g81 release lineage

./g81 sync twrp
./g81 build twrp
./g81 validate twrp
./g81 release twrp
```

Build parallelism defaults to all logical CPUs. Override it with
`G81_BUILD_JOBS` or `G81_SYNC_JOBS`. The scripts never flash a device.

The Lineage target selects `lineage_g81-user` and runs `mka bacon systemimage`:
it produces the normal flashable OTA zip and a standalone `system.img`. The
latter is required by the legacy partition layout and is checked by the
validator before release. TWRP remains an `omni_g81-eng` recovery build, as is
normal for this legacy recovery branch.

Development manifests track the named branches. `./g81 release` runs
`repo manifest -r`, so the release directory contains the exact SHA for every
checked-out project alongside artifact hashes. Keep the generated Lineage
release private unless redistribution rights for every bundled proprietary
component have been reviewed.

See `NAMING.md` for the naming decisions and the boundary between the public
source repositories and the private vendor repository.
