# 多角色文本配音工具

这是一个基于Edge TTS的多角色文本配音工具，支持英语、西班牙语和葡萄牙语的多种声音。

## 功能特点

- 支持多种语言（英语、西班牙语、葡萄牙语）
- 每种语言提供多个男声和女声选项
- 可调节语速
- 支持多角色配音
- 实时预览播放
- 简洁美观的用户界面

## 技术栈

- 后端：Python + Flask + Edge TTS
- 前端：React + Material-UI + Vite
- 部署：Render

## 本地开发

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/multi-tts-tool.git
cd multi-tts-tool
```

2. 安装后端依赖：
```bash
pip install -r requirements.txt
```

3. 启动后端服务：
```bash
python app.py
```

4. 安装前端依赖：
```bash
npm install
```

5. 启动前端开发服务器：
```bash
npm run dev
```

6. 访问 http://localhost:3000 即可使用工具

## 部署

本项目使用Render进行部署，配置文件已包含在`render.yaml`中。

1. 在Render上创建新的Blueprint
2. 连接到你的Git仓库
3. Render会自动检测配置并部署服务

## 使用说明

1. 选择语言和语速
2. 为每个角色选择合适的声音
3. 输入要转换的文本
4. 点击播放按钮预览
5. 可以添加或删除角色

## 许可证

MIT 