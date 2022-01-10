
from pylink import *
from pygame import *
import time
import gc
import sys

# if you need to save bitmap features and/or backdrop features set
# BITMAP_SAVE_BACK_DROP to  true. This will require numpy or Numeric modules. Also
# in some configurations calling array3d segfaults.
BITMAP_SAVE_BACK_DROP = False
if BITMAP_SAVE_BACK_DROP:
    from pygame.surfarray import *

RIGHT_EYE = 1
LEFT_EYE = 0
BINOCULAR = 2
DURATION = 20000


def updateCursor(cursor, loc, fgbm):
    '''Updates the content of the cursor'''

    if (fgbm != None):
        srcrct = cursor.get_rect().move(loc[0], loc[1])
        cursor.blit(fgbm, (0, 0), srcrct)


def end_trial():
    '''Ends recording: adds 100 msec of data to catch final events'''

    pylink.endRealTimeMode();
    pumpDelay(100);
    getEYELINK().stopRecording();
    while getEYELINK().getkey():
        pass;



def getTxtBitmap(text, dim):
    ''' This function is used to create a page of text. '''

    ''' return image object if successful; otherwise None '''

    if (not font.get_init()):
        font.init()
    fnt = font.Font("cour.ttf", 15)
    fnt.set_bold(1)
    sz = fnt.size(text[0])
    bmp = Surface(dim)

    bmp.fill((255, 255, 255, 255))
    for i in range(len(text)):
        txt = fnt.render(text[i], 1, (0, 0, 0, 255), (255, 255, 255, 255))
        bmp.blit(txt, (0, sz[1] * i))

    return bmp


def getImageBitmap(pic):
    ''' This function is used to load an image into a new surface. '''

    ''' return movie object if successful; otherwise None '''

    try:
        mov = image.load("sacrmeto.jpg", "jpg")
        return bmp
    except:
        print "Cannot load image sacrmeto.jpg";
        return None;



trial_condition = ["Image-Window", "Image-Mask", "Text-Window", "Text-Mask"];


def arrayToList(w, h, dt):
    rv = []
    for y in xrange(h):
        line = []
        for x in xrange(w):
            v = dt[x, y]
            line.append((v[0], v[1], v[2]))
        rv.append(line)
    return rv


