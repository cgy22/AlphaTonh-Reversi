# AlphaTonh · Reversi

<img src="https://dornhub.eu.org/resources/images/TonhTzeAI/TonhTzeAI-logo-v1-light.svg" alt="TonhTzeAI-logo-v1-light" width="400"><img src="https://dornhub.eu.org/resources/images/TonhTzeAI/TonhTzeAI-logo-v1-dark.svg" alt="TonhTzeAI-logo-v1-dark" width="400">

---

## About the Game

**AlphaTonh · Reversi** is a complete Reversi (also known as Othello) game built with Python and Tkinter. It features a lightweight AlphaGo-style AI opponent named **"𣿅子"** ("TonhTze") powered by the **Monte Carlo Tree Search (MCTS)** algorithm, delivering a classic strategy experience with a modern, clean light-themed interface.

Take control of the black pieces, flip your opponent's discs, and dominate the 8×8 board. The AI "𣿅子" comes with four distinct emotional states — thinking, waiting, winning, and losing — each displayed through custom artwork, giving the opponent a living, breathing personality.

The game runs natively on Windows, macOS, and Linux, with a single-file `.exe` build available for Windows users.

---

### Features

| Category | Features |
| :--- | :--- |
| 🎮 **Game States** | Main Menu → Playing → Paused → Game Over / Settlement |
| 🧠 **AI Opponent** | MCTS-based AI "𣿅子" with 4 difficulty levels (Easy / Normal / Hard / Master) |
| 👹 **AI Personality** | 4 emotional states (Thinking / Waiting / Winning / Losing) with custom artwork |
| ♟️ **Board System** | Standard 8×8 Reversi board with valid move hints for both players |
| 🎨 **Themes** | 7 light color schemes (𣿅国绿 / 大江蓝 / 秋茗红 / 铁山青 / 凤凰金 / 兰花紫 / 梨花粉) |
| 💥 **Visual Effects** | Smooth piece flipping, animated hints, clean modern UI |
| 📊 **HUD** | Score, current turn, AI level, AI move count, AI total time, AI average time per move |
| ⚙️ **Settings Menu** | AI thinking time, board cell size, hint toggle, side selection, reset to defaults |
| 🖼️ **Customization** | Change window icon, board background, AI artwork folder at runtime |
| ⏱️ **Timing** | Each AI move's elapsed time and cumulative total are displayed in real-time |
| 🔤 **Unicode Support** | Automatic font fallback for Extended-B Chinese characters (SimSun-ExtB) and emoji |

---

### Controls

| Key / Action | Function |
| :--- | :--- |
| `Left Click` | Place a piece on a valid square |
| `Settings → AI Level` | Change AI difficulty (Easy / Normal / Hard / Master) |
| `Settings → AI Thinking Time` | Set AI's thinking time per move (0.2 ~ 30 seconds) |
| `Settings → Board Cell Size` | Resize the board cells (40 ~ 120 pixels) |
| `Settings → Show Hints` | Toggle valid-move hint dots |
| `Settings → Choose Side` | Choose whether you play Black (first) or White (second) |
| `Appearance → Color Theme` | Switch between 7 light color schemes |
| `Appearance → Change Icon` | Load a custom window icon |
| `Appearance → Change Board Image` | Load a custom board background image |
| `Appearance → AI Artwork Folder` | Load custom AI state images |
| `Game → New Game` | Start a new game |
| `Game → Exit` | Quit the application |
| `Help → About` | View author, copyright, website, and license information |

---

### Tech Stack

- **Language:** Python 3.8+
- **GUI:** Tkinter / ttk (standard library)
- **Algorithm:** Monte Carlo Tree Search (MCTS) with UCB1 selection
- **AI Name:** 𣿅子 (TonhTze) — uses Unicode Extended-B characters
- **Rendering:** Double-buffered Canvas 2D drawing, ~60 FPS
- **Packaging:** PyInstaller (single-file `.exe`)
- **Deployment:** No external dependencies beyond Python standard library

---

### Audio Credits

This game currently ships **without audio**. If you wish to add background music or sound effects, you are free to do so under your own licensing.

> **Note:** All AI artwork (thinking / waiting / win / lose images) are private art creations by DornGames / Dorn Hub and are licensed under the **Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License (CC BY-NC-ND 4.0)**. You may not use them for commercial purposes, modify them, or distribute them without proper attribution.

---

### Download & Play

> The game is distributed via **GitHub Releases** — download the latest `.exe` and run it directly, no installation required!

