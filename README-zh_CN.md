# Maverick

[![][image-1]][1] [![Build Status][image-2]][2] ![][image-3]

## Overview | 概述

Maverick 是一个基于 Python 构建的静态博客生成器。类似 Hexo和 Jekyll, 使用 Markdown (`.md`) 文件作为输入源, 输出格式优美、结构良好的静态网站页面
 (`.html`). 它内置许多有用的特性(feed, search, sitemap, etc.), 支持增强的 Markdown 语法，增加内置的图像处理.

如果您对复杂的插件和复杂的配置感到厌倦，只需尝试一下Maverick。 您可以专注于写作，让Maverick负责其余的工作。

欢迎提交 Pull requests。如果你有一些问题和建议，请前往 [issue area][3] 给我们留言。 提问之前，请先阅读完本文档。

## Usage | 使用

Maverick是使用现代Python构建的，目前至少需要** Python 3.5 **，请确保已将其安装在计算机上。

### Install | 安装

克隆仓库：

```bash
git clone https://github.com/AlanDecode/Maverick.git ./Maverick && cd ./Maverick
```

安装依赖：

```bash
pip install -r prod_req.txt
```

如果出现错误，请验证你 Python 和 pip 的版本。然后编辑默认的配置文件：

```bash
vi ./config.py
```

现在，让我们使用默认设置。 在终端中键入以下命令：

```bash
python ./build.py
```

...在 `test_dist` 文件夹中生成了一个示例静态站点！ 你可以把它们上传到 GitHub Pages 或者其他的服务器。

### Generate your own site | 生成自己的网站

默认情况下, Maverick 递归搜索 `test_src` 文件夹下所有的 `.md` 文件, 所以将你的 Markdown 文件放在这，并运行 `python ./build.py`。 静态网页文件将在 `test_dist` 文件夹中生成。 Maverick 使用被称为 `YAML frontmatter` 来获得文章元数据，如果你使用过 Hexo 或者 Jekyll, 你应当非常熟悉他们;如果你对他们不熟悉，请继续往下看。

## File arrangement and `frontmatter`

在 Maverick 中，File arrangement 在你的源文件中并不重要，您可以按类别，日期或任何您喜欢的东西进行排列，Maverick会尝试自动查找它们。

取而代之的是，每个 Markdown 文件的 `frontmatter` 告诉Maverick它的 slug，类别，标签和发布日期等。`frontmatter` 是每个Markdown文件顶部的一小段文字，如下所示：

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

`frontmatter` 开始和结束于 `---`, 它将信息储存为 `key: value`。 下面列出了所有可用的选项：

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
|  `comment`   | false    | false         | true, false            | Turn on comment for this article. See how to enable comment in [Comment][4] section. |
|    `tags`    | false    | -             | -                      | Tags of this article. If there are multiple tags, write them as above. Don't forget spaces before and after `-`. |
| `categories` | false    | -             | -                      | Categories of this article. If there are multiple categories, write them as above. Don't forget spaces before and after `-` |

我建议您保留一份 Maverick 随附的示例文章样本，以作为这些选项的参考。

## Configurations | 构建

尽管 Maverick 比许多其他生成器要简单得多，但是它确实有一些需要注意的配置，可以在config.py中进行修改。 下面列出了所有这些选项。

### Options for Maverick | Maverick 的选项

| Option                    | Default Value                                   | Explanation                                                  |
| ------------------------- | ----------------------------------------------- | ------------------------------------------------------------ |
| `site_prefix`             | `"/"`                                           | 网站目录。This value will be used to generate permalinks of your posts. Possible values are like `https://myblog.com/` or `https://me.com/blog/` or  just `/blog/`. If you want to put your site under sub directory, this option can be useful.  Don't forget `/` at the end. |
| `source_dir`              | `"./test_src/"`                                 | 源文件夹。A directory in which Maverick will try to find your articles. This can be any location on your machine, so feel free to store your articles in Dropbox, iCloud Drive or anywhere else to get them synced across multiple devices. |
| `build_dir`               | `"./test_dist/"`                                | 静态文件生成文件夹。Where Maverick should place all generated HTML files. This can be any location on your machine, just make sure you have write permission on it. |
| `template`                | `"Galileo"`                                     | 主题文件夹。Specify the template to render your site. Please refer to [Themes][5] for more details. |
| `index_page_size`         | `10`                                            | 主页文章数量。The number of posts to show per page, change it to any number you like. |
| `archives_page_size`      | `30`                                            | 归档页文章数量。The number of posts to show per page in archive list, category list and tag list. |
| `fetch_remote_imgs`       | `False`                                         | 是否拉去远端图片。Specify how Maverick will take care of your images. Please refer to [Images and Static Assets][6] for more details. |
| `locale`                  | `Asia/Shanghai`                                 | 本地时区。Specify where you are. Valid options are listed [here][7]. |
| `enable_jsdelivr`         | {<br />"enabled": False,<br />"repo": ""<br />} | 是不是启用 jsdelivr 。If you host your site on GitHub Pages, this option can enable [jsDelivr][8] as CDN service for all your static files, including JS files, CSS files and images. See `config.py` and preview site for an example. Basically, set `"enabled"` to `True` and set `"repo"` to `<user>/<repo>@<branch>`. |
| `category_by_folder`      | `False`                                         | 分类方式。Category contents by folder structure rather than front-matter. |

