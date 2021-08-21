from manim import *
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer_for_filename
from pygments.styles import get_all_styles
import bs4
from enum import Enum
from collections import namedtuple, defaultdict
from typing import (
    TYPE_CHECKING,
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    Sequence,
    Tuple,
    Union,
)
from manim.mobject.types.opengl_vectorized_mobject import OpenGLVMobject
from manim.mobject.types.opengl_surface import OpenGLSurface

CANVAS_SIZE = [8 * 16 / 9, 8]
PANEL_PADDING = 0.1

PANEL_CODE = 0
PANEL_VARS = 1
PANEL_TRACE = 2
PANEL_OUTPUT = 4


class CodeDisplayWindow(VGroup):
    title_text = 'NoTitle'
    def __init__(self, title_text=None):
        super().__init__()
        if title_text: self.title_text = title_text
        self.rectangle = Rectangle(width=CANVAS_SIZE[0] - 0.1, height=CANVAS_SIZE[1] - 0.1)
        self.title_bar = Rectangle(width=CANVAS_SIZE[0] - PANEL_PADDING, height=0.4).flip()
        self.title_bar.set_stroke(width=0)
        self.title_bar.set_fill(opacity=0.1)
        self.title_bar.align_to(self.rectangle, UP).align_to(self.rectangle, LEFT)
        self.title_bar.add_updater(lambda d: d.align_to(self.rectangle, UP).align_to(self.rectangle, LEFT))
        self.title = Text(self.title_text).scale(0.5)
        self.title.move_to(self.title_bar.get_center())
        self.title.add_updater(lambda d: d.move_to(self.title_bar.get_center()))
        self.add(self.title_bar)
        self.add(self.rectangle)

    def set_height(self, height):
        self.rectangle.stretch_to_fit_height(height, about_edge=UP)

    def stretch_to_fit_width(self, *args, **kwargs):
        self.rectangle.stretch_to_fit_width(*args, **kwargs)
        self.title_bar.stretch_to_fit_width(*args, **kwargs)

    @override_animation(Create)
    def _create_override(self, **anim_args):
        self.add(self.title)
        anim = AnimationGroup(
            AnimationGroup(
                AnimationGroup(
                    Create(self.rectangle, **anim_args),
                    Create(self.title_bar, **anim_args),
                    lag_ratio=0),
                Create(self.title, run_time=0.7, **anim_args),
                lag_ratio = 0.5
            ),
            Animation(self, suspend_mobject_updating=False, **anim_args),
        )
        return anim

    @override_animation(Uncreate)
    def _uncreate_override(self, **anim_args):
        anim = AnimationGroup(
            Uncreate(self.title, run_time=0.7, **anim_args),
            AnimationGroup(
                Uncreate(self.rectangle, **anim_args),
                Uncreate(self.title_bar, **anim_args),
                lag_ratio=0),
            lag_ratio = 0.5
        )
        return anim


class CodePanel(CodeDisplayWindow):
    title_text = 'program.py'

class VarsPanel(CodeDisplayWindow):
    title_text = 'Variables'

class OutputPanel(CodeDisplayWindow):
    title_text = 'Output'

class TracePanel(CodeDisplayWindow):
    title_text = 'Stack'


