.PHONY: all
.PHONY: all_html
all: doc/latex2/requirements.pdf req-graph1.png req-graph2.png all_html

# Adding new files (especially requirements) can not automatically
# handled.  The 'force' target tries to handle this.
.PHONY: force
force: 
	rm .rmtoo_dependencies
	${MAKE} all

#
# This is the way the rmtoo must be called.
#
CALL_RMTOO=./bin/rmtoo -m . -f doc/requirements/Config3.py

#
# Dependency handling
#  The file .rmtoo_dependencies is created by rmtoo itself.
#
include .rmtoo_dependencies

all_html: ${OUTPUT_HTML}

# And how to make the dependencies
.rmtoo_dependencies:
	./bin/rmtoo -m . -f doc/requirements/Config3.py \
		-d doc/requirements \
		--create-makefile-dependencies=.rmtoo_dependencies

req-graph1.png: req-graph1.dot
	dot -Tpng -o req-graph1.png req-graph1.dot

req-graph2.png: req-graph2.dot
	dot -Tpng -o req-graph2.png req-graph2.dot

# Two calls are needed: one for the requirments converting and one for
# backlog creation.
doc/latex2/requirements.pdf: ${REQS_LATEX2} doc/latex2/requirements.tex
	(cd doc/latex2 && \
	   gnuplot ../../contrib/gnuplot_stats_reqs_cnt.inc && \
	   epstopdf stats_reqs_cnt.eps)
	(cd doc/latex2 && pdflatex requirements.tex; \
		pdflatex requirements.tex; \
		pdflatex requirements.tex)

.PHONY: clean
clean:
	rm -f req-graph1.png req-graph2.png doc/latex2/reqtopics.tex \
		req-graph1.dot req-graph2.dot \
		doc/latex2/requirements.aux doc/latex2/requirements.dvi \
		doc/latex2/requirements.log doc/latex2/requirements.out \
		doc/latex2/requirements.pdf doc/latex2/requirements.toc 
	rm -fr debian/rmtoo build

PYSETUP = python setup.py

.PHONY: install
install:
	$(PYSETUP) install --prefix=${DESTDIR}/usr \
		--install-scripts=${DESTDIR}/usr/bin

.PHONY: tests
tests:
	nosetests -w rmtoo -v --with-coverage -s --cover-package=rmtoo

.PHONY: deb
deb:
	debuild -I -Imake_latex.log
