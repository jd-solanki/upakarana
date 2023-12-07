install:
	poetry install

dev:
	python main.py

clean:
	rm -rf dist build

build: clean
	pyinstaller --onefile main.py

preview:
	./dist/main