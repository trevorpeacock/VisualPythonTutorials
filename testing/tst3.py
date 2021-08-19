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

RIGHT_PANEL_WIDTH = 5
RIGHT_PANEL_RATIO = 0.5


class ChangePhases(Enum):
    PRE_SWAP = 0
    NEW_LINE_SHUFFLE = 1
    NEW_LINE_WRITE = 2
    LINES = 3
    POST_SWAP = 4


class LinePartCreationActions(Enum):
    NEW_LINE = 0
    INSERT = 1


ChangeDefinition = namedtuple('ChangeDefinition', ['phase', 'change'])


class ProgramCodeLinePart:
    def __init__(self, new, creation_action):
        self.current = ''
        self.symbols = None
        self.new = new
        self.action = creation_action

    def get_new_code(self, no_whitespace=False):
        if no_whitespace:
            return self.new.replace(' ', '').replace('\t', '')
        return self.new

    def changes(self, symbols, line_is_new, replacement):
        changes = []
        if self.new == '':
            self.symbols.submobjects = list(reversed(self.symbols.submobjects))
            changes.append(ChangeDefinition(ChangePhases.LINES, Uncreate(self.symbols)))
        elif self.current == '':
            if line_is_new:
                changes.append(ChangeDefinition(ChangePhases.NEW_LINE_WRITE, Create(symbols)))
            else:
                changes.append(ChangeDefinition(ChangePhases.LINES, Create(symbols)))
        elif self.current == self.new:
            if replacement:
                changes.append(
                    ChangeDefinition(ChangePhases.LINES, ReplacementTransform(self.symbols, symbols)))
            else:
                changes.append(
                    ChangeDefinition(ChangePhases.NEW_LINE_SHUFFLE, ReplacementTransform(self.symbols, symbols)))
        else:
            changes.append(
                ChangeDefinition(ChangePhases.LINES, ReplacementTransform(self.symbols, symbols)))
        self.current = self.new
        self.symbols = symbols
        #print(f'"{self.current}" -> "{self.new}"', changes)
        return changes

    def split(self, index):
        current = self.current[:index], self.current[index:]
        new = self.new[:index], self.new[index:]
        no_whitespace_index = len(current[0].replace(' ', '').replace('\t', ''))
        symbols = self.symbols[:no_whitespace_index], self.symbols[no_whitespace_index:]
        parts = ProgramCodeLinePart(new[0], None), ProgramCodeLinePart(new[1], None)
        parts[0].current = current[0]
        parts[1].current = current[1]
        parts[0].symbols = symbols[0]
        parts[1].symbols = symbols[1]
        return parts


class ProgramCodeLine:
    def __init__(self, line):
        self.parts = [ProgramCodeLinePart(line, LinePartCreationActions.NEW_LINE)]
        self.new = True
        self.replacement = False
        self.symbols = None
        self.delete = False

    def get_new_code(self, no_whitespace=False):
        return ''.join([part.get_new_code(no_whitespace) for part in self.parts])

    def replace(self, old_text, new_text):
        new_parts = []
        for part in self.parts:
            code = part.get_new_code()
            lengths = [len(x) for x in code.split(old_text, 1)]
            if len(lengths) == 1:
                new_parts.append(part)
                continue
            parts = part.split(lengths[0])
            parts = [parts[0]] + list(parts[1].split(-lengths[1]))
            parts[1].new = new_text
            new_parts += [p for p in parts if p.current]
        self.parts = new_parts
        self.replacement = True

    def insert_line(self, line, pos, new_text):
        self.lines[line].insert(pos, new_text)

    def insert(self, insert_pos, new_text):
        new_parts = []
        pos = 0
        for part in self.parts:
            code = part.get_new_code()
            if pos < insert_pos < pos + len(code):
                parts = part.split(insert_pos - pos)
                parts = [parts[0], ProgramCodeLinePart(new_text, LinePartCreationActions.INSERT), parts[1]]
                new_parts += [p for p in parts if p.new]
            else:
                new_parts.append(part)
            pos += len(code)
        self.parts = new_parts
        self.replacement = True

    def changes(self, symbols):
        pos = 0
        for part in self.parts:
            text = part.get_new_code(True)
            yield from part.changes(symbols[pos:pos+len(text)], self.new, self.replacement)
            pos += len(text)
        part = ProgramCodeLinePart(self.get_new_code(), None) # replace part(s)
        part.current = part.new
        part.symbols = symbols
        self.parts = [part]
        self.new = False
        self.replacement = False


