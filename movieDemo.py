
# Demo of MovieStim
# Different systems have different sets of codecs.
#avbin (which PsychoPy uses to load movies) seems not to load compressed audio on all systems.
# To create a movie that will play on all systems I would recommend using the format:
    #video: H.264 compressed,
    #audio: Linear PCM


from __future__ import division

from psychopy import visual, core, event

win = visual.Window((800, 600))
mov = visual.MovieStim(win, 'movies/75h.mp4', size=(600, 400),
    flipVert=False, flipHoriz=False, loop=False)


print('orig movie size=%s' % mov.size)
print('duration=%.2fs' % mov.duration)
globalClock = core.Clock()

while mov.status != visual.FINISHED:
    mov.draw()
    win.flip()
    if event.getKeys():
        break

win.close()
core.quit()