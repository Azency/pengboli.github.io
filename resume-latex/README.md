# 李鹏博简历 · LaTeX 源码

此目录保存中文简历源码、模板和字体，可直接在本目录编译。

| 文件 | 用途 |
| --- | --- |
| `resume_llm.tex` | LLM / RL Infra 投递版，网站中文简历对应的源码 |
| `resume2.tex` | 中文完整母版 |
| `resume.cls` | 页面布局、标题和个人信息命令 |
| `zh_CN-Adobefonts_external.sty` | 从本地 `fonts/` 加载中文字体 |
| `fontawesome.sty` | 图标命令 |
| `linespacing_fix.sty` | 行间距设置 |
| `fonts/` | 原简历使用的中英文字体与图标字体 |
| `Makefile` | 编译入口 |

## 编译

安装包含 XeLaTeX、latexmk 和 xeCJK 的 TeX Live / MacTeX。字体通过相对路径加载，须先进入本目录：

```sh
cd resume-latex
make
```

输出为 `build/resume_llm.pdf` 和 `build/resume2.pdf`。也可用 `make llm` 或 `make full` 单独编译一个版本。编译产物已加入本目录的 `.gitignore`。

没有 `make` 时，可以直接运行：

```sh
latexmk -xelatex -interaction=nonstopmode -halt-on-error -outdir=build resume_llm.tex
latexmk -xelatex -interaction=nonstopmode -halt-on-error -outdir=build resume2.tex
```

## 更新网站中文简历

修改 `resume_llm.tex` 并编译、检查生成的 PDF 后，在本目录运行：

```sh
cp build/resume_llm.pdf ../assets/pengbo-li-cv-zh.pdf
```

英文 CV 由仓库中的 `scripts/build_cv.py` 使用 ReportLab 生成，其可编辑内容仍在该脚本中。