1. Go to the **Releases** page of this repository:  
   [https://github.com/cgy22/AlphaTonh-Reversi/releases](https://github.com/cgy22/AlphaTonh-Reversi/releases)
2. Download the latest **`AlphaTonh-Reversi.exe`** from the "Assets" section of the newest release.
3. Double-click the `.exe` to launch the game — it starts immediately.

> ⚠️ **Note:** The `.exe` is a single-file, self-contained build. No Python installation, no extra files, no plugins required. Windows Defender or other antivirus software may flag it as a false positive — please add it to your trusted list.

If you prefer to run from source or build it yourself, see the next section.

---

### Build from Source

**Prerequisites:**
- Python 3.8 or newer
- (Optional) PyInstaller for building the standalone `.exe`

**Steps:**

1. Clone this repository:
   ```bash
   git clone https://github.com/cgy22/AlphaTonh-Reversi.git
   cd AlphaTonh-Reversi
   ```

2. Run the game directly:
   ```bash
   python Reversi.py
   ```

3. To build a standalone Windows executable:
   ```bash
   pip install pyinstaller
   pyinstaller --onefile --windowed --name "AlphaTonh-Reversi" \
       --add-data "ai_images;ai_images" \
       --add-data "icon.ico;." \
       Reversi.py
   ```

4. The output `dist/AlphaTonh-Reversi.exe` is your single-file distribution.

**Project Structure:**
```
AlphaTonh-Reversi/
├── Reversi.py
├── icon.ico
├── README.md
└── ai_images/
    ├── thinking.png
    ├── waiting.png
    ├── win.png
    └── lose.png
```

---

### Team & Copyright

**Sub-Team:** DornGames  
**Copyright © 2023-2026 DornGames. All Rights Reserved.**

**Parent Team:** Dorn Hub  
**Copyright © 2021-2026 Dorn Hub. All Rights Reserved.**

---

### License

This project is licensed under the **MIT License** — a permissive license that allows you to freely use, modify, and distribute the software, provided that the original copyright notice is retained.  
All AI artwork is owned privately by us and is licensed under the **CC BY-NC-ND 4.0** license.

**Copyright © 2026 DornGames / Dorn Hub**

---

A toast with Prickly Pear juice!🍹  
DornGames & Dorn Hub

---

# AlphaTonh · 𣿅子棋

<img src="https://dornhub.eu.org/resources/images/TonhTzeAI/TonhTzeAI-logo-v1-light.svg" alt="TonhTzeAI-logo-v1-light" width="400"><img src="https://dornhub.eu.org/resources/images/TonhTzeAI/TonhTzeAI-logo-v1-dark.svg" alt="TonhTzeAI-logo-v1-dark" width="400">

---

## 关于游戏

**《AlphaTonh · 𣿅子棋》** 是一款使用 Python 与 Tkinter 开发的完整黑白棋（又称苹果棋、翻转棋）游戏。它内置了一位名为 **"𣿅子"** 的轻量级 AlphaGo 风格 AI 对手，采用 **蒙特卡洛树搜索（MCTS）** 算法驱动，带来经典策略体验与现代化的浅色界面。

操控黑棋，翻转对手的棋子，掌控 8×8 棋盘。AI 对手"𣿅子"拥有四种不同的情绪状态 —— 思考中、等待中、胜利、失败 —— 每种状态都配有专属立绘，让对手仿佛拥有了鲜活的生命力。

游戏原生支持 Windows、macOS 和 Linux，并为 Windows 用户提供单文件 `.exe` 成品。

---

### 功能特性

| 类别 | 功能 |
| :--- | :--- |
| 🎮 **游戏状态** | 主菜单 → 游戏进行 → 暂停 → 失败 / 结算 |
| 🧠 **AI 对手** | 基于 MCTS 的 AI"𣿅子"，4 种难度（简单 / 普通 / 困难 / 大师） |
| 👹 **AI 人格** | 4 种情绪状态（思考 / 等待 / 胜利 / 失败），配专属立绘 |
| ♟️ **棋盘系统** | 标准 8×8 黑白棋棋盘，为双方显示合法落子提示 |
| 🎨 **主题配色** | 7 种浅色配色方案（𣿅国绿 / 大江蓝 / 秋茗红 / 铁山青 / 凤凰金 / 兰花紫 / 梨花粉） |
| 💥 **视觉效果** | 平滑翻子动画、提示点动画、现代简洁 UI |
| 📊 **HUD 界面** | 分数、当前执子、AI 等级、AI 步数、AI 总用时、AI 平均每步用时 |
| ⚙️ **设置菜单** | AI 思考时间、棋盘格子大小、提示点开关、选择执子方、恢复默认设置 |
| 🖼️ **外观定制** | 运行时更换窗口图标、棋盘背景图、AI 立绘文件夹 |
| ⏱️ **计时显示** | 实时显示 AI 每步耗时与累计总用时 |
| 🔤 **Unicode 支持** | 自动为扩展 B 区汉字（SimSun-ExtB）与 emoji 切换字体 |

---

### 操作说明

| 按键 / 操作 | 功能 |
| :--- | :--- |
| `鼠标左键` | 在合法位置落子 |
| `设置 → AI 等级` | 切换 AI 难度（简单 / 普通 / 困难 / 大师） |
| `设置 → AI 思考时间` | 设定 AI 每步思考时间（0.2 ~ 30 秒） |
| `设置 → 棋盘格子大小` | 调整棋盘格子像素大小（40 ~ 120 像素） |
| `设置 → 显示可落子提示` | 开关合法落子提示点 |
| `设置 → 选择执子方` | 选择你执黑（先行）或执白（后行） |
| `外观 → 配色主题` | 在 7 种浅色配色方案间切换 |
| `外观 → 更换窗口图标` | 加载自定义窗口图标 |
| `外观 → 更换棋盘背景图` | 加载自定义棋盘背景图 |
| `外观 → 选择 AI 立绘文件夹` | 加载自定义 AI 状态立绘 |
| `游戏 → 新游戏` | 开始新一局 |
| `游戏 → 退出` | 关闭程序 |
| `帮助 → 关于` | 查看作者、版权、网站与许可证信息 |

---

### 技术栈

- **编程语言：** Python 3.8+
- **图形界面：** Tkinter / ttk（标准库）
- **核心算法：** 蒙特卡洛树搜索（MCTS），UCB1 选择策略
- **AI 名称：** 𣿅子（TonhTze）—— 使用 Unicode 扩展 B 区汉字
- **渲染方式：** 双缓冲 Canvas 2D 绘制，目标 60 FPS
- **打包工具：** PyInstaller（单文件 `.exe`）
- **部署方式：** 除 Python 标准库外无任何外部依赖

---

### 音频版权声明

本游戏目前**不包含音频**。如果您希望添加背景音乐或音效，可在您自己的许可证下自由添加。

> **注意：** 所有 AI 立绘（思考 / 等待 / 胜利 / 失败 图片）均为 DornGames / Dorn Hub 的私人艺术创作，采用 **CC BY-NC-ND 4.0** 授权。未经适当署名，您不得将其用于商业目的、修改或分发。

---

### 下载与运行

> 游戏通过 **GitHub Releases** 发布 —— 下载最新的 `.exe` 直接运行，无需安装！

1. 访问本仓库的 **Releases（发行版）** 页面：  
   [https://github.com/cgy22/AlphaTonh-Reversi/releases](https://github.com/cgy22/AlphaTonh-Reversi/releases)
2. 在最新版本的 **Assets（资源）** 区域下载 **`AlphaTonh-Reversi.exe`**。
3. 双击 `.exe` 即可启动游戏 —— 无需任何额外操作。

> ⚠️ **注意：** `.exe` 是单文件自包含版本，无需安装 Python、无需附带其他文件、无需插件。Windows Defender 或部分杀毒软件可能误报，请将其加入信任列表。

如果你想从源码运行或自行构建，请参阅下一节。

---

### 从源码构建

**前置条件：**
- Python 3.8 或更新版本
- （可选）PyInstaller，用于构建独立 `.exe`

**构建步骤：**

1. 克隆本仓库：
   ```bash
   git clone https://github.com/cgy22/AlphaTonh-Reversi.git
   cd AlphaTonh-Reversi
   ```

2. 直接运行游戏：
   ```bash
   python Reversi.py
   ```

3. 构建独立的 Windows 可执行文件：
   ```bash
   pip install pyinstaller
   pyinstaller --onefile --windowed --name "AlphaTonh-Reversi" \
       --add-data "ai_images;ai_images" \
       --add-data "icon.ico;." \
       Reversi.py
   ```

4. 生成的 `dist/AlphaTonh-Reversi.exe` 即为单文件成品。

**项目结构：**
```
AlphaTonh-Reversi/
├── Reversi.py
├── icon.ico
├── README.md
└── ai_images/
    ├── thinking.png
    ├── waiting.png
    ├── win.png
    └── lose.png
```

---

### 团队与版权

**子团队：** DornGames  
**Copyright © 2023-2026 DornGames. All Rights Reserved.**

**母团队：** Dorn Hub  
**Copyright © 2021-2026 Dorn Hub. All Rights Reserved.**

---

### 许可证

本项目采用 **MIT 许可证** —— 一个宽松型许可证，允许您自由使用、修改和分发本软件，但需保留原始版权声明。  
所有 AI 立绘版权为私有，采用 **CC BY-NC-ND 4.0** 许可证。

**Copyright © 2026 DornGames / Dorn Hub**

---

*最后更新：2026年10月13日*

---

敬上一杯刺梨汁！🍹  
DornGames & Dorn Hub


---
