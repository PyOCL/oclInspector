import os
import pyopencl as cl

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def print_info(data):
    for row in data:
        if type(row[2]) == list:
            print("{0:<2} {1:<40}: {2: >40}".format(row[0], row[1], row[2][0]))
            for i in range(1, len(row[2])):
                print("{0:<2} {1:<40}: {2: >40}".format("", "", row[2][i]))
        else:
            print("{0:<2} {1:<40}: {2: >40}".format(*row))

def format_byte(val):
    assert type(val) == int

    if val < 1024:
        return "{0}B".format(val)
    elif val < 1024 * 1024:
        return "{0:.2f}KB".format(float(val) / 1024)
    elif val < 1024 * 1024 * 1024:
        return "{0:.2f}MB".format(float(val) / 1024 / 1024)
    elif val < 1024 * 1024 * 1024 * 1024:
        return "{0:.2f}GB".format(float(val) / 1024 / 1024/ 1024)
    else:
        return "{0:.2f}TB".format(float(val) / 1024 / 1024/ 1024 / 1024)

def format_mhz(val):
    assert type(val) == int

    if (val < 1024):
        return "{0}MHz".format(val)
    else:
        return "{0}GHz".format(int(val / 1024));

def format_ocl_enum(clz, val):
    try:
        return clz.to_string(val)
    except Exception as e:
        return val

def format_ocl_device_fp_config(val):
    cfg = cl.device_fp_config
    items = [cfg.CORRECTLY_ROUNDED_DIVIDE_SQRT,
             cfg.DENORM,
             cfg.FMA,
             cfg.INF_NAN,
             cfg.ROUND_TO_INF,
             cfg.ROUND_TO_NEAREST,
             cfg.ROUND_TO_ZERO,
             cfg.SOFT_FLOAT]
    ret = []
    for item in items:
        if val & item == item:
            ret.append(cfg.to_string(item))
    return ret

def format_ocl_device_exec_capabilities(val):
    ec = cl.device_exec_capabilities
    items = [ec.KERNEL,
             ec.NATIVE_KERNEL]
    ret = []
    for item in items:
        if val & item == item:
            ret.append(ec.to_string(item))
    return ret

def format_ocl_command_queue_properties(val):
    enum = cl.command_queue_properties
    items = [enum.ON_DEVICE,
             enum.ON_DEVICE_DEFAULT,
             enum.OUT_OF_ORDER_EXEC_MODE_ENABLE,
             enum.PROFILING_ENABLE]
    ret = []
    for item in items:
        if val & item == item:
            ret.append(enum.to_string(item))
    return ret

def format_ocl_device_svm_capabilities(val):
    enum = cl.device_svm_capabilities
    items = [enum.ATOMICS,
             enum.COARSE_GRAIN_BUFFER,
             enum.FINE_GRAIN_BUFFER,
             enum.FINE_GRAIN_SYSTEM]
    ret = []
    for item in items:
        if val & item == item:
            ret.append(enum.to_string(item))
    return ret

def format_timer_resolution(val):
    return "{0} nanoseconds".format(val)
