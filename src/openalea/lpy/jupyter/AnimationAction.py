import ipywidgets as widgets


def ipyplot(lsystem):
    play = widgets.Play(
        value=50,
        min=0,
        max=100,
        step=1,
        interval=500,
        description="Press play",
        disabled=False
    )


import asyncio

class Timer:
    def __init__(self, timeout, callback):
        self._timeout = timeout
        self._callback = callback
        self._task = asyncio.ensure_future(self._job())

    async def _job(self):
        await asyncio.sleep(self._timeout)
        self._callback()

    def cancel(self):
        self._task.cancel()

def debounce(wait):
    """ Decorator that will postpone a function's
        execution until after `wait` seconds
        have elapsed since the last time it was invoked. """
    def decorator(fn):
        timer = None
        def debounced(*args, **kwargs):
            nonlocal timer
            def call_it():
                fn(*args, **kwargs)
            if timer is not None:
                timer.cancel()
            timer = Timer(wait, call_it)
        return debounced
    return decorator    

class AnimationBase:
    def __init__(self):
        self.rewindButton = widgets.Button(
            disabled=False,
            tooltip='Rewind',
            icon='fa-backward' # (FontAwesome names without the `fa-` prefix)
        )

        self.playButton = widgets.Button(
            disabled=False,
            tooltip='Play',
            icon='fa-play' 
        )

        self.stepButton = widgets.Button(
            disabled=False,
            tooltip='Step',
            icon='fa-step-forward' 
        )

        self.runButton = widgets.Button(
            disabled=False,
            tooltip='Run',
            icon='fa-fast-forward' 
        )

        self.pauseButton = widgets.Button(
            disabled=False,
            tooltip='Pause',
            icon='fa-pause' 
        )

        self.layout = widgets.HBox([self.rewindButton, 
                                    self.playButton, 
                                    self.stepButton, 
                                    self.runButton, 
                                    self.pauseButton])
        self.output = widgets.Output()

        self.playButton.on_click(self._play)
        self.rewindButton.on_click(self._rewind)
        self.stepButton.on_click(self._step)
        self.runButton.on_click(self._run)
        self.pauseButton.on_click(self._pause)
        display(self.layout, self.output)

    def _play(self, b): self.play()
    def _step(self, b): self.step()
    def _rewind(self, b): self.rewind()
    def _run(self, b): self.run()
    def _pause(self, b): self.pause()

    def play(self):
        pass

    def rewind(self):
        pass

    def step(self):
        pass

    def run(self):
        pass

    def pause(self):
        pass

from openalea.lpy import Lsystem
from openalea.plantgl.algo.view import perspectiveimage
import matplotlib.pyplot as plt
from IPython.display import Image, display, clear_output

class LpyAnimation (AnimationBase):
    def __init__(self, code):
        AnimationBase.__init__(self)
        self.code = code
        self.rewind()

    def plot(self, lstring):
        scene = self.lsystem.sceneInterpretation(lstring)
        image = perspectiveimage(scene)
        if not image is None:
            with self.output:
                widgets.interaction.show_inline_matplotlib_plots()
                self.output.clear_output(True)
                fig, ax = plt.subplots(figsize=(9, 9))
                img = ax.imshow(image)
                widgets.interaction.show_inline_matplotlib_plots()
                self.output.append_display_data(img)

    def play(self):
        for i in range(self.lsystem.derivationLength):
            self.lstring = self.lsystem.derive(self.lstring,i,1)
            self.plot(self.lstring)

    def rewind(self):
        self.lsystem = Lsystem()
        self.lsystem.setCode(self.code)
        self.lstring = self.lsystem.axiom
        self.plot(self.lstring)

    def step(self):
        self.lstring = self.lsystem.derive(self.lstring, 1)
        self.plot(self.lstring)

    def run(self):
        self.lstring = self.lsystem.derive()
        self.plot(self.lstring)

    def pause(self):
        pass

class LpyStringAnimation (AnimationBase):
    def __init__(self, code):
        AnimationBase.__init__(self)
        self.code = code
        self.rewind()
        print('init')

    def plot(self, lstring):
        display(str(lstring))

    def play(self):
        print('play')
        for i in range(self.lsystem.derivationLength):
            self.lstring = self.lsystem.derive(self.lstring,i,1)
            self.plot(self.lstring)

    def rewind(self):
        self.lsystem = Lsystem()
        self.lsystem.setCode(self.code)
        self.lstring = self.lsystem.axiom
        self.plot(self.lstring)

    def step(self):
        print('step')
        self.lstring = self.lsystem.derive(self.lstring, 1)
        self.plot(self.lstring)

    def run(self):
        self.lstring = self.lsystem.derive()
        self.plot(self.lstring)

    def pause(self):
        pass