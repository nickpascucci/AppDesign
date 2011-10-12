# This file contains commands to lint and test the statistics
# calculator program.

SRCS=processing.py
TESTS=processing_test.py

lint:
	pylint --reports=n --include-ids=y --disable R0903,R0904,C0103 $(SRCS)

test:
	@for test in $(TESTS); do \
		echo "Running $$test." ; \
		./$$test ; \
	done