### Options for Your Site | 你网站的选项

| Option            | Default Value                             | Explanation                                                  |
| ----------------- | ----------------------------------------- | ------------------------------------------------------------ |
| `site_name`       | `"Hellow Maverick!"`                      | 网站标题。Website name. Change it to something really cool!             |
| `site_logo`       | -                                         | 网站 logo。Website logo. Better be a square image.                      |
| `site_build_date` | `"2019-12-06T12:00+08:00"`                | 网站创建时间。When you build this site.                                    |
| `author`          | -                                         | 作者名称。Author's name.                                               |
| `email`           | -                                         | 作者邮件。Author's email.                                              |
| `author_homepage` | `"/"`                                     | 作者主页。Author's homepage.                                           |
| `description`     | `"A marvelous site powered by Maverick!"` | 网站描述。Description of your site.                                    |
| `keywords`        | -                                         | 网站关键字。Four or five keywords about your site.                       |
| `external_links`  | -                                         | 友情链接。Will be used in `Links` section on home page.                |
| `nav`             | -                                         | Will be used to generate navigations behind site title.      |
| `social_links`    | -                                         | 社交链接。Will be used to generate social links behind site title.     |
| `valine`          | -                                         | 评论配置。Maverick now supports Valine as its comment system. Please refer to [Comments][9] for more information. |
| `head_addon`      | -                                         | 添加到 `<head>` 的内容。Content here will be added to `<head>` tag of generated HTMLs, you can put some `meta` tag here, or use `<link>` and `<script>` to import custom CSS and JavaScript files. |
| `footer_addon`    | -                                         | 添加到 `<footer>` 的内容。Content here will be added to `<footer>` tag. You can add some additional info here. |
| `body_addon`      | -                                         | 添加到 `<body>` 的内容。Content here will be added to `<body>` tag, external JavaScripts and can be put here. |
| `language`        | `"english"`                               | 网站语言。Site language.                                               |
| `background_img`  | -                                         | 背景图片。Background image for your site. Better be light-colored.     |

💡 注意： 您可以通过 `${option_name}` 来访问其他选项。例如，如果你将 `site_prefix` 设置为 `/`，`${site_prefix}logo.png`将被解析成 `/logo.png`。 使用此功能时，**当心无限循环**。

💡 注意： 如果您启用了jsDelivr作为CDN服务，你可以使用 `${static_prefix}` 替换 `${site_prefix}` 来引用静态文件。

💡 注意： 您还可以使用 `config.py` 以外的配置文件，只需在构建时指定它即可：

```bash
python ./build.py -c "./my_conf.py"
# or
python ./build.py --config "./my_conf.py"
```

## Images and Static Assets | 图像和静态文件

Maverick是一个灵活的生成器，它不需要您将文件放在某个固定位置，取而代之的是设置 `source_dir` 文件夹。它会自动检测所有源文件来构建您的站点。
但是图像和其他的静态文件夹呢？例如像字体或者其他。Maverick 有自己的规则来处理这些问题。

### Static Assets | 静态文件

如果在 `source_dir` 下有一个名为 `static` 的文件夹，Maverick 将会拷贝改文件夹中的所有内容到 `build_dir` 。例如，如果 `source_dir` 看起来像这样：

```
source_dir/
	- static/
		- favicon.ico
		- robots.txt
		- font/
   	- ...
```

结果将是这样的：

```
build_dir/
	- favicon.ico
	- robots.txt
	- fonts/
```

简单吧？

### Images | 图像

你可以将所有的图像放在 `static` 文件夹中，Maverick 的设计可以非常巧妙地处理图像。事实上，你可以将你的图像文件放在你机器的**任何位置**，或者通过 URL 在你的 Markdown 文件中插入远端图像，当生成你的静态网站时，Maverick 将会把图像收集在一起，并将他们放在一个统一的位置， 同时处理您文章中的链接。

通过这种方式，您可以使用任何喜欢的在线服务自由地管理图像，或者仅将它们保存在本地计算机上，并按文章中的相对或绝对路径引用它们。许多Markdown编辑器(像出色的 [Typora]())都支持插入本地图像并可以正确显示它们。这是真正的 **所见即所得** （你所看到的就是你得到的）。例如，如果您具有这样的文件夹结构：

```
source_dir/
	- assets/
		- pic.jpg
	- article.md
```

在 `article.md` 文件中，您可以像下面这样插入`pic.jpg`：

```markdown
![](./assets/pic.jpg)
```

