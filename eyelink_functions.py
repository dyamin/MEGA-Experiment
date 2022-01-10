import psychopy
import pylink as pl


def eyeTrkInit(sp):
    el = pl.EyeLink()
    el.sendCommand("screen_pixel_coords = 0 0 %d %d" % sp)
    el.sendMessage("DISPLAY_COORDS  0 0 %d %d" % sp)

    if el.getTrackerVersion() == 3:
        tvstr = el.getTrackerVersionString()
        vindex = tvstr.find("EYELINK CL")
        tracker_software_ver = int(float(tvstr[(vindex + len("EYELINK CL")):].strip()))
        print(tracker_software_ver)

    el.sendCommand("select_parser_configuration 0")
    el.sendCommand("pupil_size_diameter = %s" % ("YES"))

    # not sure what this is
    el.sendCommand("link_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,BUTTON")
    # this for the file
    el.sendCommand("link_sample_data  = LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS,HTARGET")
    # not sure what this is
    el.sendCommand("button_function 5 'accept_target_fixation'");

    return (el)


def eyeTrkCalib(el, sp, cd):
    pl.pylink_c.openGraphics(sp, cd)
    pl.pylink_c.setCalibrationColors((255, 255, 255), (0, 0, 0))
    pl.pylink_c.setTargetSize(int(sp[0] / 70), int(sp[1] / 300))
    pl.pylink_c.setCalibrationSounds("", "", "")
    pl.pylink_c.setDriftCorrectSounds("", "off", "off")
    el.doTrackerSetup(el)
    pl.closeGraphics()
    # el.setOfflineMode()


def driftCor(el, sp, cd):
    blockLabel = psychopy.visual.TextStim(expWin, text="Press the space bar to begin drift correction", pos=[0, 0],
                                          color="white", bold=True, alignHoriz="center", height=0.5)
    notdone = True
    while notdone:
        blockLabel.draw()
        expWin.flip()
        if keyState[key.SPACE] == True:
            eyeTrkCalib(el, sp, cd)
            expWin.winHandle.activate()
            keyState[key.SPACE] = False
            notdone = False
