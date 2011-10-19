# Application Design - CP215 Block 2 2011
# This Makefile contains commands which are global to the code produced
# for this class. These include testing and linting and documenting commands.
#
# Licensed under the MIT License. See the full text in LICENSE.

SUBDIRS = bookmarks download search sound stats wordcount
TOPLEVEL = $(shell basename `pwd`)

lint:
	@for dir in $(SUBDIRS); do \
		cd $$dir ; \
		make lint ; \
		cd .. ; \
	done

test:
	@for dir in $(SUBDIRS); do \
		cd $$dir ; \
		make test ; \
		cd .. ; \
	done

docs: clean-docs
	pydoc -w ./
	@mv *.html docs/

clean-docs:
	-rm docs/*

dist:
	@-rm AppDesign.tar.gz
	@cd ../ ; \
	tar -czf AppDesign.tar.gz $(TOPLEVEL); \
	mv AppDesign.tar.gz $(TOPLEVEL)

presubmit: test docs dist

clean:
	@-rm *.pyc
	@-for dir in $(SUBDIRS); do \
		cd $$dir ; \
		rm *.pyc ; \
		cd .. ; \
	done