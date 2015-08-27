
# files in data folder
PRODUCT_COPY_FILES += \
	device/flowdata/provue/data/statnet/dns1:data/statnet/dns1 \
	device/flowdata/provue/data/statnet/dns2:data/statnet/dns2 \
	device/flowdata/provue/data/statnet/gateway:data/statnet/gateway \
	device/flowdata/provue/data/statnet/ipaddress:data/statnet/ipaddress \
	device/flowdata/provue/data/statnet/mask:data/statnet/mask \
	device/flowdata/provue/data/statnet/netmask:data/statnet/netmask \
	device/flowdata/provue/data/statnet1/dns1:data/statnet1/dns1 \
	device/flowdata/provue/data/statnet1/dns2:data/statnet1/dns2 \
	device/flowdata/provue/data/statnet1/gateway:data/statnet1/gateway \
	device/flowdata/provue/data/statnet1/ipaddress:data/statnet1/ipaddress \
	device/flowdata/provue/data/statnet1/mask:data/statnet1/mask \
	device/flowdata/provue/data/statnet1/netmask:data/statnet1/netmask \
	device/flowdata/provue/data/authorized_keys:data/ssh/authorized_keys

# files in system folder
PRODUCT_COPY_FILES += \
	device/flowdata/provue/system/debshell:system/bin/debshell \
	device/flowdata/provue/system/launch_debian:system/bin/launch_debian \
	device/flowdata/provue/system/restartApache:system/bin/restartApache \
	device/flowdata/provue/system/setup_debian:system/bin/setup_debian \
	device/flowdata/provue/system/stop_provue:system/bin/stop_provue \
	device/flowdata/provue/system/setup.eth0:system/bin/setup.eth0 \
	device/flowdata/provue/system/setup.eth1:system/bin/setup.eth1 \
        device/flowdata/provue/system/stop_adbd:system/bin/stop_adbd \
        device/flowdata/provue/system/start_adbd:system/bin/start_adbd \
        device/flowdata/provue/system/provue_uptime:system/bin/provue_uptime \
        device/flowdata/provue/system/setup_button:system/bin/setup_button \
        device/flowdata/provue/system/launch_spel:system/bin/launch_spel \
        device/flowdata/provue/system/launch_apache:system/bin/launch_apache \
        device/flowdata/provue/system/setdate:system/bin/setdate \

# files in media folder
PRODUCT_COPY_FILES += \
	device/flowdata/provue/media/bootanimation.zip:system/media/bootanimation.zip \
	device/flowdata/provue/gpio-20.kl:data/system/devices/keylayout/gpio-20.kl

LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)
LOCAL_MODULE := Reader
LOCAL_SOURCE_FILES := system/$(LOCAL_MODULE).apk
LOCAL_MODULE_CLASS := APPS
LOCAL_MODULE_SUFFIX := $(COMMON_ANDROID_PACKAGE_SUFFIX)
LOCAL_MODULE_TAGS := optional
LOCAL_CERTIFICATE := PRESIGNED

include $(BUILD_PREBUILT)
