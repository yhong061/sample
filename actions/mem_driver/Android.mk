LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)

LOCAL_MODULE := test_mem

LOCAL_MODULE_TAGS := optional

LOCAL_SRC_FILES :=mem_driver.c

LOCAL_MODULE_PATH := /home/yhong/Sample/kernel/xc6130_reg
LOCAL_SHARED_LIBRARIES :=       \
    libcutils                   \
    liblog


LOCAL_CPPFLAGS += -g  -Wall -O2 -DDEBUG -DSOAP_MEM_DEBUG -pthread

include $(BUILD_EXECUTABLE)
