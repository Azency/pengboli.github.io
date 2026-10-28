# Pengbo Li · 李鹏博

中英双语个人主页，展示 ML Systems / LLM RL 研究、论文、实习经历与教育背景。纯 HTML、CSS、JavaScript，无需安装 npm 包或构建框架。

## 本地预览

在仓库目录运行：

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

打开 <http://127.0.0.1:8000>。中文预览用 <http://127.0.0.1:8000/?lang=zh>，英文用 `?lang=en`。页面会记住手动选择的语言；首次访问默认英文。关闭 JavaScript 后仍可阅读完整英文页面。

## 发布到 GitHub Pages

1. 将代码推送到本仓库的 `main` 分支。
2. 在仓库 **Settings → Pages → Build and deployment → Source** 选择 **GitHub Actions**。
3. 在 **Actions → Deploy personal homepage to GitHub Pages** 中运行工作流；之后每次推送 `main` 都会自动更新。

当前仓库属于 `Azency`，名称是 `pengboli.github.io`，默认地址因此是：

<https://azency.github.io/pengboli.github.io/>

如需使用 <https://azency.github.io/>，需要将仓库改名为 `azency.github.io`。若想使用 `pengboli.github.io`，需要拥有名为 `pengboli` 的 GitHub 账号或组织。全部站内资源使用相对路径，因此兼容以上两种部署路径。不要仅通过修改文件名或 README 来更改域名。

也可以不用 Actions：在 Pages 中选择 **Deploy from a branch → main → / (root)**；此时可移除 `.github/workflows/deploy.yml`，避免两套发布流程同时运行。

## 修改内容

| 文件 | 用途 |
| --- | --- |
| `index.html` | 个人介绍、论文、经历、联系方式；中英文本由 `data-en` / `data-zh` 保存 |
| `styles.css` | 排版、配色、移动端与打印样式 |
| `site.js` | 语言切换、偏好保存、导航高亮 |
| `assets/pengbo-li.jpeg` | 主页照片，来自指定的 `images/IMG_1301.jpeg` |
| `assets/pengbo-li-cv-zh.pdf` | 中文 LLM / RL Infra 简历 |
| `assets/favicon.svg` | 浏览器标签页图标 |
| `.github/workflows/deploy.yml` | GitHub Pages 自动发布流程 |

更新双语文本时，同时修改元素正文（无 JavaScript 时的英文回退）、`data-en` 与 `data-zh`。论文原始标题、作者名、技术术语保留英文。添加内容后检查桌面、手机及两种语言的显示效果。

## 内容来源

初版内容整理自工作区 `resume_llm.tex` 和 `resume2.tex`，使用指定的 `IMG_1301.jpeg` 与已有的中文简历 PDF。论文元数据参考正文所链接的 arXiv、OpenReview、出版社页面及作者主页。论文配图是概念示意，不是实验曲线。性能结果限定于对应论文的实验设置。

网站不使用第三方字体、分析脚本、Cookie 横幅或运行时依赖。联系按钮使用 `mailto:`；GitHub、论文和简历链接可直接打开。
