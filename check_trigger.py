from psychopy import visual, event, core, gui, data, parallel
import time

para_port = parallel.ParallelPort(address=0x0378) #uses psychopy.parallel to interact with NS
para_port.setData(0) # zeros the port
#
# para_port.setData(122)  # start experiment code is 122
# time.sleep(0.1)
# para_port.setData(0)

for r in range(1,9):
    print(2**r)
    para_port.setData(2**r)  # start experiment code is 122
    time.sleep(0.1)
    para_port.setData(0)  # start experiment code is 122

    time.sleep(2)
