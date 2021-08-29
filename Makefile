.DEFAULT_GOAL := run

VENVPATH=venv

$(VENVPATH):
	virtualenv $(VENVPATH)
	bash -c "virtualenv $(VENVPATH) -p python3 && source $(VENVPATH)/bin/activate && pip install --upgrade pip setuptools && pip install -r requirements.txt"
	bash -c "source $(VENVPATH)/bin/activate && pip install -e manimcoder"

.PHONY: setup
setup: $(VENVPATH)

.PHONY: clean
clean:
	rm -dfr $(VENVPATH)
	rm -dfr media

flow: setup
	bash -c "source $(VENVPATH)/bin/activate && manim -a -ql -p videos/flow.py"

function_intro: setup
	bash -c "source $(VENVPATH)/bin/activate && manim -a -qh videos/function_intro.py"

.PHONY: run
run: function_intro

.PHONY: test
test: setup
	bash -c "source $(VENVPATH)/bin/activate && manim -a -ql -p testing/test.py"
#	bash -c "source $(VENVPATH)/bin/activate && manim -ql -p videos/function_intro.py BestPractices"
