from plx_gpib_ethernet import PrologixGPIBEthernet
import pdb

# untested scraps to control a RS FSP series spectrum analyzer
# https://cdn.rohde-schwarz.com/pws/dl_downloads/dl_common_library/dl_manuals/gb_1/f/fsp_1/FSP_OpMa_en.pdf 
# mit license

GPIB_ADDR_FSP30 = "20"

class FSP30():
    def __init__(self, prologix = False, gpib_addr = GPIB_ADDR_FSP30):
        if not prologix:
            self.gpib = PrologixGPIBEthernet('192.168.1.128')
            self.gpib.connect()
        else:
            self.gpib = prologix

        self.gpib_addr = gpib_addr

        self.gpib.select(self.gpib_addr)
        self.preset()
        pdb.set_trace()
        assert 'FSP-30' in self.gpib.query('*IDN?')


    def read_peak(self):
        self.gpib.select(self.gpib_addr)

        self.gpib.write('INIT:IMM;*WAI')
        self.gpib.write('CALC:MARK:MAX')
        f = float(self.gpib.query('CALC:MARK:X?'))
        amp = float(self.gpib.query('CALC:MARK:Y?'))

        return {'freq':f,'amp':amp}

    def get_sweep(self):
        self.gpib.select(self.gpib_addr)
        self.gpib.write('FORM:DATA: REAL,32')
        self.gpib.write('INIT:IMM;*WAI')
        vals = self.gpib.query('TRACE? TRACE1')
        
        # this probably won't work, I need to read back the sweep size
        # see  FSP operator manual page 4.259 
        return vals

    def set_reflevel(self, reflevel):
        self.gpib.select(self.gpib_addr)

        # sets ref level, units of dBm
        self.gpib.write('DISP:WIND:TRAC:Y:SPAC LOG')
        self.gpib.write('DISP:WIND:TRAC:Y:RLEV ' + str(reflevel) + 'dBm') 
   
    def set_vrange(self, vrange):
        self.gpib.select(self.gpib_addr)
        self.gpib.write('DISP:WIND:TRAC:Y' + str(vdiv) + ' dB')
   
    def set_span(self, span, center, points):
        self.gpib.select(self.gpib_addr)
        self.gpib.write("SWE:TIME:AUTO ON")
        self.gpib.write("SENSe:SWEep:POINts " + str(points))
        self.gpib.write("SENSe:FREQuency:CENTer " + str(center)+'Hz')
        self.gpib.write("SENSe:FREQuency:SPAN " + str(span)+'Hz')
    
    def get_span(self):
        self.gpib.select(self.gpib_addr)
        points = int(self.gpib.query("SENSe:SWEep:POINts?"))
        center = float(self.gpib.query("SENSe:FREQuency:CENTer?"))
        span = float(self.gpib.query("SENSe:FREQuency:SPAN?"))
        return linspace(center - span / 2.0, center + span / 2.0, points) * 1e9
 
    def preset(self):
        self.gpib.select(self.gpib_addr)

        self.gpib.write('*RST')
        self.gpib.write('*CLS')
        self.gpib.write('INIT:CONT OFF')

    
def dbm_to_watt(p):
    return pow(10.0,p/10)/1000

# example usage: grabs and plots values from signal_analyzer with correct amplitude scaling
if __name__ == "__main__":
    fsp = FSP30()
    fsp.set_span(2e9, 5e9, 401)
    fsp.set_reflevel(20)
    print fsp.read_peak()

