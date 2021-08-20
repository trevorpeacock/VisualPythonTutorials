from manim import *
from manimcoder import *

class MovingFrameBox(Scene):
    def construct(self):
        program = CodeDisplay()
        code = ProgramCode("""for i in range(4): # loop\n  print([1, 2, 3, 4])""", program.panel_side.panel_top.title_bar)
        #code.align_to(program.panel_side.panel_top.title_bar, LEFT).align_to(program.panel_side.panel_top.title_bar, UP)
        #code.add_updater(lambda d: d.align_to(program.panel_side.panel_top.title_bar, LEFT).align_to(program.panel_side.panel_top.title_bar, UP))


        self.play(Create(program), code.changes())
        self.wait(1)
        #program.program.rectangle.stretch_to_fit_width(5, about_edge=LEFT)
        #self.play(ApplyMethod(program.program.rectangle.stretch_to_fit_width, 5, {'about_edge':LEFT}))
        self.play(ApplyMethod(program.set_panels, PANEL_CODE))
        self.wait(0.5)
        self.play(ApplyMethod(program.set_panels, PANEL_CODE+PANEL_VARS))
        self.wait(0.5)
        self.play(ApplyMethod(program.set_panels, PANEL_CODE+PANEL_VARS+PANEL_TRACE))
        self.wait(0.5)
        self.play(ApplyMethod(program.set_panels, PANEL_CODE+PANEL_VARS+PANEL_TRACE+PANEL_OUTPUT))
        self.wait(0.5)
        self.play(ApplyMethod(program.set_panels, PANEL_CODE))
        self.wait(2)
