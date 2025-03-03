my-site/                  # 项目根目录
├── src/                  # 存放原始内容（Markdown 文件）
│   ├── posts/            # 文章目录（按日期或分类组织）
│   │   └── 2023-10-20-hello-world.md
│   └── pages/            # 独立页面（如关于页、联系页）
│       └── about.md
├── templates/            # HTML 模板（用于渲染 Markdown）
│   ├── base.html         # 基础布局模板
│   └── post.html         # 文章详情页模板
├── assets/               # 静态资源
│   ├── css/              # 样式文件
│   │   └── style.scss   # 或 style.css
│   ├── js/               # JavaScript 文件
│   └── images/           # 图片资源
├── build/                # 生成的 HTML 文件（构建后自动生成）
├── scripts/              # 构建脚本
│   └── build.py          # Python 生成脚本（或其他语言）
└── config.yml            # 全局配置（可选，存储站点标题、作者等）