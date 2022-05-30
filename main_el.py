# ===============
# Import modules
# ===============
from __future__ import division

import os  # for file/folder operations
import time

import numpy as np
import numpy.random as rnd  # for random number generators
from psychopy import visual, event, core, gui, data, parallel, prefs

import config
import eyelink_functions
import feedback

prefs.hardware['audioLib'] = ['PTB', 'sounddevice', 'pyo', 'pygame']  # change this with blckrok
movpath = 'metroMovies_coded'  # directory where images can be found
movlist = np.linspace(1, config.num_movies, num=config.num_movies, dtype=int)  # image names without the suffixes
folder_laptop = r'C:\Users\Daniel Yamin\Documents\moviesExperiment_230121'
os.chdir(folder_laptop)

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
if config.get_subject_info:
    dlg = gui.DlgFromDict(dictionary=exp_info, title=exp_name)
    # If 'Cancel' is pressed, quit
    edfFileName = exp_info['edfFileName']
    if dlg.OK == False:
        core.quit()

print(exp_info['session'])
if exp_info['session'] == '1st':
    movpath = 'metroMovies1_coded'  # directory where images can be found
    # movpath = 'metroMovies'  # directory where images can be found

elif exp_info['session'] == '2nd':
    movpath = 'metroMovies2_coded'  # directory where images can be found

# Get date and time
exp_info['date'] = data.getDateStr()
exp_info['exp_name'] = exp_name

# Create a unique filename for the experiment data
if not os.path.isdir(config.datapath):
    os.makedirs(config.datapath)
data_fname = exp_info['participant'] + '_' + exp_info['date']
data_fname = os.path.join(config.datapath, data_fname)

writer = feedback.set_feedback_file(data_fname, exp_info)

# ========================
# Prepare the trials
# ========================
# Check if all movies exist
for mov in movlist:
    num = str(mov).zfill(3)
    if not os.path.exists(os.path.join(movpath, num + config.sfx)):
        print(os.path.exists(os.path.join(movpath, num + config.sfx)))

        raise Exception('movies files not found in movies folder: ' + num)

# Randomize the image order
rnd.shuffle(movlist)  # Took it for debugging
movlist = np.append(movlist, config.end_movie_num)  # add the "end" movie

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
                           method='sequential', originPath=config.datapath)

# =====================
# intiate eyelink
# =====================
if config.eyelink_on:
    sp = (config.scrsize[0], config.scrsize[1])
    cd = 32
    el = eyelink_functions.eyeTrkInit(sp)
    el_version = el.getTrackerVersion()
    eyelink_functions.eyeTrkCalib(el, sp, cd)
    print(edfFileName)
    el.openDataFile(edfFileName)

if config.eeg_on:
    para_port = parallel.ParallelPort(address=0x0378)  # uses psychopy.parallel to interact with NS
    para_port.setData(0)  # zeros the port
# ===============================
# Creation of window and stimuli
# ===============================
# Open a window
win = visual.Window(size=config.scrsize, color='grey', units='pix', fullscr=config.full_screen)
win.mouseVisible = False
# Define trial start text
start_message = visual.TextStim(win, text=config.first_msg_eng,
                                color='black', height=30, alignText='center', antialias=False)

end_message = visual.TextStim(win, text="Thank you, please wait",
                              color='black', height=80)
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
movieDum = visual.MovieStim3(win, movie_fname, flipVert=False, size=config.scrsize, flipHoriz=False, loop=False)
core.wait(1)
movieDum.draw()
win.flip()
win.flip()

n = 0
if 'space' in keys:
    if config.eyelink_on:
        el.startRecording(1, 1, 1, 1)
    if config.eeg_on:
        para_port.setData(122)  # start experiment code is 122
        time.sleep(0.1)
        para_port.setData(0)
    for i in np.arange(0, len(movlist)):
        n += 1
        win.flip()
        trl_clock.reset()
        # Empty the keypresses list
        event.getKeys()
        # Set the movie:
        num = str(movlist[i]).zfill(3)
        movie_fname = movpath + '/' + num + str(config.sfx)
        tag = str(movlist[i])
        movie = visual.MovieStim3(win, movie_fname, flipVert=False, size=config.scrsize, flipHoriz=False, loop=False)

        core.wait(2 - trl_clock.getTime())

        movie.draw()
        trl_clock.reset()

        if config.eyelink_on:
            el.sendMessage("tagstrt " + tag)
        if config.eeg_on:
            print(movlist[i])
            para_port.setData(int(movlist[i]))  # begin trial experiment with the number of the movie
            time.sleep(0.1)
            para_port.setData(0)

        while trl_clock.getTime() < movie.duration:
            # el.sendMessage("mov"+tag +" flip" +str(n))
            win.flip()
            movie.draw()
        if config.eyelink_on:
            el.sendMessage("tagfin " + tag)
        if config.eeg_on:
            para_port.setData(255)  # end trial experiment code is 254
            time.sleep(0.1)
            para_port.setData(0)

        keys = event.getKeys('escape')
        win.flip()

        # print("movie n" + str(n) +" played" )
        if 'escape' in keys:
            # Escape press = quit the experiment
            break
        # movie=None
        if config.feedback_on and movlist[i] < 103:
            feedback.ask_feedback(win, movie_fname, data_fname)
# Advance to the next trial

# =====================
# End of the experiment
# ======================
end_message.draw()
win.flip()

# close eyelink
if config.eyelink_on:
    el.setOfflineMode()
    core.wait(0.5)
    el.closeDataFile()
    el.receiveDataFile(edfFileName, edfFileName)
    el.close()
if config.eeg_on:
    para_port.setData(222)  # end experiment code is 222
    time.sleep(0.1)
    para_port.setData(0)

# Save all data to a file
trials.saveAsWideText(data_fname + '.csv', delim=',')

# Quit the experiment
keys = event.waitKeys(keyList=['space', 'escape', 'q'])
if 'space' or 'escape' or 'q' in keys:
    win.close()
    core.quit()
