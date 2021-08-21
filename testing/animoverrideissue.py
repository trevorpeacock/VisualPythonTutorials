from manim import *


class Broken(VGroup):
    def __init__(self, shape=Circle):
        super().__init__()
        self.dot = Dot()
        self.add(self.dot)
        self.shape = shape()
        self.shape.move_to(self.dot.get_center())
        self.shape.add_updater(lambda d: d.move_to(self.dot.get_center()))

    @override_animation(Create)
    def create(self, **kwargs):
        return AnimationGroup(
            FadeIn(self.dot, **kwargs),
            FadeIn(self.shape, **kwargs)
        )

class Fixed(Broken):
    @override_animation(Create)
    def create(self, **kwargs):
        return AnimationGroup(
            FadeIn(self.dot, **kwargs),
            FadeIn(self.shape, **kwargs),
            Animation(self, suspend_mobject_updating=False),
        )

class IssueDemoOverrideAnimation(Scene):
    def construct(self):
        rootobj = Dot()
        plain_triangle = Triangle()
        plain_triangle.add_updater(lambda d: d.move_to(rootobj.get_center() + LEFT * 6))
        broken_vg = Broken(Circle).shift(LEFT * 4)
        broken_vg.add_updater(lambda d: d.move_to(rootobj.get_center() + LEFT * 4))
        fixed_vg = Fixed(Square)
        fixed_vg.add_updater(lambda d: d.move_to(rootobj.get_center() + LEFT * 2))
        broken_manim = ManimBanner().scale(0.5).shift(RIGHT * 3)
        broken_manim.add_updater(lambda d: d.move_to(rootobj.get_center() + RIGHT * 3))
        self.play(AnimationGroup(
            Create(rootobj),
            Create(plain_triangle),
            Create(broken_vg),
            Create(fixed_vg),
            Create(broken_manim),
            run_time=10,
            lag_ratio=1
        ))
        self.play(broken_manim.expand())
        self.wait()
        self.play(ApplyMethod(rootobj.shift, DOWN*3))
        self.play(ApplyMethod(rootobj.shift, UP*3))
        self.wait()
