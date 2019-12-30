![](https://raw.githubusercontent.com/AlanDecode/Maverick/master/banner.png)

[![](https://img.shields.io/badge/Preview-GitHub-blue?style=flat-square)](https://alandecode.github.io/Maverick/) [![Build Status](https://github.com/AlanDecode/Maverick/workflows/Build/badge.svg)](https://github.com/AlanDecode/Maverick/actions) ![](https://img.shields.io/github/license/AlanDecode/Maverick.svg?style=flat-square)

## Overview

Maverick is a static blog generator built with python. Like Hexo and Jekyll, it takes Markdown (`.md`) files as input, and output beautifully formated and well structured website pages (`.html`). It has a bunch of built-in useful features (feed, search, sitemap, etc.), with extended Markdown syntax and enhanced image processing pipeline.

If you are tired of intricate plugins and complicated configurations, just give Maverick a try. You can focus on writing, let Maverick take care of the rest.

Pull requests are surely welcome. If you have any questions or suggestions, please head to [issue area](https://github.com/AlanDecode/Maverick/issues) and leave us a message. Before that, let's finish this document.

## Usage

Maverick is built with modern Python, currently at least **Python 3.5** is required, make sure you have it installed on your machine.

### Install

Clone this repository:

```bash
git clone https://github.com/AlanDecode/Maverick.git ./Maverick && cd ./Maverick
```

Install dependencies:

```bash
pip install -r prod_req.txt
```

If error occurs, please verify your Python and pip version. Then edit the default configuration file:

```bash
vi ./config.py
```

For now let's use the default settings. Type this command in your terminal:

```bash
python ./build.py
```

...and a sample static site is generated in `test_dist` folder! You can then upload them to GitHub Pages or any other server. 

### Generate your own site

By default, Maverick searches all `.md` files recursively under `test_src` folder, so put your Markdown files in it and run `python ./build.py` then everything you need will be in `test_dist` folder. Maverick uses so-called `YAML frontmatter` to get meta data of your articles, if you have tried Hexo or Jekyll, you should already be familiar with it; if you don't, let's look into it now.

## File arrangement and `frontmatter`

In Maverick, arrangement of your source article files is **not** important, you can arrange them by category, date or anything you like, Maverick will try to find them automatically.

Instead, `frontmatter` of each Markdown file tells Maverick its slug, category, tags and publish date, etc. `frontmatter` is a short piece of text on top of each Markdown file, like this:

```
---
layout: post
title: A interesting story
slug: a-interesting-story
date: 2019-12-11 16:08
status: publish
author: AlanDecode
categories: 
  - Daily
tags: 
  - Travel
  - Family
---

<!-- Your content here -->
```

`frontmatter` starts and ends with `---`, it stores information as `key: value` pair. All available options are listed bellow:

|     Key      | Required | Default Value | Possible Value         | Explanation                                                  |
| :----------: | -------- | ------------- | ---------------------- | ------------------------------------------------------------ |
|   `layout`   | false    | post          | post, page             | Type of this article.                                        |
|   `title`    | true     | -             | -                      | The of this article                                          |
|    `slug`    | true     | `title`       | -                      | Maverick uses this value to generate URL of this article. For example: `https://me.com/archives/a-interesting-story`. |
|    `date`    | true     | -             | -                      | Publish date of this article in `yyyy-mm-dd hh:ss` format.   |
|   `status`   | false    | publish       | publish, hidden, draft | Status of this article.                                      |
|   `author`   | false    | -             | -                      | Author of this article.                                      |
|  `excerpt`   | false    | -             | -                      | Will be used as excerpt of this article in home page and HTML `head` tag. If not set, Maverick will try to find `<!--more-->` and use content before as excerpt.  If still not found, the first paragraph will be used. |
|  `showfull`  | false    | false         | true, false            | If set to `true`, full content will show in home page.       |
|  `comment`   | false    | false         | true, false            | Turn on comment for this article. See how to enable comment in [Comment](#comments) section. |
|    `tags`    | false    | -             | -                      | Tags of this article. If there are multiple tags, write them as above. Don't forget spaces before and after `-`. |
| `categories` | false    | -             | -                      | Categories of this article. If there are multiple categories, write them as above. Don't forget spaces before and after `-` |

I suggest you keep a copy of sample articles come with Maverick as a reference to these options.

## Configurations

Although Maverick is much simpler than many other generators, it does have a few configurations you need to take care of, which you can modify in `config.py`. All these options  are listed bellow.

### Options for Maverick

| Option               | Default Value                                   | Explanation                                                  |
| -------------------- | ----------------------------------------------- | ------------------------------------------------------------ |
| `site_prefix`        | `"/"`                                           | This value will be used to generate permalinks of your posts. Possible values are like `https://myblog.com/` or `https://me.com/blog/` or  just `/blog/`. If you want to put your site under sub directory, this option can be useful.  Don't forget `/` at the end. |
| `source_dir`         | `"./test_src/"`                                 | A directory in which Maverick will try to find your articles. This can be any location on your machine, so feel free to store your articles in Dropbox, iCloud Drive or anywhere else to get them synced across multiple devices. |
| `build_dir`          | `"./test_dist/"`                                | Where Maverick should place all generated HTML files. This can be any location on your machine, just make sure you have write permission on it. |
| `template`           | `"Galileo"`                                     | Specify the template to render your site. Currently `Galileo` is available. |
| `index_page_size`    | `10`                                            | The number of posts to show per page, change it to any number you like. |
| `archives_page_size` | `30`                                            | The number of posts to show per page in archive list, category list and tag list. |
| `fetch_remote_imgs`  | `False`                                         | Specify how Maverick will take care of your images. Please refer to [Images and Static Assets](#images-and-static-assets) for more details. |
| `locale`             | `Asia/Shanghai`                                 | Specify where you are. Valid options are listed [here](https://stackoverflow.com/questions/13866926/is-there-a-list-of-pytz-timezones). |
| `enable_jsdelivr`    | {<br />"enabled": False,<br />"repo": ""<br />} | If you host your site on GitHub Pages, this option can enable [jsDelivr](https://www.jsdelivr.com/) as CDN service for all your static files, including JS files, CSS files and images. See `config.py` and preview site for an example. Basically, set `"enabled"` to `True` and set `"repo"` to `<user>/<repo>@<branch>`. |
| `category_by_folder` | `False`                                         | Category contents by folder structure rather than front-matter. |

### Options for Your Site

| Option            | Default Value                             | Explanation                                                  |
| ----------------- | ----------------------------------------- | ------------------------------------------------------------ |
| `site_name`       | `"Hellow Maverick!"`                      | Website name. Change it to something really cool!            |
| `site_logo`       | -                                         | Website logo. Better be a square image.                      |
| `site_build_date` | `"2019-12-06T12:00+08:00"`                | When you build this site.                                    |
| `author`          | -                                         | Author's name.                                               |
| `email`           | -                                         | Author's email.                                              |
| `author_homepage` | `"/"`                                     | Author's homepage.                                           |
| `description`     | `"A marvelous site powered by Maverick!"` | Description of your site.                                    |
| `keywords`        | -                                         | Four or five keywords about your site.                       |
| `external_links`  | -                                         | Will be used in `Links` section on home page.                |
| `nav`             | -                                         | Will be used to generate navigations behind site title.      |
| `social_links`    | -                                         | Will be used to generate social links behind site title.     |
| `valine`          | -                                         | Maverick now supports Valine as its comment system. Please refer to [Comments](#comments) for more information. |
| `head_addon`      | -                                         | Content here will be added to `<head>` tag of generated HTMLs, you can put some `meta` tag here, or use `<link>` and `<script>` to import custom CSS and JavaScript files. |
| `footer_addon`    | -                                         | Content here will be added to `<footer>` tag. You can add some additional info here. |
| `body_addon`      | -                                         | Content here will be added to `<body>` tag, external JavaScripts and can be put here. |
| `language`        | `"english"`                               | Site language.                                               |
| `background_img`  | -                                         | Background image for your site. Better be light-colored.     |

💡 Note: You can access other options by `${option_name}`. For example `${site_prefix}logo.png` will be parsed as `/logo.png` if you set `site_prefix` to `/`. When using this feature, **watch out for infinite loops**.

💡 Note: You can use `${static_prefix}` instead of `${site_prefix}` to reference static files, if you enabled jsDelivr as CDN service.

💡 Note: you can also use configuration file other than `config.py`, just specify it when build:

```bash
python ./build.py -c "./my_conf.py"
# or
python ./build.py --config "./my_conf.py"
```

## Images and Static Assets

Maverick is a flexible generator, it does not require you to put your files in some fixed location, instead, by setting `source_dir`, it automatically detects all source files to build your site. But what about images and other static assets like fonts or others? Well, Maverick has its own rule to solve this problem.

### Static Assets

If there is a folder named `static` under `source_dir`, Maverick will copy all contents in that folder to `build_dir`.  For example, if a `source_dir` looks like this:

```
source_dir/
	- static/
		- favicon.ico
		- robots.txt
		- font/
   	- ...
```

The result will be like this:

```
build_dir/
	- favicon.ico
	- robots.txt
	- fonts/
```

Simple, right?

### Images

You can of course put all your images under `static` folder, however, Maverick is designed to handle images very smartly. In fact, you can put your images **anywhere** on your machine, or insert remote images by URL in your Markdown file, when generating your static site, Maverick will try to gather them all together, putting them into a unified position and  taking care of the links in your article in the same time.

In this way, you can freely manage your images with any online services you like, or just save them locally on your machine and reference them by relative or absolute path in your article. Many Markdown editors (like the awesome [Typora]()) support inserting local images and can display them properly. This enables **real-WYSIWYG** (What You See Is What You Get). For example, if you have a folder structure like this:

```
source_dir/
	- assets/
		- pic.jpg
	- article.md
```

In `article.md`, you insert `pic.jpg` like bellow:

```markdown
![](./assets/pic.jpg)
```

When parsing `article.md`, Maverick will try to find `./assets/pic.jpg` on your machine, once been found, Maverick copies it to `build_dir/archives/asstes/`, and then change the link in `article.md`.

Here is one more reason why Maverick is designed this way. In many cases, for example, light-box and photo arrangements on web pages requires predefined image dimensions. Instead of fetching size information at front-end, parsing size information at building stage can dramatically improve the experience. **Besides, this design can enable jsDelivr as CDN service for all your images.** 

It's special for remote images though. We can't easily get size information of them, so Maverick can try to download remote images to local disk and treat them as local images, this feature is disabled by default, you can turn it on by setting `fetch_remote_imgs` to `True` in configuration file. If you don't want to download full images to, just leave  `fetch_remote_imgs` as `False`, Maverick will try to get the size of the image by downloading very small part of it (in most cases only 1~2 KB is needed).

All remote images and size information are cached locally, so Maverick won't download and parse them during every generation.

## Markdown

Maverick uses [mistune 0.8.4](https://github.com/lepture/mistune/tree/v1) as its back-bone Markdown parser, with some extending.

### Math Equations

You can insert math equations with like this:

```
# inline math
$m\times n$

## block math
$$C_{m\times k}=A_{m\times n}\cdot B_{n\times k}$$
```

### Code Highlighting

Just specify the language when inserting code block with markdown syntax, and it will automatically be highlighted:

```
​```cpp
int main(int argc , char** argv){
    std::cout << "Hello World!\n";
    return 0;
}
​```
```

### Ruby

Type something like this:

```
I am {{Darth Vader:Your Father}}!
```

And it will be rendered as: I am <ruby>Darth Vader<rp> (</rp><rt>Your Father</rt><rp>)</rp>!</ruby>

### Link Card

Type something like this:

```
[Name](link)+(image URL)
```

It will be rendered as a link card with a images and a title. 

### Inline Footnotes

Insert inline Footnotes like this:

```
Maverick is a staic blog generator[^Built with Python.].
```

### DPlayer

Thanks to [DPlayer](http://dplayer.js.org/), you can easily insert beautiful video player into your posts:

```
[dplayer]https://path/to/veideo.mp4[/dplayer]
```

You can add more options to it like this:

```
[dplayer data-theme="#b7daff"]https://path/to/video.mp4[/dplayer]
```

Checkout more options [here](http://dplayer.js.org/guide.html).

## Comments

Maverick has built-in [Valine](https://valine.js.org/) support, please refer to  [Valine Docs](https://valine.js.org/en/quickstart.html) for more information. You need to fill `valine` entry in configuration file with these options:

```python
valine = {
    "enable": True,
    "appId": "<your appId here>",
    "appKey": "<your appKey here>",
    "notify": "false",
    "visitor": "false",
    "recordIP": "false",
    "serverURLs": None,
    "placeholder": "Just go go~"
}
```

## Development

Pull requests are surely welcome. See [theme-Dev.md](https://github.com/AlanDecode/Maverick/blob/master/theme-Dev.md) for documentation on developing a theme for Maverick.

## License

MIT © [AlanDecode](https://github.com/AlanDecode).
