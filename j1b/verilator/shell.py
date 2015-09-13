import sys
from datetime import datetime
import time
import array
import struct
import os

sys.path.append("build/lib/python/")
import vsimj1b

sys.path.append("../../shell")
import swapforth

class TetheredJ1b(swapforth.TetheredTarget):
    cellsize = 4

    def open_ser(self, port, speed):
        self.ser = vsimj1b.vsimj1b()

    def reset(self):
        ser = self.ser
        ser.reset()
        for c in '    1 tth !':
            ser.write(c)
        ser.write('\r')

        while 1:
            c = ser.read(1)
            print repr(c)
            if c == chr(30):
                break

    def boot(self, bootfile = None):
        sys.stdout.write('Contacting... ')
        self.reset()
        print 'established'

    def interrupt(self):
        self.reset()

    def serialize(self):
        l = self.command_response('0 here dump')
        lines = l.strip().replace('\r', '').split('\n')
        s = []
        for l in lines:
            l = l.split()
            s += [int(b, 16) for b in l[1:17]]
        s = array.array('B', s).tostring().ljust(32768, chr(0xff))
        return array.array('i', s)

if __name__ == '__main__':
    swapforth.main(TetheredJ1b)