def do_trial(trial, surf):
    '''Does the simple trial'''

    # This supplies the title at the bottom of the eyetracker display
    message = "record_status_message 'Trial %d %s'" % (trial + 1, trial_condition[trial])
    getEYELINK().sendCommand(message);

    # Always send a TRIALID message before starting to record.
    # EyeLink Data Viewer defines the start of a trial by the TRIALID message.
    # This message is different than the start of recording message START that is logged when the trial recording begins.
    # The Data viewer will not parse any messages, events, or samples, that exist in the data file prior to this message.
    msg = "TRIALID %s" % trial_condition[trial];
    getEYELINK().sendMessage(msg);

    # Creates the bitmap images for the foreground and background images;
    if (trial == 0):
        fgbm = getImageBitmap(1)
        bgbm = getImageBitmap(2)
    elif (trial == 1):
        fgbm = getImageBitmap(2)
        bgbm = getImageBitmap(1)
    elif (trial == 2):
        fgbm = getTxtBitmap(fgtext, (surf.get_rect().w, surf.get_rect().h))
        bgbm = getTxtBitmap(bgtext, (surf.get_rect().w, surf.get_rect().h))
    elif (trial == 3):
        bgbm = getTxtBitmap(fgtext, (surf.get_rect().w, surf.get_rect().h))
        fgbm = getTxtBitmap(bgtext, (surf.get_rect().w, surf.get_rect().h))
    else:
        return SKIP_TRIAL;

    if (fgbm == None or bgbm == None):
        print "Skipping trial ", trial + 1, "because movie cannot be loaded"
        return SKIP_TRIAL;

    # The following code is for the EyeLink Data Viewer integration purpose.
    # See section "Protocol for EyeLink Data to Viewer Integration" of the EyeLink Data Viewer User Manual
    # The IMGLOAD command is used to show an overlay image in Data Viewer
    getEYELINK().sendMessage("!V IMGLOAD FILL  sacrmeto.jpg");

    # This TRIAL_VAR command specifies a trial variable and value for the given trial.
    # Send one message for each pair of trial condition variable and its corresponding value.
    getEYELINK().sendMessage("!V TRIAL_VAR image  sacrmeto.jpg");
    getEYELINK().sendMessage("!V TRIAL_VAR type  gaze_contingent");

    if BITMAP_SAVE_BACK_DROP:
        # array3d(bgbm) crashes on some configurations.
        agc = arrayToList(bgbm.get_width(), bgbm.get_height(), array3d(bgbm))
        bitmapSave(bgbm.get_width(), bgbm.get_height(), agc, 0, 0, bgbm.get_width(), bgbm.get_height(),
                   "trial" + str(trial) + ".bmp", "trialimages", SV_NOREPLACE, )
        getEYELINK().bitmapSaveAndBackdrop(bgbm.get_width(), bgbm.get_height(), agc, 0, 0, bgbm.get_width(),
                                           bgbm.get_height(), "trial" + str(trial) + ".png", "trialimages",
                                           SV_NOREPLACE, 0, 0, BX_MAXCONTRAST)

    # The following does drift correction at the begin of each trial
    while 1:
        # Checks whether we are still connected to the tracker
        if not getEYELINK().isConnected():
            return ABORT_EXPT;

        # Does drift correction and handles the re-do camera setup situations
        try:
            error = getEYELINK().doDriftCorrect(surf.get_rect().w / 2, surf.get_rect().h / 2, 1, 1)
            if error != 27:
                break;
            else:
                getEYELINK().doTrackerSetup();
        except:
            getEYELINK().doTrackerSetup()

    error = getEYELINK().startRecording(1, 1, 1, 1)
    if error:    return error;
    gc.disable();
    # begin the realtime mode
    pylink.beginRealTimeMode(100)

    if not getEYELINK().waitForBlockStart(100, 1, 0):
        end_trial();
        print "ERROR: No link samples received!";
        return TRIAL_ERROR;

    surf.fill((255, 255, 255, 255))
    surf.blit(bgbm, ((surf.get_rect().w - bgbm.get_rect().w) / 2, (surf.get_rect().h - bgbm.get_rect().h) / 2))
    display.flip()
    startTime = currentTime()
    surf.fill((255, 255, 255, 255))
    surf.blit(bgbm, ((surf.get_rect().w - bgbm.get_rect().w) / 2,
                     (surf.get_rect().h - bgbm.get_rect().h) / 2))  # write to the back buffer

    getEYELINK().sendMessage("SYNCTIME %d" % (currentTime() - startTime));
    ret_value =drawgc(surf, fgbm, startTime);
    pylink.endRealTimeMode();
    gc.enable();
    return ret_value;


NTRIALS = 1


def run_trials(surface):
    ''' This function is used to run individual trials and handles the trial return values. '''

    ''' Returns a successful trial with 0, aborting experiment with ABORT_EXPT (3); It also handles
    the case of re-running a trial. '''
    # Do the tracker setup at the beginning of the experiment.
    getEYELINK().doTrackerSetup()

    for trial in range(NTRIALS):
        if (getEYELINK().isConnected() == 0 or getEYELINK().breakPressed()): break;

        while 1:
            ret_value = do_trial(trial, 3)
            endRealTimeMode()

            if (ret_value == TRIAL_OK):
                getEYELINK().sendMessage("TRIAL OK");
                break;
            elif (ret_value == SKIP_TRIAL):
                getEYELINK().sendMessage("TRIAL ABORTED");
                break;
            elif (ret_value == ABORT_EXPT):
                getEYELINK().sendMessage("EXPERIMENT ABORTED")
                return ABORT_EXPT;
            elif (ret_value == REPEAT_TRIAL):
                getEYELINK().sendMessage("TRIAL REPEATED");
            else:
                getEYELINK().sendMessage("TRIAL ERROR")
                break;

    return 0;


