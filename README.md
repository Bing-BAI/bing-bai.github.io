# Bing Bai / 白冰

个人品牌网站：AI 解决方案、匿名项目案例、技术记录，以及使用阿里云百炼 RAG 的问答入口。前端部署在 GitHub Pages，后端单独部署。

## 当前内容

首页展示个人定位、三类能力与八篇匿名项目与研究文章。文章归档集中展示「项目经历」与「技术思考」，项目卡片支持横向滚动；首页保留这两个栏目的入口。原来的三篇示例仍保留独立链接，在首页与归档中隐藏。真实文章尚待添加。

AI 助手界面和 Node.js 后端已实现，默认关闭。需在北京百炼创建并发布知识库应用、配置后端密钥并完成真实调用验证，才能启用。详见 [百炼连接与部署](docs/bailian-setup.md)。

## 本地构建和预览

需要 Python 3.10+：

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python build.py
.venv/bin/python -m http.server 8000 --directory _site
```

打开 http://localhost:8000 。修改源文件后重新构建并刷新。

## 写文章

在 `posts/` 新建英文文件名，例如 `2026-09-08-first-project.md`：

```md
---
title: 从一个业务问题开始
date: 2026-09-08
category: 项目复盘
summary: 记录如何确定技术路径，以及过程中的取舍。
---
## 问题与约束

这里支持 **加粗**、*斜体*、[链接](https://github.com/Bing-BAI)。

- 数据条件
- 运行环境
```

支持 1–6 级标题、段落、有序/无序及嵌套列表、引用、加粗、斜体、删除线、链接、图片、行内代码、围栏代码块、表格、分隔线。禁用原始 HTML 执行。不内置数学公式、脚注、任务复选框或 Mermaid 渲染；不是全部 GitHub 扩展语法。

使用 markdown-it-py 按 CommonMark 基础语法加表格和删除线扩展渲染。图片可放入 `assets/`，文章中使用 `../assets/文件名.png`；图片路径相对于生成后的文章页。代码块带语言标识，但当前不做彩色语法高亮。

元数据仍是简单的单行 `key: value`，不是完整 YAML。日期必须为 `YYYY-MM-DD`；`draft: true` 和未来日期的文章不会生成公开页面。移除 `sample: true` 后，文章会出现在首页和归档。

## 修改品牌内容

- `site.json`：站名、介绍和后端公开 URL（不能放密钥）
- `profile.json`：个人定位、价值主张、六种工作方法、项目元数据、教育与认证
- `projects/*.md`：八篇项目与研究文章的七项拆解正文
- `project_content.py`：加载并校验项目文章的结构
- `assets/style.css`：网站样式
- `backend/agent-prompt.md`：百炼智能体的系统提示词
- `backend/server.mjs`：北京百炼应用 API 代理

原始简历和内部客户资料不进入 Git 仓库。本地审阅与知识库候选文件放在被忽略的 `.local/`，构建器不复制这些文件。`.well-known/assetlinks.json` 原样保留。

## 部署

GitHub 仓库的 Settings → Pages → Source 使用 GitHub Actions。推送到 `main` 自动构建并发布 `_site`。只上传生成的网站目录，后端、原始资料和密钥不进入页面产物。

后端独立部署到阿里云函数计算，参阅 [连接指南](docs/bailian-setup.md)。

## 验证

```sh
.venv/bin/python verify_site.py
node --test backend/server.test.mjs
```

后端测试使用模拟百炼响应，不连接真实模型、不产生费用；不能替代上线后的真实知识库验收。

## 同步百炼知识资料

修改公开项目或认证后，运行 `python3 export_knowledge.py`，会在被 Git 忽略的 `.local/bailian-knowledge/` 生成九份 Markdown，并更新 `.local/bailian-knowledge.zip`。脚本仅读取整理过的 `profile.json` 和 `projects/*.md`，不读取原始资料、不执行上传。审阅后，在百炼替换对应文件并等待索引更新。

项目正文须依次包含七个二级标题：目标、输入、用户流程、输出、任务边界、验收标准、迭代。标题、卡片摘要和 `knowledge_id` 在 `profile.json` 维护。现有知识文档 ID 保持稳定，调整展示顺序不会改变上传文件名。新增项目时同步维护后端来源白名单，并运行后端测试验证映射。
