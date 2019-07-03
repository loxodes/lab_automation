# script to measure insertion loss with a power meter and signal generator
from pylab import *
from plx_gpib_ethernet import PrologixGPIBEthernet
import argparse
import pdb

from equipment.gigatronics_2520a import Gigatronics2520A
from equipment.agilent_e4418b import AgilentE4418B

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='scalar network analyzer')

    parser.add_argument('--cal', default = False, help='specify name of calibration file')
    parser.add_argument('--ddir', default = './data/', help='specify name of calibration file')
    parser.add_argument('filename', help='specify name of output file') 

    args = parser.parse_args()


    prologix = PrologixGPIBEthernet('192.168.1.128', timeout = 10)
    prologix.connect()
    meter = AgilentE4418B(prologix = prologix)
    synth = Gigatronics2520A(prologix = prologix)

    freqs = np.arange(1e9, 20.1e9, .25e9)

    synth.set_cw_power(0)
    synth.output_on()
    
    meas = np.empty_like(freqs)

    for (i,f) in enumerate(freqs):
        synth.set_cw_frequency(f)
        meas[i] = meter.read_power(f)
        print('f: {}, p: {}'.format(f/1e9, meas[i]))
   
    cal = False


    with open(args.ddir + args.filename, 'w') as datafile:
        if args.cal:
            with open(args.ddir + args.cal) as calfile:
                cal = np.load(calfile)
                assert np.array_equal(cal['frequencies'], freqs)
                meas -= cal['power']


        np.savez(datafile, frequencies=freqs, power=meas, calfile=args.cal)
    
    plt.plot(freqs, meas)
    plt.savefig('sweep.png') 

    synth.output_off()

    

