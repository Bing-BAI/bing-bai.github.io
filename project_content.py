"""Load the curated profile and the seven-section Markdown project articles."""
import json
import re

SECTION_TITLES = ('目标', '输入', '用户流程', '输出', '任务边界', '验收标准', '迭代')
SECTION_IDS = ('goal', 'inputs', 'user-flow', 'outputs', 'scope', 'acceptance', 'iteration')

def load_profile(root):
    profile = json.loads((root / 'profile.json').read_text(encoding='utf-8'))
    seen_slugs, seen_knowledge = set(), set()
    for project in profile['projects']:
        slug, knowledge = project['slug'], project['knowledge_id']
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug) or slug in seen_slugs or knowledge in seen_knowledge:
            raise ValueError('Invalid or duplicate project identity')
        seen_slugs.add(slug); seen_knowledge.add(knowledge)
        text = (root / 'projects' / f'{slug}.md').read_text(encoding='utf-8')
        sections = re.split(r'^## (.+)\s*$', text, flags=re.M)
        if tuple(sections[1::2]) != SECTION_TITLES:
            raise ValueError(f'{slug}: expected the seven project sections in order')
        project['case_study'] = [dict(id=key, title=title, content=body.strip())
            for key, title, body in zip(SECTION_IDS, sections[1::2], sections[2::2])]
        if any(not s['content'] for s in project['case_study']):
            raise ValueError(f'{slug}: empty project section')
    return profile
