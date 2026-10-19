# G81 environment restoration

## What belongs together

* 15.1 = Android8.1/API27, historical 8-project source patch export, stock-era
  vendor image SHA256 `95a5dfaaaa9f3db8d5d5cf37fae1f21b28027dafd910c815c3068162c7892f9e`.
* 17.1 = Android10/API29, 12-project source patch export, cumulative vendor
  image SHA256 `9d4bee1e55a3a274e7e06ea8685c77bf2a260466e1a3c148edb8f414d68350b8`.
* Kernel is unchanged stock3.18.79, SHA256
  `c6d2c9b973d859054bc60c98e9afed37b5d11c813ab66b930534405b8e6a1c7d`.
* Do not combine version branches. A prebuilt vendor image is not generated
  from its helper source directories automatically.

## Build host

15.1: the saved `g81em1-android-build:20.04` Docker image contains JDK8 and
Python2/3. If restoring the private offline backup, use
`zstd -dc builder-20.04.tar.zst | docker load`. The legacy container recipe is
retained separately for review. The image export preserves the actual installed
environment without depending on a changing download URL or EOL apt packages.
For an online setup, build `container/Dockerfile` after checking its pinned repo
launcher download; do not silently remove checksum validation on a changed URL.

17.1: the bundled `prebuilts/jdk/jdk9/linux-x86` is selected by this source's
Soong configuration. Install normal Android10 Linux host dependencies, including
git/git-lfs/repo, Python3, build-essential, gcc/g++-multilib, bc, bison, flex,
gperf, zip/unzip, zlib1g-dev, lib32z1-dev, libncurses5, libssl-dev, libxml2-utils,
xsltproc, rsync, curl, ccache and host OpenJDK11. The observed host was
Ubuntu22.04 amd64. Source and output need ext4 (not a raw NTFS checkout).

Run `./g81-build check VERSION SOURCE` before `build`; set
`G81_BUILD_JOBS=28` or a lower value. Use a new OUT_DIR for a clean-build test.
`graph` builds rules only; it never demonstrates a successful compilation.

## Offline backup layout (private, not committed to public GitHub)

The backup disk has project-home and build-environment tar.zst archives,
archive checksums, repository bundles **plus LFS payloads**, the actual builder
image, and read-only copies of the current phone's ROM partitions. Original
stock/calibration backups and diagnostic logs stay in these private archives.
Git bundles alone do not contain LFS contents or dirty/untracked files.

Before extracting, check `sha256sum -c SHA256SUMS` in the archive directory.
Restore to empty directories on ext4 with `tar --zstd --acls --xattrs -xpf ...`.
The top-level project archive maps to `~/Projects/G81EM1`; the build archive
maps to `/media/meto/LINEAGE_BUILD/G81EM1`. Keep those paths for the first
restore because historical symlinks and repo alternates use them. Relocation
requires inspecting and rewriting those references, not just moving a folder.
The manifest-based fresh sync path avoids historical absolute-path dependencies.

Only the Linux OS partition is scheduled for formatting. Preserve both the
LINEAGE_BUILD ext4 disk and the separate NTFS backup disk; identify them by
their UUIDs in the private restore report. No formatting is part of these scripts.
After installation, mount the retained disks, restore project files, reload the
builder image, install host dependencies and rerun input/patch checks. Reauthenticate
GitHub separately; no account tokens or SSH keys are published in the repos.

The ROM partition copies are disaster-recovery inputs, not a universal automatic
flash package. They do not include userdata or transfer the phone's calibration
to another device. The stable phone is not reset merely to verify a PC backup.
