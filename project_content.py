"""Load the curated profile and the seven-section Markdown project articles."""
import json
import re

SECTION_TITLES = ('目标', '输入', '用户流程', '输出', '任务边界', '验收标准', '迭代')
SECTION_IDS = ('goal', 'inputs', 'user-flow', 'outputs', 'scope', 'acceptance', 'iteration')

def load_profile(root, lang="zh"):
    profile = json.loads((root / 'profile.json').read_text(encoding='utf-8'))
    source = profile
    if lang == "en":
        profile = json.loads((root / "locales/en/profile.json").read_text(encoding="utf-8"))
        for key in ("capabilities", "about_paragraphs", "value_propositions", "methods", "career", "education", "languages", "skill_groups", "certifications"):
            if len(profile[key]) != len(source[key]):
                raise ValueError(f"English {key} entries must match Chinese content")
        translated = {p["slug"]: p for p in profile["projects"]}
        if len(translated) != len(profile["projects"]) or set(translated) != {p["slug"] for p in source["projects"]}:
            raise ValueError("English project metadata must match Chinese project slugs")
        profile["projects"] = [dict(translated[p["slug"]], knowledge_id=p["knowledge_id"], tags=p["tags"]) for p in source["projects"]]
        for key in ("github", "medium", "skills", "english_name"):
            profile[key] = source[key]
        for original, translated_cert in zip(source["certifications"], profile["certifications"]):
            for key in ("url", "holder", "valid_until", "official_name"):
                translated_cert[key] = original[key]
    titles = SECTION_TITLES if lang == "zh" else ("Goal", "Inputs", "User flow", "Outputs", "Scope", "Acceptance criteria", "Iteration")
    seen_slugs, seen_knowledge = set(), set()
    for project in profile['projects']:
        slug, knowledge = project['slug'], project['knowledge_id']
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug) or slug in seen_slugs or knowledge in seen_knowledge:
            raise ValueError('Invalid or duplicate project identity')
        seen_slugs.add(slug); seen_knowledge.add(knowledge)
        article = root / 'projects' / f'{slug}.md'
        if lang == 'en':
            article = root / 'locales/en/projects' / f'{slug}.md'
        text = article.read_text(encoding='utf-8')
        sections = re.split(r'^## (.+)\s*$', text, flags=re.M)
        if tuple(sections[1::2]) != titles:
            raise ValueError(f'{slug}: expected the seven project sections in order')
        project['case_study'] = [dict(id=key, title=title, content=body.strip())
            for key, title, body in zip(SECTION_IDS, sections[1::2], sections[2::2])]
        if any(not s['content'] for s in project['case_study']):
            raise ValueError(f'{slug}: empty project section')
    return profile
