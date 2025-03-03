import os
import re
import yaml
import shutil
import markdown
from jinja2 import Environment, FileSystemLoader

# ---------- 配置 -----------
SRC_DIR = "src"                  # Markdown 源文件目录
TEMPLATE_DIR = "templates"       # 模板目录
BUILD_DIR = "build"              # 输出目录
ASSETS_DIR = "assets"            # 静态资源目录
CONFIG_FILE = "config.yml"       # 全局配置文件（可选）
# ---------------------------

def parse_front_matter(content):
    """解析 Markdown 文件的 Front Matter（元数据）"""
    front_matter = {}
    if content.startswith("---"):
        parts = re.split(r'---\n', content, 2)
        if len(parts) >= 3:
            try:
                front_matter = yaml.safe_load(parts[1])
            except yaml.YAMLError as e:
                print(f"Front Matter 解析错误: {e}")
            content = parts[2].lstrip()
    return front_matter, content

def main():
    # 初始化 Jinja2 模板环境
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

    # 读取全局配置（如果存在）
    config = {}
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            config = yaml.safe_load(f)

    # 清空并重建输出目录
    if os.path.exists(BUILD_DIR):
        shutil.rmtree(BUILD_DIR)
    os.makedirs(BUILD_DIR, exist_ok=True)

    # 处理所有 Markdown 文件
    for root, _, files in os.walk(SRC_DIR):
        for filename in files:
            if not filename.endswith(".md"):
                continue

            # 读取文件内容
            md_path = os.path.join(root, filename)
            with open(md_path, "r", encoding="utf-8") as f:
                raw_content = f.read()

            # 解析 Front Matter 和正文
            front_matter, md_body = parse_front_matter(raw_content)

            # 转换 Markdown 为 HTML
            html_body = markdown.markdown(
                md_body,
                extensions=["extra", "codehilite", "toc"]
            )

            # 合并配置数据
            context = {
                "config": config,
                "page": front_matter,
                "content": html_body
            }

            # 选择模板（优先使用 Front Matter 中的定义）
            template_name = front_matter.get("template", "base.html")
            template = env.get_template(template_name)

            # 渲染 HTML
            output_html = template.render(context)

            # 生成输出路径
            rel_path = os.path.relpath(root, SRC_DIR)
            output_dir = os.path.join(BUILD_DIR, rel_path)
            os.makedirs(output_dir, exist_ok=True)

            html_filename = f"{os.path.splitext(filename)[0]}.html"
            output_path = os.path.join(output_dir, html_filename)

            # 写入文件
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(output_html)

    # 复制静态资源
    if os.path.exists(ASSETS_DIR):
        shutil.copytree(ASSETS_DIR, os.path.join(BUILD_DIR, "assets"))

    print("构建完成！生成文件位于 build/ 目录")

if __name__ == "__main__":
    main()
    os.system(f"start {os.path.join(BUILD_DIR, 'index.html')}")