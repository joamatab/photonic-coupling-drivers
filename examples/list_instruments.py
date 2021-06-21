import pyvisa as visa

rm = visa.ResourceManager("@py")
# rm = visa.ResourceManager()
print(list(rm.list_resources()))

# inst = rm.open_resource('ASRL/dev/ttyUSB0::INSTR')
# print(inst.query('*IDN?'))

# inst = rm.open_resource('COM3')
# print(inst.query('*IDN?'))


ip = "192.168.111.231"  # keithley
ip = "192.168.111.229"  # keithley
ip = "192.168.111.187"  # keithley
ip = "192.168.111.158"  # prologix
# address = f"TCPIP::{ip}::5025::SOCKET"
inst = rm.open_resource(f"TCPIP::{ip}::INSTR")
# print(address)
# inst = rm.open_resource(address)
print(inst.query("*IDN?"))
