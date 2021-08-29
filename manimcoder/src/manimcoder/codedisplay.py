from manim import *
from manimcoder.programcode import *
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
    content_class = Text
    def __init__(self, title_text=None):
        super().__init__()
        if title_text: self.title_text = title_text
        self.rectangle = Rectangle(width=CANVAS_SIZE[0] - 0.1, height=CANVAS_SIZE[1] - 0.1)
        self.title_bar = Rectangle(width=CANVAS_SIZE[0] - PANEL_PADDING, height=0.4).flip()
        self.title_bar.set_stroke(width=0)
        self.title_bar.set_fill(opacity=0.1)
        self.title_bar.align_to(self.rectangle, UP+LEFT)
        self.title_bar.add_updater(lambda d: d.align_to(self.rectangle, UP+LEFT))
        self.title = Text(self.title_text).scale(0.5)
        self.title.move_to(self.title_bar.get_center())
        self.title.add_updater(lambda d: d.move_to(self.title_bar.get_center()))
        self.content = self.generate_content()
        self.add(self.title_bar)
        self.add(self.rectangle)

    def generate_content(self, *args, **kwargs):
        if self.content_class == Text and len(args)==0:
            content = self.content_class('TEST', *args, **kwargs).scale(0.5)
        else:
            content = self.content_class(*args, **kwargs)
        content.next_to(self.title_bar, DOWN).align_to(self.title_bar, LEFT).shift((UP+RIGHT)*0.1)
        content.add_updater(lambda d: d.next_to(self.title_bar, DOWN).align_to(self.title_bar, LEFT).shift((UP+RIGHT)*0.1))
        return content

    def set_height(self, height):
        self.rectangle.stretch_to_fit_height(height, about_edge=UP)

    def stretch_to_fit_width(self, *args, **kwargs):
        self.rectangle.stretch_to_fit_width(*args, **kwargs)
        self.title_bar.stretch_to_fit_width(*args, **kwargs)

    def content_create_animation(self, **anim_args):
        return [Create(self.content, **anim_args)]

    def content_uncreate_animation(self, **anim_args):
        return [Uncreate(self.content, **anim_args)]

    @override_animation(Create)
    def _create_override(self, **anim_args):
        self.add(self.title)
        if self.content:
            self.add(self.content)
        anim = AnimationGroup(
            AnimationGroup(
                AnimationGroup(
                    Create(self.rectangle, **anim_args),
                    Create(self.title_bar, **anim_args),
                    lag_ratio=0
                ),
                AnimationGroup(
                    Create(self.title, run_time=0.7, **anim_args),
                    *self.content_create_animation(**anim_args),
                    lag_ratio=0
                ),
                lag_ratio = 0.7
            ),
            Animation(self, suspend_mobject_updating=False, **anim_args),
        )
        return anim

    @override_animation(Uncreate)
    def _uncreate_override(self, **anim_args):
        anim = AnimationGroup(
            AnimationGroup(
                Uncreate(self.title, run_time=0.7, **anim_args),
                *self.content_uncreate_animation(**anim_args),
                lag_ratio=0
            ),
            AnimationGroup(
                Uncreate(self.rectangle, **anim_args),
                Uncreate(self.title_bar, **anim_args),
                lag_ratio=0),
            lag_ratio = 0.5
        )
        return anim

class ProgramCodeCodeDisplayWindow(CodeDisplayWindow):
    content_class = ProgramCode
    lexer = 'python'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.oldrunarrorw = None
        self.newrunarrow = None

    def content_create_animation(self, **anim_args):
        return [
            Create(self.content, **anim_args),
            self.content.changes()
        ]

    def content_uncreate_animation(self, **anim_args):
        # TODO: include arrow
        return [
            Uncreate(self.content.all_text, **anim_args),  # TODO: Hack
            Uncreate(self.content, **anim_args),
       ]

    def generate_content(self):
        content = self.content_class('', lexer=self.lexer)
        content.align_to(self.title_bar, DOWN+LEFT).shift((DOWN+RIGHT)*0.1)
        content.add_updater(lambda d: d.align_to(self.title_bar, DOWN+LEFT).shift((DOWN+RIGHT)*0.1))
        return content

    def update_runarrow(self, obj):
        self.oldrunarrow = self.newrunarrow
        if obj is None:
            self.newrunarrow = None
        else:
            start = UP * self.content.code.lines[obj].symbols.get_center()[1]
            start += RIGHT * self.rectangle.get_center()[0] + LEFT * self.rectangle.width / 2
            end = start + RIGHT*0.5
            self.newrunarrow = Arrow(
                start=start,
                end=end,
                buff=0.05,
                stroke_width=15,
                max_stroke_width_to_length_ratio=900,
                max_tip_length_to_length_ratio=0.8,
            )

    def runarrow(self):
        if self.oldrunarrow is None and self.newrunarrow is None:
            raise Exception
        if self.oldrunarrow is not None and self.newrunarrow is not None:
            return ReplacementTransform(self.oldrunarrow, self.newrunarrow)
        if self.newrunarrow:
            return FadeIn(self.newrunarrow)
        return FadeOut(self.oldrunarrow)


