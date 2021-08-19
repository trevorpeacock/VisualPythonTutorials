from manim import *


import copy
import hashlib
import os
import re
import typing
from contextlib import contextmanager
from pathlib import Path
from typing import Dict

import manimpango
import numpy as np
from manimpango import MarkupUtils, PangoUtils, TextSetting

from manim import config, logger
from manim.constants import *
from manim.mobject.geometry import Dot
from manim.mobject.svg.svg_mobject import SVGMobject
from manim.mobject.types.vectorized_mobject import VGroup
from manim.utils.color import WHITE, Colors

TEXT_MOB_SCALE_FACTOR = 0.05


class Text(SVGMobject):
    r"""Display (non-LaTeX) text rendered using `Pango <https://pango.gnome.org/>`_.
    Text objects behave like a :class:`.VGroup`-like iterable of all characters
    in the given text. In particular, slicing is possible.
    Parameters
    ----------
    text : :class:`str`
        The text that need to created as mobject.
    Returns
    -------
    :class:`Text`
        The mobject like :class:`.VGroup`.
    Examples
    ---------
    .. manim:: Example1Text
        :save_last_frame:
        class Example1Text(Scene):
            def construct(self):
                text = Text('Hello world').scale(3)
                self.add(text)
    .. manim:: TextColorExample
        :save_last_frame:
        class TextColorExample(Scene):
            def construct(self):
                text1 = Text('Hello world', color=BLUE).scale(3)
                text2 = Text('Hello world', gradient=(BLUE, GREEN)).scale(3).next_to(text1, DOWN)
                self.add(text1, text2)
    .. manim:: TextItalicAndBoldExample
        :save_last_frame:
        class TextItalicAndBoldExample(Scene):
            def construct(self):
                text1 = Text("Hello world", slant=ITALIC)
                text2 = Text("Hello world", t2s={'world':ITALIC})
                text3 = Text("Hello world", weight=BOLD)
                text4 = Text("Hello world", t2w={'world':BOLD})
                text5 = Text("Hello world", t2c={'o':YELLOW}, disable_ligatures=True)
                text6 = Text(
                    "Visit us at docs.manim.community",
                    t2c={"docs.manim.community": YELLOW},
                    disable_ligatures=True,
               )
                text6.scale(1.3).shift(DOWN)
                self.add(text1, text2, text3, text4, text5 , text6)
                Group(*self.mobjects).arrange(DOWN, buff=.8).set_height(config.frame_height-LARGE_BUFF)
    .. manim:: TextMoreCustomization
            :save_last_frame:
            class TextMoreCustomization(Scene):
                def construct(self):
                    text1 = Text(
                        'Google',
                        t2c={'[:1]': '#3174f0', '[1:2]': '#e53125',
                             '[2:3]': '#fbb003', '[3:4]': '#3174f0',
                             '[4:5]': '#269a43', '[5:]': '#e53125'}, size=1.2).scale(3)
                    self.add(text1)
    As :class:`Text` uses Pango to render text, rendering non-English
    characters is easily possible:
    .. manim:: MultipleFonts
        :save_last_frame:
        class MultipleFonts(Scene):
            def construct(self):
                morning = Text("வணக்கம்", font="sans-serif")
                chin = Text(
                    "見 角 言 谷  辛 辰 辵 邑 酉 釆 里!", t2c={"見 角 言": BLUE}
                )  # works same as ``Text``.
                mess = Text("Multi-Language", weight=BOLD)
                russ = Text("Здравствуйте मस नम म ", font="sans-serif")
                hin = Text("नमस्ते", font="sans-serif")
                arb = Text(
                    "صباح الخير \n تشرفت بمقابلتك", font="sans-serif"
                )  # don't mix RTL and LTR languages nothing shows up then ;-)
                japanese = Text("臂猿「黛比」帶著孩子", font="sans-serif")
                self.add(morning,chin,mess,russ,hin,arb,japanese)
                for i,mobj in enumerate(self.mobjects):
                    mobj.shift(DOWN*(i-3))
    .. manim:: PangoRender
        :quality: low
        class PangoRender(Scene):
            def construct(self):
                morning = Text("வணக்கம்", font="sans-serif")
                self.play(Write(morning))
                self.wait(2)
    Tests
    -----
    Check that the creation of :class:`~.Text` works::
        >>> Text('The horse does not eat cucumber salad.')
        Text('The horse does not eat cucumber salad.')
    """

    def __init__(
        self,
        text: str,
        fill_opacity: float = 1.0,
        stroke_width: int = 0,
        color: str = WHITE,
        size: int = 1,
        line_spacing: int = -1,
        font: str = "",
        slant: str = NORMAL,
        weight: str = NORMAL,
        t2c: Dict[str, str] = None,
        t2f: Dict[str, str] = None,
        t2g: Dict[str, tuple] = None,
        t2s: Dict[str, str] = None,
        t2w: Dict[str, str] = None,
        gradient: tuple = None,
        tab_width: int = 4,
        # Mobject
        height: int = None,
        width: int = None,
        should_center: bool = True,
        unpack_groups: bool = True,
        disable_ligatures: bool = False,
        **kwargs,
    ):
        self.size = size
        self.line_spacing = line_spacing
        self.font = font
        self.slant = slant
        self.weight = weight
        self.gradient = gradient
        self.tab_width = tab_width
        if t2c is None:
            t2c = {}
        if t2f is None:
            t2f = {}
        if t2g is None:
            t2g = {}
        if t2s is None:
            t2s = {}
        if t2w is None:
            t2w = {}
        # If long form arguments are present, they take precedence
        t2c = kwargs.pop("text2color", t2c)
        t2f = kwargs.pop("text2font", t2f)
        t2g = kwargs.pop("text2gradient", t2g)
        t2s = kwargs.pop("text2slant", t2s)
        t2w = kwargs.pop("text2weight", t2w)
        self.t2c = t2c
        self.t2f = t2f
        self.t2g = t2g
        self.t2s = t2s
        self.t2w = t2w

        self.original_text = text
        self.disable_ligatures = disable_ligatures
        text_without_tabs = text
        if text.find("\t") != -1:
            text_without_tabs = text.replace("\t", " " * self.tab_width)
        self.text = text_without_tabs
        if self.line_spacing == -1:
            self.line_spacing = self.size + self.size * 0.3
        else:
            self.line_spacing = self.size + self.size * self.line_spacing
        file_name = self.text2svg()
        PangoUtils.remove_last_M(file_name)
        SVGMobject.__init__(
            self,
            file_name,
            color=color,
            fill_opacity=fill_opacity,
            stroke_width=stroke_width,
            height=height,
            width=width,
            should_center=should_center,
            unpack_groups=unpack_groups,
            **kwargs,
        )
        self.text = text
        if self.disable_ligatures:
            if config.renderer == "opengl":
                self.set_submobjects(self.gen_chars())
            else:
                self.submobjects = [*self.gen_chars()]
        self.chars = self.get_group_class()(*self.submobjects)
        self.text = text_without_tabs.replace(" ", "").replace("\n", "")
        if config.renderer == "opengl":
            nppc = self.n_points_per_curve
        else:
            nppc = self.n_points_per_cubic_curve
        for each in self:
            if len(each.get_points()) == 0:
                continue
            points = each.get_points()
            last = points[0]
            each.clear_points()
            for index, point in enumerate(points):
                each.append_points([point])
                if (
                    index != len(points) - 1
                    and (index + 1) % nppc == 0
                    and any(point != points[index + 1])
                ):
                    each.add_line_to(last)
                    last = points[index + 1]
            each.add_line_to(last)
        if self.t2c:
            self.set_color_by_t2c()
        if self.gradient:
            self.set_color_by_gradient(*self.gradient)
        if self.t2g:
            self.set_color_by_t2g()
        # anti-aliasing
        if height is None and width is None:
            self.scale(TEXT_MOB_SCALE_FACTOR)

    def __repr__(self):
        return f"Text({repr(self.original_text)})"

    def gen_chars(self):
        chars = self.get_group_class()()
        submobjects_char_index = 0
        for char_index in range(self.text.__len__()):
            if self.text[char_index] in (" ", "\t", "\n"):
                space = Dot(radius=0, fill_opacity=0, stroke_opacity=0)
                if char_index == 0:
                    space.move_to(self.submobjects[submobjects_char_index].get_center())
                else:
                    space.move_to(
                        self.submobjects[submobjects_char_index - 1].get_center()
                    )
                chars.add(space)
            else:
                chars.add(self.submobjects[submobjects_char_index])
                submobjects_char_index += 1
        return chars

    def find_indexes(self, word: str, text: str):
        """Internally used function. Finds the indexes of ``text`` in ``word``."""
        temp = re.match(r"\[([0-9\-]{0,}):([0-9\-]{0,})\]", word)
        if temp:
            start = int(temp.group(1)) if temp.group(1) != "" else 0
            end = int(temp.group(2)) if temp.group(2) != "" else len(text)
            start = len(text) + start if start < 0 else start
            end = len(text) + end if end < 0 else end
            return [(start, end)]
        indexes = []
        index = text.find(word)
        while index != -1:
            indexes.append((index, index + len(word)))
            index = text.find(word, index + len(word))
        return indexes

    # def full2short(self, kwargs):
    #     """Internally used function. Formats some expansion to short forms.
    #     text2color -> t2c
    #     text2font -> t2f
    #     text2gradient -> t2g
    #     text2slant -> t2s
    #     text2weight -> t2w
    #     """
    #     if "text2color" in kwargs:
    #         self.t2c = kwargs.pop("text2color")
    #     if "text2font" in kwargs:
    #         self.t2f = kwargs.pop("text2font")
    #     if "text2gradient" in kwargs:
    #         self.t2g = kwargs.pop("text2gradient")
    #     if "text2slant" in kwargs:
    #         self.t2s = kwargs.pop("text2slant")
    #     if "text2weight" in kwargs:
    #         self.t2w = kwargs.pop("text2weight")

    def set_color_by_t2c(self, t2c=None):
        """Internally used function. Sets color for specified strings."""
        t2c = t2c if t2c else self.t2c
        for word, color in list(t2c.items()):
            for start, end in self.find_indexes(word, self.original_text):
                self.chars[start:end].set_color(color)

    def set_color_by_t2g(self, t2g=None):
        """Internally used. Sets gradient colors for specified
        strings. Behaves similarly to ``set_color_by_t2c``."""
        t2g = t2g if t2g else self.t2g
        for word, gradient in list(t2g.items()):
            for start, end in self.find_indexes(word, self.original_text):
                self.chars[start:end].set_color_by_gradient(*gradient)

    def text2hash(self):
        """Internally used function.
        Generates ``sha256`` hash for file name.
        """
        settings = (
            "PANGO" + self.font + self.slant + self.weight
        )  # to differentiate Text and CairoText
        settings += str(self.t2f) + str(self.t2s) + str(self.t2w)
        settings += str(self.line_spacing) + str(self.size)
        settings += str(self.disable_ligatures)
        id_str = self.text + settings
        hasher = hashlib.sha256()
        hasher.update(id_str.encode())
        return hasher.hexdigest()[:16]

    def text2settings(self):
        """Internally used function. Converts the texts and styles
        to a setting for parsing."""
        settings = []
        t2x = [self.t2f, self.t2s, self.t2w]
        for i in range(len(t2x)):
            fsw = [self.font, self.slant, self.weight]
            if t2x[i]:
                for word, x in list(t2x[i].items()):
                    for start, end in self.find_indexes(word, self.text):
                        fsw[i] = x
                        settings.append(TextSetting(start, end, *fsw))
        # Set all text settings (default font, slant, weight)
        fsw = [self.font, self.slant, self.weight]
        settings.sort(key=lambda setting: setting.start)
        temp_settings = settings.copy()
        start = 0
        for setting in settings:
            if setting.start != start:
                temp_settings.append(TextSetting(start, setting.start, *fsw))
            start = setting.end
        if start != len(self.text):
            temp_settings.append(TextSetting(start, len(self.text), *fsw))
        settings = sorted(temp_settings, key=lambda setting: setting.start)

        if re.search(r"\n", self.text):
            line_num = 0
            for start, end in self.find_indexes("\n", self.text):
                for setting in settings:
                    if setting.line_num == -1:
                        setting.line_num = line_num
                    if start < setting.end:
                        line_num += 1
                        new_setting = copy.copy(setting)
                        setting.end = end
                        new_setting.start = end
                        new_setting.line_num = line_num
                        settings.append(new_setting)
                        settings.sort(key=lambda setting: setting.start)
                        break
        for setting in settings:
            if setting.line_num == -1:
                setting.line_num = 0
        return settings

    def text2svg(self):
        """Internally used function.
        Convert the text to SVG using Pango
        """
        size = self.size * 10
        line_spacing = self.line_spacing * 10
        dir_name = config.get_dir("text_dir")
        disable_liga = self.disable_ligatures
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        hash_name = self.text2hash()
        file_name = os.path.join(dir_name, hash_name) + ".svg"
        if os.path.exists(file_name):
            return file_name
        settings = self.text2settings()
        width = 600
        height = 400
        print(START_X, START_Y, width, height)

        return manimpango.text2svg(
            settings,
            size,
            line_spacing,
            disable_liga,
            file_name,
            START_X,
            START_Y,
            width,
            height,
            self.text,
        )

    def init_colors(self, propagate_colors=True):
        super().init_colors(propagate_colors=propagate_colors)
        