class CodeDisplayWindowColumn(VGroup):
    bottom_panel_height = 5
    top_panel_class = CodeDisplayWindow
    bottom_panel_class = CodeDisplayWindow
    panel_state = PANEL_CODE
    def __init__(self, top_panel_class=None, bottom_panel_class=None):
        super().__init__()
        if top_panel_class: self.top_panel_class = top_panel_class
        if bottom_panel_class: self.bottom_panel_class = bottom_panel_class
        self.panel_top = self.generate_top_panel()
        self.panel_bottom = self.generate_bottom_panel()
        self.add(self.panel_top)
        self.add(self.panel_bottom)
        #self.panel_bottom.add_updater(lambda d: d.next_to(self.panel_top.rectangle, DOWN, buff=0.1))
        #self.panel_bottom.add_updater(lambda d: d.align_to(self.panel_top, UP+LEFT).shift(DOWN*(CANVAS_SIZE[1] - PANEL_PADDING - self.bottom_panel_height)))
        #self.panel_bottom.add_updater(lambda d: d.move_to(self.panel_top.get_center()))
        self.show_second_panel(False)

    def generate_top_panel(self):
        return self.top_panel_class()

    def generate_bottom_panel(self):
        return self.bottom_panel_class()

    def set_width(self, width):
        self.panel_top.stretch_to_fit_width(width, about_edge=LEFT)
        self.panel_bottom.stretch_to_fit_width(width, about_edge=LEFT)

    def set_bottom_panel_height(self, height):
        self.bottom_panel_height = height
        if self.bottom_panel_visible:
            self.panel_top.set_height(CANVAS_SIZE[1] - PANEL_PADDING * 2 - self.bottom_panel_height)
        else:
            self.panel_top.set_height(CANVAS_SIZE[1] - PANEL_PADDING)
        self.panel_bottom.set_height(self.bottom_panel_height)
        self.panel_bottom.next_to(self.panel_top, DOWN, buff=0.1)

    def show_second_panel(self, show):
        self.bottom_panel_visible = show
        self.set_bottom_panel_height(self.bottom_panel_height)

    @override_animation(Create)
    def _create_override(self, **anim_args):
        anim = AnimationGroup(
            AnimationGroup(
                Create(self.panel_top, **anim_args),
                Create(self.panel_bottom, **anim_args),
                lag_ratio = 0.25
            ),
            Animation(self, suspend_mobject_updating=False, **anim_args),
        )
        return anim

    @override_animation(Uncreate)
    def _uncreate_override(self, **anim_args):
        anim = AnimationGroup(
            Uncreate(self.panel_top, **anim_args),
            Uncreate(self.panel_bottom, **anim_args),
            lag_ratio = 0
        )
        return anim


class MainCodeDisplayWindowColumn(CodeDisplayWindowColumn):
    bottom_panel_height = 1
    top_panel_class = CodePanel
    bottom_panel_class = OutputPanel


class SideCodeDisplayWindowColumn(CodeDisplayWindowColumn):
    bottom_panel_height = 2
    top_panel_class = VarsPanel
    bottom_panel_class = TracePanel


class BaseCodeDisplay(VGroup):
    left_column_class = CodeDisplayWindowColumn
    right_column_class = CodeDisplayWindowColumn
    panel_state = PANEL_CODE
    side_panel_width = 5
    def __init__(self, left_column_class=None, right_column_class=None):
        super().__init__()
        if left_column_class: self.left_column_class = left_column_class
        if right_column_class: self.right_column_class = right_column_class
        self.panel_main = self.generate_left_column()
        self.panel_side = self.generate_right_column()
        self.add(self.panel_main)
        self.add(self.panel_side)
        #self.panel_side.panel_top.rectangle.add_updater(lambda d: d.next_to(self.panel_main.panel_top.rectangle, RIGHT, buff=0.1).align_to(self.panel_main.panel_top.rectangle, UP))
        self.set_panels(self.panel_state)

    def generate_left_column(self):
        return self.left_column_class()

    def generate_right_column(self):
        return self.right_column_class()

    def set_side_panel_width(self, width):
        self.side_panel_width = width
        self.panel_side.set_width(self.side_panel_width)
        if self.panel_state & PANEL_VARS:
            self.panel_main.set_width(CANVAS_SIZE[0] - PANEL_PADDING * 2 - self.side_panel_width)
        else:
            self.panel_main.set_width(CANVAS_SIZE[0] - PANEL_PADDING)
        self.panel_side.next_to(self.panel_main, RIGHT, buff=0.1).align_to(self.panel_main, UP)

    def set_panels(self, panels):
        self.panel_state = panels
        self.set_side_panel_width(self.side_panel_width)
        self.panel_main.show_second_panel(self.panel_state & PANEL_OUTPUT)
        self.panel_side.show_second_panel(self.panel_state & PANEL_TRACE)
        return self

    @override_animation(Create)
    def _create_override(self, **anim_args):
        anim = AnimationGroup(
            AnimationGroup(
                Create(self.panel_main, **anim_args),
                Create(self.panel_side, **anim_args),
                lag_ratio = 0.25
            ),
            Animation(self, suspend_mobject_updating=False, **anim_args),
        )
        return anim

    @override_animation(Uncreate)
    def _uncreate_override(self, **anim_args):
        anim = AnimationGroup(
            AnimationGroup(
                Uncreate(self.panel_main, **anim_args),
                Uncreate(self.panel_side, **anim_args),
                lag_ratio = 0
            ),
        )
        return anim

class CodeDisplay(BaseCodeDisplay):
    left_column_class = MainCodeDisplayWindowColumn
    right_column_class = SideCodeDisplayWindowColumn
    side_panel_width = 5
