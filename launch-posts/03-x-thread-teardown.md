# X (Twitter) 深度技术拆解连推（3-Tweet Thread）

> **公式定位**：`X10 - How-I Teardown Thread`
> **目标信号**：Bookmarks 收藏与 Dwell Time 停留时长

---

### 1/3 (痛点与背景)：
```text
很多开发者尝试做“AI 自动视频剪辑”，第一反应都是拿 Python 的 MoviePy 拼片段。

我们踩了两个月坑才发现：MoviePy 在长视频切片时是灾难。原版 AutoCut“用 Markdown 剪视频”的思路极具美感，但跑几次长视频后半段嘴型必崩。

核心原因在于重采样漂移与帧率舍入，每切一刀都在累积误差 (1/3)
```

### 2/3 (硬核解法)：
```text
工业级的解法有两个硬约束：

1. 彻底干掉 MoviePy，改用原生 FFmpeg FilterGraph 单图级联，音视频在解码器层面强行对齐；
2. 人发音前 150ms 嘴唇先动并吸气。紧贴时间戳硬切一定会吞声（比如把 Jev 吞成 ev）。必须在切片逻辑里加入 0.18s 的 Pre-roll 与 0.15s 的 Post-roll 缓冲 (2/3)
```

### 3/3 (开源与致敬)
```text
好的 AI 工具往往败在音视频工程细节上。

感谢 AutoCut 原作者李沐老师带来的优雅交互思路。修好底层的音画时钟与呼吸缓冲后，这套“用 Markdown 剪视频”依然是我们日常出片最高效的工作流。

代码与 Agent Skill 已开源：https://github.com/huhao121/autocut-skill (3/3)
```
