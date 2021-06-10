
import visa
import plab

from ThorlabsPM100 import ThorlabsPM100

rm = visa.ResourceManager()
instances = ['USB0::0x1313::0x8078::P0017917::INSTR', 'GPIB0::1::INSTR']

# laser = plab.lasers.TSL550(instances[1])
# pm = plab.power_meters.Pm100Usb(inst[0])

inst = rm.open_resource(instances[0])
pm = ThorlabsPM100(inst=inst)


print(pm.read)
# laser = rm.open_resource(instances[1])
# print(laser.query('*IDN?'))