# This file contains commands to lint and test the statistics
# calculator program.

SRCS=bookmark.py bookmark_store.py
TESTS=bookmark_test.py bookmark_store_test.py

lint:
	pylint --reports=n --include-ids=y --disable R0903,R0904 $(SRCS)

test:
	@for test in $(TESTS); do \
		echo "Running $$test." ; \
		./$$test ; \
	done
