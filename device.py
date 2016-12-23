import pyopencl as cl
import re
import utils

from pyopencl import device_info as di

class Device():
    # TODO: try to implement sub-devices part, REFERENCE_COUNT is one of sub-devices.
    MEMORY_INFO = [{"key": "GLOBAL_MEM_CACHELINE_SIZE", "name": "Global memory cache line size",
                    "type": "byte_int"},
                   {"key": "GLOBAL_MEM_CACHE_SIZE", "name": "Global memory cache size",
                    "type": "byte_int"},
                   {"key": "GLOBAL_MEM_CACHE_TYPE", "name": "Global memory cache type",
                    "type": "device_mem_cache_type"},
                   {"key": "GLOBAL_MEM_SIZE", "name": "Global memory size", "type": "byte_int"},
                   {"key": "GLOBAL_VARIABLE_PREFERRED_TOTAL_SIZE",
                    "available": {"type": "version", "value": 2},
                    "name": "Max preferred size of global variables", "type": "byte_int"},
                   {"key": "LOCAL_MEM_SIZE", "name": "Local memory size", "type": "byte_int"},
                   {"key": "LOCAL_MEM_TYPE", "name": "Local memory type",
                    "type": "device_local_mem_type"},
                   {"key": "MAX_CONSTANT_ARGS", "name": "Max constant arguments count",
                    "type": "int"},
                   {"key": "MAX_CONSTANT_BUFFER_SIZE", "name": "Max size of a constant buffer",
                    "type": "byte_int"},
                   {"key": "MAX_GLOBAL_VARIABLE_SIZE",
                    "available": {"type": "version", "value": 2},
                    "name": "Max global variable size", "type": "byte_int"},
                   {"key": "MAX_MEM_ALLOC_SIZE", "name": "Max size of memory object allocation",
                    "type": "byte_int"},
                   {"key": "MAX_PARAMETER_SIZE", "name": "Max parameter size", "type": "byte_int"},
                   {"key": "MAX_PIPE_ARGS", "name": "Max pipe objects", "type": "int",
                    "available": {"type": "version", "value": 2}},
                   {"key": "MAX_WORK_GROUP_SIZE", "name": "max work group size", "type": "int"},
                   {"key": "MAX_WORK_ITEM_DIMENSIONS", "name": "max work item dimensions",
                    "type": "int"},
                   {"key": "MAX_WORK_ITEM_SIZES", "name": "max work item size",
                    "type": "int3"},
                   {"key": "MEM_BASE_ADDR_ALIGN", "name": "base address align", "type": "int"},
                   {"key": "LOCAL_MEM_SIZE", "name": "Local memory size", "type": "byte_int"},
                   {"key": "QUEUE_ON_DEVICE_MAX_SIZE", "name": "The max size of the device queue",
                    "type": "byte_int", "available": {"type": "version", "value": 2}},
                   {"key": "QUEUE_ON_DEVICE_PREFERRED_SIZE", "name": "The size of the device queue",
                    "type": "byte_int", "available": {"type": "version", "value": 2}},
                   {"key": "QUEUE_ON_DEVICE_PROPERTIES", "name": "Device command-queue properties",
                    "type": "command_queue_properties",
                    "available": {"type": "version", "value": 2}},
                   {"key": "QUEUE_ON_HOST_PROPERTIES", "name": "Host command-queue properties",
                    "type": "command_queue_properties"},
                ]
    DEVICE_INFO = [{"key": "ADDRESS_BITS", "name": "Address size", "type": "int"},
                   {"key": "AVAILABLE", "name": "Available", "type": "bool"},
                   {"key": "BUILT_IN_KERNELS", "name": "Built-in kernels",
                    "available": {"type": "version", "value": 1.2},
                    "type": "semicoloned_string"},
                   {"key": "COMPILER_AVAILABLE", "name": "Compiler available", "type": "bool"},
                   {"key": "DRIVER_VERSION", "name": "Driver version", "type": "string"},
                   {"key": "ENDIAN_LITTLE", "name": "Little endian", "type": "bool"},
                   {"key": "ERROR_CORRECTION_SUPPORT", "name": "Error-correction supported",
                    "type": "bool"},
                   {"key": "EXECUTION_CAPABILITIES", "name": "Execution capabilities",
                    "type": "device_exec_capabilities"},
                   {"key": "EXTENSIONS", "name": "Extensions", "type": "spaced_string"},
                   {"key": "DRIVER_VERSION", "name": "Driver version", "type": "string"},
                   {"key": "MAX_CLOCK_FREQUENCY", "name": "Frequency", "type": "mhz"},
                   {"key": "MAX_COMPUTE_UNITS", "name": "Compute units", "type": "int"},
                   {"key": "MAX_ON_DEVICE_EVENTS", "name": "Max on device event", "type": "int"},
                   {"key": "MAX_ON_DEVICE_QUEUES", "name": "Max on device queue", "type": "int",
                    "available": {"type": "version", "value": 2}},
                   {"key": "LINKER_AVAILABLE", "name": "Linker available", "type": "bool"},
                   {"key": "MAX_SAMPLERS", "name": "Max sampler used in a kernel", "type": "int"},
                   {"key": "NAME", "name": "Device name", "type": "string"},
                   {"key": "OPENCL_C_VERSION", "name": "OpenCL C version", "type": "string"},
                   {"key": "PIPE_MAX_ACTIVE_RESERVATIONS", "name": "The max reservations",
                    "type": "int", "available": {"type": "version", "value": 2}},
                   {"key": "PIPE_MAX_PACKET_SIZE", "name": "The max size of pipe packet",
                    "type": "byte_int", "available": {"type": "version", "value": 2}},
                   {"key": "PREFERRED_GLOBAL_ATOMIC_ALIGNMENT", "name": "Global atomic align",
                    "type": "int", "available": {"type": "version", "value": 2}},
                   {"key": "PREFERRED_INTEROP_USER_SYNC", "name": "Memory share sync by User",
                    "type": "bool", "available": {"type": "version", "value": 1.2}},
                   {"key": "PREFERRED_LOCAL_ATOMIC_ALIGNMENT", "name": "Local atomic align",
                    "type": "int", "available": {"type": "version", "value": 2}},
                   {"key": "PREFERRED_PLATFORM_ATOMIC_ALIGNMENT", "name": "Platform atomic align",
                    "type": "int", "available": {"type": "version", "value": 2}},
                   {"key": "PRINTF_BUFFER_SIZE", "name": "Printf buffer size",
                    "type": "byte_int", "available": {"type": "version", "value": 1.2}},
                   {"key": "PROFILING_TIMER_RESOLUTION", "name": "Profiling timer resolution",
                    "type": "timer_resolution"},
                   {"key": "TYPE", "name": "Type of device", "type": "device_type"},
                   {"key": "VENDOR", "name": "Vendor name", "type": "string"},
                   {"key": "VENDOR_ID", "name": "Vendor ID", "type": "int"},
                   {"key": "VERSION", "name": "Version", "type": "string"},
                  ]
    DATA_TYPE_INFO = [{"key": "DOUBLE_FP_CONFIG", "name": "Double supported",
                       "available": {"type": "extensions", "value": "cl_khr_fp64"},
                       "type": "device_fp_config"},
                      {"key": "HALF_FP_CONFIG", "name": "Half supported",
                       "available": {"type": "extensions", "value": "cl_khr_fp16"},
                       "type": "device_fp_config"},
                      {"key": "NATIVE_VECTOR_WIDTH_CHAR", "name": "ISA vector width for char",
                       "type": "int"},
                      {"key": "NATIVE_VECTOR_WIDTH_DOUBLE", "name": "ISA vector width for double",
                       "type": "int"},
                      {"key": "NATIVE_VECTOR_WIDTH_FLOAT", "name": "ISA vector width for float",
                       "type": "int"},
                      {"key": "NATIVE_VECTOR_WIDTH_HALF", "name": "ISA vector width for half",
                       "type": "int"},
                      {"key": "NATIVE_VECTOR_WIDTH_INT", "name": "ISA vector width for int",
                       "type": "int"},
                      {"key": "NATIVE_VECTOR_WIDTH_LONG", "name": "ISA vector width for long",
                       "type": "int"},
                      {"key": "NATIVE_VECTOR_WIDTH_SHORT", "name": "ISA vector width for short",
                       "type": "int"},
                      {"key": "PREFERRED_VECTOR_WIDTH_CHAR",
                       "name": "Preferred native vector width for char", "type": "int"},
                      {"key": "PREFERRED_VECTOR_WIDTH_DOUBLE",
                       "name": "Preferred native vector width for double", "type": "int"},
                      {"key": "PREFERRED_VECTOR_WIDTH_FLOAT",
                       "name": "Preferred native vector width for float", "type": "int"},
                      {"key": "PREFERRED_VECTOR_WIDTH_HALF",
                       "name": "Preferred native vector width for half", "type": "int",
                       "available": {"type": "version", "value": 1.1}},
                      {"key": "PREFERRED_VECTOR_WIDTH_INT",
                       "name": "Preferred native vector width for int", "type": "int"},
                      {"key": "PREFERRED_VECTOR_WIDTH_LONG",
                       "name": "Preferred native vector width for long", "type": "int"},
                      {"key": "PREFERRED_VECTOR_WIDTH_SHORT",
                       "name": "Preferred native vector width for short", "type": "int"},
                      {"key": "SINGLE_FP_CONFIG", "name": "Single supported",
                       "type": "device_fp_config"},
                      {"key": "SVM_CAPABILITIES", "name": "SVM capabilities",
                       "type": "device_svm_capabilities"},

                     ]
    IMAGE_INFO = [{"key": "IMAGE2D_MAX_HEIGHT", "name": "2D image max height", "type": "int"},
                  {"key": "IMAGE2D_MAX_WIDTH", "name": "2D image max width", "type": "int"},
                  {"key": "IMAGE3D_MAX_DEPTH", "name": "3D image max depth", "type": "int"},
                  {"key": "IMAGE3D_MAX_HEIGHT", "name": "3D image max height", "type": "int"},
                  {"key": "IMAGE3D_MAX_WIDTH", "name": "3D image max width", "type": "int"},
                  {"key": "IMAGE_MAX_ARRAY_SIZE", "available": {"type": "version", "value": 1.2},
                   "name": "Max images in a 1D or 2D image array", "type": "int"},
                  {"key": "IMAGE_MAX_BUFFER_SIZE", "available": {"type": "version", "value": 1.2},
                   "name": "Max pixels for an image", "type": "int"},
                  {"key": "IMAGE_SUPPORT", "name": "Image supported", "type": "bool"},
                  {"key": "MAX_READ_IMAGE_ARGS", "name": "Max read-only image objects",
                   "type": "int"},
                  {"key": "MAX_READ_WRITE_IMAGE_ARGS", "name": "Max read-write image objects",
                   "type": "int", "available": {"type": "version", "value": 2}},
                  {"key": "MAX_WRITE_IMAGE_ARGS", "name": "Max write-only image objects",
                   "type": "int"}
                 ]

    VALUE_FORMATTER = {"bool": lambda v: "True" if v else "False",
                       "byte_int": utils.format_byte,
                       "command_queue_properties": utils.format_ocl_command_queue_properties,
                       "device_exec_capabilities": utils.format_ocl_device_exec_capabilities,
                       "device_fp_config": utils.format_ocl_device_fp_config,
                       "device_mem_cache_type": lambda v: cl.device_mem_cache_type.to_string(v),
                       "device_local_mem_type": lambda v: cl.device_local_mem_type.to_string(v),
                       "device_svm_capabilities": utils.format_ocl_device_svm_capabilities,
                       "device_type": lambda v: cl.device_type.to_string(v),
                       "int": str,
                       "int3": str,
                       "mhz": utils.format_mhz,
                       "semicoloned_string": lambda v: v.split(";"),
                       "spaced_string": lambda v: v.split(),
                       "string": str,
                       "timer_resolution": utils.format_timer_resolution
                      }

    ITEM_LIST = [MEMORY_INFO, DEVICE_INFO, DATA_TYPE_INFO, IMAGE_INFO]

    def __init__(self, device, item_list=None):
        self.__device = device
        self.__item_list = item_list

    def enter(self):
        utils.cls()
        utils.print_info([["", "Device name", self.__device.name],
                          ["", "Device type", cl.device_type.to_string(self.__device.type)],
                          ["", "Device version", self.__device.version],
                          ["", "Device Profile", self.__device.profile]])
        print("=" * 85)

    def list(self):
        if self.__item_list is None:
            utils.print_info([[1, "Memory", "Memory info({0})".format(len(Device.MEMORY_INFO))],
                              [2,
                               "Device info",
                               "Device info({0})".format(len(Device.DEVICE_INFO))],
                              [3,
                               "Data type",
                               "Data type info({0})".format(len(Device.DATA_TYPE_INFO))],
                              [4, "Image", "Image info({0})".format(len(Device.IMAGE_INFO))]])
            return 4
        else:
            infos = []
            for item in self.__item_list:
                infos.append(self.evaluate_result(item))
            utils.print_info(infos)
            return 0

    def choose(self, index):
        if self.__item_list is None:
            return Device(self.__device, Device.ITEM_LIST[index])
        else:
            return None

    def prompt(self):
        if self.__item_list is None:
            return "Please choose which information group you want to see"
        else:
            return None

    def evaluate_available(self, available):
        if available["type"] == "version":
            m = re.search("^[A-Za-z]+\s([\d.]+)", self.__device.version)
            return float(m.group(1)) >= available["value"] if m else False
        elif available["type"] == "extensions":
            return available["value"] in self.__device.extensions.split()
        else:
            return False

    def evaluate_result(self, item):
        if "available" in item and self.evaluate_available(item["available"]) is False:
            return ["", item["name"], "Not available ({0})".format(item["available"]["type"])]

        if item["type"] not in Device.VALUE_FORMATTER:
            return ["", item["name"], "Type, {0}, is not supported".format(item["type"])]

        val_err = False
        if hasattr(di, item["key"]):
            try:
                val = self.__device.get_info(getattr(di, item["key"]))
            except Exception as e:
                val = "ERROR TO READ VALUE"
                val_err = True
        else:
            val = "pyopencl doesn't support this."
            val_err = True

        return ["", item["name"], val if val_err else Device.VALUE_FORMATTER[item["type"]](val)]
