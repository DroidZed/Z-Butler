#IMAGE_TAG=latest
include .env

install:
	uv sync

bot:
	py .\src\app.py

test:
	uv run pytest -vs .

build:
	docker build -t droidzed/z-butler:$(IMAGE_TAG) .

compose:
	docker compose up -d

decompose:
	docker compose down

module:
	mkdir .\src\modules\${NAME}

	echo "from .${NAME}_api import *" > ./src/modules/${NAME}/__init__.py
	echo "print('hi')" > ./src/modules/${NAME}/${NAME}_api.py
	echo "print('hi')" > ./src/tests/test_${NAME}_api.py
	echo "from .${NAME} import *" >> ./src/modules/__init__.py
