from manim import *
from manimcoder import *


class HighlightBox(VGroup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.oldhighlighting = None
        self.highlighting = None

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


class FunctionIntro(ScriptScene):
    def construct(self):
        self.wait(17)
        self.script("""
        A function, more generally known as a "subroutine", is a set of instructions that are grouped together, usually designed to perform a specific task.
        
        We're talking here about procedural programming languages, a type of imperative language, where instructions run in a specific order, as opposed to declarative languages, or what you might be used to in mathematics, where a function defines a relationship between two sets of values.
        """)
        program_text = VGroup(Text("program:"), Text("."), Text("."), Text("."), Text("."), Text("."), Text("."), Text("."), Text("."), Text(".")).arrange(direction=DOWN, buff=0.5).set_color(YELLOW)
        function_text = VGroup(Text("function():"), Text("."), Text("."), Text("."), Text("."), Text("."), Text(".")).arrange(direction=DOWN, buff=0.5).set_color(YELLOW).scale(0.7)
        function_text.shift(RIGHT*4 + UP)
        program_arrow = Arrow(
            start=program_text[1],
            end=program_text[-1],
            buff=0,
        ).shift(LEFT)
        self.play(Create(program_text), Create(program_arrow))
        self.script("""
        Most people learning a programming language for the first time will be learning a procedural language such as python.
        """)
        self.script("""
        That usual step by step order of instructions can be interrupted by calling a function.

        When a function is called, instead of executing the next instruction of your program, the first instruction of the function will be executed.
        """)
        self.wait(27)
        function_call_arrow = Arrow(
            start=program_text[5],
            end=function_text[1],
        )
        function_return_arrow = Arrow(
            start=function_text[-1],
            end=program_text[6],
        )
        self.play(FadeOut(program_arrow), Create(function_text))
        self.play(AnimationGroup(Create(function_call_arrow), Create(function_return_arrow), lag_ratio=0.5))
        self.play(FadeOut(program_text), FadeOut(function_text), FadeOut(function_call_arrow), FadeOut(function_return_arrow))
        self.wait()
        self.script("""
        The instructions inside the function will be run in order, much as if it was its own program.
        Only when the functions instructions are complete, will the instructions in the main program continue to run.
        
        There might be many builtin functions in python you already know. (print, len, min, sum, sorted)

        Functions are often designed so that they can be called several times, allowing shorter programs by grouping commonly used sets of instructions.
        
        Functions can also be used simply to group instructions to make a program more readable.
        """)
        self.wait()


class ProgramFlow(ScriptScene):
    def construct(self):
        self.wait(4)
        self.script("""
        Lets take a look at how program flow is affected by functions.
        
        Take this simple program, that prints the words one two and three.
        """)
        program = CodeDisplay()
        program.vars.var_length = 1
        program.set_panels(PANEL_CODE)
        program.code.content.replace_code("""print("one")\nprint("two")\nprint("three")""")
        self.play(Create(program))

        self.script("""
        This behaves just as you might expect. Python will process each print statement in turn, and our output shows one two and three.
        """)
        self.wait(5)
        self.play(ApplyMethod(program.set_panels, PANEL_CODE+PANEL_OUTPUT))
        program.code.update_runarrow(0)
        self.play(program.code.runarrow())
        program.output.add_line('one')
        self.play(program.output.content.changes())
        program.code.update_runarrow(1)
        self.play(program.code.runarrow())
        program.output.add_line('two')
        self.play(program.output.content.changes())
        program.code.update_runarrow(2)
        self.play(program.code.runarrow())
        program.output.add_line('three')
        self.play(program.output.content.changes())
        program.code.update_runarrow(None)
        self.play(program.code.runarrow())
        self.wait(1)
        self.script("""
        Lets add a simple function. We'll talk in more detail about defining functions, for now just know that the def keyword indicates to python we want to create a function
        """)
        program.code.content.replace_code("""def my_function():\n   print("two")\n\nprint("one")\nmy_function()\nprint("three")""")
        program.output.clear_lines()
        self.play(program.code.content.changes(), program.output.content.changes())
        self.script("""
        On initial reading of this program, you might expect the print statements to run in order, printing two, one, three, but remember that functions interrupt the normal program flow.
        """)
        self.wait(11)
        program.code.update_runarrow(1)
        self.play(program.code.runarrow())
        program.code.update_runarrow(3)
        self.play(program.code.runarrow())
        program.code.update_runarrow(5)
        self.play(program.code.runarrow())
        program.code.update_runarrow(None)
        self.play(program.code.runarrow())
        self.script("""
        When python processes this program it first sees our function definition, indicated by def. Python does not not run the instructions here in the way it would run a simple program, rather it simply remembers these instructions for later.
        """)
        self.wait(6)
        program.code.update_runarrow(0)
        self.play(program.code.runarrow())
        self.script("""
        Next, python executes our first print statement, outputting one just as we would expect.
        """)
        self.wait(8)
        program.code.update_runarrow(3)
        self.play(program.code.runarrow())
        program.output.add_line('one')
        self.play(program.output.content.changes())
        self.script("""
        Next python encounters the name of our function. It remembers this point in the program, like a bookmark to come back to later, and now starts to execute our function
        """)
        self.wait(5)
        program.code.update_runarrow(4)
        self.play(program.code.runarrow())
        program.code.update_runarrow(0)
        self.play(program.code.runarrow())
        self.script("""
        The instruction inside our function is as straightforward as it looks, and outputs the word two.
        """)
        self.wait(7)
        program.code.update_runarrow(1)
        self.play(program.code.runarrow())
        program.output.add_line('two')
        self.play(program.output.content.changes())
        self.script("""
        Having completed all instructions in the function, python returns to the point it left before running the function, and continues with the next and final line, outputting three.
        """)
        self.wait(17)
        program.code.update_runarrow(4)
        self.play(program.code.runarrow())
        program.code.update_runarrow(5)
        self.play(program.code.runarrow())
        program.output.add_line('three')
        self.play(program.output.content.changes())
        program.code.update_runarrow(None)
        self.play(program.code.runarrow())
        self.script("""
        I'm sure we can agree that in this simple situation, using a function is an unnecessary over-complication. Lets explore how we can use a function to do a more useful calculation for us.
        """)
        self.wait(15)
        self.play(Uncreate(program))
        self.wait()


class FunctionDefinition(ScriptScene):
    def construct(self):
        highlight = HighlightBox()
        self.script("""
        To do that lets look first more closely at how we define a function in python.
        
        The essential python syntax is the def keyword, a function name, a set of round brackets, and a colon.
        """)
        self.wait(4)
        code = ProgramCode('def function_name():', lexer='python')
        code.move_to(LEFT*Text('def function_name(data):', font='FreeMono').scale(0.8).width/2)
        cc = code.changes()
        self.play(cc)
        self.script("""
        A function can take in data through arguments, provided between the brackets, and it can return data using a return statement inside the function body.
        """)
        self.wait(10)
        code.insert(0, 18, 'data')
        cc = code.changes()
        self.play(cc)

        self.wait(2)
        code.append_line('  return data')
        cc = code.changes()
        self.play(cc)

        self.wait(1)
        self.play(Uncreate(code), Uncreate(code.all_text))
        self.script("""
        Now lets look at a simple real world example.
        """)
        self.wait(1)
        program = CodeDisplay()
        program.code.content.text_scale = 0.7
        program.vars.var_length = 12
        program.set_panels(PANEL_CODE)
        self.play(Create(program))
        self.script("""
        A rice farmer needs to know how long their crop will take to grow and, the rice grains to dry out, and be ready for harvest.
        """)
        self.wait(4)
        program.code.content.replace_code("""def growing_days():""")
        self.play(program.code.content.changes())
        self.script("""
        The biggest factor determining growth rate of rice is the average temperature the plant experiences while maturing.
        """)
        self.wait(4)
        program.code.content.insert(0, 17, 'temperature')
        self.play(program.code.content.changes())
        self.script("""
        At a typical 24 degrees Celsius, a grower might expect a crop to take 130 days from sewing to planting.
        """)
        self.wait(9)
        program.code.content.append_line('   days = 130')
        self.play(program.code.content.changes())
        self.script("""
        That time would shorten as the temperature increases, and lengthen as the temperature decreases.
        """)
        self.wait(5)
        program.code.content.replace(1, '130', '130 - (temperature-24) * 6') # days = 274 - temperature * 6
        self.play(program.code.content.changes())
        self.script("""
        Another factor is the variety of rice, with many varieties following this basic formula, but some varieties, known as short season varieties, taking about 5 days fewer to mature.
        """)
        self.wait(5)
        program.code.content.insert(0, 28, ', crop_season')
        self.play(program.code.content.changes())

        self.wait(8)
        program.code.content.append_line("   if crop_season == 'short':")
        program.code.content.append_line("      return days - 5")
        program.code.content.append_line("   return days")
        self.play(program.code.content.changes())
        self.script("""
        Here is an example program including our function to calculate rice growth.
        """)
        """
        def growing_days(temperature, crop_season):
           days = 274 - temperature * 6
           days = 130 - (temperature-24) * 6
           if crop_season == 'short':
              return days - 5
           return days

        harvest = growing_days(24.5, 'short')
        """
        self.wait(4)
        program.code.content.replace(1, '130 - (temperature-24) * 6', '274 - temperature * 6')
        program.code.content.append_line("")
        program.code.content.append_line("harvest = growing_days(24.5, 'short')")
        self.play(program.code.content.changes())
        self.script("""
        Lets read this line by line just as python would.
        
        Just as in the previous example, python first encounters our function definition.
        """)
        self.wait(8)
        program.code.update_runarrow(0)
        self.play(program.code.runarrow())
        self.script("""
        Python doesn't execute any code inside the function, it only checks that the code valid, syntactically correct python code, and them remembers those instrucitons for later.
        
        Python knows all these lines are part of the function because they are all indented. The spaces at the start of each line group these instructions inside the function.
        """)
        self.wait(17)
        rectangle = Rectangle(
            height=program.code.content.code.lines[4].symbols.get_center()[1] - program.code.content.code.lines[0].symbols.get_center()[1],
            width=program.code.content.code.lines[0].symbols[0:3].width
        ).next_to(program.code.content.code.lines[0].symbols, DOWN, buff=0).align_to(program.code.content.code.lines[0].symbols, LEFT)
        self.play(GrowFromCenter(rectangle))
        self.script("""
        The function ends when python encounters the first line of code that is no longer indented.
        """)
        self.wait(9)
        arrow = Arrow(
            start=program.code.content.code.lines[0].symbols[1],
            end=program.code.content.code.lines[6].symbols[1],
        )
        self.play(FadeOut(rectangle), Create(arrow))
        self.script("""
        That next line, is our very simple program.
        """)
        self.wait(3)
        program.code.update_runarrow(6)
        self.play(program.code.runarrow(), FadeOut(arrow))
        self.script("""
        It calls our function to calculate the number of days our rice crop sound grow for, given a particular temperature and variety, and stores the result.

        We start on the right with the function call, passing the number 24.5 and the string "short" to our function.
        """)
        self.wait(13)
        highlight.update_highlight(program.code.content.code.lines[6].symbols_range(10, -1))
        self.play(highlight.highlight())
        self.script("""
        At this point python stops running our program, and begins executing our function.
        """)
        self.wait(9)
        highlight.update_highlight(None)
        program.code.update_runarrow(0)
        self.play(highlight.highlight(), program.code.runarrow(), FadeOut(arrow))
        self.script("""
        This function defines two arguments, or parameters, pieces of information passed into the function.
        
        Within the function, this data is given the variable names specified in the function definition. So here temperature contains the value 24.5 and crop_season contains the string "short".
        """)
        self.wait(17)
        program.code.content.replace(0, 'temperature', "24.5       ")
        self.play(program.code.content.changes())

        self.wait(2)
        program.code.content.replace(0, 'crop_season', "'short'    ")
        self.play(program.code.content.changes())

        self.wait(2)
        program.code.content.replace(0, "24.5       , 'short'    ", 'temperature, crop_season')
        self.play(program.code.content.changes())
        self.script("""
        Python executes the first line of our function, substituting in the value 24.5 for temperature, and calculating days to be 127.
        """)
        self.wait(2)
        program.code.update_runarrow(1)
        self.play(program.code.runarrow())

        self.wait(2)
        program.code.content.replace(1, 'temperature', '24.5')
        self.play(program.code.content.changes())

        self.wait(2)
        program.code.content.replace(1, '274 - 24.5 * 6', '127')
        self.play(program.code.content.changes())
        self.script("""
        The next line tests the value stored in crop_season, to see if it matches the value "short".
        """)
        self.wait(4)
        program.code.update_runarrow(2)
        self.play(program.code.runarrow())
        self.script("""
        In this case it does, so python begins running the block defined by the if statement.
        """)
        self.wait(3)
        program.code.update_runarrow(3)
        self.play(program.code.runarrow())
        self.script("""
        Here we encounter a return statement.
        
        Return statements tell python to stop executing the function, and return to the point in the program where the function was run.
        
        Return statements are not required, and as you saw in the last example, the function returned automatically when it ran out of instructions.
        
        In this case however, we want our function to return some useful information, and so we provide that after our return statement.
        
        Python evaluates this expression, taking the value of day, subtracting five, and exits the function.
        """)
        self.wait(33)
        program.code.content.replace(3, 'days', '127')
        self.play(program.code.content.changes())
        self.wait(2)
        program.code.content.replace(3, '127 - 5', '122')
        self.play(program.code.content.changes())
        self.script("""
        If the value of crop_season had been different, python would not have branched to the return in this if block, and instead would have executed this second return statement, which simply returns the value of days.
        """)
        self.wait(10)
        program.code.update_runarrow(4)
        self.play(program.code.runarrow())
        self.script("""
        Having completed execution of the function, python returns to this line, which it had not finished executing.
        """)
        self.wait(8)
        program.code.update_runarrow(6)
        self.play(program.code.runarrow())
        self.script("""
        The value returned by the function can now be used to allocate to the harvest variable.
        """)
        self.wait(5)
        program.code.content.replace(6, "growing_days(24.5, 'short')", '122')
        self.play(program.code.content.changes())
        self.wait(5)
        self.play(Uncreate(program))
        self.wait()


class FunctionArguments(ScriptScene):
    def construct(self):
        program = CodeDisplay()
        program.code.content.text_scale = 0.5
        program.vars.content.text_scale = 0.5
        program.set_side_panel_width(4.5)
        program.vars.var_length = 12
        program.set_panels(PANEL_CODE)
        """
        def growing_days(temperature, crop_season):
           days = 274 - temperature * 6
           if crop_season == 'short':
              return days - 5
           return days
    
        t_av = 24.5
        variety = 'long'
        print(growing_days(t_av, variety))
        """
        program.code.content.replace_code("""def growing_days(temperature, crop_season):\n   days = 274 - temperature * 6\n   if crop_season == 'short':\n      return days - 5\n   return days\n\nt_av = 24.5\nvariety = 'long'\nprint(growing_days(t_av, variety))""")

        self.script("""
        Lets take a deeper look at how arguments work.
        
        Lets modify our program so that our data are saved to variables before calling our function.
        """)
        self.wait(1)
        self.play(Create(program))
        self.script("""
        Keen eyed among you may have spotted that we have different variable names inside and outside the function.
        """)
        self.wait(10)
        self.play(AnimationGroup(
            Indicate(program.code.content.code.lines[0].symbols_range(17, -3)),
            Indicate(program.code.content.code.lines[8].symbols_range(19, -3)),
            run_time=2
        ))
        self.script("""
        To understand this, we have to explore how python handles what is called scope.
        """)
        self.script("""
        Just as variables you create are forgotten by the computer when a program ends, variables created in a function are kept separately from the main program, and are similarly forgotten when the function ends.
        
        This is what we mean by scope, a collection of variables that are relevant only to a particular block of code.
        
        Lets re-run our program, and keep track of variables and their associated scope.
        
        As you know by now, the first line of code that runs is the assignment of the number 24.5 to t_av. Lets record that in our list of variables in memory.

        Similarly, we store the string "long" in our variety variable
        """)
        self.wait(27)
        self.play(ApplyMethod(program.set_panels, PANEL_CODE+PANEL_VARS))

        self.wait(13)
        program.vars.set_var('t_av', ' 24.5')
        self.play(program.vars.changes())

        self.wait(3)
        program.vars.set_var('variety', "'long'")
        self.play(program.vars.changes())
        self.script("""
        Now we come to a line involving our function call, and just as you would in maths class, python looks at the brackets first, and reads this line from inside-out.
        
        First, the expressions in the innermost brackets are evaluated.
        
        In this simple case, the variables evaluate simply to their values.
        """)
        self.wait(15)
        program.code.content.replace(8, 't_av, variety', "24.5, 'long'")
        self.play(program.code.content.changes())
        self.script("""
        Next python evaluates the function call.
        """)
        self.wait(3)
        self.play(Indicate(program.code.content.code.lines[8].symbols_range(6, -2)), run_time=2)
        self.script("""
        Its worth noting that when python processed this def keyword, it actually remembers our function as a variable, not containing a value, but a reference to the instructions that make up the function.
        """)
        self.wait(10)
        program.vars.set_var('growing_days', "<func>")
        self.play(program.vars.changes())
        self.script("""
        The difference when using the name of a function in a program, is that you can place brackets after the function name, which instructs python to execute the code therein.

        We don't normally think of function definitions as variable assignments, because we don't normally change a function after its created, and so we won't record it for the purposes of this discussion.
        """)
        self.wait(20)
        program.vars.remove_var('growing_days')
        self.play(program.vars.changes())
        self.script("""
        Before python executes our function, it prepares the arguments, with the values provided to the function.
        
        Within the scope of the function, the values are assigned to the variable names in the function definition.
        """)
        self.wait(10)
        program.vars.add_scope('growing_days')
        self.play(program.vars.changes())

        program.vars.set_var('temperature', " 24.5")
        program.vars.set_var('crop_season', "'long'")
        self.play(program.vars.changes())
        self.script("""
        Observe that while these values were stored in the variables t_av and and variety in our main program, those same values, not the variables that contain them, but just the values themselves are passed to the function.

        As the function executes, and assigns new variables, they, just like the function arguments, are stored separate from the main program, within the functions scope.
        """)
        self.wait(15)
        program.vars.set_var('days', " 127")
        self.play(program.vars.changes())
        self.script("""
        As the function ends, the evaluated value of the expression after the return statement is provided back to our main program.

        In this case, not the variable days, but the value it contains.
        
        Returning to the main program, python has evaluated the value of this expression by running the function, all of the variables created within the function are forgotten, and the returned value is provided to the print function, which outputs the value to the user.
        """)
        self.wait(26)
        program.vars.remove_scope()
        self.play(program.vars.changes())

        self.wait(3)
        program.code.content.replace(8, "growing_days(24.5, 'long')", '127')
        self.play(program.code.content.changes())
        self.script("""
        Its worth noting, that if our function does not include a return statement, or includes a return statement with no expression, the special value None is returned instead.
        """)
        self.wait(13)
        self.play(Uncreate(program))
        self.wait()

class SpecialCases(ScriptScene):
    def construct(self):
        highlight = HighlightBox()

        program = CodeDisplay()
        program.vars.var_length = 1
        program.set_panels(PANEL_CODE+PANEL_VARS)
        program.output.content.text_scale = 0.5

        self.script("""
        Now lets look at some special cases
        
        If a function assigns a variable with a name that was already used outside the function, python creates a new variable within the scope of the function, that shadows, or makes inaccessible the variable in the outer scope.
        """)
        self.wait(2)
        program.code.content.replace_code("""def function():\n   x = 2\n\nx=1\nfunction()""")
        program.vars.set_var('x', '1')
        self.play(Create(program))

        self.wait(5)
        program.vars.add_scope('function')
        program.vars.set_var('x', '2')
        self.play(program.vars.changes())

        self.wait(4)
        self.play(program.vars.content.code.lines[1].symbols.animate.scale(1.25))
        self.play(program.vars.content.code.lines[1].symbols.animate.scale(0.8).set_color('#222222'))
        self.script("""
        It is possible to read values from the outer scope, but this can cause confusion, as a function may appear to behave differently when you inadvertently modify an outside variable.

        Note that Python will prevent you reading from the outer scope, then assigning a variable with that name.
        """)
        self.wait(11)
        self.play(program.vars.changes())

        self.wait(1)
        program.code.content.insert_line(1, '   y = x')
        program.vars.remove_var('x')
        cc = program.code.content.changes()
        program.code.update_runarrow(1)
        self.play(cc, program.vars.changes(), program.code.runarrow())
        self.play(ApplyMethod(program.set_panels, PANEL_CODE+PANEL_VARS+PANEL_OUTPUT))
        program.output.add_line("UnboundLocalError: local variable 'x'")
        program.output.add_line("referenced before assignment")
        self.play(program.output.content.changes())
        self.script("""
        If your function needs to return multiple values, they can be listed after return, separated by commas.
        """)
        self.wait(4)
        program.vars.remove_scope()
        program.code.update_runarrow(None)
        program2 = CodeDisplay()
        program2.vars.var_length = 1
        program2.set_panels(PANEL_CODE)
        program2.code.content.replace_code('\n'.join([
            "def function():",
            "   return 1, 2, 3",
            "",
            "val1, val2, val3 = function()",
            "print(val1)",
            "print(val2)",
            "print(val3)",
        ]))
        self.play(AnimationGroup(
            AnimationGroup(
                program.vars.changes(),
                program.code.runarrow(),
                Uncreate(program),
            ),
            Create(program2),
            lag_ratio=0.8
        ))
        program = program2
        self.script("""
        These values are returned as a tuple, which you can unpack into variables outside the function.
        """)
        self.wait(5)
        self.play(Indicate(program.code.content.code.lines[3].symbols_by_search('val1, val2, val3')))
        self.script("""
        There is one other way functions can change variables outside the function, and that's when a mutable object is passed to a function.
        
        Mutable objects are objects that can be mutated, or changed, such as lists sets and dictionaries.
        
        You can add and remove items from these objects, without having to assign a new variable
        """)
        self.wait(12)
        program.code.content.replace_code('\n'.join([
            "x = []",
            "x.append(1)",
            "print(x)",
        ]))
        self.play(program.code.content.changes())
        self.script("""
        Immutable objects include integers, floats and strings.
        
        There is no way to change thees objects
        """)
        self.wait(9)
        program.code.content.replace_code('\n'.join([
            "x = 1",
            "x + 1",
            "print(x)",
        ]))
        self.play(program.code.content.changes())
        self.script("""
        If you want to change a variable containing an immutable object, you have to assign the variable a new value.
        """)
        self.wait(11)
        program.code.content.insert(1, 0, 'x = ')
        self.play(program.code.content.changes())
        self.script("""
        Now lets look at how that works as a function argument
        """)
        self.wait(3)
        program.code.content.replace_code('\n'.join([
            "def my_function(arg):",
            "   arg.append(1)",
            "",
            "x = []",
            "my_function(x)",
            "print(x)",
        ]))
        self.play(program.code.content.changes())
        self.script("""
        Here the list referenced by x is passed into the function, and as the function is set up, the variable arg also references the same list.
        
        Note earlier we were talking about assigning values to variables. That explanation was incomplete, as all python variables are references.
        """)
        self.wait(10)
        program2.vars.var_length = 3
        self.play(ApplyMethod(program.set_panels, PANEL_CODE+PANEL_VARS))

        self.wait(10)
        program.vars.set_var('x', '[]')
        program.vars.add_scope('my_function')
        program.vars.set_var('arg', '[]')
        self.play(program.vars.changes())
        self.script("""
        That distinction was immaterial when discussing immutable objects, but when discussing mutable objects, its important to realise that if we set another variable to equal the first, we are not setting the second variable to an equivalent list, a copy, we are actually setting the second variable to reference the very same object in memory.
        
        In our example, we'll denote that, by showing arg as being equal to x, to make it clear that arg does not reference a unique list of its own.
        """)
        self.wait(10)
        program.vars.set_var('arg', 'x')
        self.play(program.vars.changes())
        self.script("""
        It now becomes clear, that as the function calls append on arg, that it is actually calling append on the list referenced by x.
        
        Thus, when the function returns, and the print is executed, we see that the list has been modified.
        """)
        self.wait(10)
        self.play(ApplyMethod(program.set_panels, PANEL_CODE+PANEL_VARS+PANEL_OUTPUT))

        self.wait(10)
        program.output.add_line('[1]')
        self.play(program.vars.changes(), program.output.content.changes())
        self.script("""
        If we try the same example with an immutable object, the function setup is the same, and again, arg references the same object as x.
        """)
        self.wait(10)
        program.code.content.replace_code('\n'.join([
            "def my_function(arg):",
            "   arg = arg + 1",
            "",
            "x = 1",
            "my_function(x)",
            "print(x)",
        ]))
        program.output.clear_lines()
        program.output.add_line('1')
        program.vars.set_var('x', '1', scope='')
        program.vars.set_var('arg', '2')
        self.play(program.code.content.changes(), program.vars.changes(), program.output.content.changes())
        self.script("""
        The difference here, is that it is not possible to make any change to the value 1.
        
        Our assignment within the function first evaluates the expression on the right, producing a new value 2, which is assigned to arg.
        
        Reassigning arg, sets arg to reference a different object in memory, and thus it is not possible in this situation for the function to modify x.
        """)
        self.wait(10)
        self.play(Uncreate(program))
        self.wait()

class BestPractices(ScriptScene):
    def construct(self):
        highlight = HighlightBox()

        program = CodeDisplay()
        program.vars.var_length = 1
        program.set_panels(PANEL_CODE)
        program.code.content.text_scale = 0.4

        self.script("""
        I'd like to conclude by discussing how functions should be used.
        
        Functions at their best, make code more readable. Even simple functions can do this
        """)
        self.wait(5)
        program.code.content.replace_code('\n'.join([
            "DENSITY_OF_STEEL = 8050 # kg per m3",
            "PI = 3.14159",
            "",
            "rod_length = 2",
            "rod_diameter = 0.05",
            "rod_mass = DENSITY_STEEL * PI * rod_diameter ** 2 * rod_length / 4",
        ]))
        self.play(Create(program))
        self.script("""
        It might not be obvious at first what this expression is doing. The variable name indicates we are calculating the weight of a rod, but its difficult to verify the calculation is correct.
        
        If however, we write a very simple function to calculate the area of a circle, and a very simple function to calculate the volume of a cylinder, both of which are much easier to understand, we can then use them to simplify our original expression.
        """)
        self.wait(20)
        program.code.content.insert_line(3, "def area_of_circle(radius):")
        program.code.content.insert_line(4, "    return PI * radius ** 2")
        program.code.content.insert_line(5, "")
        program.code.content.insert_line(6, "def volume_of_cylinder(radius, length):")
        program.code.content.insert_line(7, "    return area_of_circle(radius) * length")
        program.code.content.insert_line(8, "")
        self.wait(10)
        self.play(program.code.content.changes())
        program.code.content.replace(
            11,
            "PI * rod_diameter ** 2 * rod_length / 4",
            "volume_of_cylinder(rod_diameter / 2, rod_length)")
        self.play(program.code.content.changes())
        self.script("""
        While the line is not any shorter, its much more obvious at a glance how the calculation is performed, and each of the functions calculations are equally simple to verify.

        For functions to make code readable, they should have descriptive names, concise, as long as necessary but not too long, but not so short as to obfuscate their meaning.
        """)
        self.wait(10)
        self.play(Uncreate(program))

        self.wait(2)
        text = HighlightedCode('x\nfunc\nvolume\nvolume_of_cylinder\ncalculate_cylinder_volume\ncylinder_volume_from_radius_and_length', lexer='python', font='FreeMono')
        text.set_color('#4444FF')
        deftext = HighlightedCode('def volume_of_cylinder():', lexer='python', font='FreeMono')
        text.shift(deftext[3].get_center() - text[0].get_center() +
                   UP * (deftext[3].height - text[0].height) / 2 +
                   RIGHT * (deftext[3].width - text[0].width) / 2)
        self.play(Create(deftext[:3]), Create(text))
        self.wait(1)
        chars = [0, 1, 5, 11, 29, 54]
        current_char = 0
        def move_char(dir, time=0.4):
            curr = chars[current_char]
            next = chars[current_char + dir]
            self.play(ApplyMethod(text.shift, UP * (
                (text[curr].get_center()[1] - text[curr].height/2) -
                (text[next].get_center()[1] - text[next].height / 2)
            )), run_time=time)
            return current_char + dir
        current_char = move_char(1, 0.4)
        current_char = move_char(1, 0.4)
        current_char = move_char(1, 0.4)
        current_char = move_char(1, 0.4)
        current_char = move_char(1, 0.4)
        current_char = move_char(-1, 0.2)
        current_char = move_char(-1, 0.2)
        self.play(Create(deftext[3:-3]), run_time=0)
        self.wait(1)
        self.play(FadeOut(text), Create(deftext[-3:]))
        self.wait(2)
        self.play(FadeOut(deftext))
        self.wait()
        self.script("""
        Functions should also obey a simple contract. Arguments in, return values out.
        """)
        self.wait(2)
        program = CodeDisplay()
        program.set_panels(PANEL_CODE+PANEL_OUTPUT)
        program.code.content.replace_code('\n'.join([
            "data = [2.4, 2.5, 2.2, 2.2, 2.3]",
            "",
            "print(data)",
            "result1 = function(data)",
            "print(data)",
            "result2 = function(data)",
            "print(result1 == result2)",
        ]))
        program.output.add_line("[2.4, 2.5, 2.2, 2.2, 2.3]")
        program.output.add_line("[2.4, 2.5, 2.2, 2.2, 2.3]")
        program.output.add_line("True")
        self.play(Create(program))
        self.wait()
        self.script("""
        If possible they shouldn't modify any mutable arguments, and the same function, called with the same arguments should return the same result.

        Functions shouldn't rely on global variables, and should not modify them.
        
        The exception being a function may read clearly marked constants, variables that never change.
        
        Constants give you a way to clearly name important pieces of information.
        """)
        self.wait(15)
        program.code.content.text_scale = 0.5
        program.code.content.replace_code('\n'.join([
            "# ratio between the circumference and diameter of a circle",
            "PI = 3.14159",
            "# the number of centimetres in one inch",
            "CM_PER_IN = 2.54",
            "# acceleration due to gravity on earth in m/s^2",
            "G_ACC = 9.8",
        ]))
        program.output.clear_lines()
        self.play(ApplyMethod(program.set_panels, PANEL_CODE), program.code.content.changes(), program.output.content.changes())
        self.script("""
        This makes programs easier to understand, and easier to debug.
        
        There are times where you might want to break this rule, but it should be very obvious when reading your code, what the consequences are
        """)
        self.wait(5)
        program.code.content.text_scale = 0.6
        program.code.content.replace_code('\n'.join([
            "print(fetch_next_temperature_reading(temperature_file))",
            "print(fetch_next_temperature_reading(temperature_file))",
            "print(fetch_next_temperature_reading(temperature_file))",
        ]))
        self.play(program.code.content.changes())

        self.wait(5)
        program.code.content.text_scale = 0.8
        program.code.content.replace_code('\n'.join([
            "x = [1, 2, 3, 4]",
            "double_list_values(x)",
            "print(x)",
        ]))
        program.output.add_line("[2, 4, 6, 8]")
        self.play(ApplyMethod(program.set_panels, PANEL_CODE+PANEL_OUTPUT), program.code.content.changes(), program.output.content.changes())

        self.wait(5)
        self.play(Uncreate(program))
        self.script("""
        I hope this discussion has shown, not only how useful functions are to create reusable instructions, and simplify code, but also how they can make your programs easier for others to read and understand.
        
        If used correctly, functions will make you a better programmer, and a better communicator, making your code easier for others to understand and modify.
        """)

        self.wait(5)
        return
        text = Text("What happens in a function\nstays in a function.")
        rect = SurroundingRectangle(text, buff=1).set_fill(color=BLACK, opacity=1)
        self.play(GrowFromCenter(VGroup(rect, text)))

        text2 = Text("Unless its returned.").next_to(text, DOWN).scale(0.8)
        self.play(ApplyMethod(rect.stretch_to_fit_height, rect.height+text2.height+0.25, {'about_edge':UP}), GrowFromCenter(text2))

        text3 = Text("Unless it modifies external mutable objects").scale(0.5).next_to(text2, DOWN, buff=0.5)
        self.play(
            ApplyMethod(rect.stretch_to_fit_height, rect.height+text3.height+0.25, {'about_edge':UP}),
            GrowFromCenter(text3))
        self.wait()
        self.play(
            ApplyMethod(rect.stretch_to_fit_height, rect.height-text3.height-0.25, {'about_edge':UP}),
            FadeOut(text3))
        self.play(ShrinkToCenter(VGroup(rect, text, text2)))
        self.wait(4)
