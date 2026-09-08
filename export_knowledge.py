"""Export only the curated public profile to a local Bailian upload bundle.

No network calls. No raw resumes, customer files, or credentials are read.
"""
import json
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from project_content import load_profile

ROOT = Path(__file__).resolve().parent
profile = load_profile(ROOT)
out = ROOT / '.local' / 'bailian-knowledge'
out.mkdir(parents=True, exist_ok=True)
files = []

def write(name, text):
    path = out / name
    path.write_text(text, encoding='utf-8')
    files.append(path)

certifications = '\n\n'.join(
    f'{c["title"]}。证书原文：{c["official_name"]}。颁发机构：{c["issuer"]}。持有人：{c["holder"]}。有效期至 {c["valid_until"]}。'
    for c in profile.get('certifications', [])
)
write('01-profile.md', '# 白冰（Bing Bai）：专业背景与能力\n\n' + profile['role'] + '。' + profile['intro']
      + '\n\n' + '\n\n'.join(profile['about_paragraphs'])
      + '\n\n## 我的目标\n\n' + profile['goal']['statement'] + '\n\n' + profile['goal']['description']
      + '\n\n## 六种工作方法\n\n' + '\n\n'.join('### ' + m['title'] + '\n\n' + m['principle'] + '\n\n' + m['practice'] for m in profile['methods']) + '\n\n## 专业认证\n\n' + certifications
      + '\n\n## 教育\n\n' + '\n'.join('- ' + x for x in profile['education'])
      + '\n\n## 核心价值\n\n' + '\n\n'.join(v['title'] + '：' + v['text'] for v in profile['value_propositions'])
      + '\n\n## 职业与研究脉络\n\n' + '\n\n'.join(c['title'] + '：' + c['text'] for c in profile['career'])
      + '\n\n## 语言\n\n' + '、'.join(profile['languages'])
      + '\n\n## 技术能力\n\n' + '\n\n'.join(g['title'] + '：' + '、'.join(g['items']) for g in profile['skill_groups'])
      + '\n\n## 工作方式\n\n按目标、输入、用户流程、输出、任务边界、验收标准和迭代拆解项目。'
      + '\n\n## 信息范围\n\n未提供当前任职、联系方式、薪资、住址或求职状态信息。不能由过去的经历推断现在的状态。\n')
for item in profile['projects']:
    sections = '\n\n'.join('## ' + s['title'] + '\n\n' + s['content'] for s in item['case_study'])
    write(f'{item["knowledge_id"]}.md', '# ' + item['title'] + '\n\n' + item['domain']
          + '\n\n白冰的角色：' + item['role'] + '\n\n' + sections
          + '\n\n客户已匿名化，不提供客户名称、内部项目文件或未审核的实验指标。\n')
with ZipFile(ROOT / '.local' / 'bailian-knowledge.zip', 'w', ZIP_DEFLATED) as archive:
    for path in files:
        archive.write(path, path.name)
print(f'Exported {len(files)} curated documents locally; no upload performed.')
