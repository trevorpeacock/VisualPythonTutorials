from manim import *
from manimcoder import *

class CircleWithContent(VGroup):
    def __init__(self):
        super().__init__()
        self.circle = Circle()
        self.content = Text("hello!")
        self.add(self.circle)
        self.add(self.content)
        self.content.add_updater(lambda d: d.align_to(self.circle.get_center(), UP+LEFT))
        #content.align_to(self.circle.get_center(), UP+LEFT)

    def clear_content(self):
        self.remove(self.content)
        self.content = None



class MovingFrameBox(Scene):
    def construct(self):
        if False:
            program = CodeDisplayWindow()
            self.play(Create(program))
            self.play(ApplyMethod(program.set_height, 5))
            self.play(ApplyMethod(program.stretch_to_fit_width, 5, {'about_edge': LEFT}))
            self.play(Uncreate(program))

        if False:
            program = CodeDisplayWindowColumn()
            program.show_second_panel(True)
            program.set_width(10)
            program.shift(RIGHT)
            self.play(Create(program))
            #self.play(ApplyMethod(program.show_second_panel, False))
            self.play(ApplyMethod(program.show_second_panel, True))
            self.play(ApplyMethod(program.set_width, 5))
            program2 = CodeDisplayWindowColumn()
            program2.show_second_panel(True)
            program2.next_to(program, RIGHT, buff=0.1).align_to(program, UP)
            program2.set_width(5)
            self.play(Create(program2))
            self.play(Uncreate(program))

        if False:
            program = CodeDisplayWindowColumn()
            #program2 = CodeDisplayWindowColumn()

            program.show_second_panel(1)
            program.set_width(5)
            #program2.set_width(5)
            #program2.next_to(program, RIGHT, buff=0.1).align_to(program, UP)
            #program2.show_second_panel(1)

            self.play(
                Create(program),
            #    Create(program2),
            )
            self.wait()
            self.play(Uncreate(program))

        if False:
            program = CodeDisplay()
            program.set_panels(PANEL_CODE+PANEL_VARS+PANEL_TRACE+PANEL_OUTPUT)
            self.play(Create(program))
            self.wait()
            self.play(ApplyMethod(program.set_panels, PANEL_CODE))
            self.play(ApplyMethod(program.set_panels, PANEL_CODE+PANEL_VARS+PANEL_TRACE+PANEL_OUTPUT))
            self.wait()
            self.play(ApplyMethod(program.panel_side.set_width, 5))
            self.play(Uncreate(program))

        if False:
            program = CodeDisplay()
            self.play(Create(program))
            self.wait()
            self.play(ApplyMethod(program.set_panels, PANEL_CODE+PANEL_VARS+PANEL_TRACE+PANEL_OUTPUT))
            self.play(ApplyMethod(program.set_panels, PANEL_CODE))
            self.wait()
            self.play(Uncreate(program))

        if True:
            program = CodeDisplay()
            program.set_panels(PANEL_CODE+PANEL_VARS+PANEL_TRACE+PANEL_OUTPUT)
            self.play(Create(program))
            self.play(ApplyMethod(program.set_side_panel_width, 7))
            self.play(
                ApplyMethod(program.panel_main.set_bottom_panel_height, 6),
                ApplyMethod(program.panel_side.set_bottom_panel_height, 4),
            )
            self.play(
                ApplyMethod(program.panel_main.set_bottom_panel_height, 1),
                ApplyMethod(program.panel_side.set_bottom_panel_height, 2),
            )
            self.play(Uncreate(program))

        return
        program = CodeDisplayWindowColumn()
        #program.stretch_to_fit_width(8, about_edge=LEFT)
        program.show_second_panel(True)
        #program.set_panels(PANEL_CODE + PANEL_VARS + PANEL_TRACE + PANEL_OUTPUT)
        #code = ProgramCode("""for i in range(4): # loop\n  print([1, 2, 3, 4])""", 'python')
        #code.align_to(program.panel_side.panel_top.title_bar, LEFT).align_to(program.panel_side.panel_top.title_bar, UP)
        #code.add_updater(lambda d: d.align_to(program.panel_side.panel_top.title_bar, DOWN+LEFT).shift(0.1 * (DOWN+RIGHT)))

        if False:
            d = Circle()
            my_mobject = Text("hello!")
            my_mobject.add_updater(lambda d: d.align_to(d.get_center(), UP+LEFT))
            self.play(Create(d), Create(my_mobject))
            self.wait()
            self.play(ApplyMethod(d.shift, DOWN*3))
            self.play(ApplyMethod(d.shift, UP*3))
            self.wait()
            #self.play(my_mobject.animate.clear_content())
            self.wait()
            return

        self.play(Create(program))
        #self.play(Create(code))
        self.wait()
        self.play(ApplyMethod(program.show_second_panel, False))
        self.wait(1)
        self.play(ApplyMethod(program.show_second_panel, True))
        self.wait(1)
        self.play(Uncreate(program))
        self.wait(1)
        return
        #program.program.rectangle.stretch_to_fit_width(5, about_edge=LEFT)
        #self.play(ApplyMethod(program.program.rectangle.stretch_to_fit_width, 5, {'about_edge':LEFT}))
        self.play(ApplyMethod(program.set_panels, PANEL_CODE))
        self.wait(0.5)
        self.play(ApplyMethod(program.set_panels, PANEL_CODE+PANEL_VARS))
        self.wait(0.5)
        self.play(code.changes())
        self.wait(0.5)
        self.play(ApplyMethod(program.set_panels, PANEL_CODE+PANEL_VARS+PANEL_TRACE))
        self.wait(0.5)
        self.play(ApplyMethod(program.set_panels, PANEL_CODE+PANEL_VARS+PANEL_TRACE+PANEL_OUTPUT))
        self.wait(0.5)
        self.play(ApplyMethod(program.set_panels, PANEL_CODE))
        self.wait(2)
