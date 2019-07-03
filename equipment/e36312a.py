import ivi
# control an E36312A (in E3631 mode)

class E36312A:
    def __init__(self):
        self.psu = ivi.rigol.rigolDP832("TCPIP0::192.168.1.102::INSTR")

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
    psu = E36312A()
    psu.set_voltage(0, 5)
    psu.set_current(0, .01)
    psu.enable_output(0)
    print(psu.get_voltage(0))
    print(psu.get_current(0))