class ProgramCodeLines:
    def __init__(self, code):
        self.lines = []
        for line in code.split('\n'):
            self.lines.append(ProgramCodeLine(line))

    def get_new_code(self, no_whitespace=False):
        return '\n'.join([line.get_new_code(no_whitespace) for line in self.lines if not line.delete])

    def insert_line(self, index, line):
        self.lines.insert(index, line)

    def replace(self, line, old_text, new_text):
        self.lines[line].replace(old_text, new_text)

    def insert(self, line, pos, new_text):
        self.lines[line].insert(pos, new_text)

    def remove_line(self, line):
        self.lines[line].delete = True

    def changes(self, symbols):
        pos = 0
        new_lines = []
        for line in self.lines:
            if line.delete:
                for part in line.parts:
                    yield ChangeDefinition(ChangePhases.NEW_LINE_SHUFFLE, FadeOut(part.symbols))
                continue
            text = line.get_new_code(True)
            yield from line.changes(symbols[pos:pos+len(text)])
            pos += len(text)
            new_lines.append(line)
        self.lines = new_lines


class ProgramCode:
    def __init__(self, code):
        super().__init__()
        self.code = ProgramCodeLines(code)
        self.positioning = []

    def _gen_coloured_text_symbols(self):
        code = self.code.get_new_code()
        all_text = Text(code, font="FreeMono")
        for instruction, args, kwargs in self.positioning:
            getattr(all_text, instruction)(*args, **kwargs)
        # print(HtmlFormatter().get_style_defs('.zenburn'))
        html = highlight(code, get_lexer_by_name("python"), HtmlFormatter(style='zenburn'))
        soup = bs4.BeautifulSoup(html, features="html.parser")
        pos = 0
        for e in soup.select('div > pre')[0]:
            if isinstance(e, bs4.element.Tag):
                text = e.text
            elif isinstance(e, bs4.element.NavigableString):
                text = e
            strip_text = text.replace(' ', '').replace('\n', '').replace('\t', '')
            group = all_text[pos:pos + len(strip_text)]
            # c = random_bright_color()
            if isinstance(e, bs4.element.Tag):
                cls = e.get('class')
                if cls:
                    assert (len(cls) == 1)
                    c, w, s = {
                        'n': ('#FFFFFF', NORMAL, NORMAL),  # ???
                        'p': ('#FFFFFF', NORMAL, NORMAL),  # ???

                        'c': ('#408080', NORMAL, ITALIC),  # Comment
                        'k': ('#008000', BOLD, NORMAL),  # Keyword
                        'o': ('#666666', NORMAL, NORMAL),  # Operator
                        'ch': ('#408080', NORMAL, ITALIC),  # Comment.Hashbang
                        'cm': ('#408080', NORMAL, ITALIC),  # Comment.Multiline
                        'cp': ('#BC7A00', NORMAL, NORMAL),  # Comment.Preproc
                        'cpf': ('#408080', NORMAL, ITALIC),  # Comment.PreprocFile
                        'c1': ('#408080', NORMAL, ITALIC),  # Comment.Single
                        'cs': ('#408080', NORMAL, ITALIC),  # Comment.Special
                        'gd': ('#A00000', NORMAL, NORMAL),  # Generic.Deleted
                        'ge': ('#FFFFFF', NORMAL, ITALIC),  # Generic.Emph
                        'gr': ('#FF0000', NORMAL, NORMAL),  # Generic.Error
                        'gh': ('#000080', BOLD, NORMAL),  # Generic.Heading
                        'gi': ('#00A000', NORMAL, NORMAL),  # Generic.Inserted
                        'go': ('#888888', NORMAL, NORMAL),  # Generic.Output
                        'gp': ('#000080', BOLD, NORMAL),  # Generic.Prompt
                        'gs': ('#FFFFFF', BOLD, NORMAL),  # Generic.Strong
                        'gu': ('#800080', BOLD, NORMAL),  # Generic.Subheading
                        'gt': ('#0044DD', NORMAL, NORMAL),  # Generic.Traceback
                        'kc': ('#008000', BOLD, NORMAL),  # Keyword.Constant
                        'kd': ('#008000', BOLD, NORMAL),  # Keyword.Declaration
                        'kn': ('#008000', BOLD, NORMAL),  # Keyword.Namespace
                        'kp': ('#008000', NORMAL, NORMAL),  # Keyword.Pseudo
                        'kr': ('#008000', BOLD, NORMAL),  # Keyword.Reserved
                        'kt': ('#B00040', NORMAL, NORMAL),  # Keyword.Type
                        'm': ('#666666', NORMAL, NORMAL),  # Literal.Number
                        's': ('#BA2121', NORMAL, NORMAL),  # Literal.String
                        'na': ('#7D9029', NORMAL, NORMAL),  # Name.Attribute
                        'nb': ('#008000', NORMAL, NORMAL),  # Name.Builtin
                        'nc': ('#0000FF', BOLD, NORMAL),  # Name.Class
                        'no': ('#880000', NORMAL, NORMAL),  # Name.Constant
                        'nd': ('#AA22FF', NORMAL, NORMAL),  # Name.Decorator
                        'ni': ('#999999', BOLD, NORMAL),  # Name.Entity
                        'ne': ('#D2413A', BOLD, NORMAL),  # Name.Exception
                        'nf': ('#0000FF', NORMAL, NORMAL),  # Name.Function
                        'nl': ('#A0A000', NORMAL, NORMAL),  # Name.Label
                        'nn': ('#0000FF', BOLD, NORMAL),  # Name.Namespace
                        'nt': ('#008000', BOLD, NORMAL),  # Name.Tag
                        'nv': ('#19177C', NORMAL, NORMAL),  # Name.Variable
                        'ow': ('#AA22FF', BOLD, NORMAL),  # Operator.Word
                        'w': ('#bbbbbb', NORMAL, NORMAL),  # Text.Whitespace
                        'mb': ('#666666', NORMAL, NORMAL),  # Literal.Number.Bin
                        'mf': ('#666666', NORMAL, NORMAL),  # Literal.Number.Float
                        'mh': ('#666666', NORMAL, NORMAL),  # Literal.Number.Hex
                        'mi': ('#666666', NORMAL, NORMAL),  # Literal.Number.Integer
                        'mo': ('#666666', NORMAL, NORMAL),  # Literal.Number.Oct
                        'sa': ('#BA2121', NORMAL, NORMAL),  # Literal.String.Affix
                        'sb': ('#BA2121', NORMAL, NORMAL),  # Literal.String.Backtick
                        'sc': ('#BA2121', NORMAL, NORMAL),  # Literal.String.Char
                        'dl': ('#BA2121', NORMAL, NORMAL),  # Literal.String.Delimiter
                        'sd': ('#BA2121', NORMAL, ITALIC),  # Literal.String.Doc
                        's2': ('#BA2121', NORMAL, NORMAL),  # Literal.String.Double
                        'se': ('#BB6622', BOLD, NORMAL),  # Literal.String.Escape
                        'sh': ('#BA2121', NORMAL, NORMAL),  # Literal.String.Heredoc
                        'si': ('#BB6688', BOLD, NORMAL),  # Literal.String.Interpol
                        'sx': ('#008000', NORMAL, NORMAL),  # Literal.String.Other
                        'sr': ('#BB6688', NORMAL, NORMAL),  # Literal.String.Regex
                        's1': ('#BA2121', NORMAL, NORMAL),  # Literal.String.Single
                        'ss': ('#19177C', NORMAL, NORMAL),  # Literal.String.Symbol
                        'bp': ('#008000', NORMAL, NORMAL),  # Name.Builtin.Pseudo
                        'fm': ('#0000FF', NORMAL, NORMAL),  # Name.Function.Magic
                        'vc': ('#19177C', NORMAL, NORMAL),  # Name.Variable.Class
                        'vg': ('#19177C', NORMAL, NORMAL),  # Name.Variable.Global
                        'vi': ('#19177C', NORMAL, NORMAL),  # Name.Variable.Instance
                        'vm': ('#19177C', NORMAL, NORMAL),  # Name.Variable.Magic
                        'il': ('#666666', NORMAL, NORMAL),  # Literal.Number.Integer.Long
                    }[cls[0]]
                    # print(c, self.code[pos:pos+len(text)])
                    group.set_color(c)
                    group.set_weight(w)
                    group.set_slant(s)
            pos += len(strip_text)
        return all_text

    def insert_line(self, before_line, text):
        self.code.insert_line(before_line, ProgramCodeLine(text))

    def replace(self, line, old_text, new_text):
        self.code.replace(line, old_text, new_text)

    def insert(self, line, pos, new_text):
        self.code.insert(line, pos, new_text)

    def remove_line(self, line):
        self.code.remove_line(line)

    def changes(self):
        phases = defaultdict(list)
        for phase, change in self.code.changes(self._gen_coloured_text_symbols()):
            phases[phase].append(change)
        for phase in phases:
            phases[phase] = AnimationGroup(*phases[phase])
        changes = []
        for phase in sorted(phases.keys(), key=lambda p: p.value):
            changes.append(phases[phase])
        return AnimationGroup(*changes, lag_ratio=1)

    def align_to(self, *args, **kwargs):
        self.positioning.append(('align_to', args, kwargs))
        return self

    def shift(self, *args, **kwargs):
        self.positioning.append(('shift', args, kwargs))
        return self


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
