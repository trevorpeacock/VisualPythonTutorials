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

.PHONY: run
run: setup
	bash -c "source $(VENVPATH)/bin/activate && manim -a -qm -p videos/flow.py"

.PHONY: test
test: setup
	bash -c "source $(VENVPATH)/bin/activate && manim -qm -p testing/tst2.py MovingFrameBox2"
