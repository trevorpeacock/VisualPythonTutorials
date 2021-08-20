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
    def __init__(self):
        super().__init__()
        self.rectangle = Rectangle(width=CANVAS_SIZE[0] - 0.1, height=CANVAS_SIZE[1] - 0.1)
        self.title_bar = Rectangle(width=CANVAS_SIZE[0] - PANEL_PADDING, height=0.5)
        self.title_bar.set_stroke(width=0)
        self.title_bar.set_fill(opacity=0.1)
        self.title_bar.add_updater(lambda d: d.align_to(self.rectangle, UP).align_to(self.rectangle, LEFT))
        self.title = Text('asdf')
        self.title.add_updater(lambda d: d.move_to(self.title_bar.get_center()))
        self.add(self.title_bar)
        self.add(self.rectangle)
        self.add(self.title)

    def set_height(self, height):
        self.rectangle.stretch_to_fit_height(height, about_edge=UP)

    def stretch_to_fit_width(self, *args, **kwargs):
        self.rectangle.stretch_to_fit_width(*args, **kwargs)
        self.title_bar.stretch_to_fit_width(*args, **kwargs)


class CodeDisplayWindowColumn(VGroup):
    def __init__(self):
        super().__init__()
        self.panel_top = CodeDisplayWindow()
        self.add(self.panel_top)
        self.panel_bottom = CodeDisplayWindow()
        self.add(self.panel_bottom)
        self.panel_bottom.add_updater(lambda d: d.next_to(self.panel_top, DOWN, buff=0.1))
        self.bottom_panel_height = 5
        self.set_initial()

    def set_initial(self):
        self.show_second_panel(False)

    def set_width(self, width):
        self.panel_top.stretch_to_fit_width(width, about_edge=LEFT)
        self.panel_bottom.stretch_to_fit_width(width, about_edge=LEFT)

    def show_second_panel(self, show):
        if show:
            self.panel_top.set_height(CANVAS_SIZE[1] - PANEL_PADDING * 2 - self.bottom_panel_height)
        else:
            self.panel_top.set_height(CANVAS_SIZE[1] - PANEL_PADDING)


class MainCodeDisplayWindowColumn(CodeDisplayWindowColumn):
    def set_initial(self):
        self.bottom_panel_height = 1
        super().set_initial()


class SideCodeDisplayWindowColumn(CodeDisplayWindowColumn):
    def set_initial(self):
        self.bottom_panel_height = 2
        super().set_initial()


class CodeDisplay(VGroup):
    def __init__(self):
        super().__init__()
        self.panel_main = MainCodeDisplayWindowColumn()
        self.add(self.panel_main)
        self.panel_side = SideCodeDisplayWindowColumn()
        self.add(self.panel_side)
        self.panel_side.add_updater(lambda d: d.next_to(self.panel_main, RIGHT, buff=0.1).align_to(self.panel_main, UP))
        self.side_panel_width = 5
        self.set_initial()

    def set_initial(self):
        self.set_panels(PANEL_CODE)

    def set_panels(self, panels):
        self.panel_side.set_width(self.side_panel_width)
        if panels & PANEL_VARS:
            self.panel_main.set_width(CANVAS_SIZE[0] - PANEL_PADDING * 2 - self.side_panel_width)
        else:
            self.panel_main.set_width(CANVAS_SIZE[0] - PANEL_PADDING)
        self.panel_main.show_second_panel(panels & PANEL_OUTPUT)
        self.panel_side.show_second_panel(panels & PANEL_TRACE)
        return self
