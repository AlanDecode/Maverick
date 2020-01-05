.PHONY: site dep
default: site

dep: prod_req.txt
	pip install -r prod_req.txt

site:
	python build.py
