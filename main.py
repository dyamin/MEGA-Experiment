# ===============
# Import modules
# ===============
from __future__ import division

import os  # for file/folder operations

import numpy as np
import numpy.random as rnd  # for random number generators
from psychopy import visual, event, core, gui, data

# ==============================================
# PARAMETERS
# ==============================================

datapath = 'data'  # directory to save data in
movpath = 'movies'  # directory where images can be found
sfx = 'h.mp4'  # suffix for the movies
movlist = np.linspace(1, 4, num=4, dtype=int)  # image names without the suffixes
scrsize = (800, 600)  # screen size in pixels
get_subject_info = 0

# ========================================
# Store info about the experiment session
# ========================================

# Get subject name, gender, age, handedness through a dialog box
exp_name = 'eye tracking memory'

exp_info = {
    'participant': '',
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
                                color='red', height=20)

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
# Start the experiment
# =====================
rt_clock = core.Clock()
change_clock = core.Clock()
# Display trial start text
start_message.draw()
win.flip()
# Wait for a spacebar press to start the trial, or escape to quit
keys = event.waitKeys(keyList=['space', 'escape'])
if 'space' in keys:
    for i in movlist:
        # Empty the keypresses list
        event.getKeys()
        win.flip()

        # Set the movie:
        print(i)
        movie_fname = movpath + '/' + str(movlist[i]) + str(sfx)
        print(movie_fname)
        movie = visual.MovieStim(win, movie_fname, flipVert=False, size=scrsize, flipHoriz=False, loop=False)
        core.wait(2)

        # Set the clocks to 0
        change_clock.reset()
        rt_clock.reset()

        # Start the trial
        # Stop trial if spacebar or escape has been pressed, or if 30s have passed
        # while movie.status != visual.FINISHED:
        while rt_clock.getTime() < movie.duration:
            keys = event.getKeys('escape')
            movie.draw()
            # Show the new screen we've drawn
            win.flip()
            if 'escape' in keys:
                # Escape press = quit the experiment
                break

        if 'escape' in keys:
            # Escape press = quit the experiment
            break
# Advance to the next trial

# =====================
# End of the experiment
# ======================


# Save all data to a file
trials.saveAsWideText(data_fname + '.csv', delim=',')
# Quit the experiment
win.close()
print('end experiment')
core.quit()