class CodePanel(ProgramCodeCodeDisplayWindow):
    title_text = 'program.py'
    def generate_content(self):
        content = self.content_class('', lexer=self.lexer)
        content.align_to(self.title_bar, DOWN+LEFT).shift(DOWN*0.1+RIGHT*0.5)
        content.add_updater(lambda d: d.align_to(self.title_bar, DOWN+LEFT).shift(DOWN*0.1+RIGHT*0.5))
        return content


class VarsPanel(ProgramCodeCodeDisplayWindow):
    title_text = 'Variables'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scopes = {'': {}}
        self.current_scope = ''
        self.var_length = 5
        self.scope_bars = {}
        self.changes_queue = []

    def get_lines(self):
        lines = {}
        scope = ''
        for lineno, line in enumerate(self.content.code.get_new_code().split('\n')):
            if line == '': continue
            if '=' in line:
                line = line.split('=')[0].strip()
                lines[(scope, line)] = lineno
            else:
                scope = line
                lines[(scope, '')] = lineno
        return lines

    def get_next_scope_line(self, scope):
        found_scope = scope == ''
        for (s, v), lineno in self.get_lines().items():
            print(found_scope, s, v, lineno)
            if s==scope and v=='':
                found_scope = True
            if found_scope and v=='':
                return lineno
        return lineno

    def last_scope_name(self):
        scope = ''
        for (s, v), lineno in self.get_lines().items():
            if v=='':
                scope = s
        return scope

    def set_var(self, varname, value, scope=None):
        if len(varname) > self.var_length:
            raise Exception(f"Var {varname} longer than var_length={self.var_length}.")
        if scope is None:
            scope = self.current_scope
        if varname not in self.scopes[scope]:
            self.scopes[scope][varname] = value
            line = varname + ' ' * (self.var_length - len(varname))
            line = f"{line} = {value}"
            if scope == self.current_scope:
                self.content.append_line(line)
            else:
                self.content.insert_line(self.get_next_scope_line(scope), line)
        else:
            self.content.replace(self.get_lines()[(scope, varname)], self.scopes[scope][varname], value)
            self.scopes[scope][varname] = value

    def remove_var(self, varname, scope=None):
        if scope is None:
            scope = self.current_scope
        self.content.remove_line(self.get_lines()[(scope, varname)])
        del self.scopes[scope][varname]

    def add_scope(self, scope):
        self.scopes[scope] = {}
        self.content.append_line(scope)
        self.current_scope = scope
        bar = Rectangle(height=0.625*self.content.text_scale, width=self.rectangle.width)
        bar.set_stroke(width=0)
        bar.set_fill(opacity=0.2)
        self.scope_bars[scope] = bar
        self.add(bar)
        self.changes_queue.append(Create(bar))

    def remove_scope(self):
        scope = self.current_scope
        del self.scopes[scope]
        for (s, _), lineno in self.get_lines().items():
            if s == scope:
                self.content.remove_line(lineno)
        self.current_scope = self.last_scope_name()
        self.changes_queue.append(FadeOut(self.scope_bars[scope]))
        del self.scope_bars[scope]

    def symbols_line(self, varname, scope=None):
        if scope is None:
            scope = self.current_scope
        return self.content.code.lines[self.get_lines()[(scope, varname)]].symbols

    def symbols_value(self, varname, scope=None):
        if scope is None:
            scope = self.current_scope
        return self.content.code.lines[self.get_lines()[(scope, varname)]].symbols[len(varname)+1:]

    def changes(self):
        changes = self.content.changes()

        if self.changes_queue:
            for scope, bar in self.scope_bars.items():
                bar.move_to(self.symbols_line('', scope=scope))
                bar.align_to(self.rectangle, LEFT)
            changes = AnimationGroup(
                *self.changes_queue,
                changes
            )
            self.changes_queue = []
        return changes


class OutputPanel(ProgramCodeCodeDisplayWindow):
    title_text = 'Output'
    lexer = 'text'
    max_lines = 4
    def add_line(self, text):
        self.content.append_line(text)
        while len(self.content.code.get_new_code().split('\n')) > self.max_lines:
            for line in self.content.code.lines:
                if not line.delete:
                    line.delete = True
                    break

    def clear_lines(self):
        self.content.remove_all_lines()


class TracePanel(CodeDisplayWindow):
    title_text = 'Stack'
    lexer = 'text'


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
    bottom_panel_height = 2.5
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = self.panel_main.panel_top
        self.output = self.panel_main.panel_bottom
        self.vars = self.panel_side.panel_top
        self.stack = self.panel_side.panel_bottom
