# ===============
# Import modules
# ===============
import os  # for file/folder operations

import numpy as np
import numpy.random as rnd  # for random number generators
import pylink
from psychopy import visual, event, core, gui, data
from pygame import *
from pylink import *

# ==============================================
# PARAMETERS
# ==============================================

datapath = 'data'  # directory to save data in
movpath = 'movies'  # directory where images can be found
sfx = 'h.mp4'  # suffix for the movies
movies_num = 4;
movlist = np.linspace(1, movies_num, num=movies_num, dtype=int)  # image names without the suffixes
scrsize = (800, 600)  # screen size in pixels
get_subject_info = 0

# ========================================
# Store info about the experiment session
# ========================================

# Get subject name, gender, age, handedness through a dialog box
exp_name = 'eye tracking memory'

exp_info = {
    'participant': '',
    'edfFileName': '',
    'gender': ('male', 'female'),
    'age': '',
    'left-handed': False
}
if get_subject_info:
    dlg = gui.DlgFromDict(dictionary=exp_info, title=exp_name)
    # If 'Cancel' is pressed, quit
    if dlg.OK == False:
        core.quit()

# Get date and time
exp_info['date'] = data.getDateStr()
exp_info['exp_name'] = exp_name

# Create a unique filename for the experiment data
if not os.path.isdir(datapath):
    os.makedirs(datapath)
data_fname = exp_info['participant'] + '_' + exp_info['date']
data_fname = os.path.join(datapath, data_fname)

# ========================
# Prepare the trials
# ========================
# Check if all movies exist
for mov in movlist:
    if (not os.path.exists(os.path.join(movpath, str(mov) + sfx))):
        raise Exception('movies files not found in movies folder: ' + str(mov))

# Randomize the image order
rnd.shuffle(movlist)

# ===============================
# Creation of window and stimuli
#  ===============================

# Open a window
win = visual.Window(size=scrsize, color='black', units='pix', fullscr=False)

# Define trial start text
start_message = visual.TextStim(win,
                                text="Just watch the movies, hit spacebar to begin.",
                                color='white', height=20)

# ========================================
# Eyelink initialization
# ========================================
eyelinktracker = EyeLink()
# Here is the starting point of the experiment
# Initializes the graphics
display.init()
display.set_mode((800, 600), FULLSCREEN | DOUBLEBUF, 32)
pylink.openGraphics()

# Opens the EDF file.
if get_subject_info:
    edfFileName = exp_info['edfFileName']
else:
    edfFileName = "TEST.EDF"
getEYELINK().openDataFile(edfFileName)

pylink.flushGetkeyQueue()
getEYELINK().setOfflineMode()

# Gets the display surface and sends a mesage to EDF file;
# surf = display.get_surface() # I already created win using psychopy
getEYELINK().sendCommand("screen_pixel_coords =  0 0 %d %d" % (win.size[0], win.size[1]))
getEYELINK().sendMessage("DISPLAY_COORDS  0 0 %d %d" % (win.size[0], win.size[1]))

# getEYELINK().sendCommand("screen_pixel_coords =  0 0 %d %d" % (surf.get_rect().w, surf.get_rect().h))
# getEYELINK().sendMessage("DISPLAY_COORDS  0 0 %d %d" % (surf.get_rect().w, surf.get_rect().h))


tracker_software_ver = 0
eyelink_ver = getEYELINK().getTrackerVersion()
if eyelink_ver == 3:
    tvstr = getEYELINK().getTrackerVersionString()
    vindex = tvstr.find("EYELINK CL")
    tracker_software_ver = int(float(tvstr[(vindex + len("EYELINK CL")):].strip()))

if eyelink_ver >= 2:
    getEYELINK().sendCommand("select_parser_configuration 0")
    if eyelink_ver == 2:  # turn off scenelink camera stuff
        getEYELINK().sendCommand("scene_camera_gazemap = NO")
else:
    getEYELINK().sendCommand("saccade_velocity_threshold = 35")
    getEYELINK().sendCommand("saccade_acceleration_threshold = 9500")

# set EDF file contents
getEYELINK().sendCommand("file_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON")
if tracker_software_ver >= 4:
    getEYELINK().sendCommand("file_sample_data  = LEFT,RIGHT,GAZE,AREA,GAZERES,STATUS,HTARGET")
else:
    getEYELINK().sendCommand("file_sample_data  = LEFT,RIGHT,GAZE,AREA,GAZERES,STATUS")

# set link data (used for gaze cursor)
getEYELINK().sendCommand("link_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,BUTTON")
if tracker_software_ver >= 4:
    getEYELINK().sendCommand("link_sample_data  = LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS,HTARGET")
else:
    getEYELINK().sendCommand("link_sample_data  = LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS")

getEYELINK().sendCommand("button_function 5 'accept_target_fixation'");

pylink.setCalibrationColors((255, 255, 255), (0, 0, 0));  # Sets the calibration target and background color
pylink.setTargetSize(int(win.size[0] / 70), int(win.size[0] / 300))  # select best size for calibration target
pylink.setCalibrationSounds("", "", "")
pylink.setDriftCorrectSounds("", "off", "off")

if (getEYELINK().isConnected() and not getEYELINK().breakPressed()):
    win = visual.Window(size=scrsize, color='black', units='pix', fullscr=False)
    start_message.draw()

    win.flip()
    # Wait for a spacebar press to start the trial, or escape to quit
    keys = event.waitKeys(keyList=['space', 'escape'])
    if 'space' in keys:
        #################
        ##  try movie  ##
        #################
        # Set the movie:
        movie_fname = movpath + '/' + '1h.mp4' + str(sfx)
        movie = visual.MovieStim(win, movie_fname, flipVert=False, size=scrsize, flipHoriz=False, loop=False)
        core.wait(2)
        rt_clock.reset()

        # Start the trial
        while rt_clock.getTime() < movie.duration:
            keys = event.getKeys('escape')
            movie.draw()
            # Show the new screen we've drawn
            win.flip()
            if 'escape' in keys:
                # Escape press = quit the experiment
                break

        # movies_trials.run_trials(win)
#
if getEYELINK() != None:
    # File transfer and cleanup!
    getEYELINK().setOfflineMode();
    msecDelay(500);

    # Close the file and transfer it to Display PC
    getEYELINK().closeDataFile()
    getEYELINK().receiveDataFile(edfFileName, edfFileName)
    getEYELINK().close();

# Close the experiment graphics
pylink.closeGraphics()
display.quit()
