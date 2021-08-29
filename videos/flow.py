from manim import *
from manimcoder import *


class ProgramFlow(Scene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.oldhighlighting = None
        self.highlighting = None
        self.oldrunarror = None
        self.newrunarrow = None

    def construct(self):
        program = CodeDisplay()
        self.program = program
        program.vars.var_length = 1
        program.set_panels(PANEL_CODE)
        program.code.content.replace_code("for i in range(4):\n  print(i)")

        self.play(Create(program), lag_time=0)

        self.update_runarrow(0)
        self.play(self.runarrow())

        self.update_highlight(program.code.content.code.lines[0].symbols_by_search('range(4)'))
        self.play(self.highlight())

        self.update_highlight(None)
        program.code.content.replace(0, 'range(4)', '[0, 1, 2, 3]')
        self.play(self.highlight(), program.code.content.changes(), lag_ratio=0) # not happening simulteneously?

        self.update_highlight(program.code.content.code.lines[0].symbols_by_search('[0, 1, 2, 3]'))
        self.play(self.highlight())

        self.update_highlight(program.code.content.code.lines[0].symbols_by_search('i'))
        self.play(self.highlight())
        self.update_highlight(None)
        self.play(self.highlight())

        self.update_highlight(program.code.content.code.lines[0].symbols_range(10, 11))
        self.play(self.highlight())

        self.update_highlight(program.code.content.code.lines[0].symbols_by_search('i'))
        program.code.content.replace(0, 'i', '0')
        self.play(program.code.content.changes(), self.highlight())
        program.code.content.replace(0, '0', 'i')

        self.play(ApplyMethod(program.set_panels, PANEL_CODE+PANEL_VARS))

        self.play(ApplyMethod(program.vars.set_var, 'i', '0'))

        program.vars.set_var('i', '0')
        vc = program.vars.content.changes()
        self.update_highlight(program.vars.symbols_line('i'))
        self.play(program.code.content.changes(), vc, self.highlight())

        self.update_highlight(program.vars.symbols_value('i'))
        self.play(self.highlight())

        self.update_runarrow(1)
        self.play(self.runarrow())

        self.update_highlight(program.code.content.code.lines[1].symbols_range(8, 9))
        program.code.content.replace(1, '(i', '(0')
        self.play(program.code.content.changes(), self.highlight())

        program.code.content.replace(1, '(0', '(i')
        self.play(program.code.content.changes())

        self.update_highlight(program.code.content.code.lines[1].symbols)
        self.play(self.highlight())

        self.play(ApplyMethod(program.set_panels, PANEL_CODE+PANEL_VARS+PANEL_OUTPUT))

        self.update_highlight(program.code.content.code.lines[1].symbols)
        self.play(self.highlight())

        program.output.add_line('0')
        oc = program.output.content.changes()
        self.update_highlight(program.output.content.code.lines[-1].symbols)
        self.play(oc, self.highlight())

        self.update_runarrow(0)
        self.update_highlight(None)
        self.play(self.highlight(), self.runarrow())

        self.update_highlight(program.code.content.code.lines[0].symbols_by_search('[0, 1, 2, 3]'))
        self.play(self.highlight())

        self.update_highlight(program.code.content.code.lines[0].symbols_by_search('1'))
        self.play(self.highlight())

        self.update_highlight(program.vars.symbols_value('i'))
        program.vars.set_var('i', '1')
        self.play(program.vars.content.changes(), self.highlight())

        self.update_highlight(program.code.content.code.lines[0].symbols_by_search('i'))
        self.play(self.highlight())

        self.update_highlight(program.code.content.code.lines[1].symbols_range(8, 9))
        self.update_runarrow(1)
        self.play(self.highlight(), self.runarrow())

        program.output.add_line('1')
        oc = program.output.content.changes()
        self.update_highlight(program.output.content.code.lines[-1].symbols)
        self.play(oc, self.highlight())

        self.update_highlight(None)
        self.play(self.highlight())

        self.update_runarrow(0)
        self.play(self.runarrow())

        program.code.content.replace(0, '[0, 1, 2, 3]', 'range(4)')
        self.play(program.code.content.changes())





        self.update_highlight(program.code.content.code.lines[0].symbols_by_search('range(4)'))
        self.play(self.highlight())

        self.update_highlight(program.vars.symbols_value('i'))
        program.vars.set_var('i', '2')
        self.play(self.highlight(), program.vars.content.changes())

        self.update_highlight(None)
        self.play(self.highlight())

        self.update_runarrow(1)
        self.play(self.runarrow())

        self.update_highlight(program.code.content.code.lines[1].symbols_range(8, 9))
        self.play(self.highlight())

        program.output.add_line('2')
        oc = program.output.content.changes()
        self.update_highlight(program.output.content.code.lines[-1].symbols)
        self.play(oc, self.highlight())

        self.update_highlight(None)
        self.play(self.highlight())

        self.update_runarrow(0)
        self.play(self.runarrow())

        program.vars.set_var('i', '3')
        self.play(program.vars.content.changes(),
                  Flash(program.vars.symbols_value('i'), flash_radius=0.6))

        self.update_runarrow(1)
        self.play(self.runarrow())

        program.output.add_line('3')
        self.play(program.output.content.changes())

        self.update_runarrow(None)
        self.play(self.runarrow())

        self.wait()

        self.play(Uncreate(program))

        self.wait()

    def update_highlight(self, obj):
        self.oldhighlighting = self.highlighting
        self.highlighting = SurroundingRectangle(obj) if obj is not None else None

    def highlight(self):
        if self.oldhighlighting is None and self.highlighting is None:
            raise Exception
        if self.oldhighlighting is not None and self.highlighting is not None:
            return ReplacementTransform(self.oldhighlighting, self.highlighting)
        if self.highlighting:
            return Create(self.highlighting)
        return FadeOut(self.oldhighlighting)

    def update_runarrow(self, obj):
        self.oldrunarrow = self.newrunarrow
        if obj is None:
            self.newrunarrow = None
        else:
            start = UP * self.program.code.content.code.lines[obj].symbols.get_center()[1]
            start += RIGHT * self.program.panel_main.panel_top.rectangle.get_center()[0] + LEFT * self.program.panel_main.panel_top.rectangle.width / 2
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
