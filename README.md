# AI 智能伴侣（AIcouple）

基于 **Streamlit + DeepSeek API** 的 AI 虚拟伴侣对话应用：你可以给 AI「伴侣」自定义昵称和性格，它会以对应角色进行拟人化对话，适合作为大模型 API 应用开发的入门与演示项目。

> 部署为公开仓库，便于演示 AI 对话应用的基本架构：前端交互（Streamlit）→ 大模型调用（OpenAI SDK / DeepSeek）→ 本地持久化（JSON）。

## ✨ 功能特点

- 🤖 **大模型对话**：通过 OpenAI SDK 调用 DeepSeek API，对话自然流畅
- 💕 **自定义角色**：可自定义伴侣昵称、性格特征，按角色人设进行回复
- ⚡ **流式输出**：AI 回复逐字实时显示，交互体验更佳
- 💬 **会话管理**：支持新建、加载、删除历史会话
- 🧠 **标题自动生成**：根据首轮对话内容自动生成会话标题
- 💾 **自动保存**：会话内容以 JSON 分文件本地存储，隐私安全
- 🎨 **简洁界面**：基于 Streamlit 构建，主聊天区 + 侧边栏控制面板

## 🛠 技术栈

| 模块 | 技术 |
| --- | --- |
| 开发语言 | Python 3.x |
| Web 界面 | Streamlit |
| 大模型接入 | OpenAI SDK（DeepSeek API，支持流式响应） |
| 数据存储 | JSON 分文件（角色设定 / 消息历史 / 时间戳） |

## 🚀 快速开始

```bash
# 1. 克隆项目
git clone https://github.com/nicai108/AIcouple.git

# 2. 安装依赖
pip install streamlit openai jinja2 requests

# 3. 配置 API 密钥（Windows PowerShell）
$env:DEEPSEEK_API_KEY = "your_api_key_here"
# Linux / macOS
export DEEPSEEK_API_KEY="your_api_key_here"

# 4. 运行
streamlit run 01.py
```

启动后浏览器自动打开 `http://localhost:8501`。

## 📖 使用说明

- **对话**：底部输入消息，AI 以设定角色实时回复并自动保存。
- **自定义伴侣**：左侧边栏设置昵称与性格描述。
- **会话管理**：侧边栏「新建会话」创建新对话，列表可切换历史会话，❌ 删除会话。

## 📁 项目结构

```
AIcouple/
├── 01.py          # 主程序：界面、对话、会话管理逻辑
├── sessions/      # 会话数据目录（运行后自动生成，按会话保存为 *.json）
└── README.md
```

## ⚠️ 注意事项

- 首次使用需配置 `DEEPSEEK_API_KEY` 环境变量，密钥请勿提交到仓库。
- 会话数据保存在本地 `sessions/` 文件夹，请勿上传到 Git（已在 .gitignore 中排除）。
- 本项目仅供学习与个人使用，请遵守所用 API 的服务条款。

