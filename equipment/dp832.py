import ivi

class DP832:
    def __init__(self):
        self.psu = ivi.rigol.rigolDP832("TCPIP0::192.168.1.132::INSTR")

    def enable_output(self, channel):
        self.psu.outputs[channel].enabled = True

    def disable_output(self, channel):
        self.psu.outputs[channel].enabled = False

    def set_voltage(self, channel, voltage):
        self.psu.outputs[channel].voltage_level = voltage

    def set_current(self, channel, current):
        self.psu.outputs[channel].current_limit = current

    def get_voltage(self, channel):
        return self.psu.outputs[channel].measure("voltage")

    def get_current(self, channel):
        return self.psu.outputs[channel].measure("current")

if __name__ == '__main__':
    dp = DP832()
    dp.set_voltage(0, 5)
    dp.set_current(0, .01)
    dp.enable_output(0)
    print(dp.get_voltage(0))
    print(dp.get_current(0))

