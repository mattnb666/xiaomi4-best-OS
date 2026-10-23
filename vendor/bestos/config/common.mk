# bestOS branding fragment for an Android 10 product.
# Inherit after the verified device/base product configuration.
# Keep device identity, fingerprint and security patch level supplied by the base.
BESTOS_VERSION := 0.1-dev

# Final product integration must verify inherited products add no extra locales.
# First entry is the default; English uses US regional conventions.
PRODUCT_LOCALES := zh_CN zh_HK zh_TW en_US

PRODUCT_PACKAGE_OVERLAYS += vendor/bestos/overlay

PRODUCT_PACKAGES += BestOSMTManager

PRODUCT_PRODUCT_PROPERTIES += \
    ro.bestos.name=bestOS \
    ro.bestos.version=$(BESTOS_VERSION)
