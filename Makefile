theme:
	cd ./Templates/Galileo && gulp

dep:
	pip install -r prod_req.txt
	cd ./Templates/Galileo && npm install -g gulp && npm install

site:
	python build.py

clean:
	cd ./Templates/Galileo && rm -rf package-lock.json

all: theme site

.PHONY: theme site clean all
