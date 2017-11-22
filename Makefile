all: run test

run:
	python3 main.py videos

test-run:
	python3 main.py videos-test

test:
	python3 main.py videos | python3 evaluate.py

test-test:
	python3 main.py videos-test | python3 evaluate.py
