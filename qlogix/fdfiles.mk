
# files in data folder
PRODUCT_COPY_FILES += \
	device/flowdata/qlogix/data/statnet/dns1:data/statnet/dns1 \
	device/flowdata/qlogix/data/statnet/dns2:data/statnet/dns2 \
	device/flowdata/qlogix/data/statnet/gateway:data/statnet/gateway \
	device/flowdata/qlogix/data/statnet/ipaddress:data/statnet/ipaddress \
	device/flowdata/qlogix/data/statnet/mask:data/statnet/mask \
	device/flowdata/qlogix/data/statnet/netmask:data/statnet/netmask \
	device/flowdata/qlogix/data/statnet1/dns1:data/statnet1/dns1 \
	device/flowdata/qlogix/data/statnet1/dns2:data/statnet1/dns2 \
	device/flowdata/qlogix/data/statnet1/gateway:data/statnet1/gateway \
	device/flowdata/qlogix/data/statnet1/ipaddress:data/statnet1/ipaddress \
	device/flowdata/qlogix/data/statnet1/mask:data/statnet1/mask \
	device/flowdata/qlogix/data/statnet1/netmask:data/statnet1/netmask \
	device/flowdata/qlogix/data/authorized_keys:data/ssh/authorized_keys

# files in system folder
PRODUCT_COPY_FILES += \
	device/flowdata/qlogix/system/debshell:system/bin/debshell \
	device/flowdata/qlogix/system/launch_debian:system/bin/launch_debian \
	device/flowdata/qlogix/system/setup_debian:system/bin/setup_debian \
	device/flowdata/qlogix/system/stop_qlogix:system/bin/stop_provue \
	device/flowdata/qlogix/system/reboot_qlogix:system/bin/reboot_provue \
	device/flowdata/qlogix/system/setup.eth0:system/bin/setup.eth0 \
	device/flowdata/qlogix/system/setup.eth1:system/bin/setup.eth1 \
        device/flowdata/qlogix/system/stop_adbd:system/bin/stop_adbd \
        device/flowdata/qlogix/system/start_adbd:system/bin/start_adbd \
        device/flowdata/qlogix/system/qlogix_uptime:system/bin/provue_uptime \
        device/flowdata/qlogix/system/setup_button:system/bin/setup_button \
        device/flowdata/qlogix/system/launch_qlogix:system/bin/launch_qlogix \
        device/flowdata/qlogix/system/launch_nginx:system/bin/launch_nginx \
        device/flowdata/qlogix/system/launch_gunicorn:system/bin/launch_gunicorn \
        device/flowdata/qlogix/system/launch_postgres:system/bin/launch_postgres \
        device/flowdata/qlogix/system/setdate:system/bin/setdate \

# files for recovery
PRODUCT_COPY_FILES += \
	device/flowdata/qlogix/init.recovery.rc:root/init.recovery.freescale.rc 

# files in media folder
PRODUCT_COPY_FILES += \
	device/flowdata/qlogix/media/bootanimation.zip:system/media/bootanimation.zip \
	device/flowdata/qlogix/gpio-20.kl:data/system/devices/keylayout/gpio-20.kl

LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)
LOCAL_MODULE := Reader
LOCAL_SOURCE_FILES := system/$(LOCAL_MODULE).apk
LOCAL_MODULE_CLASS := APPS
LOCAL_MODULE_SUFFIX := $(COMMON_ANDROID_PACKAGE_SUFFIX)
LOCAL_MODULE_TAGS := optional
LOCAL_CERTIFICATE := PRESIGNED

include $(BUILD_PREBUILT)
