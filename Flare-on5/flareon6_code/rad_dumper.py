#!/usr/bin/python3

import r2pipe
import time


r2 = r2pipe.open("magic_patched",flags=['-e','dbg.profile=magic_patched.rr2','-d']) #load file
r2.cmd('db 0x403b5a')

for a in range(1,667):
    r2.cmd('dc')
    time.sleep(.25)
    r2.cmd('s 0x605100')
    r2.cmd('wtf {}_run.txt 0x2500'.format(a))

r2.quit()
print('end')
