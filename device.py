import pyopencl as cl
import utils

from pyopencl import device_info as di

class Device():
    # TODO: finish the list from PIPE_MAX_ACTIVE_RESERVATIONS
    # TODO: implement the interpreter of info array
    # TODO: try to implement sub-devices part
    MEMORY_INFO = [{"key": di.GLOBAL_MEM_CACHELINE_SIZE, "name": "Global memory cache line size",
                    "type": "byte_int"},
                   {"key": di.GLOBAL_MEM_CACHE_SIZE, "name": "Global memory cache size",
                    "type": "byte_int"},
                   {"key": di.GLOBAL_MEM_CACHE_TYPE, "name": "Global memory cache type",
                    "type": "device_mem_cache_type"},
                   {"key": di.GLOBAL_MEM_SIZE, "name": "Global memory size", "type": "byte_int"},
                   {"key": di.GLOBAL_VARIABLE_PREFERRED_TOTAL_SIZE,
                    "available": {"type": "version", "value": 2},
                    "name": "Maximum preferred total size of global variables", "type": "byte_int"},
                   {"key": di.LOCAL_MEM_SIZE, "name": "Local memory size", "type": "byte_int"},
                   {"key": di.LOCAL_MEM_TYPE, "name": "Local memory type",
                    "type": "device_local_mem_type"},
                   {"key": di.MAX_CONSTANT_ARGS, "name": "Max constant arguments count",
                    "type": "int"},
                   {"key": di.MAX_CONSTANT_BUFFER_SIZE, "name": "Max size of a constant buffer",
                    "type": "byte_int"},
                   {"key": di.MAX_GLOBAL_VARIABLE_SIZE,
                    "available": {"type": "version", "value": 2},
                    "name": "Max global variable size", "type": "byte_int"},
                   {"key": di.MAX_MEM_ALLOC_SIZE, "name": "Max size of memory object allocation",
                    "type": "byte_int"},
                   {"key": di.MAX_PARAMETER_SIZE, "name": "Max parameter size", "type": "byte_int"},
                   {"key": di.MAX_PIPE_ARGS, "name": "Max pipe objects", "type": "int",
                    "available": {"type": "version", "value": 2}},
                   {"key": di.MAX_WORK_GROUP_SIZE, "name": "max work group size", "type": "int"},
                   {"key": di.MAX_WORK_ITEM_DIMENSIONS, "name": "max work item dimensions",
                    "type": "int"},
                   {"key": di.MAX_WORK_ITEM_SIZES, "name": "max work item size",
                    "type": "int3"},
                   {"key": di.MEM_BASE_ADDR_ALIGN, "name": "base address align", "type": "int"},
                   {"key": di.LOCAL_MEM_SIZE, "name": "Local memory size", "type": "byte_int"},
                   {"key": di.LOCAL_MEM_SIZE, "name": "Local memory size", "type": "byte_int"},
                   {"key": di.LOCAL_MEM_SIZE, "name": "Local memory size", "type": "byte_int"}
                ]
    DEVICE_INFO = [{"key": di.ADDRESS_BITS, "name": "Address size", "type": "int"},
                   {"key": di.AVAILABLE, "name": "Available", "type": "bool"},
                   {"key": di.BUILT_IN_KERNELS, "name": "Built-in kernels",
                    "available": {"type": "version", "value": 1.2},
                    "type": "semicoloned_string"},
                   {"key": di.COMPILER_AVAILABLE, "name": "Compiler available", "type": "bool"},
                   {"key": di.DRIVER_VERSION, "name": "Driver version", "type": "string"},
                   {"key": di.ENDIAN_LITTLE, "name": "Little endian", "type": "bool"},
                   {"key": di.ERROR_CORRECTION_SUPPORT, "name": "Error-correction supported",
                    "type": "bool"},
                   {"key": di.EXECUTION_CAPABILITIES, "name": "Execution capabilities",
                    "type": "device_exec_capabilities"},
                   {"key": di.EXTENSIONS, "name": "Extensions", "type": "spaced_string"},
                   {"key": di.DRIVER_VERSION, "name": "Driver version", "type": "string"},
                   {"key": di.MAX_CLOCK_FREQUENCY, "name": "Frequency", "type": "mhz"},
                   {"key": di.MAX_COMPUTE_UNITS, "name": "Compute units", "type": "int"},
                   {"key": di.MAX_ON_DEVICE_EVENTS, "name": "Max on device event", "type": "int"},
                   {"key": di.MAX_ON_DEVICE_QUEUES, "name": "Max on device queue", "type": "int",
                    "available": {"type": "version", "value": 2}},
                   {"key": di.LINKER_AVAILABLE, "name": "Linker available", "type": "bool"},
                   {"key": di.MAX_SAMPLERS, "name": "Max sampler used in a kernel", "type": "int"},
                   {"key": di.NAME, "name": "Device name", "type": "string"},
                   {"key": di.OPENCL_C_VERSION, "name": "OpenCL C version", "type": "string"}
                  ]
    DATA_TYPE_INFO = [{"key": di.DOUBLE_FP_CONFIG, "name": "Double supported",
                       "available": {"type": "extensions", "value": "cl_khr_fp64"},
                       "type": "device_fp_config"},
                      {"key": di.HALF_FP_CONFIG, "name": "Half supported",
                       "available": {"type": "extensions", "value": "cl_khr_fp16"},
                       "type": "device_fp_config"},
                      {"key": di.NATIVE_VECTOR_WIDTH_CHAR, "name": "ISA vector width for char",
                       "type": "int"},
                      {"key": di.NATIVE_VECTOR_WIDTH_DOUBLE, "name": "ISA vector width for double",
                       "type": "int"},
                      {"key": di.NATIVE_VECTOR_WIDTH_FLOAT, "name": "ISA vector width for float",
                       "type": "int"},
                      {"key": di.NATIVE_VECTOR_WIDTH_HALF, "name": "ISA vector width for half",
                       "type": "int"},
                      {"key": di.NATIVE_VECTOR_WIDTH_INT, "name": "ISA vector width for int",
                       "type": "int"},
                      {"key": di.NATIVE_VECTOR_WIDTH_LONG, "name": "ISA vector width for long",
                       "type": "int"},
                      {"key": di.NATIVE_VECTOR_WIDTH_SHORT, "name": "ISA vector width for short",
                       "type": "int"}
                     ]
    IMAGE_INFO = [{"key": di.IMAGE2D_MAX_HEIGHT, "name": "2D image max height", "type": "pixel"},
                  {"key": di.IMAGE2D_MAX_WIDTH, "name": "2D image max width", "type": "pixel"},
                  {"key": di.IMAGE3D_MAX_DEPTH, "name": "3D image max depth", "type": "pixel"},
                  {"key": di.IMAGE3D_MAX_HEIGHT, "name": "3D image max height", "type": "pixel"},
                  {"key": di.IMAGE3D_MAX_WIDTH, "name": "3D image max width", "type": "pixel"},
                  {"key": di.IMAGE_MAX_ARRAY_SIZE, "available": {"type": "version", "value": 1.2},
                   "name": "Max images in a 1D or 2D image array", "type": "int"},
                  {"key": di.IMAGE_MAX_BUFFER_SIZE, "available": {"type": "version", "value": 1.2},
                   "name": "Max pixels for an image", "type": "int"},
                  {"key": di.IMAGE_SUPPORT, "name": "Image supported", "type": "bool"},
                  {"key": di.MAX_READ_IMAGE_ARGS, "name": "Max read-only image objects",
                   "type": "int"},
                  {"key": di.MAX_READ_WRITE_IMAGE_ARGS, "name": "Max read-write image objects",
                   "type": "int", "available": {"type": "version", "value": 2}},
                  {"key": di.MAX_WRITE_IMAGE_ARGS, "name": "Max write-only image objects",
                   "type": "int"}
                 ]

    def __init__(self, device, sub=None):
        self.__device = device
        self.__sub = sub

    def enter(self):
        utils.cls()
        utils.print_info([["", "Device name", self.__device.name],
                          ["", "Device type", cl.device_type.to_string(self.__device.type)],
                          ["", "Device version", self.__device.version]])
        print("=" * 80)

    def list(self):
        if self.__sub is None:
            group = ["Memory", "Device", "Data type", "Image"]
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
            return 0

    def choose(self, index):
        # TODO: implement choose sub group of device
        return None

    def prompt(self):
        if self.__sub is None:
            return "Please choose which information group you want to see"
        else:
            return None
