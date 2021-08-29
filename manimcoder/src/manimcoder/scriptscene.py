from manim import *
import re

starting_whitespace_re = re.compile(r"^( *)")
ignore_start_end_blanks = re.compile(r"^([ \t\r\f\v]*\n)*(.*?)(\n[ \t\r\f\v]*)*$", flags=re.DOTALL)

class ScriptScene(Scene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.script_lines = []

    def script(self, text, *args, **kwargs):
        text = ignore_start_end_blanks.match(text).group(2)
        text = text.replace('\t', '    ').split('\n')
        spaces = [len(starting_whitespace_re.match(l).group(1)) for l in text if l.strip()]
        spaces = min(spaces) if spaces else 0
        text = [l[spaces:] for l in text]
        self.script_lines.append('\n'.join(text))
        if args or kwargs:
            self.play(*args, **kwargs)

    def render(self, *args, **kwargs):
        render = super().render(*args, **kwargs)
        print('\n\n'.join(['='*20] + self.script_lines + ['='*20]))
        return render
