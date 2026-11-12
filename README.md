# Yu Wan · 万宇 — 个人学术主页

个人介绍、研究方向、研究动态、13 篇论文、开源项目与联系方式。样式参考 zzaiyan.github.io：白底学术排版、淡彩导航栏、左侧头像与个人资料、右侧简介、蓝色论文标题与图文论文卡片，使用同款 Cabin 字体。支持中英文、深浅色、论文筛选和搜索、BibTeX 复制与下载，以及手机访问。

## 本地预览

双击 `index.html` 即可查看。也可以运行：

```powershell
cd D:\code\Yu-Wan-Homepage
python -m http.server 8000
```

浏览器打开 http://localhost:8000 。无需安装 Node.js、Ruby 或其他依赖。

## 修改内容

- `data/profile.json`：姓名、邮箱、学术链接与论文列表。
- `data/news.json`：News 的发表日期、来源和本人通讯作者论文。全部动态合并为一个按发表日期倒序排列的列表，每条正文注明本人为第一作者、合著作者或通讯作者。用户确认的通讯论文为 IEGC-FSDN（IEEE SPL）和全色锐化论文（测绘学报英文版）。优先使用在线发表日期：CoRE-UIR 为 2026-08-08，TDRE 为 2026-09-04；LAD-Enhancer 为 2026-07-08，DFI-FODN 为 2025-08-03，地形重建论文为 2025-02-25。MS-FODN 的 2025-03 由本人确认；级联学习论文根据期刊 citation_online_date 使用 2026-03-23。其余日期尚未核实到月日，暂只显示年份并置于同年已知月份的条目之后；不以 DOI 年月、元数据登记日期或索引默认的 1 月 1 日代替发表日期。预印本明确标明性质。更改后重新构建即可同步更新中英文。
- `data/publication-order.json`：论文展示排序。期刊优先按展示档位排列（ISPRS J PRS → IEEE TGRS → IEEE JSTARS → IEEE SPL → 其他期刊），同档优先本人第一作者，再按年份降序；会议单列，预印本最后。档位是可调整的展示偏好，不表示实时影响因子或单篇论文的引用排名。代表作、全部论文和年份筛选沿用同一顺序。
- `template.html`：简介、研究方向、项目、统计展示及页面结构。
- `assets/style.css`：页面样式与响应式布局。
- `assets/app.js`：语言、主题、筛选、引用与论文大图查看交互。
- `assets/publications/`：12 篇论文的卡片预览图，`full/` 保存完整尺寸图片。
- `data/figure-sources.json`：逐篇记录图号、来源、尺寸与提取方式；按要求，全色锐化论文不配图。
- `assets/portrait.jpg`：来自 Google Scholar 的公开头像，可替换。

修改数据或模板后，运行 `python build.py` 重新生成 `index.html`。统计数字是 **2026-11-01 的快照**，不是实时统计；数据和日期从 `data/profile.json` 生成。论文作者按 Scholar 的公开缩写展示，部分列表含省略号；BibTeX 为这些元数据的简要导出，投稿引用建议以出版社提供的完整记录为准。

## 发布到 GitHub Pages

### VisitorTrace 访客地图

已准备与参考主页相同的 VisitorTrace 接入，位置在页尾，移动端自动改为单列。`data/visitor-trace.json` 中填写自己服务的 HTTPS `base_url`、`site_id`，将 `enabled` 改为 `true`，再运行 `python build.py` 并推送即可启用。未配置时不显示空控件、不发送统计请求。使用官方一体化 widget.js 同时显示地图与记录访问，不额外加载 tracker，避免重复计数。

VisitorTrace 后端需要单独部署，GitHub Pages 仅托管静态页面。按 [官方部署指南](https://github.com/zzaiyan/VisitorTrace/blob/main/docs/deployment.md) 启动服务，在管理后台为 `https://kikyouwy.github.io` 创建独立站点并配置 Allowed Origins、GeoIP 和公开地图。不要使用参考主页的站点 ID，否则会混入他人统计。这里只填写公开服务地址和站点 ID，管理员密码不应提交到仓库。

1. 在你自己的 GitHub 账号创建 `KIKYOUWY.github.io` 仓库（账号以实际使用的为准）。
2. 将本文件夹中的网站文件上传至 `main` 分支；无需上传 `reference-template` 和 `reference-git-residue`。
3. 在仓库 **Settings → Pages → Source** 中选择 **GitHub Actions**。
4. 随后的 push 或手动运行 `Deploy homepage to GitHub Pages` 工作流会发布页面。

使用 `KIKYOUWY.github.io` 仓库时，网址为 `https://kikyouwy.github.io/`；普通仓库也可部署，页面使用相对资源路径。本项目仓库为 https://github.com/KIKYOUWY/KIKYOUWY.github.io，通过 GitHub Actions 部署到 https://kikyouwy.github.io/。后续修改推送到 main 后会自动发布。

## 资料来源与致谢

- Google Scholar：https://scholar.google.com/citations?user=BlMgiksAAAAJ
- GitHub：https://github.com/KIKYOUWY
- 联系邮箱：来自 TDRE / AdverseMoE 官方仓库 README。
- 学术主页结构与功能参考：https://github.com/zzaiyan/zzaiyan.github.io （MIT，许可见 `LICENSE.template`）。本页为独立的静态实现。
- 论文配图来自官方项目、出版社原文、Semantic Scholar 对应论文图表索引及本地同名作者稿件。逐篇来源见 `data/figure-sources.json`。图像保留完整比例，可点击放大、切换原始尺寸，并打开原图和图源链接。
- PDF 配图通过渲染图像所在区域提取，保留叠加的矢量文字与箭头，透明背景合成为白色。MS-FODN 的可获取图源为 602×380，保留其原始分辨率，未人工放大。
- 论文图与照片的权利归原作者所有。
- 未填入未核实的学位、入学年份、导师关系、奖项与实习信息。

`reference-template` 是原参考项目的本地副本，不参与构建或部署。

VID-AMTF: IEEE TGRS Early Access, 2026, DOI 10.1109/TGRS.2026.3750106. Metadata and full author list verified against Crossref; framework image sourced from the official VID-AMTF repository. The existing November 1 acceptance News links to this article; no unverified online publication day is added.
