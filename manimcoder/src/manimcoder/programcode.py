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


class ChangePhases(Enum):
    PRE_SWAP = 0
    NEW_LINE_SHUFFLE = 1
    NEW_LINE_WRITE = 2
    LINES = 3
    POST_SWAP = 4


class LinePartCreationActions(Enum):
    NEW_LINE = 0
    INSERT = 1


ChangeDefinition = namedtuple('ChangeDefinition', ['phase', 'change', 'new_elements'])


class ProgramCodeLinePart:
    def __init__(self, new, creation_action):
        self.current = ''
        self.symbols = VGroup()
        self.new = new
        self.action = creation_action

    def get_new_code(self, no_whitespace=False):
        if no_whitespace:
            return self.new.replace(' ', '').replace('\t', '')
        return self.new

    def changes(self, symbols, line_is_new, replacement):
        changes = []
        if self.new == '':
            if self.current != '':
                self.symbols.submobjects = list(reversed(self.symbols.submobjects))
                changes.append(ChangeDefinition(ChangePhases.LINES, Uncreate(self.symbols), None))
        elif self.current == '':
            if line_is_new:
                changes.append(ChangeDefinition(ChangePhases.NEW_LINE_WRITE, Create(symbols), symbols))
            else:
                changes.append(ChangeDefinition(ChangePhases.LINES, Create(symbols), symbols))
        elif self.current == self.new:
            if replacement:
                changes.append(
                    ChangeDefinition(ChangePhases.LINES, ReplacementTransform(self.symbols, symbols), symbols))
            else:
                changes.append(
                    ChangeDefinition(ChangePhases.NEW_LINE_SHUFFLE, ReplacementTransform(self.symbols, symbols), symbols))
        else:
            changes.append(
                ChangeDefinition(ChangePhases.LINES, ReplacementTransform(self.symbols, symbols), symbols))
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
            if lengths[1]==0:
                parts = list(parts)
            else:
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
        if insert_pos == 0:
            new_parts.append(ProgramCodeLinePart(new_text, LinePartCreationActions.INSERT))
        for part in self.parts:
            code = part.get_new_code()
            if pos < insert_pos <= pos + len(code):
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
        self.symbols = symbols
        self.parts = [part]
        self.new = False
        self.replacement = False

    def symbols_range(self, start, stop):
        symbols = []
        code = self.get_new_code()
        if stop < 0:
            stop = len(code) + stop + 1
        pos = 0
        for i, c in enumerate(code):
            if start <= i < stop:
                symbols.append(self.symbols[pos])
            pos += len(c.strip(' ').strip('\t'))
        return VGroup(*symbols)

    def symbols_by_search(self, text):
        index = self.get_new_code().index(text)
        if index == -1:
            raise IndexError()
        return self.symbols_range(index, index + len(text))

class ProgramCodeLines:
    def __init__(self, code):
        self.lines = []
        self.add_code(code)

    def add_code(self, code):
        for line in code.split('\n'):
            self.lines.append(ProgramCodeLine(line))

    def get_new_code(self, no_whitespace=False):
        return '\n'.join([line.get_new_code(no_whitespace) for line in self.lines if not line.delete])

    def insert_line(self, index, line):
        self.lines.insert(index, line)

    def append_line(self, line):
        self.lines.append(line)

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
                    yield ChangeDefinition(ChangePhases.NEW_LINE_SHUFFLE, FadeOut(part.symbols), None)
                continue
            text = line.get_new_code(True)
            yield from line.changes(symbols[pos:pos+len(text)])
            pos += len(text)
            new_lines.append(line)
        self.lines = new_lines

    def symbols(self):
        for line in self.lines:
            yield line.symbols


class HighlightedCode(Text):
    def __init__(self, code, *args, **kwargs):
        self.lexer = kwargs.pop('lexer', 'text')
        self.highlight_style = kwargs.pop('style', 'vim')
        super().__init__(code, *args, **kwargs)
        html = highlight(code, self.lexer, HtmlFormatter(style=self.highlight_style))
        soup = bs4.BeautifulSoup(html, features="html.parser")
        pos = 0
        for e in soup.select('div > pre')[0]:
            if isinstance(e, bs4.element.Tag):
                text = e.text
            elif isinstance(e, bs4.element.NavigableString):
                text = e
            strip_text = text.replace(' ', '').replace('\n', '').replace('\t', '')
            group = self[pos:pos + len(strip_text)]
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

class ProgramCode(VMobject):
    def __init__(self, code, lexer='text', highlight_style='zenburn'):
        super().__init__()
        self.code = ProgramCodeLines(code)
        self.lexer = get_lexer_by_name('text') if lexer is None else lexer
        if isinstance(self.lexer, str):
            self.lexer = get_lexer_by_name(self.lexer)
        self.highlight_style = highlight_style
        self.reference_dot = Dot(radius=0)
        self.add(self.reference_dot)
        self.all_text = None

    def _gen_coloured_text_symbols(self):
        code = self.code.get_new_code()
        all_text = HighlightedCode(code, font="FreeMono", lexer=self.lexer, style=self.highlight_style).scale(0.8)
        self.all_text = all_text
        if len(all_text):
            all_text.align_to(self.reference_dot, UP + LEFT)
        # print(HtmlFormatter().get_style_defs('.zenburn'))
        return all_text

    def insert_line(self, before_line, text):
        self.code.insert_line(before_line, ProgramCodeLine(text))

    def append_line(self, line):
        self.code.lines.append(ProgramCodeLine(line))

    def replace(self, line, old_text, new_text):
        self.code.replace(line, old_text, new_text)

    def insert(self, line, pos, new_text):
        self.code.insert(line, pos, new_text)

    def remove_line(self, line):
        self.code.remove_line(line)

    def replace_code(self, new_code):
        for lineno, _ in enumerate(self.code.lines):
            self.remove_line(lineno)
        self.code.add_code(new_code)

    def changes(self):
        phases = defaultdict(list)
        for phase, change, symbols in self.code.changes(self._gen_coloured_text_symbols()):
            if symbols:
                symbols.relative_position = self.reference_dot.get_center() - symbols.get_center()
                symbols.add_updater(lambda d: d.move_to(self.reference_dot.get_center() - d.relative_position))
            phases[phase].append(change)
        for phase in phases:
            phases[phase] = AnimationGroup(*phases[phase])
        changes = []
        for phase in sorted(phases.keys(), key=lambda p: p.value):
            changes.append(phases[phase])
        return AnimationGroup(*changes, lag_ratio=0) #TODO: set time of irrelevant changes to 0, so lag time can be set to 1 without causing pauses

    def symbols(self):
        return VGroup(*self.code.symbols())
