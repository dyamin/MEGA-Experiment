import eyelink_functions

scrsize = (1920, 1080)  # screen size in pixels
sp = (scrsize[0], scrsize[1])
cd = 32
el = eyelink_functions.eyeTrkInit(sp)
el_version = el.getTrackerVersion()

eyelink_functions.eyeTrkCalib(el, sp, cd)
