from manim import *
from manimcoder import *

class CircleWithContent(VGroup):
    def __init__(self):
        super().__init__()
        self.circle = Circle()
        self.content = Text("hello!")
        self.add(self.circle)
        self.add(self.content)
        self.content.add_updater(lambda d: d.align_to(self.circle.get_center(), UP+LEFT))
        #content.align_to(self.circle.get_center(), UP+LEFT)

    def clear_content(self):
        self.remove(self.content)
        self.content = None



class MovingFrameBox(Scene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.oldhighlighting = None
        self.highlighting = None
        self.oldrunarror = None
        self.newrunarrow = None

    def construct(self):
        if False:
            program = CodeDisplayWindow()
            self.play(Create(program))
            self.play(ApplyMethod(program.set_height, 5))
            self.play(ApplyMethod(program.stretch_to_fit_width, 5, {'about_edge': LEFT}))
            self.play(Uncreate(program))

        if False:
            program = CodeDisplayWindowColumn()
            program.show_second_panel(True)
            program.set_width(10)
            program.shift(RIGHT)
            self.play(Create(program))
            #self.play(ApplyMethod(program.show_second_panel, False))
            self.play(ApplyMethod(program.show_second_panel, True))
            self.play(ApplyMethod(program.set_width, 5))
            program2 = CodeDisplayWindowColumn()
            program2.show_second_panel(True)
            program2.next_to(program, RIGHT, buff=0.1).align_to(program, UP)
            program2.set_width(5)
            self.play(Create(program2))
            self.play(Uncreate(program))

        if False:
            program = CodeDisplayWindowColumn()
            #program2 = CodeDisplayWindowColumn()

            program.show_second_panel(1)
            program.set_width(5)
            #program2.set_width(5)
            #program2.next_to(program, RIGHT, buff=0.1).align_to(program, UP)
            #program2.show_second_panel(1)

            self.play(
                Create(program),
            #    Create(program2),
            )
            self.wait()
            self.play(Uncreate(program))

        if False:
            program = CodeDisplay()
            program.set_panels(PANEL_CODE+PANEL_VARS+PANEL_TRACE+PANEL_OUTPUT)
            self.play(Create(program))
            self.wait()
            self.play(ApplyMethod(program.set_panels, PANEL_CODE))
            self.play(ApplyMethod(program.set_panels, PANEL_CODE+PANEL_VARS+PANEL_TRACE+PANEL_OUTPUT))
            self.wait()
            self.play(ApplyMethod(program.panel_side.set_width, 5))
            self.play(Uncreate(program))

        if False:
            program = CodeDisplay()
            self.play(Create(program))
            self.wait()
            self.play(ApplyMethod(program.set_panels, PANEL_CODE+PANEL_VARS+PANEL_TRACE+PANEL_OUTPUT))
            self.play(ApplyMethod(program.set_panels, PANEL_CODE))
            self.wait()
            self.play(Uncreate(program))

        if False:
            program = CodeDisplay()
            program.set_panels(PANEL_CODE+PANEL_VARS+PANEL_TRACE+PANEL_OUTPUT)
            self.play(Create(program))
            self.play(ApplyMethod(program.set_side_panel_width, 7))
            self.play(
                ApplyMethod(program.panel_main.set_bottom_panel_height, 6),
                ApplyMethod(program.panel_side.set_bottom_panel_height, 4),
            )
            self.play(
                ApplyMethod(program.panel_main.set_bottom_panel_height, 1),
                ApplyMethod(program.panel_side.set_bottom_panel_height, 2),
            )
            self.play(Uncreate(program))

        if False:
            code = ProgramCode("aa", lexer='python')
            code.insert(0, 1, "print('hello')")
            assert(code.code.get_new_code()=="aprint('hello')a")

            code = ProgramCode("a", lexer='python')
            code.insert(0, 0, "print('hello')")
            assert(code.code.get_new_code()=="print('hello')a")

            code = ProgramCode("a", lexer='python')
            code.insert(0, 1, "print('hello')")
            assert(code.code.get_new_code()=="aprint('hello')")

            code = ProgramCode("", lexer='python')
            code.insert(0, 0, "print('hello')")
            assert(code.code.get_new_code()=="print('hello')")

            code = ProgramCode("('hello')", lexer='python')
            code.insert(0, 0, 'print')
            code.insert(0, 5, "_test")
            assert(code.code.get_new_code()=="print_test('hello')")

        if False:
            code = ProgramCode("for i in range(4):\n  print([1,2,3,4])", lexer='python')
            self.play(Create(code))
            self.play(code.changes())
            code.replace_code("def test():\n  return 'testing'")
            self.play(code.changes())
            self.wait()

        if False:
            program = CodeDisplay()
            program.set_panels(PANEL_CODE+PANEL_VARS+PANEL_TRACE+PANEL_OUTPUT)
            code = ProgramCode("for i in range(4):\n  print([1,2,3,4])", lexer='python')
            code.add_updater(lambda d: d.align_to(program.panel_side.panel_top.title_bar, DOWN+LEFT).shift((DOWN+RIGHT) * 0.1))

            self.play(Create(code))
            self.play(Create(program), code.changes(), lag_time=0)
            self.play(ApplyMethod(program.set_panels, PANEL_CODE))
            self.play(ApplyMethod(program.set_panels, PANEL_CODE+PANEL_VARS+PANEL_TRACE+PANEL_OUTPUT))
            self.wait()

        if False:
            rectangle1 = Rectangle(width=10, height=4).shift(
                (LEFT+UP)*1.5)
            code1 = ProgramCode("""for i in range(4): # loop\n  print([1, 2, 3, 4])""", lexer='python')
            code1.align_to(rectangle1, LEFT).shift(RIGHT * 0.25)
            code1.align_to(rectangle1, UP).shift(DOWN * 0.25)

            self.play(Create(rectangle1), Create(code1), code1.changes())

            for _ in range(2):
                code1.insert_line(1, '  print("asdf")')
                self.play(code1.changes())
                code1.replace(0, 'range(4)', '[0, 1, 2, 3]')
                self.play(code1.changes())
                code1.replace(0, ']:', 'x')
                self.play(code1.changes())
                code1.replace(0, 'loop', 'looping')
                self.play(code1.changes())
                code1.replace(0, 'looping', 'loop')
                self.play(code1.changes())
                code1.replace(0, 'for i', 'x')
                code1.replace(0, '0, 1, 2, 3', 'x')
                self.play(code1.changes())
                code1.replace(1, 'asdf', '')
                self.play(code1.changes())
                code1.insert(1, 9, 'asdf')
                # code1.replace(1, '""', '"asdf"')
                self.play(code1.changes())
                code1.replace(0, 'x', 'for i')
                code1.replace(0, '[xx', 'range(4):')
                self.play(code1.changes())
                code1.remove_line(1)
                self.play(code1.changes())
            self.wait(1)

        if True:
            program = CodeDisplay()
            program.set_panels(PANEL_CODE+PANEL_VARS)
            program.vars.var_length = 1
            self.play(Create(program), lag_time=0)
            self.play(ApplyMethod(program.set_panels, PANEL_CODE))
            self.play(ApplyMethod(program.set_panels, PANEL_CODE+PANEL_VARS))
            program.vars.set_var('i', '3')
            self.play(program.vars.changes())
            program.vars.set_var('b', '4')
            self.play(program.vars.changes())
            program.vars.set_var('i', '4')
            self.play(program.vars.changes())
            program.vars.set_var('c', '0')
            self.play(program.vars.changes())
            program.vars.set_var('d', '0')
            self.play(program.vars.changes())
            program.vars.remove_var('b')
            self.play(program.vars.changes())
            program.vars.remove_var('i')
            self.play(program.vars.changes())
            program.vars.remove_var('d')
            self.play(program.vars.changes())
            program.vars.set_var('i', '3')
            self.play(program.vars.changes())
            program.vars.add_scope('function')
            self.play(program.vars.changes())
            program.vars.set_var('i', '3')
            self.play(program.vars.changes())
            self.play(ApplyMethod(program.set_panels, PANEL_CODE))
            #self.wait() # TODO: i = 10 causes double-side unless pause is placed here (or above or below)
            self.play(ApplyMethod(program.set_panels, PANEL_CODE+PANEL_VARS))
            program.vars.set_var('i', '10', scope='')
            self.play(program.vars.changes())
            program.vars.set_var('x', '3')
            self.play(program.vars.changes())
            program.vars.add_scope('subfunction')
            self.play(program.vars.changes())
            program.vars.set_var('i', '3')
            self.play(program.vars.changes())
            program.vars.remove_scope()
            self.play(program.vars.changes())
            program.vars.remove_scope()
            self.play(program.vars.changes())
            program.vars.add_scope('function2')
            self.play(program.vars.changes())
            program.vars.set_var('i', '3')
            self.play(program.vars.changes())
            program.vars.remove_scope()
            self.play(program.vars.changes())
            self.wait(4)

        if False:
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
