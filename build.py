"""Build the public site; only explicitly selected content is exported."""
from pathlib import Path
from html import escape as e
from datetime import date
import json
import shutil
import re
from rendering import markdown
from project_content import load_profile

ROOT = Path(__file__).resolve().parent
OUT = ROOT / '_site'
config = json.loads((ROOT / 'site.json').read_text())
profile = load_profile(ROOT)


posts = []
for path in (ROOT / 'posts').glob('*.md'):
    match = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)(.*)\Z', path.read_text(), re.S)
    if not match:
        raise ValueError(f'{path}: invalid front matter')
    front, body = match.groups()
    post = dict(line.split(':', 1) for line in front.strip().splitlines())
    post = {k.strip(): v.strip() for k, v in post.items()}
    for key in ('title', 'date', 'category', 'summary'):
        if not post.get(key):
            raise ValueError(f'{path}: missing {key}')
    date.fromisoformat(post['date'])
    if post.get('draft') == 'true' or post['date'] > date.today().isoformat():
        continue
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
    nav = ''.join(f'<a href="{prefix}{href}" {"aria-current=page" if key == active else ""}>{label}</a>' for key, href, label in [('home','index.html','首页'), ('archive','archive.html','文章归档'), ('about','about.html','关于我'), ('ask','ask.html','向 Agent 提问')])
    return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)} · {e(config['title'])}</title><meta name="description" content="{e(description or config['description'], quote=True)}">
