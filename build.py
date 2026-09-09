"""Build the public site; only explicitly selected content is exported."""
from pathlib import Path
from html import escape as e
from datetime import date
import json
import shutil
import re
import hashlib
from rendering import markdown
from project_content import load_profile

ROOT = Path(__file__).resolve().parent

def build_language(lang):
    OUT = ROOT / '_site' / ('en' if lang == 'en' else '')
    config = json.loads((ROOT / 'site.json').read_text())
    if lang == 'en':
        config.update(json.loads((ROOT / 'locales/en/site.json').read_text()))
    profile = load_profile(ROOT, lang)
    asset_version = hashlib.sha256((ROOT / 'assets/style.css').read_bytes() + (ROOT / 'assets/main.js').read_bytes()).hexdigest()[:12]
    ui = json.loads((ROOT / f'locales/{lang}.json').read_text())
    def labels(text):
        return re.sub(r'\[\[(\w+)\]\]', lambda m: e(ui[m[1]], quote=True), text)




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
        if lang == 'en':
            translated = ROOT / 'locales/en/posts' / path.name
            if translated.exists():
                match_en = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)(.*)\Z', translated.read_text(), re.S)
                if not match_en:
                    raise ValueError(f'{translated}: invalid front matter')
                metadata = dict(line.split(':', 1) for line in match_en[1].strip().splitlines())
                metadata = {k.strip(): v.strip() for k, v in metadata.items()}
                for key in ('title', 'category', 'summary'):
                    if not metadata.get(key):
                        raise ValueError(f'{translated}: missing {key}')
                    post[key] = metadata[key]
                post['body'] = markdown(match_en[2])
            else:
                post.update(title=ui['untranslated'], category=ui['chinese_article'], summary=ui['translation_pending'],
                    body=f'<p>{e(ui["translation_pending"])}</p><p><a href="../../posts/{path.stem}.html" lang="zh-CN">{e(ui["read_chinese"])}</a></p>')
        posts.append(post)
    posts.sort(key=lambda p: (p['date'], p['slug']), reverse=True)
    OUT.mkdir(parents=True, exist_ok=True)
    # Remove only previously generated article pages, keeping the source untouched.
    if (OUT / 'posts').exists():
        shutil.rmtree(OUT / 'posts')
    (OUT / 'posts').mkdir()
    if lang == 'zh':
        shutil.copytree(ROOT / 'assets', OUT / 'assets', dirs_exist_ok=True)
    if lang == 'zh' and (ROOT / '.well-known').exists():
        shutil.copytree(ROOT / '.well-known', OUT / '.well-known', dirs_exist_ok=True)

    def page(title, content, prefix='./', active='home', description=None, route=None):
        route = route or ('index.html' if active == 'home' else f'{active}.html')
        base = prefix + ('../' if lang == 'en' else '')
        zh_url, en_url = base + route, base + 'en/' + route
        switch = '<div class="language-switch" role="group" aria-label="Language / 语言">' + ''.join(
            f'<a href="{url}" lang="{code}" hreflang="{code}" data-language="{code}"' +
            (' aria-current="true"' if selected else '') + f'>{label}</a>'
            for code, url, label, selected in [('zh-CN', zh_url, '中', lang == 'zh'), ('en', en_url, 'EN', lang == 'en')]
        ) + '</div>'
        if lang == 'en':
            content = re.sub(r'((?:href|src)=")([.]{1,2}/)assets/', lambda m: m[1] + ('../' if m[2] == './' else '../../') + 'assets/', content)
        alternates = f'<link rel="alternate" hreflang="zh-CN" href="{zh_url}"><link rel="alternate" hreflang="en" href="{en_url}"><link rel="alternate" hreflang="x-default" href="{zh_url}">'
        nav = ''.join(f'<a href="{prefix}{href}" {"aria-current=page" if key == active else ""}>{label}</a>' for key, href, label in [('home','index.html','[[home]]'), ('archive','archive.html','[[archive]]'), ('about','about.html','[[about]]'), ('ask','ask.html','[[ask]]')])
        return labels(f'''<!doctype html>
    <html lang="{'en' if lang == 'en' else 'zh-CN'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
    <title>{e(title)} · {e(config['title'])}</title><meta name="description" content="{e(description or config['description'], quote=True)}">
    {alternates}<meta name="theme-color" content="#f5f5f2"><link rel="icon" href="{base}assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{base}assets/style.css?v={asset_version}"><script src="{base}assets/main.js?v={asset_version}" defer></script></head>
    <body><a class="skip" href="#main">[[skip]]</a><div class="shell"><header class="header"><div class="brand-group"><a class="brand" href="{prefix}index.html" aria-label="[[home_label]]"><span class="brand-icon" aria-hidden="true">冰</span></a>{switch}</div><nav aria-label="[[navigation]]">{nav}</nav></header>
    <main id="main">{content}</main><footer><span>© {date.today().year} {e(config['author'])} · AI Solutions & Engineering</span><span>[[footer]]</span></footer></div></body></html>''')

    def meta(p):
        return f'<span class="category">{e(p["category"])}</span><time datetime="{p["date"]}">{p["date"].replace("-", ".")}</time>' + ('<span class="sample">[[sample]]</span>' if p.get('sample') == 'true' else '')

    def card(p, index):
        return f'''<article class="post-row" data-category="{e(p['category'], quote=True)}"><span class="post-number">{index:02}</span><div><div class="meta">{meta(p)}</div><h3><a href="./posts/{p['slug']}.html">{e(p['title'])}</a></h3><p>{e(p['summary'])}</p></div><span class="row-arrow" aria-hidden="true">↗</span></article>'''

    published = [p for p in posts if p.get('sample') != 'true']
    categories = list(dict.fromkeys(p['category'] for p in published))
    filters = '<div class="filters" role="group" aria-label="[[filter_label]]" hidden>' + ''.join(f'<button type="button" aria-pressed="{str(i == 0).lower()}" data-filter="{e(c, quote=True) if i else '*'}">{e(c)}</button>' for i,c in enumerate(['[[all_articles]]'] + categories)) + '</div>'
    def project_card(p, i):
        return f'<a class="project-card" href="./projects/{p["slug"]}.html"><div class="project-top"><span>{i:02} / [[projects]]</span><span aria-hidden="true">↗</span></div><p class="project-domain">{e(p["domain"])}</p><h3>{e(p["title"])}</h3><p>{e(p["challenge"])}</p><div class="tags">' + ''.join(f'<span>{e(t)}</span>' for t in p['tags']) + '</div></a>'

    hero = f'''<section class="brand-hero"><div class="hero-copy"><div class="eyebrow">{e(profile['role'])}</div><h1>[[hero_first]]<br><span>[[hero_second]]</span></h1><p>{e(profile['intro'])}</p><div class="hero-actions"><a class="primary-link" href="#projects">[[explore]] <span>↗</span></a><a class="text-link" href="./ask.html">[[ask_link]] →</a></div></div><aside class="identity-card"><div class="identity-monogram">Bing</div><h2 class="identity-contact"><span>{e(profile['name'])} ｜</span> <a href="mailto:bingbai.me@gmail.com">bingbai.me@gmail.com</a></h2><p>AI SOLUTIONS & ENGINEERING</p><a href="./about.html">[[meet]] <span>↗</span></a></aside></section>'''
    capabilities = '<section class="capabilities" aria-label="[[capabilities]]">' + ''.join(f'<div><span class="eyebrow">0{i}</span><h2>{e(c["title"])}</h2><p>{e(c["text"])}</p><small>{e(c["tags"])}</small></div>' for i,c in enumerate(profile['capabilities'],1)) + '</section>'
    def project_section(*, archive=False):
        destination = '' if archive else '<a href="./archive.html#projects">[[all_projects]] →</a>'
        return '<section id="projects" class="projects-section"><div class="section-title"><div><h2>[[projects]]</h2><p class="section-description">[[project_description]]</p></div><div class="section-actions">' + destination + '<div class="carousel-controls" hidden><button type="button" data-scroll="-1" aria-controls="project-track" aria-label="[[previous]]">←</button><button type="button" data-scroll="1" aria-controls="project-track" aria-label="[[next]]">→</button></div></div></div><div id="project-track" class="projects-grid" tabindex="0" role="region" aria-label="[[track]]">' + ''.join(project_card(p,i) for i,p in enumerate(profile['projects'],1)) + '</div></section>'

    articles = ''.join(card(p,i+1) for i,p in enumerate(published)) or '<div class="writing-empty"><p>[[notes_empty]]</p><span>[[notes_description]]</span></div>'
    writing = '<section id="writing" class="writing-section"><div class="section-title"><div><h2>[[notes]]</h2></div><a href="./archive.html#writing">[[all_articles]] →</a></div>' + articles + '</section>'
    (OUT / 'index.html').write_text(page('[[home]]', hero + capabilities + project_section() + writing))
    archive_links = f'<nav class="archive-sections" aria-label="[[archive_sections]]"><a href="#projects">[[projects]] <span>{len(profile["projects"]):02}</span></a><a href="#writing">[[notes]] <span>{len(published):02}</span></a></nav>'
    archive_writing = '<section id="writing" class="writing-section"><div class="section-title"><h2>[[notes]]</h2><span>' + str(len(published)) + ' [[article_count]]</span></div>' + (filters if published else '') + articles + '<p class="filter-status sr-only" aria-live="polite"></p></section>'
    archive = '<section class="simple-head archive-head"><h1>[[archive]]</h1><p>[[archive_intro]]</p></section>' + archive_links + project_section(archive=True) + archive_writing
    (OUT / 'archive.html').write_text(page('[[archive]]', archive, active='archive'))
    certificates = '<section class="certifications" aria-label="[[certifications]]"><h2>[[certifications]]</h2>' + ''.join(
        f'<div class="certification-card"><span class="certification-mark" aria-hidden="true">ACP</span><div><h3>{e(c["title"])}</h3><p class="certification-name">{e(c["official_name"])}</p><a class="certificate-link" href="{e(c["url"],quote=True)}" target="_blank" rel="noopener noreferrer">[[certificate_link]] <span aria-hidden="true">↗</span><span class="sr-only">[[new_tab]]</span></a></div></div>'
        for c in profile.get('certifications', [])
    ) + '</section>'
    social_links = '<div class="social-links" aria-label="[[social]]">' + ''.join(
        f'<a class="social-link" href="{e(profile[key],quote=True)}" target="_blank" rel="noopener noreferrer" aria-label="[[visit]] {label} [[profile_page]][[new_tab]]"><img src="./assets/icons/{key}.svg" width="26" height="26" alt="" aria-hidden="true"></a>'
        for key, label in [('github', 'GitHub'), ('medium', 'Medium')] if profile.get(key)
    ) + '</div>'
    about_intro = '<div class="about-intro">' + ''.join(f'<p>{e(text)}</p>' for text in profile['about_paragraphs']) + '</div>'
    values = '<section class="about-values"><h2>[[values]]</h2><div class="value-grid">' + ''.join(f'<div class="value-card"><h3>{e(v["title"])}</h3><p>{e(v["text"])}</p></div>' for v in profile['value_propositions']) + '</div></section>'
    goal = f'<section class="about-goal"><span class="eyebrow">[[goal]]</span><h2>{e(profile["goal"]["statement"])}</h2><p>{e(profile["goal"]["description"])}</p></section>'
    methods = '<section class="about-methods"><h2>[[methods]]</h2><p class="section-intro">[[method_intro]]</p><ol class="method-grid">' + ''.join(f'<li><span class="method-number" aria-hidden="true">{i:02}</span><h3>{e(m["title"])}</h3><p class="method-principle">{e(m["principle"])}</p><p>{e(m["practice"])}</p></li>' for i,m in enumerate(profile['methods'],1)) + '</ol></section>'
    career = '<section class="about-career"><h2>[[career]]</h2><ol class="career-list">' + ''.join(f'<li><h3>{e(item["title"])}</h3><p>{e(item["text"])}</p></li>' for item in profile['career']) + '</ol></section>'
    education = '<section><h2>[[education]]</h2><ul>' + ''.join(f'<li>{e(x)}</li>' for x in profile['education']) + '</ul><div class="language-list">' + ''.join(f'<span>{e(x)}</span>' for x in profile['languages']) + '</div></section>'
    skills = '<section class="about-skills"><h2>[[skills]]</h2>' + ''.join(f'<div class="skill-row"><h3>{e(group["title"])}</h3><div class="tags">' + ''.join(f'<span>{e(item)}</span>' for item in group['items']) + '</div></div>' for group in profile['skill_groups']) + '</section>'
    about = f'<section class="simple-head"><div class="eyebrow">ABOUT BING</div><h1>{e(profile["english_name"]) if lang == 'en' else e(profile["english_name"]) + ' / ' + e(profile["name"])}</h1><p>{e(profile["role"])}</p></section><article class="prose about">' + about_intro + values + goal + methods + career + certificates + education + skills + '<h2>[[connect]]</h2>' + social_links + '</article>'
    (OUT / 'about.html').write_text(page('[[about]]', about, active='about'))
    if (OUT / 'projects').exists():
        shutil.rmtree(OUT / 'projects')
    (OUT / 'projects').mkdir(exist_ok=True)
    for p in profile['projects']:
        sections = p['case_study']
        outline = '<nav class="case-nav" aria-label="[[outline]]">' + ''.join(f'<a href="#case-{e(section["id"],quote=True)}"><span>{i:02}</span> {e(section["title"])}</a>' for i, section in enumerate(sections, 1)) + '</nav>'
        body = ''.join(f'<section id="case-{e(section["id"],quote=True)}" class="case-section"><h2><span class="case-number">{i:02}</span>{e(section["title"])}</h2>{markdown(section["content"])}</section>' for i, section in enumerate(sections, 1))
        content = f'<div class="reading"><a class="back" href="../archive.html#projects">[[back_projects]]</a><header class="article-head"><div class="eyebrow">{e(p["domain"])}</div><h1>{e(p["title"])}</h1><p>{e(p["role"])}</p></header>{outline}<article class="prose case-study">{body}</article><div class="article-end">[[anonymized]]</div><a class="back" href="../ask.html">[[ask_more]] →</a></div>'
        (OUT / 'projects' / f'{p["slug"]}.html').write_text(page(p['title'], content, prefix='../', active='', description=p['challenge'], route=f'projects/{p["slug"]}.html'))

    for p in posts:
        content = f'<div class="reading"><a class="back" href="../archive.html">[[back_posts]]</a><header class="article-head"><div class="meta">{meta(p)}</div><h1>{e(p["title"])}</h1><p>{e(p["summary"])}</p></header><article class="prose">{p["body"]}</article><div class="article-end">[[thanks]]</div><a class="back" href="../archive.html">[[browse]] →</a></div>'
        (OUT / 'posts' / f'{p["slug"]}.html').write_text(page(p['title'], content, prefix='../', active='', description=p['summary'], route=f'posts/{p["slug"]}.html'))
    api_url = config.get('agent_api_url', '').strip()
    if api_url and not api_url.startswith('https://'):
        raise ValueError('agent_api_url must use HTTPS')
    questions = ['[[q1]]', '[[q2]]', '[[q3]]']
    ask = '<section class="simple-head"><div class="eyebrow">ASK BING’S AGENT</div><h1>[[ask_heading]]</h1><p>[[ask_intro]]</p></section><section class="chat-panel" aria-label="[[assistant]]"><div class="chat-intro"><span class="agent-mark">B.</span><div><h2>[[agent_name]]</h2><p>[[agent_intro]]</p></div></div><div class="question-chips">' + ''.join(f'<button type="button" data-question="{e(q,quote=True)}" disabled>{e(q)} ↗</button>' for q in map(labels, questions)) + f'</div><p id="agent-status" role="status">' + ('[[connecting]]' if api_url else '[[pending]]') + f'</p><div id="conversation" role="log" aria-live="polite" aria-label="[[conversation]]"></div><form id="ask-form" data-api="{e(api_url,quote=True)}"><label for="question">[[question]]</label><textarea id="question" name="question" rows="3" maxlength="1000" placeholder="[[placeholder]]" disabled required></textarea><div class="compose-footer"><small>[[privacy]]</small><button class="primary-link" type="submit" disabled>[[send]] ↗</button></div></form><noscript>[[noscript]]</noscript></section>'
    (OUT / 'ask.html').write_text(page('[[ask]]', ask, active='ask'))
    (OUT / '.nojekyll').touch()
    print(f'Built brand site: {len(profile["projects"])} projects, {len(published)} published articles, agent configured: {bool(api_url)}')


if __name__ == '__main__':
    for language in ('zh', 'en'):
        build_language(language)
