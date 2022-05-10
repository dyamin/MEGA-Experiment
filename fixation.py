# ===============
# Import modules
# ===============
from __future__ import division

import os  # for file/folder operations

import numpy as np
import numpy.random as rnd  # for random number generators
from psychopy import visual, event, core, gui, data

import eyelink_functions
import feedback

# ==============================================
# PARAMETERS
# ==============================================
eyelink_on = 1
get_subject_info = 1
feedback_on = 1

datapath = 'data_fixation'  # directory to save data in
movpath = 'movies'  # directory where images can be found
sfx = 'p.mp4'  # suffix for the movies
num_movies = 3  # not including end
end_movie_num = 103
movlist = np.linspace(1, num_movies, num=num_movies, dtype=int)  # image names without the suffixes
scrsize = (1920, 1080)  # screen size in pixels
# scrsize = (800,600)                # screen size in pixels

edfFileName = 'eyelinkfile.edf'

# ========================================
# Store info about the experiment session
# ========================================

# Get subject name, gender, age, handedness through a dialog box
exp_name = 'eye tracking memory'

exp_info = {
    'participant': '',
    'edfFileName': '',
    'gender': ('male', 'female'),
    'session': ('1st', '2nd'),
    'age': '',
    'left-handed': False
}
if get_subject_info:
    dlg = gui.DlgFromDict(dictionary=exp_info, title=exp_name)
    # If 'Cancel' is pressed, quit
    edfFileName = exp_info['edfFileName']
    if dlg.OK == False:
        core.quit()

print(exp_info['session'])
if exp_info['session'] == '1st':
    movpath = 'movies_1'  # directory where images can be found
elif exp_info['session'] == '2nd':
    movpath = 'movies_2'  # directory where images can be found

# Get date and time
exp_info['date'] = data.getDateStr()
exp_info['exp_name'] = exp_name

# Create a unique filename for the experiment data
if not os.path.isdir(datapath):
    os.makedirs(datapath)
data_fname = exp_info['participant'] + '_' + exp_info['date']
data_fname = os.path.join(datapath, data_fname)

writer = feedback.set_feedback_file(data_fname, exp_info)

# ========================
# Prepare the trials
# ========================
# Check if all movies exist
for mov in movlist:
    num = str(mov).zfill(3)
    if (not os.path.exists(os.path.join(movpath, num + sfx))):
        raise Exception('movies files not found in movies folder: ' + num)

# Randomize the image order
rnd.shuffle(movlist)
movlist = np.append(movlist, end_movie_num)

# ==========================
# Define the trial sequence
# ==========================

# Define a list of trials with their properties:
#   - Which image (without the suffix)
#   - Which orientation
stim_order = []
for im, in zip(movlist):
    stim_order.append({'mov': mov})

trials = data.TrialHandler(stim_order, nReps=1, extraInfo=exp_info,
                           method='sequential', originPath=datapath)

# =====================
# intiate eyelink
# =====================
if eyelink_on:
    sp = (scrsize[0], scrsize[1])
    cd = 32
    el = eyelink_functions.eyeTrkInit(sp)
    el_version = el.getTrackerVersion()

    eyelink_functions.eyeTrkCalib(el, sp, cd)

    el.openDataFile(edfFileName)
# ===============================
# Creation of window and stimuli
#  ===============================
# Open a window
win = visual.Window(size=scrsize, color='black', units='pix', fullscr=True)
win.mouseVisible = False
# Define trial start text
start_message = visual.TextStim(win,
                                text="You will be watching short movies, \n "
                                     "after each movie please state whether you saw it before, press 1 if you saw it and 2 if you didn't, \n "
                                     "Then you will be asked to rate your confidence level between 1-4 : \n "
                                     "1= not confident , 4= very confident. \n \n"
                                     "press spacebar to continue",
                                color='white', height=None, alignHoriz='center', alignVert='center', antialias=False)

# brk_message="break, please close your eyes and "

end_message = visual.TextStim(win, text="Thank you, please wait",
                              color='white', height=20)
# ===============================
# start the experiment
#  ===============================

trl_clock = core.Clock()
# Display trial start text
start_message.draw()

win.mouseVisible = False  # make cursor invisible

win.flip()
# Wait for a spacebar press to start the trial, or escape to quit
keys = event.waitKeys(keyList=['space', 'escape'])

# load fake movie
movie_fname = movpath + '/' + "dummyMov.mp4"
movieDum = visual.MovieStim3(win, movie_fname, flipVert=False, size=scrsize, flipHoriz=False, loop=False)
core.wait(1)
movieDum.draw()
win.flip()
win.flip()

n = 0
if 'space' in keys:
    if eyelink_on:
        el.startRecording(1, 1, 1, 1)
    for i in np.arange(0, len(movlist)):
        n += 1
        win.flip()
        trl_clock.reset()
        # Empty the keypresses list
        event.getKeys()
        # Set the movie:
        num = str(movlist[i]).zfill(3)
        movie_fname = movpath + '/' + num + str(sfx)
        tag = str(movlist[i])
        movie = visual.MovieStim3(win, movie_fname, flipVert=False, size=scrsize, flipHoriz=False, loop=False)

        core.wait(2 - trl_clock.getTime())

        movie.draw()
        trl_clock.reset()

        if eyelink_on:
            el.sendMessage("tagstrt " + tag)

        while trl_clock.getTime() < movie.duration:
            # el.sendMessage("mov"+tag +" flip" +str(n))
            win.flip()
            movie.draw()
        if eyelink_on:
            el.sendMessage("tagfin " + tag)
        keys = event.getKeys('escape')
        win.flip()
        # print("movie n" + str(n) +" played" )
        if 'escape' in keys:
            # Escape press = quit the experiment
            break
        # movie=None
        if (feedback_on and movlist[i] < end_movie_num):
            feedback.ask_feedback(win, movie_fname, data_fname)
# Advance to the next trial

# =====================
# End of the experiment
# ======================
end_message.draw()
win.flip()

# close eyelink
if eyelink_on:
    el.setOfflineMode()
    core.wait(0.5)
    el.closeDataFile()
    el.receiveDataFile(edfFileName, edfFileName)
    el.close()

# Save all data to a file
trials.saveAsWideText(data_fname + '.csv', delim=',')

# Quit the experiment
keys = event.waitKeys(keyList=['space', 'escape'])
if 'space' in keys:
    win.close()
    core.quit()
