# This file contains commands to lint and test the statistics
# calculator program.

SRCS=locate.py
TESTS=locate_test.py

lint:
	pylint --reports=n --include-ids=y $(SRCS)

test:
	@for test in $(TESTS); do \
		./$$test ; \
	done