class Paragraph(VGroup):
    r"""Display a paragraph of text.
    For a given :class:`.Paragraph` ``par``, the attribute ``par.chars`` is a
    :class:`.VGroup` containing all the lines. In this context, every line is
    constructed as a :class:`.VGroup` of characters contained in the line.
    Parameters
    ----------
    line_spacing : :class:`int`, optional
        Represents the spacing between lines. Default to -1, which means auto.
    alignment : :class:`str`, optional
        Defines the alignment of paragraph. Default to "left". Possible values are "left", "right", "center"
    Examples
    --------
    Normal usage::
        paragraph = Paragraph('this is a awesome', 'paragraph',
                              'With \nNewlines', '\tWith Tabs',
                              '  With Spaces', 'With Alignments',
                              'center', 'left', 'right')
    Remove unwanted invisible characters::
        self.play(Transform(remove_invisible_chars(paragraph.chars[0:2]),
                            remove_invisible_chars(paragraph.chars[3][0:3]))
    """

    def __init__(self, *text, line_spacing=-1, alignment=None, **config):
        self.line_spacing = line_spacing
        self.alignment = alignment
        VGroup.__init__(self)

        lines_str = "\n".join(list(text))
        self.lines_text = Text(lines_str, line_spacing=line_spacing, **config)
        lines_str_list = lines_str.split("\n")
        self.chars = self.gen_chars(lines_str_list)

        chars_lines_text_list = self.get_group_class()()
        char_index_counter = 0
        print(lines_str_list)
        print(self.lines_text)
        print(lines_str_list)
        for line_index in range(lines_str_list.__len__()):
            chars_lines_text_list.add(
                self.lines_text[
                    char_index_counter : char_index_counter
                    + lines_str_list[line_index].__len__()
                    + 1
                ]
            )
            print(char_index_counter , char_index_counter + lines_str_list[line_index].__len__() + 1)
            char_index_counter += lines_str_list[line_index].__len__() + 1
        self.lines = []
        self.lines.append([])
        for line_no in range(chars_lines_text_list.__len__()):
            self.lines[0].append(chars_lines_text_list[line_no])
        self.lines_initial_positions = []
        for line_no in range(self.lines[0].__len__()):
            self.lines_initial_positions.append(self.lines[0][line_no].get_center())
        self.lines.append([])
        self.lines[1].extend(
            [self.alignment for _ in range(chars_lines_text_list.__len__())]
        )
        self.add(*self.lines[0])
        self.move_to(np.array([0, 0, 0]))
        if self.alignment:
            self.set_all_lines_alignments(self.alignment)

    def gen_chars(self, lines_str_list):
        """Function to convert plain string to 2d-VGroup of chars. 2d-VGroup mean "VGroup of VGroup".
        Parameters
        ----------
        lines_str_list : :class:`str`
            Plain text string.
        Returns
        -------
        :class:`~.VGroup`
            The generated 2d-VGroup of chars.
        """
        char_index_counter = 0
        chars = self.get_group_class()()
        for line_no in range(lines_str_list.__len__()):
            chars.add(self.get_group_class()())
            chars[line_no].add(
                *self.lines_text.chars[
                    char_index_counter : char_index_counter
                    + lines_str_list[line_no].__len__()
                    + 1
                ]
            )
            char_index_counter += lines_str_list[line_no].__len__() + 1
        return chars

    def set_all_lines_alignments(self, alignment):
        """Function to set all line's alignment to a specific value.
        Parameters
        ----------
        alignment : :class:`str`
            Defines the alignment of paragraph. Possible values are "left", "right", "center".
        """
        for line_no in range(0, self.lines[0].__len__()):
            self.change_alignment_for_a_line(alignment, line_no)
        return self

    def set_line_alignment(self, alignment, line_no):
        """Function to set one line's alignment to a specific value.
        Parameters
        ----------
        alignment : :class:`str`
            Defines the alignment of paragraph. Possible values are "left", "right", "center".
        line_no : :class:`int`
            Defines the line number for which we want to set given alignment.
        """
        self.change_alignment_for_a_line(alignment, line_no)
        return self

    def set_all_lines_to_initial_positions(self):
        """Set all lines to their initial positions."""
        self.lines[1] = [None for _ in range(self.lines[0].__len__())]
        for line_no in range(0, self.lines[0].__len__()):
            self[line_no].move_to(
                self.get_center() + self.lines_initial_positions[line_no]
            )
        return self

    def set_line_to_initial_position(self, line_no):
        """Function to set one line to initial positions.
        Parameters
        ----------
        line_no : :class:`int`
            Defines the line number for which we want to set given alignment.
        """
        self.lines[1][line_no] = None
        self[line_no].move_to(self.get_center() + self.lines_initial_positions[line_no])
        return self

    def change_alignment_for_a_line(self, alignment, line_no):
        """Function to change one line's alignment to a specific value.
        Parameters
        ----------
        alignment : :class:`str`
            Defines the alignment of paragraph. Possible values are "left", "right", "center".
        line_no : :class:`int`
            Defines the line number for which we want to set given alignment.
        """
        self.lines[1][line_no] = alignment
        if self.lines[1][line_no] == "center":
            self[line_no].move_to(
                np.array([self.get_center()[0], self[line_no].get_center()[1], 0])
            )
        elif self.lines[1][line_no] == "right":
            self[line_no].move_to(
                np.array(
                    [
                        self.get_right()[0] - self[line_no].width / 2,
                        self[line_no].get_center()[1],
                        0,
                    ]
                )
            )
        elif self.lines[1][line_no] == "left":
            self[line_no].move_to(
                np.array(
                    [
                        self.get_left()[0] + self[line_no].width / 2,
                        self[line_no].get_center()[1],
                        0,
                    ]
                )
            )


