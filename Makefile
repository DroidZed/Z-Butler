#IMAGE_TAG=latest
include .env

install:
	poetry install --no-root

bot:
	py .\src\app.py

module:
	mkdir .\src\modules\${MODULE_NAME}

	echo from .${MODULE_NAME}_api import * > ./src/modules/${MODULE_NAME}/__init__.py
	echo print('hi') > ./src/modules/${MODULE_NAME}/${MODULE_NAME}_api.py
	echo print('hi') > ./src/tests/test_${MODULE_NAME}_api.py
	echo from .${MODULE_NAME} import * >> ./src/modules/__init__.py

# Note: these ^^^ lines only work on windows !

test:
	py -m pytest -vs .

build:
	docker build -t droidzed/z-butler:$(IMAGE_TAG) .

compose:
	docker compose up -d

decompose:
	docker compose down
