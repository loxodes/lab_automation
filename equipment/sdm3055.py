import vxi11

class SDM3055:
    def __init__(self, ip = '192.168.1.155'):
        self.instr = vxi11.Instrument(ip)

        try:
            print(self.instr.ask("*IDN?"))
        except:
            print("connecting to instrument failed.. exiting")

    def get_voltage(self, acdc = 'DC'):
        return self.instr.ask('MEAS:VOLT:%s? AUTO' %acdc)

    def get_current(self, acdc = 'DC'):
        return self.instr.ask('MEAS:CURR:%s? AUTO' %acdc)


if __name__ == '__main__':
    sdm = SDM3055()
    print(sdm.get_voltage())

