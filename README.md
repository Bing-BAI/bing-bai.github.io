# 阿冰成长记录

一个适合 GitHub Pages 的中文个人博客。暖白纸感、绿色点缀，包含首页、分类筛选、文章归档、关于我和独立文章页面。适配手机，关闭 JavaScript 也能浏览全部文章。

## 本地预览

需要 Python 3.9 或更高版本，无需安装依赖：

```sh
python3 build.py
python3 -m http.server 8000 --directory _site
```

打开 http://localhost:8000 。修改后重新运行构建，再刷新浏览器。

## 发布到 GitHub Pages

1. 在自己的 GitHub 账号下创建仓库。个人主页可使用 `你的用户名.github.io`，也可使用普通仓库名（如 `blog`）。
2. 将本项目源文件（包括 `.github` 目录）上传或推送到仓库的 `main` 分支，不需要上传 `_site`。
3. 进入仓库 **Settings → Pages → Build and deployment → Source**，选择 **GitHub Actions**。
4. 在 **Actions** 中运行 **Publish blog to GitHub Pages → Run workflow**。以后每次推送到 `main` 都会自动更新博客。
5. 部署成功后，在 **Settings → Pages** 或工作流部署结果中查看真实网址。

官方说明：https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages

页面使用相对链接，兼容个人域名根目录和普通仓库的子目录。若默认分支不是 `main`，同步修改 `.github/workflows/pages.yml` 的分支名。

## 发布新文章

在 `posts/` 新建一个 Markdown 文件，例如 `2026-09-08-my-first-post.md`。文件名请使用英文、数字和短横线，它也是文章链接的一部分：

```md
---
title: 我的第一篇成长记录
date: 2026-09-08
category: 成长随笔
summary: 一句话介绍这篇文章。
---
这里写正文。

## 今天的小收获

写下一个具体的进步。

- 一件学会的事
- 一个想继续探索的问题

> 留给未来自己的一句话。
```

这个轻量构建器支持段落、二级标题、无序列表、引用。不处理完整 Markdown 语法（如链接、图片、加粗和代码块），HTML 会被转义为文字。日期须为 `YYYY-MM-DD`。每篇文章都会公开发布；不要放入草稿或私人内容，未来日期也不会自动隐藏。

三篇初始内容均为示例，不代表你的真实经历。可删除或改写；正式文章移除 `sample: true` 即可。归档和分类自动从文章生成。

## 修改个人信息

编辑 `site.json` 的博客名称、作者、简介和标语。关于页的其他文字在 `build.py` 中，视觉样式在 `assets/style.css` 中。

## 项目结构

- `posts/`：文章源文件
- `site.json`：个人信息
- `assets/`：样式、分类交互和图标
- `build.py`：静态页面生成器
- `.github/workflows/pages.yml`：GitHub Pages 自动发布
- `_site/`：生成的网站（不提交 Git）
