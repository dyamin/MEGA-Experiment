import csv

from psychopy import visual, event

import config


def set_feedback_file(data_fname, exp_info):

    with open(data_fname + ".csv", 'w+') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([exp_info['participant']] + [exp_info['age']] + [exp_info['gender']] + [exp_info['date']])
        writer.writerow(['mov?'] + ['seen?'] + ['confidence?'])

    return writer


def ask_feedback(win, movie_fname, data_fname):
    # this function asks feedback and saves it to csv file
    if config.is_hebrew:
        message1 = visual.TextStim(win,
                               text=config.feedback_seen_msg_heb,  languageStyle='RTL',
                               color='black', height=80, alignText='center', antialias=False)
    else:
        message1 = visual.TextStim(win,
                               text=config.feedback_seen_msg_eng,
                               color='black', height=80, alignText='center', antialias=False)
    message1.draw()
    win.flip()

    keys1 = []
    while not keys1:
        keys1 = event.getKeys(keyList=['1', '2', 'num_1', 'num_2'])

    if config.is_hebrew:
        message2 = visual.TextStim(win,
                               text=config.feedback_confidence_msg_heb,  languageStyle='RTL',
                               color='black', height=60, alignText='center', antialias=False)
    else:
        message2 = visual.TextStim(win,
                                   text=config.feedback_confidence_msg_eng,
                                   color='black', height=60, alignText='center', antialias=False)

    message2.draw()
    win.flip()
    keys2 = []
    while not keys2:
        keys2 = event.getKeys(keyList=['1', '2', '3', '4', 'num_1', 'num_2', 'num_3', 'num_4'])

    if '1' or '2' or '3' or '4' or 'num_1' or 'num_2' or 'num_3' or 'num_4' in keys2:
        with open(data_fname + ".csv", 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([movie_fname] + [keys1] + [keys2])
