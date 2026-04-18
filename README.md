# AI智能伴侣

一个基于Streamlit和DeepSeek AI的虚拟伴侣聊天应用，提供个性化的对话体验。

## 功能特点

- 🤖 **AI智能对话**：集成DeepSeek AI模型，提供自然流畅的对话体验
- 💕 **个性化伴侣**：可自定义伴侣昵称和性格特征
- 💬 **流式输出**：实时显示AI回复，提升交互体验
- 📝 **会话管理**：支持新建、加载和删除历史会话
- 💾 **自动保存**：会话内容自动保存到本地JSON文件
- 🎨 **友好界面**：基于Streamlit构建的简洁美观界面

## 技术栈

- **Python 3.x**
- **Streamlit**：Web应用框架
- **OpenAI SDK**：调用DeepSeek API
- **JSON**：会话数据存储

## 环境要求

- Python 3.8+
- DeepSeek API密钥

## 安装步骤

1. 克隆或下载项目文件

2. 安装依赖包：
```bash
pip install streamlit openai jinja2 requests
```

3. 设置环境变量：
```bash
# Windows PowerShell
$env:DEEPSEEK_API_KEY="your_api_key_here"

# Linux/Mac
export DEEPSEEK_API_KEY="your_api_key_here"
```

## 运行方式

```bash
streamlit run 01.py
```

运行后会自动打开浏览器访问应用（默认地址：http://localhost:8501）

## 使用说明

### 基本对话
1. 在底部输入框输入消息
2. AI会以设定的伴侣角色进行回复
3. 对话内容会实时显示并自动保存

### 自定义伴侣
在左侧边栏可以设置：
- **昵称**：伴侣的称呼
- **性格**：伴侣的性格特征描述

### 会话管理
- **新建会话**：点击"新建会话"按钮创建新对话
- **历史会话**：在侧边栏查看和切换历史会话
- **删除会话**：点击会话旁边的❌按钮删除

## 项目结构

```
伴侣/
├── 01.py              # 主程序文件
├── sessions/          # 会话数据存储目录（自动生成）
│   └── *.json         # 各个会话的JSON文件
└── README.md          # 项目说明文档
```

## 注意事项

- 首次使用需要配置DeepSeek API密钥
- 会话数据保存在`sessions`文件夹中
- 建议定期备份重要的会话记录
- 请遵守API使用规范和限制

## 许可证

本项目仅供学习和个人使用。
