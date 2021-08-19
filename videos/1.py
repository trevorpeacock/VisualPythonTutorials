from manim import *
from manimcoder import *


class MovingFrameBox(Scene):
    def construct(self):
        rectangle1 = Rectangle(width=CANVAS_SIZE[0] - RIGHT_PANEL_WIDTH - 0.1, height=CANVAS_SIZE[1] - 0.1).shift(
            LEFT * RIGHT_PANEL_WIDTH / 2)
        rectangle2 = Rectangle(width=RIGHT_PANEL_WIDTH - 0.1, height=CANVAS_SIZE[1] * RIGHT_PANEL_RATIO - 0.1) \
            .shift(RIGHT * (CANVAS_SIZE[0] / 2 - RIGHT_PANEL_WIDTH / 2)).shift(
            UP * CANVAS_SIZE[1] * RIGHT_PANEL_RATIO / 2)
        rectangle3 = Rectangle(width=RIGHT_PANEL_WIDTH - 0.1, height=CANVAS_SIZE[1] * (1 - RIGHT_PANEL_RATIO) - 0.1) \
            .shift(RIGHT * (CANVAS_SIZE[0] / 2 - RIGHT_PANEL_WIDTH / 2)).shift(
            DOWN * CANVAS_SIZE[1] * RIGHT_PANEL_RATIO / 2)

        code1 = ProgramCode("""for i in range(4): # loop\n  print([1, 2, 3, 4])""")
        code1.align_to(rectangle1, LEFT).shift(RIGHT * 0.25)
        code1.align_to(rectangle1, UP).shift(DOWN * 0.25)
        code2 = Text("""for i in range(4): # loop\n  print([1, 2, 3, 4], "asdf")""", font="FreeMono")
        code2.align_to(rectangle1, LEFT).shift(RIGHT * 0.25)
        code2.align_to(rectangle1, UP).shift(DOWN * 0.25)

        self.play(
            AnimationGroup(Create(rectangle1), Create(rectangle2), Create(rectangle3), code1.changes(), lag_ratio=0.25))

        for _ in range(2):
            self.wait(1)
            code1.insert_line(1, '  print("asdf")')
            self.play(code1.changes())
            self.wait(1)
            code1.replace(0, 'range(4)', '[0, 1, 2, 3]')
            self.play(code1.changes())
            code1.replace(0, ']:', 'x')
            self.play(code1.changes())
            code1.replace(0, 'for i', 'x')
            code1.replace(0, '0, 1, 2, 3', 'x')
            self.play(code1.changes())
            code1.replace(1, 'asdf', '')
            self.play(code1.changes())
            code1.insert(1, 9, 'asdf')
            #code1.replace(1, '""', '"asdf"')
            self.play(code1.changes())
            code1.replace(0, 'x', 'for i')
            code1.replace(0, '[xx', 'range(4):')
            self.play(code1.changes())
            code1.remove_line(1)
            self.play(code1.changes())

        # self.play(AnimationGroup(ReplacementTransform(code1, code2), run_time=0))
        # self.play(ReplacementTransform(text2, text3))
        # self.play(ReplacementTransform(text3, text4))
        # self.play(ReplacementTransform(text4, text5))
        self.wait(2)
