# GPIB communication with a keithley 2400 via a "Keysight" 82357B
# linux-gpib for the 82357B installed via the following guide,
# https://tomverbeure.github.io/2023/01/29/Installing-Linux-GPIB-Drivers-for-the-Agilent-82357B.html

import pyvisa
import numpy as np
import time

class Keithley2400:
    def __init__(self, gpib_addr = 'GPIB0::24::INSTR', display = False, rm = None):
        if rm == None:
            rm = pyvisa.ResourceManager('@py') # '@py' because of https://github.com/pyvisa/pyvisa/issues/645
        
        self.instr = rm.open_resource(gpib_addr)
        assert '2400' in self.instr.query('*IDN?')
        self.instr.write('*RST')
        
        if display:
            self.instr.write('DISP:ENAB 1')
        else:
            self.instr.write('DISP:ENAB 0')

        self.instr.write(':SYSTem:BEEPer:STATe OFF')

    def enable_output(self, state):
        if state == True:
            self.instr.write(':OUTP ON')
        else:
            self.instr.write(':OUTP OFF')
    
    def set_local(self):
        self.instr.write('SYSTEM:KEY 23')
        self.instr.write('DISP:ENAB 1')

    def voltage_sweep(self, v_start, v_stop, v_points=101, compliance=0.1e3):
        self.enable_output(False)
        self.instr.write(":SOUR:FUNC:MODE VOLT")
        self.instr.write(":SENS:CURR:PROT:LEV " + str(compliance))
        self.instr.write(":SENS:CURR:RANGE:AUTO 1")


        v_sweep = np.linspace(v_start, v_stop, v_points, endpoint=True)
        v_meas = np.zeros_like(v_sweep)
        i_meas = np.zeros_like(v_sweep)

        self.instr.write(":SOUR:VOLT " + str(v_start))
        self.enable_output(True)

        for (i, v_set) in enumerate(v_sweep):
            self.instr.write(":SOUR:VOLT " + str(v_set))
            time.sleep(0.1)

            data = self.instr.query(":READ?").split(',')

            i_meas[i] = float(data[1])
            v_meas[i] = float(data[0])
        
        self.enable_output(False)

        return v_meas, i_meas
    
    def __exit__(self):
        self.instr.close()

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import pdb

    smu = Keithley2400()
    v, i = smu.voltage_sweep(v_start=-20, v_stop=20, v_points = 201)

    plt.grid(True)
    plt.title('leakage current')
    plt.yscale('log')
    plt.xlabel('voltage (V)')
    plt.ylabel('magnitude of current (A)')
    plt.plot(v, np.abs(i))
    plt.show()

    pdb.set_trace()
    