<meta name="theme-color" content="#f5f5f2"><link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{prefix}assets/style.css"><script src="{prefix}assets/main.js" defer></script></head>
<body><a class="skip" href="#main">跳至内容</a><div class="shell"><header class="header"><a class="brand" href="{prefix}index.html"><span class="brand-icon">B.</span><span>{e(config['title'])}<small>AI SOLUTIONS & ENGINEERING</small></span></a><nav aria-label="主导航">{nav}</nav></header>
<main id="main">{content}</main><footer><span>© {date.today().year} {e(config['author'])} · AI Solutions & Engineering</span><span>从问题出发，在交付中持续迭代。</span></footer></div></body></html>'''

def meta(p):
    return f'<span class="category">{e(p["category"])}</span><time datetime="{p["date"]}">{p["date"].replace("-", ".")}</time>' + ('<span class="sample">示例文章</span>' if p.get('sample') == 'true' else '')

def card(p, index):
    return f'''<article class="post-row" data-category="{e(p['category'], quote=True)}"><span class="post-number">{index:02}</span><div><div class="meta">{meta(p)}</div><h3><a href="./posts/{p['slug']}.html">{e(p['title'])}</a></h3><p>{e(p['summary'])}</p></div><span class="row-arrow" aria-hidden="true">↗</span></article>'''

published = [p for p in posts if p.get('sample') != 'true']
categories = list(dict.fromkeys(p['category'] for p in published))
filters = '<div class="filters" role="group" aria-label="按分类筛选" hidden>' + ''.join(f'<button type="button" aria-pressed="{str(i == 0).lower()}" data-filter="{e(c, quote=True)}">{e(c)}</button>' for i,c in enumerate(['全部文章'] + categories)) + '</div>'
def project_card(p, i):
    return f'<a class="project-card" href="./projects/{p["slug"]}.html"><div class="project-top"><span>{i:02} / 项目经历</span><span aria-hidden="true">↗</span></div><p class="project-domain">{e(p["domain"])}</p><h3>{e(p["title"])}</h3><p>{e(p["challenge"])}</p><div class="tags">' + ''.join(f'<span>{e(t)}</span>' for t in p['tags']) + '</div></a>'

hero = f'''<section class="brand-hero"><div class="hero-copy"><div class="eyebrow">{e(profile['role'])}</div><h1>让 AI 走出实验，<br><span>进入真实业务。</span></h1><p>{e(profile['intro'])}</p><div class="hero-actions"><a class="primary-link" href="#projects">探索我的项目 <span>↗</span></a><a class="text-link" href="./ask.html">向我的 Agent 提问 →</a></div></div><aside class="identity-card"><div class="identity-monogram">Bing</div><h2>{e(profile['name'])}</h2><p>AI SOLUTIONS & ENGINEERING</p><div class="identity-detail"><span>关注</span><strong>{e(profile["focus"])}</strong></div><div class="identity-detail"><span>研究</span><strong>高效学习与模型压缩</strong></div><a href="./about.html">认识我 <span>↗</span></a></aside></section>'''
capabilities = '<section class="capabilities" aria-label="专业能力">' + ''.join(f'<div><span class="eyebrow">0{i}</span><h2>{e(c["title"])}</h2><p>{e(c["text"])}</p><small>{e(c["tags"])}</small></div>' for i,c in enumerate(profile['capabilities'],1)) + '</section>'
def project_section(*, archive=False):
    destination = '' if archive else '<a href="./archive.html#projects">全部项目 →</a>'
    return '<section id="projects" class="projects-section"><div class="section-title"><div><h2>项目经历</h2><p class="section-description">用项目，说明我如何解决问题。</p></div><div class="section-actions">' + destination + '<div class="carousel-controls" hidden><button type="button" data-scroll="-1" aria-controls="project-track" aria-label="向左浏览项目">←</button><button type="button" data-scroll="1" aria-controls="project-track" aria-label="向右浏览项目">→</button></div></div></div><div id="project-track" class="projects-grid" tabindex="0" role="region" aria-label="项目经历，横向滚动浏览">' + ''.join(project_card(p,i) for i,p in enumerate(profile['projects'],1)) + '</div></section>'

articles = ''.join(card(p,i+1) for i,p in enumerate(published)) or '<div class="writing-empty"><p>技术思考正在整理。</p><span>接下来会在这里分享项目复盘、技术判断与工程实践。</span></div>'
writing = '<section id="writing" class="writing-section"><div class="section-title"><div><h2>技术思考</h2></div><a href="./archive.html#writing">全部文章 →</a></div>' + articles + '</section>'
(OUT / 'index.html').write_text(page('首页', hero + capabilities + project_section() + writing))
archive_links = f'<nav class="archive-sections" aria-label="归档栏目"><a href="#projects">项目经历 <span>{len(profile["projects"]):02}</span></a><a href="#writing">技术思考 <span>{len(published):02}</span></a></nav>'
archive_writing = '<section id="writing" class="writing-section"><div class="section-title"><h2>技术思考</h2><span>' + str(len(published)) + ' 篇文章</span></div>' + (filters if published else '') + articles + '<p class="filter-status sr-only" aria-live="polite"></p></section>'
archive = '<section class="simple-head archive-head"><h1>文章归档</h1><p>项目经历与技术思考，记录从问题到交付的过程。</p></section>' + archive_links + project_section(archive=True) + archive_writing
(OUT / 'archive.html').write_text(page('文章归档', archive, active='archive'))
certificates = '<section class="certifications" aria-label="专业认证"><h2>专业认证</h2>' + ''.join(
    f'<div class="certification-card"><span class="certification-mark" aria-hidden="true">ACP</span><div><h3>{e(c["title"])}</h3><p class="certification-name">{e(c["official_name"])}</p><a class="certificate-link" href="{e(c["url"],quote=True)}" target="_blank" rel="noopener noreferrer">查看证书原件 <span aria-hidden="true">↗</span><span class="sr-only">（在新标签页打开）</span></a></div></div>'
    for c in profile.get('certifications', [])
) + '</section>'
social_links = '<div class="social-links" aria-label="社交平台">' + ''.join(
    f'<a class="social-link" href="{e(profile[key],quote=True)}" target="_blank" rel="noopener noreferrer" aria-label="访问白冰的 {label} 主页（在新标签页打开）"><img src="./assets/icons/{key}.svg" width="26" height="26" alt="" aria-hidden="true"></a>'
    for key, label in [('github', 'GitHub'), ('medium', 'Medium')] if profile.get(key)
) + '</div>'
about_intro = '<div class="about-intro">' + ''.join(f'<p>{e(text)}</p>' for text in profile['about_paragraphs']) + '</div>'
values = '<section class="about-values"><h2>我能带来的价值</h2><div class="value-grid">' + ''.join(f'<div class="value-card"><h3>{e(v["title"])}</h3><p>{e(v["text"])}</p></div>' for v in profile['value_propositions']) + '</div></section>'
goal = f'<section class="about-goal"><span class="eyebrow">我的目标</span><h2>{e(profile["goal"]["statement"])}</h2><p>{e(profile["goal"]["description"])}</p></section>'
methods = '<section class="about-methods"><h2>我的工作方法</h2><p class="section-intro">把复杂问题变得可理解、可验证，再把有效经验沉淀为下一次可以复用的方法。</p><ol class="method-grid">' + ''.join(f'<li><span class="method-number" aria-hidden="true">{i:02}</span><h3>{e(m["title"])}</h3><p class="method-principle">{e(m["principle"])}</p><p>{e(m["practice"])}</p></li>' for i,m in enumerate(profile['methods'],1)) + '</ol></section>'
career = '<section class="about-career"><h2>职业与研究脉络</h2><ol class="career-list">' + ''.join(f'<li><h3>{e(item["title"])}</h3><p>{e(item["text"])}</p></li>' for item in profile['career']) + '</ol></section>'
education = '<section><h2>教育与语言</h2><ul>' + ''.join(f'<li>{e(x)}</li>' for x in profile['education']) + '</ul><div class="language-list">' + ''.join(f'<span>{e(x)}</span>' for x in profile['languages']) + '</div></section>'
skills = '<section class="about-skills"><h2>技术能力</h2>' + ''.join(f'<div class="skill-row"><h3>{e(group["title"])}</h3><div class="tags">' + ''.join(f'<span>{e(item)}</span>' for item in group['items']) + '</div></div>' for group in profile['skill_groups']) + '</section>'
about = f'<section class="simple-head"><div class="eyebrow">ABOUT BING</div><h1>{e(profile["english_name"])} / {e(profile["name"])}</h1><p>{e(profile["role"])}</p></section><article class="prose about">' + about_intro + values + goal + methods + career + certificates + education + skills + '<h2>建立连接</h2>' + social_links + '</article>'
(OUT / 'about.html').write_text(page('关于我', about, active='about'))
(OUT / 'projects').mkdir(exist_ok=True)
for p in profile['projects']:
    sections = p['case_study']
    outline = '<nav class="case-nav" aria-label="项目拆解目录">' + ''.join(f'<a href="#case-{e(section["id"],quote=True)}"><span>{i:02}</span> {e(section["title"])}</a>' for i, section in enumerate(sections, 1)) + '</nav>'
    body = ''.join(f'<section id="case-{e(section["id"],quote=True)}" class="case-section"><h2><span class="case-number">{i:02}</span>{e(section["title"])}</h2>{markdown(section["content"])}</section>' for i, section in enumerate(sections, 1))
    content = f'<div class="reading"><a class="back" href="../archive.html#projects">← 返回项目经历</a><header class="article-head"><div class="eyebrow">{e(p["domain"])}</div><h1>{e(p["title"])}</h1><p>{e(p["role"])}</p></header>{outline}<article class="prose case-study">{body}</article><div class="article-end">客户信息已匿名化 · 仅展示个人参与范围</div><a class="back" href="../ask.html">向 Agent 了解更多 →</a></div>'
    (OUT / 'projects' / f'{p["slug"]}.html').write_text(page(p['title'], content, prefix='../', active='', description=p['challenge']))

for p in posts:
    content = f'<div class="reading"><a class="back" href="../archive.html">← 返回文章列表</a><header class="article-head"><div class="meta">{meta(p)}</div><h1>{e(p["title"])}</h1><p>{e(p["summary"])}</p></header><article class="prose">{p["body"]}</article><div class="article-end">— 谢谢你读到这里 —</div><a class="back" href="../archive.html">浏览全部记录 →</a></div>'
    (OUT / 'posts' / f'{p["slug"]}.html').write_text(page(p['title'], content, prefix='../', active='', description=p['summary']))
api_url = config.get('agent_api_url', '').strip()
if api_url and not api_url.startswith('https://'):
    raise ValueError('agent_api_url must use HTTPS')
questions = ['白冰主要擅长哪些 AI 技术？', '有哪些从模型到系统的项目经验？', '在 RAG 项目中承担过什么工作？']
ask = '<section class="simple-head"><div class="eyebrow">ASK BING’S AGENT</div><h1>从一个问题，认识我。</h1><p>了解我的项目经历、技术方向与工作方式。</p></section><section class="chat-panel" aria-label="个人知识助手"><div class="chat-intro"><span class="agent-mark">B.</span><div><h2>白冰的 Agent</h2><p>根据经确认的个人资料回答，并展示回答依据。</p></div></div><div class="question-chips">' + ''.join(f'<button type="button" data-question="{e(q,quote=True)}" disabled>{e(q)} ↗</button>' for q in questions) + f'</div><p id="agent-status" role="status">' + ('正在连接知识助手…' if api_url else '知识助手正在准备中。你可以先浏览项目和个人介绍。') + f'</p><div id="conversation" role="log" aria-live="polite" aria-label="问答记录"></div><form id="ask-form" data-api="{e(api_url,quote=True)}"><label for="question">你的问题</label><textarea id="question" name="question" rows="3" maxlength="1000" placeholder="例如：白冰是怎样处理客户的离线部署需求的？" disabled required></textarea><div class="compose-footer"><small>问题会发送给阿里云百炼处理，请勿填写私人信息。每次提问独立回答。</small><button class="primary-link" type="submit" disabled>发送问题 ↗</button></div></form><noscript>请启用 JavaScript 使用知识助手。</noscript></section>'
(OUT / 'ask.html').write_text(page('向 Agent 提问', ask, active='ask'))
(OUT / '.nojekyll').touch()
print(f'Built brand site: {len(profile["projects"])} projects, {len(published)} published articles, agent configured: {bool(api_url)}')