解析 `article.md` 时，Maverick 将尝试在您的机器上找到 `./assets/pic.jpg`，如果找到，Maverick 将其复制到 `build_dir/archives/asstes/`，然后在 `article.md` 中更改链接。

Maverick 采取这样设计的一个重要原因是，在许多案例中，比如网页上的 light-box 和照片布置需要预定义的图像尺寸。与在前端获取大小信息不同，在构建阶段解析大小信息可以极大地改善体验。 **此外，此设计还可以为所有图像启用jsDelivr作为CDN服务。**

但是它对远程图像来说很特殊。我们无法轻松得到它的大小信息，所以 Maverick 先尝试下载远端图像到本地磁盘，将它们视为本地图像。这个特性是默认禁用的，你可以通过修改配置文件中的 `fetch_remote_imgs` 为 `True` 来打开它。如果你不想将完整图像下载到本地，请保持这个选项为 `False` ，Maverick 将尝试通过下载图像的一小部分来获取图像的大小（在大多数情况下，只有需要1 〜2 KB）。

所有远程图像和尺寸信息都在本地缓存，因此 Maverick 不会每次构建中下载图像文件。

## Markdown

Maverick 使用 [mistune 0.8.4][11] 作为其基础Markdown解析器，并进行了一些扩展。

### Math Equations | 数学方程

您可以像这样插入数学方程：

```
# inline math
$m\times n$

## block math
$$C_{m\times k}=A_{m\times n}\cdot B_{n\times k}$$
```

### Code Highlighting | 代码高亮

使用 Markdown 语法插入代码块时只需指定语言，它将自动突出显示：


```cpp
int main(int argc , char** argv){
    std::cout << "Hello World!\n";
    return 0;
}
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
[Name][12]+(image URL)
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
````

Checkout more options [here](http://dplayer.js.org/guide.html).

## Themes

Maverick has two built-in themes, [Galileo](https://github.com/AlanDecode/Maverick-Theme-Galileo) and [Kepler](https://github.com/AlanDecode/Maverick-Theme-Kepler). You can easily switch between theme by setting `template` entry in config.py:

```python
template = 'Galileo' # or 'Kepler'
````

对于第三方主题，有三种使用方式。

1. 将第三方主题放在 `Templates` 文件夹下，然后在 config.py 将 `template` 设置为主题名称。例如，如果您具有这样的文件结构：

```
Templates/
	__init__.py
	MyTheme/
		__init__.py
```

   你需要在 config.py 文件中将 `template` 设置为下面这样：

```python
template = "MyTheme"
```

2. 将第三方主题放在任何本地文件夹下，然后在config.py中设置 `template`。 例如，如果您具有这样的文件夹结构：
```
/some/path/to/MyTheme/
	__init__.py
```

   你需要在 config.py 文件中将 `template` 设置为下面这样：
   
```python
template = {
    "name": "MyTheme",
    "type": "local",
    "path": "/some/path/to/MyTheme/" # could also use relatetive path to Maverick
}
```


3. 从远程Git存储库安装主题。 如果主题是Git开源的，则可以配置Maverick直接使用它。 例如，您还可以像这样使用 `Kepler` 主题：

```python
template = {
    "name": "Kepler",
    "type": "git",
    "url": "https://github.com/AlanDecode/Maverick-Theme-Kepler.git",
    "branch": "latest"
}
```

   请咨询主题提供人以获取详细安装信息。

## Comments | 评论

Maverick 有内置对 [Valine][13] 的支持, 有关更多信息请参考 [Valine Docs][14]。 你需要在配置文件中填写以下以下参数：

```python
valine = {
    "enable": True,
    "el": '#vcomments',
    "appId": "<your appId here>",
    "appKey": "<your appKey here>",
}
```

## Development | 开发

欢迎提交 Pull requests 。 查看 [theme-Dev.md][15] 有关为 Maverick 开发主题的文档。

## License

MIT © [AlanDecode][16].

[1]:	https://alandecode.github.io/Maverick/
[2]:	https://github.com/AlanDecode/Maverick/actions
[3]:	https://github.com/AlanDecode/Maverick/issues
[4]:	#comments
[5]:	#Themes
[6]:	#images-and-static-assets
[7]:	https://stackoverflow.com/questions/13866926/is-there-a-list-of-pytz-timezones
[8]:	https://www.jsdelivr.com/
[9]:	#comments
[11]:	https://github.com/lepture/mistune/tree/v1
[12]:	link
[13]:	https://valine.js.org/
[14]:	https://valine.js.org/en/quickstart.html
[15]:	https://github.com/AlanDecode/Maverick/blob/master/theme-Dev.md
[16]:	https://github.com/AlanDecode

[image-1]:	https://img.shields.io/badge/Preview-GitHub-blue?style=flat-square
[image-2]:	https://github.com/AlanDecode/Maverick/workflows/Build/badge.svg
[image-3]:	https://img.shields.io/github/license/AlanDecode/Maverick.svg?style=flat-square
