# 中英文维护

默认入口是中文，现有网址不变；英文页面位于 /en/。不按浏览器语言自动跳转。进入英文版后，导航、项目卡片和返回链接都保持英文。页头“中｜EN”链接指向同一页面，JavaScript 保留当前章节锚点；关闭 JavaScript 时仍可切换页面。

## 共用布局，分开编辑内容

| 内容 | 中文 | 英文 |
| --- | --- | --- |
| 导航、按钮、固定提示 | locales/zh.json | locales/en.json |
| 人物介绍、能力、方法、项目标题与摘要 | profile.json | locales/en/profile.json |
| 网站标题与描述 | site.json | locales/en/site.json |
| 项目正文 | projects/同名.md | locales/en/projects/同名.md |
| 技术思考正文 | posts/同名.md | locales/en/posts/同名.md |

build.py 是两种语言共用的模板。固定文字使用 [[key]] 引用语言文件；布局和样式不复制为两套。assets/main.js 中交互状态通过 textFor 配对维护。资源共用，构建生成版本参数，避免旧 CSS 和 JS 影响新页面。

项目 slug、顺序、知识库 ID、技术标签、社交链接、证书链接及证书事实以中文源为准，由加载器共享给英文版。共享字段不在英文 profile 中重复维护。英文项目列表必须与中文列表一一对应；缺少正文或七段结构不正确时构建失败。

## 修改现有内容

1. 修改中文源和对应英文内容，保持事实、个人贡献、阶段与任务边界一致。
2. 运行 python3 check_translations.py，它会列出中文发生变化、尚未复核英文的源文件。
3. 完成英文复核后，只记录相应文件。例如：

   python3 check_translations.py --record profile.json projects/visual-product-search.md

4. 运行 .venv/bin/python build.py 和 .venv/bin/python verify_site.py。
5. 提交源文件、译文与 locales/en/reviewed-sources.json，推送后自动发布。

不要直接编辑 _site/；它是生成目录。record 是编辑者对译文同步的确认，不会自动翻译，也不能代替语义审阅。只改样式不需要更新内容复核记录。

## 新增项目

在中文和英文 profile 的 projects 中使用相同 slug，分别写标题、领域、职责与摘要。两边各建同名 Markdown 文件。七个二级标题按以下顺序：

| 中文 | 英文 |
| --- | --- |
| 目标 | Goal |
| 输入 | Inputs |
| 用户流程 | User flow |
| 输出 | Outputs |
| 任务边界 | Scope |
| 验收标准 | Acceptance criteria |
| 迭代 | Iteration |

章节锚点由构建器统一生成，所以可以在对应章节之间切换语言。新项目的知识库引用白名单仍按 docs/bailian-setup.md 单独维护。

## 技术思考与缺失译文

中文 posts/ 决定日期、草稿状态、示例标记和是否发布；英文同名文件包含 title、category、summary 前置信息和正文。日期与发布状态沿用中文，避免两个版本发布节奏漂移。

已配对英文的技术思考也纳入 check_translations.py；修改中文正文后，复核英文并用 --record posts/文件名.md 记录。

未翻译的技术思考会生成英文提示页，明确说明只有中文版本，并链接到中文原文。目前三个历史示例文章采用这种方式，仍不出现在首页和归档。八篇正式项目文章均已有英文正文。

## Agent

此次提供了英文问答页面、界面状态和英文示例问题，Agent 仍未接通。现有百炼知识库导出保持中文资料源，避免重复文档干扰引用 ID。真正接通时还需验证英文提问的检索效果、模型回答语言和引用质量；切换网页语言本身不代表完成了英文 RAG 验证。
