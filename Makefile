install:
	poetry install

dev:
	python main.py

clean:
	rm -rf dist build main.spec

build: clean
	python pyinstaller.py

preview: build
	./dist/main