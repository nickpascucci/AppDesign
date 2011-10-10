# This file contains commands to lint and test the statistics
# calculator program.

SRCS=mapper.py reducer.py source.py
TESTS=mapper_test.py reducer_test.py

lint:
	pylint --reports=n --include-ids=y $(SRCS)

test:
	@for test in $(TESTS); do \
		./$$test ; \
	done
