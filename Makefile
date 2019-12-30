.PHONY: theme site clean all
default: site

theme:
	cd ./Templates/Galileo && gulp

dep:
	pip install -r prod_req.txt
	cd ./Templates/Galileo && npm install -g gulp && npm install

site:
	python build.py

all: theme site
