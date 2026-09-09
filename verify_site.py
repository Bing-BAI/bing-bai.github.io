from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
import json
import re
from rendering import markdown
from project_content import load_profile

sample = '''# 一级
## 二级
### 三级

**加粗** *斜体* ~~删除~~ [主页](https://example.com) `code`

1. 项目
2. 项目

> 引用

```python
print('hello')
```

| 列一 | 列二 |
| --- | --- |
| 甲 | 乙 |

![图](../assets/favicon.svg)

<script>alert(1)</script>

[坏链接](javascript:alert(1))
'''
html = markdown(sample)
for marker in ['<h1>', '<h2>', '<h3>', '<strong>', '<em>', '<s>', '<ol>', '<blockquote>', '<pre>', '<table>', '<img ', '<code>']:
    assert marker in html, marker
assert '<script>' not in html
assert 'href="javascript:' not in html

root=Path('_site').resolve()
class Links(HTMLParser):
    def __init__(self): super().__init__(); self.refs=[]
    def handle_starttag(self, tag, attrs):
        for key,value in attrs:
            if key in ('href','src') and value and not value.startswith(('#','http','mailto:','data:')):
                self.refs.append(urlsplit(value).path)
pages=list(root.rglob('*.html'))
for page in pages:
    parser=Links(); parser.feed(page.read_text())
    for ref in parser.refs:
        target=(page.parent/unquote(ref)).resolve()
        assert target.is_relative_to(root) and target.is_file(), (page,ref)
profile = load_profile(Path('.'))
assert len(pages) == 2 * (4 + len(profile['projects']) + len(list((root / 'posts').glob('*.html')))), len(pages)
expected_titles = ['目标', '输入', '用户流程', '输出', '任务边界', '验收标准', '迭代']
for project in profile['projects']:
    assert [section['title'] for section in project['case_study']] == expected_titles
    assert (root / 'projects' / f'{project["slug"]}.html').exists()
assert 'sample' not in Path('_site/index.html').read_text()
assert (root/'.well-known/assetlinks.json').read_bytes()==Path('.well-known/assetlinks.json').read_bytes()
for path in root.rglob('*'):
    assert path.name not in ('.env','profile.json','server.mjs','brand-and-knowledge.md')
    if path.suffix in ('.html','.js','.json','.css'):
        text=path.read_text()
        for private_marker in ('DASHSCOPE_API_KEY','resume-material','bingbai.jp@gmail.com','JR East','Yahata','Kepco','Corpy','TEPCO','AISIN','Komatsu'):
            assert private_marker not in text, (path,private_marker)
print(f'Markdown features, safe rendering, {len(pages)} page links, and private-file exclusion verified.')

# Both language routes exist and link to the matching page, including deep articles.
assert set(json.loads(Path('locales/zh.json').read_text())) == set(json.loads(Path('locales/en.json').read_text()))
english = load_profile(Path('.'), 'en')
assert [p['slug'] for p in english['projects']] == [p['slug'] for p in profile['projects']]
for page in pages:
    text = page.read_text()
    assert not re.search(r'\[\[\w+\]\]', text), page
    rel = page.relative_to(root).as_posix()
    is_en = rel.startswith('en/')
    assert f'<html lang="{ "en" if is_en else "zh-CN" }">' in text
    assert text.count('data-language=') == 2
    routes = re.findall(r'<a href="([^"]+)" lang="[^"]+" hreflang="[^"]+" data-language="([^"]+)"', text)
    route = rel.removeprefix('en/')
    for href, lang in routes:
        expected = root / ('en/' if lang == 'en' else '') / route
        assert (page.parent / href).resolve() == expected, (page, href)
for page in (root / 'en').rglob('*.html'):
    # Only the brand character and the language switch intentionally stay Chinese.
    text = re.sub(r'<[^>]*>', '', page.read_text())
    remaining = re.sub('[冰中]', '', text)
    assert not re.search(r'[\u3400-\u9fff]', remaining), page
print('Bilingual routes, switch targets, locale completeness and English copy verified.')

for page in pages:
    text = page.read_text()
    for ref in re.findall(r'href="([^"]+)"', text):
        url = urlsplit(ref)
        if url.scheme or url.netloc or not url.fragment:
            continue
        destination = (page.parent / unquote(url.path)).resolve() if url.path else page
        assert f'id="{unquote(url.fragment)}"' in destination.read_text(), (page, ref)
print('All static section links verified.')
