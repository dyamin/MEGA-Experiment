import ctypes

# ==============================================
# PARAMETERS
# ==============================================

eyelink_on = 1
is_hebrew = 0
get_subject_info = 1
feedback_on = 1
eeg_on = 0
full_screen = True

datapath = 'data'  # directory to save data
sfx = 'p.mp4'  # suffix for the movies
num_movies = 64  # not including end
end_movie_num = 65


def get_screen_size():
    user32 = ctypes.windll.user32
    return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

# Screen size: 345mm, 195mm
# scrsize = get_screen_size()
# scrsize = (1536, 864)  # screen size in pixels
# scrsize = (1920, 1080)  # screen size in pixels
scrsize = (3840, 2160)  # screen size in pixels

edfFileName = 'OS'

first_msg_eng = "You will be watching short movies, \n " \
                "after each movie please state whether you saw it before, \n" \
                "press 1 if you saw it \n press 2 if you didn't, \n " \
                "Then you will be asked to rate your confidence level between 1-4 : \n " \
                "1= not confident , 4= very confident. \n \n" \
                "press spacebar to continue"

feedback_seen_msg_eng = "Have you seen this movie before? \n 1 =Yes  \n 2 = No"

feedback_seen_msg_heb = "האם ראית את\n" \
                        "הסרט לפני?\n" \
                        "1=כן 2=לא"

feedback_confidence_msg_eng = "How confident are you? \n "\
                              "not confident- 1 \n 2 \n 3 \n very confident-4."

feedback_confidence_msg_heb = "כמה אתה בטוח?\n" \
                              "1-לא בטוח\n" \
                              "4-בטוח מאוד"
