import requests
import base64
import os
import json

# GitHub 配置
REPO_OWNER = "xingchen857"
REPO_NAME = "multi-tts-tool"
BRANCH = "main"
API_BASE = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents"

def create_file(path, content, commit_message):
    # 将文件内容转换为Base64
    content_bytes = content.encode('utf-8')
    content_base64 = base64.b64encode(content_bytes).decode('utf-8')
    
    # 准备请求数据
    data = {
        "message": commit_message,
        "content": content_base64,
        "branch": BRANCH
    }
    
    # 发送请求
    headers = {
        "Authorization": f"Bearer {os.environ.get('GITHUB_TOKEN')}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    response = requests.put(f"{API_BASE}/{path}", 
                          headers=headers,
                          data=json.dumps(data))
    
    if response.status_code in [201, 200]:
        print(f"Successfully uploaded {path}")
    else:
        print(f"Failed to upload {path}: {response.status_code}")
        print(response.json())

# 读取并上传所有文件
files_to_upload = {
    "app.py": open("app.py", "r", encoding='utf-8').read(),
    "requirements.txt": open("requirements.txt", "r", encoding='utf-8').read(),
    "package.json": open("package.json", "r", encoding='utf-8').read(),
    "vite.config.js": open("vite.config.js", "r", encoding='utf-8').read(),
    "src/App.jsx": open("src/App.jsx", "r", encoding='utf-8').read(),
    "src/main.jsx": open("src/main.jsx", "r", encoding='utf-8').read(),
    "index.html": open("index.html", "r", encoding='utf-8').read(),
    "render.yaml": open("render.yaml", "r", encoding='utf-8').read(),
    "README.md": open("README.md", "r", encoding='utf-8').read(),
    ".gitignore": open(".gitignore", "r", encoding='utf-8').read(),
    ".github/workflows/deploy.yml": open(".github/workflows/deploy.yml", "r", encoding='utf-8').read()
}

for path, content in files_to_upload.items():
    create_file(path, content, "初始化多角色文本配音工具") 