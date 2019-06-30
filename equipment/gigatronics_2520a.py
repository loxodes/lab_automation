from plx_gpib_ethernet import PrologixGPIBEthernet

# scraps to control a gigatronics 2520A signal generator

GPIB_ADDR_2520A = 6

class Gigatronics2520A():
    def __init__(self, prologix = False, gpib_addr = GPIB_ADDR_2520A):
        if not prologix:
            self.gpib = PrologixGPIBEthernet('192.168.1.128')
            self.gpib.connect()
        else:
            self.gpib = prologix

        self.gpib.select(gpib_addr)
        self.gpib.write('*RST')
        assert '2520A' in self.gpib.query('*IDN?')

    def set_cw_frequency(self, freq):
        self.gpib.write('SOURCE:FREQUENCY:FIX {}HZ'.format(str(int(freq))))
        f_readback = float(self.gpib.query('SOURCE:FREQUENCY?'))
        assert f_readback == freq

    def set_cw_power(self, power_dbm):
        self.gpib.write('SOURCE:POWER:LEVEL:IMM:AMPLITUDE {}DBM'.format(str(int(power_dbm))))
        p_readback = float(self.gpib.query('SOURCE:POWER:LEVEL:IMM:AMPLITUDE?'))
        assert int(p_readback) == power_dbm

    def output_on(self):
        self.gpib.write('OUTPUT ON')
        assert float(self.gpib.query('OUTPUT:STATE?')) == 1

    def output_off(self):
        self.gpib.write('OUTPUT OFF')
        assert float(self.gpib.query('OUTPUT:STATE?')) == 0

if __name__ == '__main__':
    synth = Gigatronics2520A()

    synth.set_cw_frequency(2.5e9)
    synth.set_cw_power(-10)
    synth.output_on()



        

    

