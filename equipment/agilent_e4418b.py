from plx_gpib_ethernet import PrologixGPIBEthernet
GPIB_ADDR_E4418B = 15
import time, pdb

class AgilentE4418B():
    def __init__(self, prologix = False, gpib_addr = GPIB_ADDR_E4418B):
        if not prologix:
            self.gpib = PrologixGPIBEthernet('192.168.1.128', timeout = 10)
            self.gpib.connect()
        else:
            self.gpib = prologix

        self.gpib_addr = gpib_addr

        self.gpib.select(self.gpib_addr)
        self.gpib.socket.recv(1024)
        self.gpib.write('*RST')
        time.sleep(1)

        assert 'E4418B' in self.gpib.query('*IDN?')
        assert 'DBM' in self.gpib.query('UNIT:POW?')

    def zero_meter(self):
        # zero the E4418B
        self.gpib.select(self.gpib_addr)
        self.gpib.write('CALIBRATION:ZERO:AUTO ONCE')
        time.sleep(5)
        assert 'E4418B' in self.gpib.query('*IDN?')

    def cal_meter(self, zero = True):
        self.gpib.select(self.gpib_addr)

        if zero:
            raw_input("disconnect the power sensor head then press enter to continue")
            self.zero_meter()

        raw_input("connect the power sensor head to the cal port then press enter to continue")
        self.gpib.select(self.gpib_addr)
        self.gpib.write('CALIBRATION:AUTO ONCE')
        time.sleep(5)
        assert 'E4418B' in self.gpib.query('*IDN?')
        print("calibration complete")

    def read_power(self, freq = 50e6):
        self.gpib.select(self.gpib_addr)
        self.gpib.write('SENS:FREQ {}HZ'.format(str(int(freq))))
        f_readback = float(self.gpib.query('SENS:FREQ?'))
        assert f_readback == freq 
        self.gpib.write('INIT1;*WAI')
        time.sleep(1) # TODO: come up with a better way of doing this..
        return float(self.gpib.query('FETC1?'))


if __name__ == '__main__':
    e4418b = AgilentE4418B()
    #e4418b.cal_meter(zero = False)

    print(e4418b.read_power(freq = 10e9))
