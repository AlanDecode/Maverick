.PHONY: Galileo Kepler site dep
default: site

Galileo:
	cd ./Templates/Galileo && make

Kepler:
	cd ./Templates/Kepler && make

dep: prod_req.txt
	pip install -r prod_req.txt

site:
	python build.py
