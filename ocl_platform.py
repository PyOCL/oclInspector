import pyopencl as cl
import utils

from device import Device

class Platform():

    def __init__(self, platform):
        self.__platform = platform

    def enter(self):
        utils.cls()
        utils.print_info([["", "Platform name",  self.__platform.name],
                          ["", "Platform profile",  self.__platform.profile],
                          ["", "Platform vendor", self.__platform.vendor],
                          ["", "Platform version", self.__platform.version],
                          ["", "Platform extensions", self.__platform.extensions.split()]])
        print("=" * 80)

    def list(self):
        idx = 1
        for device in self.__platform.get_devices():
            utils.print_info([[idx, "Device name", device.name],
                             ["", "Device type", cl.device_type.to_string(device.type)],
                             ["", "Device version", device.version]])
            idx = idx + 1
            print("-" * 85)
        return idx - 1

    def choose(self, index):
        return Device(self.__platform.get_devices()[index])

    def prompt(self):
        return "Please choose which device you want to see"
