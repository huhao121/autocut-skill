# X (Twitter) 中文极客推文发布方案

> **算法规则核验（符合 sergebulaev/x-skills 2026 规范）**：
> - 0 个 `#` 话题标签（原生极客风，防 spam 降权）
> - 主推文 0 个外部链接
> - 外部链接统一在第一条作者 Reply 评论区放出
> - 采用 `X10 - How-I Teardown` 骨架，针对 Bookmarks 收藏与 Reposts 转发

---

### Tweet 1（主推文 · 0标签 0外链，直接发）：

```text
我日常做视频教程几乎不用剪映或 PR，剪辑全跑在一个被官方停更的开源项目 AutoCut 上。

它的思路极具美感：Whisper 识别出 Markdown 检查单，在文档里删字打勾，视频就自动把废话和死等剪掉。

但原版有个致命硬伤：底层用 MoviePy 拼片段，切 50 刀后累积时钟漂移 1 秒以上，后半段嘴型和声音完全脱节，还会吞辅音。

我们彻底重构了它的底层：
1. 换成原生 FFmpeg FilterGraph 单图级联，切 100 刀时钟也绝对锁死；
2. 引入 0.18s 开口吸气与 0.15s 尾音缓冲，彻底根除吞辅音和“先动嘴后发声”；
3. 顺便做成了可以让 Agent 直接调用的标准 Skill，导出速度快了 8 倍。

顺手在 GitHub 开源了，送给所有饱受音画脱节折磨的视频开发者。
```

---

### Tweet 2（作者首条 Reply 挂载）：

```text
GitHub 仓库已开源：https://github.com/huhao121/autocut-skill

（致敬原作者李沐老师 @mli 开源 AutoCut 的优雅设计，代码纯净、零多余依赖，只要装了 ffmpeg 就能跑）

欢迎 Star 收藏或交流音视频 FilterGraph 极客玩法！
```
