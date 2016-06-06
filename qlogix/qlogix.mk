# This is a FSL Android Reference Design platform based on i.MX6Q ARD board
# It will inherit from FSL core product which in turn inherit from Google generic

$(call inherit-product, device/flowdata/qlogix/imx6.mk)
$(call inherit-product-if-exists,vendor/google/products/gms.mk)

# Overrides
PRODUCT_NAME := qlogix
PRODUCT_DEVICE := qlogix
PRODUCT_BRAND := Flowdata
PRODUCT_MANUFACTURER := Gateworks

# Files to copy to the root (ramdisk) and system (rom) filesystems
PRODUCT_COPY_FILES += \
	device/flowdata/qlogix/required_hardware.xml:system/etc/permissions/required_hardware.xml \
	device/flowdata/qlogix/init.rc:root/init.freescale.rc \
	device/flowdata/qlogix/audio_policy.conf:system/etc/audio_policy.conf \
	device/flowdata/qlogix/audio_effects.conf:system/vendor/etc/audio_effects.conf \
	device/flowdata/qlogix/init.sh:system/bin/init.sh

PRODUCT_COPY_FILES +=	\
	external/linux-firmware-imx/firmware/vpu/vpu_fw_imx6d.bin:system/lib/firmware/vpu/vpu_fw_imx6d.bin 	\
	external/linux-firmware-imx/firmware/vpu/vpu_fw_imx6q.bin:system/lib/firmware/vpu/vpu_fw_imx6q.bin

PRODUCT_COPY_FILES +=	\
	device/flowdata/common/input/gsc_input.kl:system/usr/keylayout/gsc_input.kl \
	device/flowdata/common/input/tca8418.kl:system/usr/keylayout/tca8418.kl \
	device/flowdata/common/input/Goodix_Capacitive_TouchScreen.idc:system/usr/idc/Goodix_Capacitive_TouchScreen.idc \
	device/flowdata/common/input/EP0810M09.idc:system/usr/idc/EP0810M09.idc \
	device/flowdata/common/input/TSC2007_Touchscreen.idc:system/usr/idc/TSC2007_Touchscreen.idc

DEVICE_PACKAGE_OVERLAYS := device/flowdata/qlogix/overlay

PRODUCT_CHARACTERISTICS := tablet

PRODUCT_AAPT_CONFIG += xlarge large tvdpi hdpi

# Hardware supported features
PRODUCT_COPY_FILES += \
	frameworks/native/data/etc/android.hardware.location.gps.xml:system/etc/permissions/android.hardware.location.gps.xml \
	frameworks/native/data/etc/android.hardware.wifi.xml:system/etc/permissions/android.hardware.wifi.xml \
	frameworks/native/data/etc/android.hardware.sensor.accelerometer.xml:system/etc/permissions/android.hardware.sensor.accelerometer.xml \
	frameworks/native/data/etc/android.hardware.faketouch.xml:system/etc/permissions/android.hardware.faketouch.xml \
	frameworks/native/data/etc/android.hardware.touchscreen.multitouch.jazzhand.xml:system/etc/permissions/android.hardware.touchscreen.multitouch.jazzhand.xml \
	frameworks/native/data/etc/android.software.sip.voip.xml:system/etc/permissions/android.software.sip.voip.xml \
	frameworks/native/data/etc/android.hardware.usb.host.xml:system/etc/permissions/android.hardware.usb.host.xml \
	frameworks/native/data/etc/android.hardware.usb.accessory.xml:system/etc/permissions/android.hardware.usb.accessory.xml \
	frameworks/native/data/etc/android.hardware.sensor.compass.xml:system/etc/permissions/android.hardware.sensor.compass.xml \
	frameworks/native/data/etc/android.hardware.bluetooth_le.xml:system/etc/permissions/android.hardware.bluetooth_le.xml \

# Devices not present by default on Gateworks boards (but you may add them)
#PRODUCT_COPY_FILES += \
	frameworks/native/data/etc/android.hardware.wifi.direct.xml:system/etc/permissions/android.hardware.wifi.direct.xml \
	frameworks/native/data/etc/android.hardware.sensor.light.xml:system/etc/permissions/android.hardware.sensor.light.xml \

# for PDK build, include only when the dir exists
# too early to use $(TARGET_BUILD_PDK)
ifneq ($(wildcard packages/wallpapers/LivePicker),)
PRODUCT_COPY_FILES += \
	packages/wallpapers/LivePicker/android.software.live_wallpaper.xml:system/etc/permissions/android.software.live_wallpaper.xml
endif
