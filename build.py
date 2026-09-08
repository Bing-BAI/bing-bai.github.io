"""Build a dependency-free blog. Supported Markdown: paragraphs, ## headings, quotes, lists."""
from pathlib import Path
from html import escape as e
from datetime import date
import json
import shutil

ROOT = Path(__file__).resolve().parent
OUT = ROOT / '_site'
config = json.loads((ROOT / 'site.json').read_text())

def markdown(text):
    blocks, paragraph, items = [], [], []
    def flush():
        if paragraph:
            blocks.append('<p>' + e(' '.join(paragraph)) + '</p>')
            paragraph.clear()
        if items:
            blocks.append('<ul>' + ''.join('<li>' + e(x) + '</li>' for x in items) + '</ul>')
            items.clear()
    for line in text.splitlines():
        if not line.strip():
            flush()
        elif line.startswith('## '):
            flush()
            blocks.append('<h2>' + e(line[3:]) + '</h2>')
        elif line.startswith('> '):
            flush()
            blocks.append('<blockquote>' + e(line[2:]) + '</blockquote>')
        elif line.startswith('- '):
            if paragraph:
                flush()
            items.append(line[2:])
        else:
            if items:
                flush()
            paragraph.append(line)
    flush()
    return '\n'.join(blocks)

posts = []
for path in (ROOT / 'posts').glob('*.md'):
    _, front, body = path.read_text().split('---', 2)
    post = dict(line.split(':', 1) for line in front.strip().splitlines())
    post = {k.strip(): v.strip() for k, v in post.items()}
    for key in ('title', 'date', 'category', 'summary'):
        if not post.get(key):
            raise ValueError(f'{path}: missing {key}')
    date.fromisoformat(post['date'])
    post.update(slug=path.stem, body=markdown(body))
    posts.append(post)
posts.sort(key=lambda p: (p['date'], p['slug']), reverse=True)
OUT.mkdir(exist_ok=True)
# Remove only previously generated article pages, keeping the source untouched.
if (OUT / 'posts').exists():
    shutil.rmtree(OUT / 'posts')
(OUT / 'posts').mkdir()
shutil.copytree(ROOT / 'assets', OUT / 'assets', dirs_exist_ok=True)
if (ROOT / '.well-known').exists():
    shutil.copytree(ROOT / '.well-known', OUT / '.well-known', dirs_exist_ok=True)

def page(title, content, prefix='./', active='home', description=None):
    nav = ''.join(f'<a href="{prefix}{href}" {"aria-current=page" if key == active else ""}>{label}</a>' for key, href, label in [('home','index.html','首页'), ('archive','archive.html','文章归档'), ('about','about.html','关于我')])
    return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)} · {e(config['title'])}</title><meta name="description" content="{e(description or config['description'], quote=True)}">
<meta name="theme-color" content="#f8f9f5"><link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{prefix}assets/style.css"><script src="{prefix}assets/main.js" defer></script></head>
<body><a class="skip" href="#main">跳至内容</a><div class="shell"><header class="header"><a class="brand" href="{prefix}index.html"><span class="brand-icon">冰</span><span>{e(config['title'])}<small>A BING’S JOURNAL</small></span></a><nav aria-label="主导航">{nav}</nav></header>
<main id="main">{content}</main><footer><span>© {date.today().year} {e(config['author'])} · 把日子写成自己的故事</span><span>写在此刻，留给未来。</span></footer></div></body></html>'''

def meta(p):
    return f'<span class="category">{e(p["category"])}</span><time datetime="{p["date"]}">{p["date"].replace("-", ".")}</time>' + ('<span class="sample">示例文章</span>' if p.get('sample') == 'true' else '')

def card(p, index):
    return f'''<article class="post-row" data-category="{e(p['category'], quote=True)}"><span class="post-number">{index:02}</span><div><div class="meta">{meta(p)}</div><h3><a href="./posts/{p['slug']}.html">{e(p['title'])}</a></h3><p>{e(p['summary'])}</p></div><span class="row-arrow" aria-hidden="true">↗</span></article>'''

categories = list(dict.fromkeys(p['category'] for p in posts))
filters = '<div class="filters" role="group" aria-label="按分类筛选" hidden>' + ''.join(f'<button type="button" aria-pressed="{str(i == 0).lower()}" data-filter="{e(c, quote=True)}">{e(c)}</button>' for i,c in enumerate(['全部文章'] + categories)) + '</div>'
hero = f'''<section class="hero"><div class="eyebrow"><span class="dot"></span> 一份持续生长的个人记录</div><h1>认真生活，<br>慢慢<span class="accent">生长。</span></h1><p>{e(config['description'])}<br>{e(config['tagline'])}</p><a class="hero-link" href="#writing">翻开我的记录 <span aria-hidden="true">↓</span></a><div class="hero-aside"><span>生活 / 学习 / 成长</span><span class="large-quote">“</span><p>把微小的进步，<br>写进漫长的日子。</p><span class="aside-line"></span><small>NOTES TO MY FUTURE SELF</small></div></section>'''
sidebar = f'''<aside class="sidebar"><div class="profile"><span class="avatar">冰</span><h2>你好，我是{e(config['author'])}。</h2><p>{e(config['about'])}</p><a href="./about.html">更多关于我 <span aria-hidden="true">↗</span></a></div><div class="side-note"><span class="eyebrow">关于这里</span><p>不急着成为谁，<br>先记录每一个真实的自己。</p><span class="small-label">保持好奇 · 持续记录</span></div></aside>'''
home = hero + f'<div class="content-grid"><section id="writing"><div class="section-title"><h2>最近的记录</h2><span>{len(posts):02} 篇文字</span></div>{filters}<div class="post-list">' + ''.join(card(p,i+1) for i,p in enumerate(posts)) + f'</div><p class="filter-status sr-only" aria-live="polite"></p></section>{sidebar}</div>'
(OUT / 'index.html').write_text(page('首页', home))
archive = '<section class="simple-head"><div class="eyebrow">THE ARCHIVE</div><h1>沿途的记录</h1><p>把散落的日子，连成一条成长的线。</p></section>' + filters + ''.join(card(p,i+1) for i,p in enumerate(posts)) + '<p class="filter-status sr-only" aria-live="polite"></p>'
(OUT / 'archive.html').write_text(page('文章归档', archive, active='archive'))
about = f'<section class="simple-head"><div class="eyebrow">A LITTLE ABOUT ME</div><h1>你好，我是{e(config["author"])}。</h1><p>{e(config["tagline"])}</p></section><article class="prose about"><p>{e(config["about"])}</p><h2>在这里记录什么</h2><p>学习中一点一滴的收获，生活里值得收藏的片刻，以及成长途中反复思考的问题。</p><h2>写给未来的自己</h2><p>希望回头看时，能看见走过的路，也能认出每一个阶段认真生活的自己。</p><a href="./archive.html">去看看沿途的记录 →</a></article>'
(OUT / 'about.html').write_text(page('关于我', about, active='about'))
for p in posts:
    content = f'<div class="reading"><a class="back" href="../index.html#writing">← 返回文章列表</a><header class="article-head"><div class="meta">{meta(p)}</div><h1>{e(p["title"])}</h1><p>{e(p["summary"])}</p></header><article class="prose">{p["body"]}</article><div class="article-end">— 谢谢你读到这里 —</div><a class="back" href="../archive.html">浏览全部记录 →</a></div>'
    (OUT / 'posts' / f'{p["slug"]}.html').write_text(page(p['title'], content, prefix='../', active='', description=p['summary']))
(OUT / '.nojekyll').touch()
print(f'Built {len(posts)} articles and 3 pages in {OUT}')
