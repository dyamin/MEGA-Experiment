import config
import eyelink_functions

sp = (config.scrsize[0], config.scrsize[1])
cd = 32
el = eyelink_functions.eyeTrkInit(sp)
el_version = el.getTrackerVersion()

eyelink_functions.eyeTrkCalib(el, sp, cd)
