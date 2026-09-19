# Naming and publication policy

## Canonical device name

`g81` is the repository codename. It is lower-case, short, stable, and follows
the established Android device-repository pattern:

```text
android_device_<vendor>_<codename>
android_device_alps_g81
device/alps/g81
lineage_g81-user
omni_g81-eng
```

`alps` is retained as the vendor namespace because that is the device's actual
Android manufacturer/vendor identity. Inventing a retail brand would make the
tree less accurate. The long stock target `g81em1_o_xc6_l10_17promax` is not a
suitable repository codename. Android's build `PRODUCT_DEVICE` is therefore
`g81`, so it can locate `device/alps/g81/BoardConfig.mk` without a link; the
long stock value is retained by the generated runtime-property override and
the bootloader-board name. That preserves the tested contract with the MTK Oreo
vendor stack.

## Repository names

- `android_manifest` is the organization entry point and build orchestrator.
- `android_device_alps_g81` is the public Android device tree.
- `proprietary_vendor_alps_g81` follows the common proprietary-vendor naming
  pattern and is private because it contains extracted binary material.
- `android_patches_g81` makes changes to upstream Lineage projects visible and
  reviewable instead of hiding them in a setup script.
- `mtk_bootlogo_g81` describes a reusable MTK logo-partition tool and its
  device scope without pretending that the output is an Android boot image.
- `stock_firmware_g81` is the private byte-for-byte recovery archive. It is
  separate from both the public source repositories and the build-time vendor
  repository, and it is never referenced by an Android manifest.

A standalone `android_kernel_alps_mt6580` repository must not be created unless
the corresponding kernel source is recovered. A prebuilt zImage is not kernel
source and stays in the private vendor repository.

## Branches and releases

Platform repositories use upstream-aligned branches: `lineage-15.1` and
`twrp-8.1`. Platform-independent orchestration and logo tooling use `main`.
Development manifests may track branches; every distributed build must include
the SHA-pinned XML exported by `repo manifest -r`.

## Publication boundary

Public repositories may contain source, configuration, patch files, extraction
scripts, hashes, and hardware facts. They must not contain stock partition
images, proprietary libraries, prebuilt kernels, calibration partitions,
backups, logs, account data, device identifiers, or factory-only applications.
The private `stock_firmware_g81` recovery repository is the explicit exception
for the preserved stock images and calibration partitions; it is not a public
repository or a build dependency.
Optional device-maintenance features must be explicit and reviewable; they are
never disguised in public patches or default manifests.
