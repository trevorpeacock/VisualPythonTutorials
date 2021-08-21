from manim import *


CANVAS_SIZE = [8*16/9, 8]

RIGHT_PANEL_WIDTH = 5
RIGHT_PANEL_RATIO = 0.5

class MovingFrameBox2(Scene):
    def construct(self):
        rectangle = Dot(radius=0)

        # create text, characters spaced approprately
        text = Text("Microscope", font="Monospace")
        text.align_to(rectangle, LEFT + UP)

        #select characters
        part1 = text[0:3]
        part2 = text[3:5]
        part2.submobjects = list(reversed(part2.submobjects))
        part3 = text[5:10]

        #text.add_updater(lambda d: d.move_to(rectangle.get_center())) # has no effect

        #part1.add_updater(lambda d: d.move_to(rectangle.get_center())) #changes relative position of each text part
        #part2.add_updater(lambda d: d.move_to(rectangle.get_center()))
        #part3.add_updater(lambda d: d.move_to(rectangle.get_center()))

        #part1_rp = (rectangle.get_center() + LEFT * rectangle.width/2 + UP * rectangle.height/2) - part1.get_center()
        #part1.add_updater(lambda d: d.move_to((rectangle.get_center() + LEFT * rectangle.width/2 + UP * rectangle.height/2) - part1_rp))
        #part2_rp = (rectangle.get_center() + LEFT * rectangle.width/2 + UP * rectangle.height/2) - part2.get_center()
        #part2.add_updater(lambda d: d.move_to((rectangle.get_center() + LEFT * rectangle.width/2 + UP * rectangle.height/2) - part2_rp))
        #part3_rp = (rectangle.get_center() + LEFT * rectangle.width/2 + UP * rectangle.height/2) - part3.get_center()
        #part3.add_updater(lambda d: d.move_to((rectangle.get_center() + LEFT * rectangle.width/2 + UP * rectangle.height/2) - part3_rp))

        part1_rp = rectangle.get_center() - part1.get_center()
        part1.add_updater(lambda d: d.move_to(rectangle.get_center() - part1_rp))
        part2_rp = rectangle.get_center() - part2.get_center()
        part2.add_updater(lambda d: d.move_to(rectangle.get_center() - part2_rp))
        part3_rp = rectangle.get_center() - part3.get_center()
        part3.add_updater(lambda d: d.move_to(rectangle.get_center() - part3_rp))

        #self.play(Create(text)) #This won't do what we want, we want to animate different characters seperately

        self.play(Create(rectangle))
        self.play(AnimationGroup(Create(part1), Create(part2), Create(part3), lag_ratio=2))
        self.play(ApplyMethod(rectangle.shift, DOWN*3))
        self.play(ApplyMethod(rectangle.shift, UP*3))
        self.play(ApplyMethod(rectangle.set_width, 10))
        self.play(ApplyMethod(rectangle.set_width, 5))

        self.wait(3)
        self.play(AnimationGroup(Uncreate(part1), Uncreate(part2), Uncreate(part3), lag_ratio=2))

class MovingFrameBox3(Scene):
    def construct(self):
        text = Text("Microscope", font="Monospace")
        print(text.submobjects)
        text.submobjects = list(reversed(text.submobjects))
        print(text.submobjects)
        self.play(AnimationGroup(Create(text)))

        self.wait(3)

class MovingFrameBox(Scene):
    def construct(self):
        rectangle1 = Rectangle(width=CANVAS_SIZE[0] - RIGHT_PANEL_WIDTH - 0.1, height=CANVAS_SIZE[1] - 0.1).shift(LEFT * RIGHT_PANEL_WIDTH / 2)
        rectangle2 = Rectangle(width=RIGHT_PANEL_WIDTH - 0.1, height=CANVAS_SIZE[1] * RIGHT_PANEL_RATIO - 0.1) \
                         .shift(RIGHT * ( CANVAS_SIZE[0] / 2 - RIGHT_PANEL_WIDTH / 2 )).shift(UP * CANVAS_SIZE[1] * RIGHT_PANEL_RATIO / 2)
        rectangle3 = Rectangle(width=RIGHT_PANEL_WIDTH - 0.1, height=CANVAS_SIZE[1] * (1 - RIGHT_PANEL_RATIO) - 0.1) \
                         .shift(RIGHT * ( CANVAS_SIZE[0] / 2 - RIGHT_PANEL_WIDTH / 2 )).shift(DOWN * CANVAS_SIZE[1] * RIGHT_PANEL_RATIO / 2)

        text1 = Code(code='for i in range(4):\n  print([1,2,3,4])', tab_width=4, background="window",
                                    language="Python", font="Monospace", style='native').code
        #text1 = VGroup(text1[0:5], text1[5:10])
        text1.align_to(rectangle1, LEFT).shift(RIGHT * 0.25)
        text1.align_to(rectangle1, UP).shift(DOWN * 0.25)

        text2 = Code(code='for i in range(4):\n\n  print([1,2,3,4])', tab_width=4, background="window",
                                    language="Python", font="Monospace", style='native').code
#        text2 = VGroup(text2[0:5], text2[5:10])
        text2.align_to(rectangle1, LEFT).shift(RIGHT * 0.25)
        text2.align_to(rectangle1, UP).shift(DOWN * 0.25)

        text3 = Code(code='for i in range(4): # loop\n\n  print([1,2,3,4], "asdf")', tab_width=4, background="window",
                                    language="Python", font="Monospace", style='native').code
        text3 = VGroup(text3[0][:-1], text3[2][2:])
        #text3[1].align_to(text3[0], LEFT)
        text3.align_to(rectangle1, LEFT).shift(RIGHT * 0.25)
        text3.align_to(rectangle1, UP).shift(DOWN * 0.25)

        text4 = Code(code='for i in range(4): # loop\n  print(2)\n  print([1,2,3,4], "asdf")', tab_width=4, background="window",
                                    language="Python", font="Monospace", style='native').code
        text4.align_to(rectangle1, LEFT).shift(RIGHT * 0.25)
        text4.align_to(rectangle1, UP).shift(DOWN * 0.25)

        text5 = Tex('Line1\nLongline2\n  Line3')
        text5 = VGroup(text5[0:5], text5[5:14], text5[14:19])
        text5.align_to(rectangle1, LEFT).shift(RIGHT * 0.25)
        text5.align_to(rectangle1, UP).shift(DOWN * 0.25)


        self.play(AnimationGroup(Create(rectangle1), Create(rectangle2), Create(rectangle3), Create(text1), lag_ratio=0.25))

        self.wait(1)
        self.play(ReplacementTransform(text1, text2))
        self.play(ReplacementTransform(text2, text3))
        self.play(ReplacementTransform(text3, text4))
        #self.play(ReplacementTransform(text4, text5))
        self.wait(3)

