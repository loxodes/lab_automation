# GPIB communication with a keithley 2400 via a "Keysight" 82357B
# linux-gpib for the 82357B installed via the following guide,
# https://tomverbeure.github.io/2023/01/29/Installing-Linux-GPIB-Drivers-for-the-Agilent-82357B.html

import pyvisa
rm = ResourceManager('@py') # '@py' because of https://github.com/pyvisa/pyvisa/issues/645

instr = rm.open_resource('GPIB0::24::INSTR')
print(instr.query('*IDN?'))



