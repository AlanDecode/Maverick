.PHONY: site dep
default: site

dep: requirements.txt
	pip install -r requirements.txt

site:
	python build.py
