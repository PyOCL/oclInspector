# oclInspector
The command line tool for showing OpenCL device information

## Dependencies
oclInspector only depends on pyopencl. Before running it, please check if the pyopencl is installed. If not, please use pip to install it:

```
pip install pyopencl
```

## Run
We can run oclInspector with the following command:

```
python inspector.py
```

## Usage

We can use number key to choose items that we want to see. There are two general commands at all pages which are `0` for going back and `-1` for exit the app immediately.

### Platform
oclInspector lists all of your OpenCL platforms for you at the first page, like:

```
=====================================================================================
 1 platform NAME   : NVIDIA CUDA
            VERSION: OpenCL 1.2 CUDA 8.0.0
            PROFILE: FULL_PROFILE
            VENDOR : NVIDIA Corporation
-------------------------------------------------------------------------------------
 2 platform NAME   : Intel(R) OpenCL
            VERSION: OpenCL 2.0
            PROFILE: FULL_PROFILE
            VENDOR : Intel(R) Corporation
-------------------------------------------------------------------------------------
Please choose which platform you want to see (1 ~ 2, 0 for back, -1 for exit):
```

### Platform devices

We can type the number to see detailed information. In this case, we type 1 if we want to see NVIDIA CUDA platform:
```
Platform name                           :                              NVIDIA CUDA
Platform profile                        :                             FULL_PROFILE
Platform vendor                         :                       NVIDIA Corporation
Platform version                        :                    OpenCL 1.2 CUDA 8.0.0
Platform extensions                     :         cl_khr_global_int32_base_atomics
                                        :     cl_khr_global_int32_extended_atomics
                                        :          cl_khr_local_int32_base_atomics
                                        :      cl_khr_local_int32_extended_atomics
                                        :                              cl_khr_fp64
                                        :            cl_khr_byte_addressable_store
                                        :                               cl_khr_icd
                                        :                        cl_khr_gl_sharing
                                        :                   cl_nv_compiler_options
                                        :             cl_nv_device_attribute_query
                                        :                      cl_nv_pragma_unroll
                                        :                      cl_nv_d3d10_sharing
                                        :                     cl_khr_d3d10_sharing
                                        :                      cl_nv_d3d11_sharing
                                        :                          cl_nv_copy_opts
================================================================================
1  Device name                             :                         GeForce GTX 950M
   Device type                             :                                      GPU
   Device version                          :                          OpenCL 1.2 CUDA
-------------------------------------------------------------------------------------
Please choose which device you want to see (1 ~ 1, 0 for back, -1 for exit):
```

oclInspector lists detailed platform information and lists all devices on this platform.

### Device

Once we choose 1 to see the GeForce GTX 950M, we can see the basic information of device and 4 information group.
```
Device name                             :                         GeForce GTX 950M
Device type                             :                                      GPU
Device version                          :                          OpenCL 1.2 CUDA
Device Profile                          :                             FULL_PROFILE
=====================================================================================
1  Memory                                  :                          Memory info(22)
2  Device info                             :                          Device info(30)
3  Data type                               :                       Data type info(18)
4  Image                                   :                           Image info(11)
Please choose which information group you want to see (1 ~ 4, 0 for back, -1 for exit):
```

### Device information group

We can choose 1 if we want to see memory information:

```
Device name                             :                         GeForce GTX 950M
Device type                             :                                      GPU
Device version                          :                          OpenCL 1.2 CUDA
Device Profile                          :                             FULL_PROFILE
=====================================================================================
Global memory cache line size           :                                     128B
Global memory cache size                :                                  80.00KB
Global memory cache type                :                         READ_WRITE_CACHE
Global memory size                      :                                   2.00GB
Max preferred size of global variables  :                  Not available (version)
Local memory size                       :                                  48.00KB
Local memory type                       :                                    LOCAL
Max constant arguments count            :                                        9
Max size of a constant buffer           :                                  64.00KB
Max global variable size                :                  Not available (version)
Max size of memory object allocation    :                                 512.00MB
Max parameter size                      :                                   4.25KB
Max pipe objects                        :                  Not available (version)
max work group size                     :                                     1024
max work item dimensions                :                                        3
max work item size                      :                         [1024, 1024, 64]
base address align                      :                                     4096
Local memory size                       :                                  48.00KB
The max size of the device queue        :                  Not available (version)
The size of the device queue            :                  Not available (version)
Device command-queue properties         :                  Not available (version)
Host command-queue properties           :            OUT_OF_ORDER_EXEC_MODE_ENABLE
                                        :                         PROFILING_ENABLE
None (1 ~ 0, 0 for back, -1 for exit):
```

- There are a few fields shown `Not available (version)` or `Not available (extensions)` which means this fields is not available on this device.
- For some devices, it cannot read OpenCL device info correctly that may be a driver issue. If this happens, the field shows `ERROR TO READ VALUE`
- If our pyopencl is too old to list properties, a field shows `pyopencl too old to have this.`

## Missing fields (TODO list)
We may find there are some missing fields at [pyopencl API](https://documen.tician.de/pyopencl/runtime_const.html#device_info):

- sub-devices related
- vendor specified: amd, intel, nv, ...
- OpenCL version greater than 2.1 (included)
- pyopencl version greater than 2016.2

## Missing informations (TODO list)
There are some objects which can be inspected and not in the list, like kernel, etc.
