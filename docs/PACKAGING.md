# Exact vendor packaging

The platform adds IMAGES/vendor.img to target-files for a prebuilt vendor,
but its OTA partition detection looks for VENDOR/. The former ZIP therefore
installed only system and boot. Device-local releasetools.py now appends the
SHA256-checked full vendor image and an asserted vendor-only partition write.
Both FullOTA and IncrementalOTA hooks use the same pinned branch-specific image.
No platform source modification was needed for this packaging fix.

The device assertion accepts g81 and g81em1_o_xc6_l10_17promax; it is not bypassed.
The updater does not write recovery, nvram, nvdata, protect or userdata.
The complete ZIP still needs a separate hardware clean-install test; producing
and inspecting it is not evidence that it has already been flashed.
