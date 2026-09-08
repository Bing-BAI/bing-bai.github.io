"""Export only the curated public profile to a local Bailian upload bundle.

No network calls. No raw resumes, customer files, or credentials are read.
"""
import json
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parent
profile = json.loads((ROOT / 'profile.json').read_text())
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
      + '\n\n' + profile['background'] + '\n\n## 专业认证\n\n' + certifications
      + '\n\n## 教育\n\n' + '\n'.join('- ' + x for x in profile['education'])
      + '\n\n## 技术工具\n\n' + '、'.join(profile['skills'])
      + '\n\n## 工作方式\n\n按目标、输入、用户流程、输出、任务边界、验收标准和迭代拆解项目。'
      + '\n\n## 信息范围\n\n未提供当前任职、联系方式、薪资、住址或求职状态信息。不能由过去的经历推断现在的状态。\n')
for index, item in enumerate(profile['projects'], 2):
    sections = '\n\n'.join('## ' + s['title'] + '\n\n' + s['content'] for s in item['case_study'])
    write(f'{index:02}-{item["slug"]}.md', '# ' + item['title'] + '\n\n' + item['domain']
          + '\n\n白冰的角色：' + item['role'] + '\n\n' + sections
          + '\n\n客户已匿名化，不提供客户名称、内部项目文件或未审核的实验指标。\n')
with ZipFile(ROOT / '.local' / 'bailian-knowledge.zip', 'w', ZIP_DEFLATED) as archive:
    for path in files:
        archive.write(path, path.name)
print(f'Exported {len(files)} curated documents locally; no upload performed.')
