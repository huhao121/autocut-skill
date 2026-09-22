# V2EX / 即刻 / 掘金等极客社区分享草稿（Show HN 风格）

**标题**：[开源] 受够了 MoviePy 音画脱节，我用原生 FFmpeg FilterGraph 重写了 AutoCut（用 Markdown 剪视频）

**正文**：

两年前李沐老师开源的 AutoCut 给出了一个极具美感的交互：用 Whisper 转录出带打勾的 Markdown，在文档里删掉废话和死等，视频就自动把口误剪掉。

对于程序员和极客博主来说，这种纯文本驱动多媒体的体验比在剪映、PR 里拉时间线爽太多。

但在生产环境日常出片时，原版有个很痛苦的硬伤：
- 底层用 MoviePy 拼片段，每切一刀都会因为重采样和帧率舍入引入毫秒误差。一段 3 分钟的视频切 50 刀，后半段声音和嘴型错位整整 1 秒多，直接无法交付；
- 硬切时间戳容易把开头的爆破辅音吞掉（比如把“Hello”切成“ello”）。

于是我用原生 FFmpeg 把它重新实现了一遍，去掉了所有臃肿的 WebUI，做成了一个纯净的 CLI 工具和 Agent Skill：

1. **零时钟漂移**：单图 FFmpeg complex FilterGraph 一次性切片并级联重映射，解码器 PTS 时钟锁死，切 100 刀时差依然是 0.00ms；
2. **防吞辅音缓冲**：前置留足 0.18s 吸气/开口动作，后置留足 0.15s 尾音缓冲，口型与呼吸非常自然；
3. **硬件加速**：支持 Apple Silicon VideoToolbox，一段 3 分钟的原片十几秒导出；
4. **Agent Skill**：直接提供了符合规范的 `SKILL.md`，可供 Claude Code / Codex / Antigravity 直接当剪辑助手调用。

开源地址：https://github.com/huhao121/autocut-skill
致敬原作者李沐老师的优雅灵感。欢迎大家体验并提建议！