CANVAS_SIZE = [8*16/9, 8]

RIGHT_PANEL_WIDTH = 5
RIGHT_PANEL_RATIO = 0.5

class MovingFrameBox(Scene):
    def construct(self):
        rectangle1 = Rectangle(width=CANVAS_SIZE[0] - RIGHT_PANEL_WIDTH - 0.1, height=CANVAS_SIZE[1] - 0.1).shift(LEFT * RIGHT_PANEL_WIDTH / 2)
        rectangle2 = Rectangle(width=RIGHT_PANEL_WIDTH - 0.1, height=CANVAS_SIZE[1] * RIGHT_PANEL_RATIO - 0.1) \
                         .shift(RIGHT * ( CANVAS_SIZE[0] / 2 - RIGHT_PANEL_WIDTH / 2 )).shift(UP * CANVAS_SIZE[1] * RIGHT_PANEL_RATIO / 2)
        rectangle3 = Rectangle(width=RIGHT_PANEL_WIDTH - 0.1, height=CANVAS_SIZE[1] * (1 - RIGHT_PANEL_RATIO) - 0.1) \
                         .shift(RIGHT * ( CANVAS_SIZE[0] / 2 - RIGHT_PANEL_WIDTH / 2 )).shift(DOWN * CANVAS_SIZE[1] * RIGHT_PANEL_RATIO / 2)

        text1 = Text('Line1\n  Line2', font="FreeMono", weight=BOLD)
        text1 = VGroup(text1[0:5], text1[5:10])
        text1.align_to(rectangle1, LEFT).shift(RIGHT * 0.25)
        text1.align_to(rectangle1, UP).shift(DOWN * 0.25)

        text2 = Text('Line1\n\n  Line3', font="FreeMono", weight=BOLD)
        text2 = VGroup(text2[0:5], text2[5:10])
        text2.align_to(rectangle1, LEFT).shift(RIGHT * 0.25)
        text2.align_to(rectangle1, UP).shift(DOWN * 0.25)

        text3 = Text('Line1\n\n  Line3', font="FreeMono", weight=BOLD)
        text3 = VGroup(text3[0:5], Text('.', color=BLACK), text3[5:10])
        text3[1].align_to(text3[0], LEFT)
        text3.align_to(rectangle1, LEFT).shift(RIGHT * 0.25)
        text3.align_to(rectangle1, UP).shift(DOWN * 0.25)

        text4 = Text('Line1\nLine2\n  Line3', font="FreeMono", weight=BOLD)
        text4 = VGroup(text4[0:5], text4[5:10], text4[10:15])
        text4.align_to(rectangle1, LEFT).shift(RIGHT * 0.25)
        text4.align_to(rectangle1, UP).shift(DOWN * 0.25)

        text5 = Text('Line1\nLongline2\n  Line3', font="FreeMono", weight=BOLD)
        text5 = VGroup(text5[0:5], text5[5:14], text5[14:19])
        text5.align_to(rectangle1, LEFT).shift(RIGHT * 0.25)
        text5.align_to(rectangle1, UP).shift(DOWN * 0.25)


        self.play(AnimationGroup(Create(rectangle1), Create(rectangle2), Create(rectangle3), Create(text1), lag_ratio=0.25))

        self.wait(1)
        self.play(ReplacementTransform(text1, text2))
        self.play(Create(text4[1]))
        self.wait(1)
        #self.play(ReplacementTransform(text2, text3), run_time=0)
        #self.play(ReplacementTransform(text3, text4))
        self.play(ReplacementTransform(text4, text5))
        self.wait(3)

