LOCAL_PATH := $(call my-dir)

PRIVATE_LOCAL_CFLAGS := -O2 -g -W -Wall

include $(CLEAR_VARS)

LOCAL_SRC_FILES := gsc_update.c
LOCAL_MODULE := gsc_update
LOCAL_MODULE_TAGS := optional
LOCAL_C_INCLUDES := $(LOCAL_PATH)/include/
LOCAL_CFLAGS := $(PRIVATE_LOCAL_CFLAGS)
LOCAL_STATIC_LIBRARIES := libcutils libc

include $(BUILD_EXECUTABLE)
