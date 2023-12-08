install:
	poetry install

styles:
	python scripts/gen_styles.py

dev: styles
	python main.py

clean:
	rm -rf dist build main.spec upakarana/styles/dist

build: clean
	python build.py

preview: build
	./dist/main