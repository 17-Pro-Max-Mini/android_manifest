#!/usr/bin/env bash

set -euo pipefail

target="${1:-}"
source_root="${2:-}"
product_name="g81"

if [[ "${target}" != lineage && "${target}" != twrp ]] || [[ ! -d "${source_root}/.repo" ]]; then
    echo "Usage: $0 lineage|twrp <android-source-root>" >&2
    exit 2
fi

product_out="${source_root}/out/target/product/${product_name}"
private_root="${source_root}/vendor/alps/g81/proprietary"
boot_limit=16777216
recovery_limit=16777216
system_size=2147483648
vendor_size=419430400
kernel_sha256=c6d2c9b973d859054bc60c98e9afed37b5d11c813ab66b930534405b8e6a1c7d
vendor_sha256=95a5dfaaaa9f3db8d5d5cf37fae1f21b28027dafd910c815c3068162c7892f9e

check_limit() {
    local image="$1"
    local limit="$2"
    local size
    [[ -f "${image}" ]] || { echo "Missing ${image}" >&2; exit 1; }
    size="$(stat -c %s "${image}")"
    (( size <= limit )) || { echo "${image} exceeds ${limit} bytes" >&2; exit 1; }
    echo "$(basename "${image}"): ${size} bytes"
}

check_limit "${product_out}/recovery.img" "${recovery_limit}"
if [[ "${target}" == twrp ]]; then
    exit 0
fi

check_limit "${product_out}/boot.img" "${boot_limit}"
for required in "${product_out}/system.img" "${product_out}/vendor.img" \
        "${private_root}/kernel" "${private_root}/vendor.img"; do
    [[ -f "${required}" ]] || { echo "Missing ${required}" >&2; exit 1; }
done

[[ "$(stat -c %s "${product_out}/vendor.img")" == "${vendor_size}" ]]
[[ "$(sha256sum "${product_out}/vendor.img" | awk '{print $1}')" == "${vendor_sha256}" ]]
cmp -- "${product_out}/vendor.img" "${private_root}/vendor.img"
[[ "$(sha256sum "${private_root}/kernel" | awk '{print $1}')" == "${kernel_sha256}" ]]

temp_dir="$(mktemp -d "${source_root}/out/g81-validate.XXXXXX")"
trap 'rm -rf -- "${temp_dir}"' EXIT

host_tools="${source_root}/out/host/linux-x86/bin"
"${host_tools}/simg2img" "${product_out}/system.img" "${temp_dir}/system.raw.img"
[[ "$(stat -c %s "${temp_dir}/system.raw.img")" == "${system_size}" ]]
"${host_tools}/e2fsck" -fn "${temp_dir}/system.raw.img"

mkdir "${temp_dir}/boot"
(
    cd "${temp_dir}/boot"
    abootimg -x "${product_out}/boot.img" >/dev/null
)
[[ "$(sha256sum "${temp_dir}/boot/zImage" | awk '{print $1}')" == "${kernel_sha256}" ]]

grep -Fqx 'ro.config.low_ram=true' "${product_out}/system/build.prop"
grep -Fqx 'ro.treble.enabled=true' "${product_out}/system/build.prop"

echo "Static LineageOS validation passed."
sha256sum "${product_out}/boot.img" "${product_out}/recovery.img" \
    "${product_out}/system.img" "${product_out}/vendor.img"
