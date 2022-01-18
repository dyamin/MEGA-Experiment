# Demo of MovieStim
# Different systems have different sets of codecs.
# avbin (which PsychoPy uses to load movies) seems not to load compressed audio on all systems.
# To create a movie that will play on all systems I would recommend using the format:
# video: H.264 compressed,
# audio: Linear PCM


from __future__ import division

from psychopy import visual, core, event

win = visual.Window((800, 600))
keystext = 'next';
text = visual.TextStim(win, keystext, pos=(0, -250), units='pix')

globalClock = core.Clock()
for i in range(1, 75):
    print(i)
    file_name = 'movies/' + str(i) + 'h.mp4'
    mov = visual.MovieStim(win, file_name, size=(600, 400), flipVert=False, flipHoriz=False, loop=False)
    print('orig movie size=%s' % mov.name)
    print('duration=%.2fs' % mov.duration)

    # Start the movie stim by preparing it to play
    shouldflip = mov.play()
    clock = core.Clock()

    while mov.status != visual.FINISHED:
        if shouldflip:
            # Movie has already been drawn , so just draw text stim and flip
            text.draw()
            win.flip()

        shouldflip = mov.draw()
        win.flip()
        for key in event.getKeys():
            if key in ['escape', 'q']:
                win.close()
                core.quit()
            elif key in ['n', ]:
                break
            elif key in ['s', ]:
                acc = 1
            else:
                acc = 0
        break

    print(acc)
    text.draw()
    win.flip()

## move to next movie
win.close()
core.quit()
