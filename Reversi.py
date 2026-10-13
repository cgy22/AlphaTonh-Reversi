import tkinter as tk
from tkinter import messagebox, simpledialog, ttk, filedialog, font as tkfont
import math
import random
import time
import os
import sys


# 打包资源路径
def resource_path(relative_path):
    """获取资源绝对路径，兼容开发环境与 PyInstaller 打包环境"""
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


# 棋盘常量
BOARD_SIZE = 8
EMPTY = 0
BLACK = 1
WHITE = -1
DIRECTIONS = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

AI_NAME = "𣿅子"


# Unicode 扩展字工具
class UnicodeText:
    """扩展字符自动字体处理：含 >U+FFFF 的字符时自动换字体"""
    HAS_EXTB  = None    # 延迟初始化（需要 Tk root）
    HAS_EMOJI = None

    @classmethod
    def _ensure_init(cls):
        if cls.HAS_EXTB is None:
            try:
                families = set(tkfont.families())
            except Exception:
                families = set()
            cls.HAS_EXTB  = "SimSun-ExtB" in families
            cls.HAS_EMOJI = "Segoe UI Emoji" in families

    @staticmethod
    def pick_font(text, base_font):
        UnicodeText._ensure_init()
        size = base_font[1]
        has_emoji = has_extb = False
        for ch in str(text):
            cp = ord(ch)
            if cp > 0xFFFF:
                if 0x1F000 <= cp <= 0x1FAFF:
                    has_emoji = True
                else:
                    has_extb = True
        if has_emoji and UnicodeText.HAS_EMOJI:
            return ("Segoe UI Emoji", size)
        if has_extb and UnicodeText.HAS_EXTB:
            return ("SimSun-ExtB", size)
        return base_font

    @staticmethod
    def setup_tags(text_widget, base_font):
        UnicodeText._ensure_init()
        size = base_font[1]
        if UnicodeText.HAS_EXTB:
            text_widget.tag_configure("extb", font=("SimSun-ExtB", size))
        if UnicodeText.HAS_EMOJI:
            text_widget.tag_configure("emoji", font=("Segoe UI Emoji", size))

    @staticmethod
    def insert_smart(text_widget, text):
        UnicodeText._ensure_init()
        start_idx = text_widget.index("end-1c")
        text_widget.insert("end", text)
        idx = start_idx
        for ch in text:
            cp = ord(ch)
            if cp > 0xFFFF:
                next_idx = text_widget.index(f"{idx}+1c")
                if 0x1F000 <= cp <= 0x1FAFF and UnicodeText.HAS_EMOJI:
                    text_widget.tag_add("emoji", idx, next_idx)
                elif UnicodeText.HAS_EXTB:
                    text_widget.tag_add("extb", idx, next_idx)
                idx = next_idx
            else:
                idx = text_widget.index(f"{idx}+1c")


# UI 配置区
class UIConfig:
    TITLE = "AlphaTonh · Reversi"

    # 关于
    APP_NAME     = "AlphaTonh · Reversi"
    APP_VERSION  = "1.0"
    AUTHOR       = "cgy22"
    COPYRIGHT    = "Copyright © 2021-2026 Dorn Hub, All Rights Reserved. Copyright © 2023-2026 DornGames, All Rights Reserved."
    WEBSITE      = "https://dornhub.eu.org"
    GITHUB       = "https://github.com/cgy22/AlphaTonh-Reversi"
    EMAIL        = "contact@dornhub.eu.org"
    DESCRIPTION  = "基于 MCTS 的黑白棋 AI 对战程序"
    LICENSE      = "MIT License | The pictures are our private art creations and are licensed under CC BY-NC-ND 4.0 License."

    # 窗口配色
    WINDOW_BG   = "#f5f6f8"
    PANEL_BG    = "#ffffff"
    TEXT_COLOR  = "#1f2430"
    SUBTEXT     = "#7a8290"
    ACCENT      = "#16DA49"
    ACCENT_HOVER= "#12b83d"
    BORDER      = "#e0e3e8"

    TTK_THEME = "clam"

    ICON_PATH = "icon.ico"

    # 棋盘尺寸
    CELL = 72
    MARGIN = 28

    # 棋盘配色
    BOARD_BG   = "#e8d5a9"
    GRID_COLOR = "#b89b6a"
    GRID_WIDTH = 1

    BOARD_IMAGE = ""

    # 棋子
    BLACK_FILL = "#1a1a1a"
    WHITE_FILL = "#fdfdfd"
    PIECE_OUTLINE = "#555555"
    PIECE_OUTLINE_WIDTH = 2
    PIECE_PADDING = 6

    # 提示点
    HINT_HUMAN = "#16DA49"
    HINT_AI    = "#ff6b8a"
    HINT_RADIUS = 6
    SHOW_HINTS = True

    # 字体
    FONT_INFO   = ("Segoe UI", 10)
    FONT_LOG    = ("Consolas", 9)
    FONT_BUTTON = ("Segoe UI Semibold", 10)
    FONT_TITLE  = ("Segoe UI Semibold", 14)

    # 面板尺寸
    PANEL_WIDTH = 34
    PANEL_HEIGHT = 20

    # AI 基本参数
    AI_TIME_LIMIT = 2.0
    MCTS_C_PARAM  = 1.414
    AI_THINK_DELAY = 100
    PASS_DELAY = 200

    # AI 等级（时间秒, 随机失误率）
    LEVELS = {
        "简单": (0.3, 0.30),
        "普通": (1.0, 0.10),
        "困难": (3.0, 0.00),
        "大师": (6.0, 0.00),
    }
    DEFAULT_LEVEL = "普通"

    # AI 状态立绘
    AI_IMG_DIR = "ai_images"
    AI_IMG_SIZE = (160, 160)
    AI_STATE_FILES = {
        "thinking": "thinking.png",
        "waiting":  "waiting.png",
        "win":      "win.png",
        "lose":     "lose.png",
    }

    # 七种配色方案
    THEMES = {
        "𣿅国绿": dict(
            WINDOW_BG="#f4faf5", PANEL_BG="#ffffff",
            BOARD_BG="#e6f4e8", GRID_COLOR="#a8d5b0",
            ACCENT="#16DA49", ACCENT_HOVER="#12b83d"),
        "大江蓝": dict(
            WINDOW_BG="#f2f6fd", PANEL_BG="#ffffff",
            BOARD_BG="#e3ecfb", GRID_COLOR="#a8c1ea",
            ACCENT="#6499FF", ACCENT_HOVER="#4a82f0"),
        "秋茗红": dict(
            WINDOW_BG="#fbf3f3", PANEL_BG="#ffffff",
            BOARD_BG="#f5e2e2", GRID_COLOR="#d4a3a3",
            ACCENT="#A51515", ACCENT_HOVER="#8a1010"),
        "铁山青": dict(
            WINDOW_BG="#f2fafb", PANEL_BG="#ffffff",
            BOARD_BG="#e0f0f2", GRID_COLOR="#9fc8ce",
            ACCENT="#349DA5", ACCENT_HOVER="#2a828a"),
        "凤凰金": dict(
            WINDOW_BG="#fdf9ee", PANEL_BG="#ffffff",
            BOARD_BG="#faedd0", GRID_COLOR="#dcbb6e",
            ACCENT="#FFB500", ACCENT_HOVER="#e6a200"),
        "兰花紫": dict(
            WINDOW_BG="#faf3fa", PANEL_BG="#ffffff",
            BOARD_BG="#f2e2f2", GRID_COLOR="#c9a3c9",
            ACCENT="#DA70D6", ACCENT_HOVER="#c45cc0"),
        "梨花粉": dict(
            WINDOW_BG="#fdf3f7", PANEL_BG="#ffffff",
            BOARD_BG="#fae0ec", GRID_COLOR="#e0a3c0",
            ACCENT="#FF69B4", ACCENT_HOVER="#e655a0"),
    }
    DEFAULT_THEME = "𣿅国绿"


class ReversiBoard:
    def __init__(self):
        self.board = [[EMPTY]*BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.board[3][3] = WHITE
        self.board[3][4] = BLACK
        self.board[4][3] = BLACK
        self.board[4][4] = WHITE
        self.current_player = BLACK

    def clone(self):
        new = ReversiBoard()
        new.board = [row[:] for row in self.board]
        new.current_player = self.current_player
        return new

    def is_on_board(self, r, c):
        return 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE

    def get_flips(self, r, c, player):
        if self.board[r][c] != EMPTY:
            return []
        flips = []
        for dr, dc in DIRECTIONS:
            line = []
            nr, nc = r + dr, c + dc
            while self.is_on_board(nr, nc) and self.board[nr][nc] == -player:
                line.append((nr, nc))
                nr += dr
                nc += dc
            if line and self.is_on_board(nr, nc) and self.board[nr][nc] == player:
                flips.extend(line)
        return flips

    def get_valid_moves(self, player=None):
        if player is None:
            player = self.current_player
        moves = []
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.board[r][c] == EMPTY and self.get_flips(r, c, player):
                    moves.append((r, c))
        return moves

    def make_move(self, r, c, player=None):
        if player is None:
            player = self.current_player
        flips = self.get_flips(r, c, player)
        if not flips:
            return False
        self.board[r][c] = player
        for fr, fc in flips:
            self.board[fr][fc] = player
        self.current_player = -player
        return True

    def pass_turn(self):
        self.current_player = -self.current_player

    def is_game_over(self):
        return (not self.get_valid_moves(BLACK)) and (not self.get_valid_moves(WHITE))

    def count(self):
        b = sum(row.count(BLACK) for row in self.board)
        w = sum(row.count(WHITE) for row in self.board)
        return b, w

class MCTSNode:
    __slots__ = ['board', 'player', 'parent', 'children',
                 'visits', 'wins', 'untried_moves', 'move']

    def __init__(self, board, player, parent=None):
        self.board = board
        self.player = player
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0.0
        self.untried_moves = board.get_valid_moves(player)
        self.move = None

    def is_fully_expanded(self):
        return len(self.untried_moves) == 0

    def is_terminal(self):
        return self.board.is_game_over()


class MCTS:
    def __init__(self, time_limit=UIConfig.AI_TIME_LIMIT,
                 c_param=UIConfig.MCTS_C_PARAM, mistake_rate=0.0):
        self.time_limit = time_limit
        self.c_param = c_param
        self.mistake_rate = mistake_rate

    def search(self, board, player):
        moves = board.get_valid_moves(player)
        if not moves:
            return None
        if len(moves) == 1:
            return moves[0]
        if random.random() < self.mistake_rate:
            return random.choice(moves)

        root = MCTSNode(board.clone(), player)
        start_time = time.time()
        while time.time() - start_time < self.time_limit:
            node = self._select(root)
            if not node.is_terminal():
                node = self._expand(node)
            result = self._simulate(node)
            self._backpropagate(node, result)

        if not root.children:
            return random.choice(moves)
        best = max(root.children, key=lambda n: n.visits)
        return best.move

    def _select(self, node):
        while not node.is_terminal() and node.is_fully_expanded():
            node = self._best_child(node)
        return node

    def _best_child(self, node):
        best_score = -float('inf')
        best_child = None
        for child in node.children:
            if child.visits == 0:
                return child
            exploit = child.wins / child.visits
            explore = self.c_param * math.sqrt(math.log(node.visits) / child.visits)
            score = exploit + explore
            if score > best_score:
                best_score = score
                best_child = child
        return best_child

    def _expand(self, node):
        if not node.untried_moves:
            return node
        move = random.choice(node.untried_moves)
        node.untried_moves.remove(move)

        new_board = node.board.clone()
        new_board.current_player = node.player
        new_board.make_move(move[0], move[1], node.player)

        next_player = -node.player
        if not new_board.get_valid_moves(next_player):
            if new_board.get_valid_moves(node.player):
                next_player = node.player

        child = MCTSNode(new_board, next_player, parent=node)
        child.move = move
        node.children.append(child)
        return child

    def _simulate(self, node):
        board = node.board.clone()
        board.current_player = node.player
        player = node.player
        consecutive_pass = 0
        while not board.is_game_over() and consecutive_pass < 2:
            moves = board.get_valid_moves(player)
            if not moves:
                player = -player
                consecutive_pass += 1
                board.current_player = player
                continue
            consecutive_pass = 0
            move = random.choice(moves)
            board.make_move(move[0], move[1], player)
            player = board.current_player

        b, w = board.count()
        if player == BLACK:
            my, opp = b, w
        else:
            my, opp = w, b
        if my > opp:
            return 1.0
        elif my < opp:
            return 0.0
        return 0.5

    def _backpropagate(self, node, result):
        current = node
        while current is not None:
            current.visits += 1
            if current.player == node.player:
                current.wins += result
            else:
                current.wins += (1.0 - result)
            current = current.parent


# 图形界面
class ReversiGUI:
    def __init__(self, root):
        cfg = UIConfig
        self.cfg = cfg
        self.root = root
        self.root.title(cfg.TITLE)

        self.theme_name = cfg.DEFAULT_THEME
        self._apply_theme_colors(cfg.THEMES[self.theme_name])

        self._setup_style()
        self._setup_icon()

        self.board = ReversiBoard()
        self.level_name = cfg.DEFAULT_LEVEL
        t, mr = cfg.LEVELS[self.level_name]
        self.ai_time_limit = t
        self.mcts = MCTS(time_limit=t, c_param=cfg.MCTS_C_PARAM, mistake_rate=mr)
        self.total_ai_time = 0.0
        self.ai_move_count = 0
        self.human_player = BLACK
        self.ai_player = WHITE
        self.show_hints = cfg.SHOW_HINTS

        self._imgs = {}
        self._load_images()
        self._load_ai_state_images()

        self.build_menu()
        self._build_ui()

        self.set_ai_state("waiting")
        self.draw_board()
        self.update_info()

    # 主题/样式
    def _apply_theme_colors(self, colors):
        cfg = self.cfg
        cfg.WINDOW_BG = colors["WINDOW_BG"]
        cfg.PANEL_BG = colors["PANEL_BG"]
        cfg.BOARD_BG = colors["BOARD_BG"]
        cfg.GRID_COLOR = colors["GRID_COLOR"]
        cfg.ACCENT = colors["ACCENT"]
        cfg.ACCENT_HOVER = colors["ACCENT_HOVER"]
        self.root.configure(bg=cfg.WINDOW_BG)

    def _setup_style(self):
        cfg = self.cfg
        style = ttk.Style()
        try:
            style.theme_use(cfg.TTK_THEME)
        except tk.TclError:
            pass
        style.configure("Accent.TButton",
                        background=cfg.ACCENT,
                        foreground="white",
                        borderwidth=0,
                        focusthickness=0,
                        font=cfg.FONT_BUTTON,
                        padding=(14, 7))
        style.map("Accent.TButton",
                  background=[("active", cfg.ACCENT_HOVER), ("pressed", cfg.ACCENT_HOVER)],
                  foreground=[("active", "white")])

    def apply_theme(self, name):
        if name not in self.cfg.THEMES:
            return
        self.theme_name = name
        self._apply_theme_colors(self.cfg.THEMES[name])
        self._setup_style()
        self._refresh_widget_colors()
        self.log_msg(f"[外观] 主题 → {name}")
        self.draw_board()

    def _refresh_widget_colors(self):
        cfg = self.cfg
        self.root.configure(bg=cfg.WINDOW_BG)

        for frame in (getattr(self, "ai_frame", None),
                      getattr(self, "panel", None)):
            if frame is None:
                continue
            try:
                frame.configure(bg=cfg.PANEL_BG, highlightbackground=cfg.BORDER)
            except tk.TclError:
                pass
            for child in frame.winfo_children():
                cls = child.__class__.__name__
                try:
                    if cls == "Label":
                        txt = child.cget("text")
                        fg = cfg.ACCENT if txt in (AI_NAME, "对局信息", "日志") else cfg.TEXT_COLOR
                        child.configure(bg=cfg.PANEL_BG, fg=fg)
                    elif cls == "Text":
                        child.configure(bg=cfg.WINDOW_BG, fg=cfg.TEXT_COLOR,
                                        insertbackground=cfg.TEXT_COLOR)
                    elif cls == "Frame":
                        child.configure(bg=cfg.PANEL_BG)
                except tk.TclError:
                    pass

        try:
            self.main_frame.configure(bg=cfg.WINDOW_BG)
        except Exception:
            pass
        try:
            self.canvas.configure(bg=cfg.BOARD_BG, highlightbackground=cfg.BORDER)
        except Exception:
            pass

    # 图标图片
    def _setup_icon(self):
        path = self.cfg.ICON_PATH
        if not path:
            return
        if not os.path.isabs(path):
            path = resource_path(path)
        if not os.path.exists(path):
            print(f"图标文件未找到：{path}")
            return
        try:
            if path.lower().endswith(".ico"):
                self.root.iconbitmap(path)
            else:
                img = tk.PhotoImage(file=path)
                self.root.iconphoto(True, img)
                self._imgs["icon"] = img
        except Exception as e:
            print("设置图标失败：", e)

    def _load_images(self):
        cfg = self.cfg
        if not cfg.BOARD_IMAGE:
            return
        path = cfg.BOARD_IMAGE
        if not os.path.isabs(path):
            path = resource_path(path)
        if not os.path.exists(path):
            print(f"棋盘背景图未找到：{path}")
            return
        try:
            self._imgs["board"] = tk.PhotoImage(file=path)
        except Exception as e:
            print("加载棋盘图失败：", e)

    def _load_ai_state_images(self):
        cfg = self.cfg
        folder = cfg.AI_IMG_DIR
        if not os.path.isabs(folder):
            folder = resource_path(folder)

        target_w, target_h = cfg.AI_IMG_SIZE

        for state, fname in cfg.AI_STATE_FILES.items():
            fpath = os.path.join(folder, fname)
            if not os.path.exists(fpath):
                continue
            try:
                img = tk.PhotoImage(file=fpath)
                w = img.width()
                if w > target_w:
                    factor = max(1, round(w / target_w))
                    img = img.subsample(factor, factor)
                self._imgs[f"ai_{state}"] = img
            except Exception as e:
                print(f"加载 AI 状态图 {fname} 失败：", e)

    # 构建 UI
    def _build_ui(self):
        cfg = self.cfg

        self.main_frame = tk.Frame(self.root, bg=cfg.WINDOW_BG)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # 棋盘
        size = cfg.CELL * BOARD_SIZE + 2 * cfg.MARGIN
        self.canvas = tk.Canvas(self.main_frame, width=size, height=size,
                                bg=cfg.BOARD_BG, highlightthickness=1,
                                highlightbackground=cfg.BORDER)
        self.canvas.pack(side=tk.LEFT, padx=12, pady=12)
        self.canvas.bind("<Button-1>", self.on_click)

        # AI 立绘区
        self.ai_frame = tk.Frame(self.main_frame, bg=cfg.PANEL_BG,
                                 highlightthickness=1,
                                 highlightbackground=cfg.BORDER)
        self.ai_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 12), pady=12)

        ai_name_font = UnicodeText.pick_font(AI_NAME, cfg.FONT_TITLE)
        self.ai_name_label = tk.Label(self.ai_frame, text=AI_NAME,
                                      bg=cfg.PANEL_BG, fg=cfg.ACCENT,
                                      font=ai_name_font)
        self.ai_name_label.pack(pady=(10, 4))

        
        self.ai_img_label = tk.Label(self.ai_frame, bg=cfg.PANEL_BG,
                                     text="(无图片)", fg=cfg.SUBTEXT,
                                     font=cfg.FONT_INFO)
        self.ai_img_label.pack(pady=6)

        self.ai_state_label = tk.Label(self.ai_frame, text="等待中",
                                       bg=cfg.PANEL_BG, fg=cfg.TEXT_COLOR,
                                       font=cfg.FONT_INFO)
        self.ai_state_label.pack(pady=(0, 10))

        # 右侧信息面板
        self.panel = tk.Frame(self.main_frame, bg=cfg.PANEL_BG,
                              highlightthickness=1,
                              highlightbackground=cfg.BORDER)
        self.panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 12), pady=12)

        tk.Label(self.panel, text="对局信息", bg=cfg.PANEL_BG, fg=cfg.ACCENT,
                 font=("Segoe UI Semibold", 12)).pack(anchor=tk.W, padx=10, pady=(10, 4))
        self.info = tk.Label(self.panel, text="", justify=tk.LEFT,
                             font=cfg.FONT_INFO, bg=cfg.PANEL_BG, fg=cfg.TEXT_COLOR)
        self.info.pack(anchor=tk.W, padx=10)

        tk.Label(self.panel, text="日志", bg=cfg.PANEL_BG, fg=cfg.ACCENT,
                 font=("Segoe UI Semibold", 12)).pack(anchor=tk.W, padx=10, pady=(12, 4))
        self.log = tk.Text(self.panel, width=cfg.PANEL_WIDTH, height=cfg.PANEL_HEIGHT,
                           font=cfg.FONT_LOG, bg=cfg.WINDOW_BG, fg=cfg.TEXT_COLOR,
                           insertbackground=cfg.TEXT_COLOR, relief=tk.FLAT,
                           borderwidth=1, highlightthickness=0)
        self.log.pack(anchor=tk.W, padx=10)
        UnicodeText.setup_tags(self.log, cfg.FONT_LOG)

        self.btn_new = ttk.Button(self.panel, text="新游戏",
                                  style="Accent.TButton", command=self.new_game)
        self.btn_new.pack(anchor=tk.W, padx=10, pady=12)

    # AI 状态切换
    def set_ai_state(self, state):
        labels = {
            "thinking": f"{AI_NAME}思考中…",
            "waiting":  f"{AI_NAME}等待中",
            "win":      f"{AI_NAME}赢了！",
            "lose":     f"{AI_NAME}输了…",
        }
        img = self._imgs.get(f"ai_{state}")
        if img:
            self.ai_img_label.config(image=img, text="")
        else:
            placeholder = {"thinking": "🤔", "waiting": "😴",
                           "win": "😎", "lose": "😭"}.get(state, "AI")
            self.ai_img_label.config(image="", text=placeholder,
                                     font=("Segoe UI Emoji", 60))
        text = labels.get(state, "")
        self.ai_state_label.config(text=text,
                                   font=UnicodeText.pick_font(text, self.cfg.FONT_INFO))

    # 菜单
    def build_menu(self):
        menubar = tk.Menu(self.root)

        game = tk.Menu(menubar, tearoff=0)
        game.add_command(label="新游戏", command=self.new_game)
        game.add_separator()
        game.add_command(label="退出", command=self.root.quit)
        menubar.add_cascade(label="游戏", menu=game)

        settings = tk.Menu(menubar, tearoff=0)

        level_menu = tk.Menu(settings, tearoff=0)
        self.var_level = tk.StringVar(value=self.level_name)
        for name in self.cfg.LEVELS:
            level_menu.add_radiobutton(label=name, variable=self.var_level,
                                       value=name,
                                       command=lambda n=name: self.set_level(n))
        settings.add_cascade(label="AI 等级", menu=level_menu)

        settings.add_command(label="设置 AI 思考时间...", command=self.dialog_ai_time)
        settings.add_command(label="设置棋盘格子大小...", command=self.dialog_cell_size)
        settings.add_separator()
        self.var_hints = tk.BooleanVar(value=self.show_hints)
        settings.add_checkbutton(label="显示可落子提示", variable=self.var_hints,
                                 command=self.toggle_hints)
        settings.add_separator()
        settings.add_command(label="选择执子方（重新开始）...", command=self.dialog_side)
        settings.add_command(label="恢复默认设置", command=self.reset_settings)
        menubar.add_cascade(label="设置", menu=settings)

        appearance = tk.Menu(menubar, tearoff=0)
        appearance.add_command(label="更换窗口图标...", command=self.browse_icon)
        appearance.add_command(label="更换棋盘背景图...", command=self.browse_board_image)
        appearance.add_separator()
        appearance.add_command(label="选择 AI 立绘文件夹...", command=self.browse_ai_folder)
        appearance.add_separator()

        theme_menu = tk.Menu(appearance, tearoff=0)
        self.var_theme = tk.StringVar(value=self.theme_name)
        for tname in self.cfg.THEMES:
            theme_menu.add_radiobutton(label=tname, variable=self.var_theme,
                                       value=tname,
                                       command=lambda n=tname: self.apply_theme(n))
        appearance.add_cascade(label="配色主题", menu=theme_menu)
        menubar.add_cascade(label="外观", menu=appearance)

        helpm = tk.Menu(menubar, tearoff=0)
        helpm.add_command(label="关于", command=self.show_about)
        menubar.add_cascade(label="帮助", menu=helpm)

        self.root.config(menu=menubar)

    # 菜单动作
    def browse_icon(self):
        path = filedialog.askopenfilename(
            title="选择窗口图标 (PNG/GIF/ICO)",
            filetypes=[("图片", "*.png *.gif *.ico"), ("全部", "*.*")])
        if not path:
            return
        self.cfg.ICON_PATH = path
        self._setup_icon()
        self.log_msg(f"[外观] 图标 → {os.path.basename(path)}")

    def browse_board_image(self):
        path = filedialog.askopenfilename(
            title="选择棋盘背景图 (PNG/GIF)",
            filetypes=[("图片", "*.png *.gif"), ("全部", "*.*")])
        if not path:
            return
        try:
            self._imgs["board"] = tk.PhotoImage(file=path)
            self.cfg.BOARD_IMAGE = path
            self.log_msg(f"[外观] 棋盘背景 → {os.path.basename(path)}")
            self.draw_board()
        except Exception as e:
            messagebox.showerror("错误", f"加载失败：{e}")

    def browse_ai_folder(self):
        folder = filedialog.askdirectory(title="选择 AI 立绘文件夹")
        if not folder:
            return
        self.cfg.AI_IMG_DIR = folder
        for k in list(self._imgs.keys()):
            if k.startswith("ai_"):
                del self._imgs[k]
        self._load_ai_state_images()
        self.log_msg(f"[外观] AI 立绘文件夹 → {folder}")
        self.set_ai_state("waiting")

    def set_level(self, name):
        t, mr = self.cfg.LEVELS[name]
        self.level_name = name
        self.ai_time_limit = t
        self.mcts.time_limit = t
        self.mcts.mistake_rate = mr
        self.log_msg(f"[设置] AI 等级 = {name}  (思考 {t}s, 失误 {int(mr*100)}%)")
        self.update_info()

    def dialog_ai_time(self):
        val = simpledialog.askfloat("AI 思考时间", "每步思考几秒？(0.2 ~ 30)",
                                    initialvalue=self.ai_time_limit,
                                    minvalue=0.2, maxvalue=30.0, parent=self.root)
        if val is None:
            return
        self.ai_time_limit = val
        self.mcts.time_limit = val
        self.log_msg(f"[设置] AI 思考时间 = {val:.2f}s")
        self.update_info()

    def dialog_cell_size(self):
        val = simpledialog.askinteger("格子大小", "每格像素大小？(40 ~ 120)",
                                      initialvalue=self.cfg.CELL,
                                      minvalue=40, maxvalue=120, parent=self.root)
        if val is None:
            return
        self.cfg.CELL = val
        self.resize_canvas()
        self.log_msg(f"[设置] 格子大小 = {val}px")

    def dialog_side(self):
        choice = simpledialog.askinteger("选择执子方",
                                         "1 = 你执黑先行；2 = 你执白后行",
                                         initialvalue=1, minvalue=1, maxvalue=2,
                                         parent=self.root)
        if choice is None:
            return
        if choice == 1:
            self.human_player, self.ai_player = BLACK, WHITE
        else:
            self.human_player, self.ai_player = WHITE, BLACK
        self.log_msg(f"[设置] 你执 {'黑' if self.human_player==BLACK else '白'}棋")
        self.new_game()
        if self.board.current_player == self.ai_player:
            self.root.after(self.cfg.AI_THINK_DELAY, self.ai_turn)

    def toggle_hints(self):
        self.show_hints = self.var_hints.get()
        self.log_msg(f"[设置] 可落子提示 = {'开' if self.show_hints else '关'}")
        self.draw_board()

    def reset_settings(self):
        self.cfg.CELL = 72
        self.cfg.MARGIN = 28
        self.set_level(self.cfg.DEFAULT_LEVEL)
        self.show_hints = True
        self.var_hints.set(True)
        self.apply_theme(self.cfg.DEFAULT_THEME)
        self.var_theme.set(self.cfg.DEFAULT_THEME)
        self.resize_canvas()
        self.log_msg("[设置] 已恢复默认")

    def show_about(self):
        cfg = self.cfg
        info = (
            f"{cfg.APP_NAME}\n"
            f"版本：{cfg.APP_VERSION}\n"
            f"————————————————\n"
            f"作者：{cfg.AUTHOR}\n"
            f"邮箱：{cfg.EMAIL}\n"
            f"网站：{cfg.WEBSITE}\n"
            f"GitHub：{cfg.GITHUB}\n"
            f"————————————————\n"
            f"{cfg.DESCRIPTION}\n"
            f"AI 对手：{AI_NAME}\n"
            f"算法：MCTS（蒙特卡洛树搜索）\n"
            f"————————————————\n"
            f"{cfg.COPYRIGHT}\n"
            f"{cfg.LICENSE}"
        )
        messagebox.showinfo("关于", info)

    def resize_canvas(self):
        cfg = self.cfg
        size = cfg.CELL * BOARD_SIZE + 2 * cfg.MARGIN
        self.canvas.config(width=size, height=size)
        self.draw_board()

    # 绘制
    def board_to_pixel(self, r, c):
        cfg = self.cfg
        return (cfg.MARGIN + c * cfg.CELL + cfg.CELL // 2,
                cfg.MARGIN + r * cfg.CELL + cfg.CELL // 2)

    def pixel_to_board(self, x, y):
        cfg = self.cfg
        c = (x - cfg.MARGIN) // cfg.CELL
        r = (y - cfg.MARGIN) // cfg.CELL
        if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
            return int(r), int(c)
        return None

    def draw_board(self):
        cfg = self.cfg
        self.canvas.delete("all")

        board_img = self._imgs.get("board")
        if board_img:
            cx = cfg.MARGIN + BOARD_SIZE * cfg.CELL // 2
            cy = cfg.MARGIN + BOARD_SIZE * cfg.CELL // 2
            self.canvas.create_image(cx, cy, image=board_img)

        for i in range(BOARD_SIZE + 1):
            x = cfg.MARGIN + i * cfg.CELL
            self.canvas.create_line(x, cfg.MARGIN, x,
                                    cfg.MARGIN + BOARD_SIZE * cfg.CELL,
                                    fill=cfg.GRID_COLOR, width=cfg.GRID_WIDTH)
            y = cfg.MARGIN + i * cfg.CELL
            self.canvas.create_line(cfg.MARGIN, y,
                                    cfg.MARGIN + BOARD_SIZE * cfg.CELL, y,
                                    fill=cfg.GRID_COLOR, width=cfg.GRID_WIDTH)

        if self.show_hints:
            for r, c in self.board.get_valid_moves(self.board.current_player):
                x, y = self.board_to_pixel(r, c)
                color = cfg.HINT_HUMAN if self.board.current_player == self.human_player else cfg.HINT_AI
                rad = cfg.HINT_RADIUS
                self.canvas.create_oval(x-rad, y-rad, x+rad, y+rad,
                                        fill=color, outline='')

        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                v = self.board.board[r][c]
                if v == EMPTY:
                    continue
                x, y = self.board_to_pixel(r, c)
                rad = cfg.CELL // 2 - cfg.PIECE_PADDING
                fill = cfg.BLACK_FILL if v == BLACK else cfg.WHITE_FILL
                self.canvas.create_oval(x-rad, y-rad, x+rad, y+rad,
                                        fill=fill, outline=cfg.PIECE_OUTLINE,
                                        width=cfg.PIECE_OUTLINE_WIDTH)

    def update_info(self):
        b, w = self.board.count()
        turn = "你" if self.board.current_player == self.human_player else AI_NAME
        avg = (self.total_ai_time / self.ai_move_count) if self.ai_move_count else 0
        text = (f"黑棋: {b}    白棋: {w}\n"
                f"你执: {'黑' if self.human_player==BLACK else '白'}\n"
                f"当前执子: {turn}\n"
                f"AI 等级: {self.level_name}\n"
                f"AI 步数: {self.ai_move_count}\n"
                f"AI 总用时: {self.total_ai_time:.2f}s\n"
                f"AI 平均每步: {avg:.2f}s")
        self.info.config(text=text,
                         font=UnicodeText.pick_font(text, self.cfg.FONT_INFO))

    def log_msg(self, msg):
        UnicodeText.insert_smart(self.log, msg + "\n")
        self.log.see("end")

    # 交互
    def on_click(self, event):
        if self.board.current_player != self.human_player:
            return
        pos = self.pixel_to_board(event.x, event.y)
        if pos is None:
            return
        r, c = pos
        if (r, c) not in self.board.get_valid_moves(self.human_player):
            return
        self.board.make_move(r, c, self.human_player)
        self.draw_board()
        self.update_info()
        self.log_msg(f"你落子: ({r},{c})")
        self.set_ai_state("thinking")
        self.root.after(self.cfg.AI_THINK_DELAY, self.ai_turn)

    def ai_turn(self):
        if self.board.is_game_over():
            self.end_game()
            return

        if not self.board.get_valid_moves(self.ai_player):
            self.board.pass_turn()
            self.log_msg(f"[{AI_NAME} 无棋可走，跳过]")
            self.draw_board()
            self.update_info()
            self.set_ai_state("waiting")
            if self.board.current_player == self.human_player:
                self.root.after(self.cfg.PASS_DELAY, self.human_can_move)
            else:
                self.root.after(self.cfg.PASS_DELAY, self.ai_turn)
            return

        self.set_ai_state("thinking")
        self.log_msg(f"[{AI_NAME} 思考中...]")
        self.root.update()

        start = time.time()
        move = self.mcts.search(self.board, self.ai_player)
        elapsed = time.time() - start
        self.total_ai_time += elapsed
        self.ai_move_count += 1

        if move is None:
            self.board.pass_turn()
        else:
            self.board.make_move(move[0], move[1], self.ai_player)
            self.log_msg(f"{AI_NAME}落子: ({move[0]},{move[1]})  用时 {elapsed:.2f}s")

        self.draw_board()
        self.update_info()

        if self.board.is_game_over():
            self.end_game()
            return

        if not self.board.get_valid_moves(self.human_player):
            self.board.pass_turn()
            self.log_msg("[你无棋可走，跳过]")
            self.draw_board()
            self.update_info()
            self.root.after(self.cfg.PASS_DELAY, self.ai_turn)
        else:
            self.set_ai_state("waiting")

    def human_can_move(self):
        if self.board.is_game_over():
            self.end_game()
            return
        if self.board.current_player != self.human_player:
            self.ai_turn()
        else:
            self.set_ai_state("waiting")

    def end_game(self):
        b, w = self.board.count()
        if self.ai_player == BLACK:
            ai_score, hu_score = b, w
        else:
            ai_score, hu_score = w, b

        if ai_score > hu_score:
            result = f"{AI_NAME}赢了！"
            self.set_ai_state("win")
        elif ai_score < hu_score:
            result = "你赢了！"
            self.set_ai_state("lose")
        else:
            result = "平局！"
            self.set_ai_state("lose")

        avg = (self.total_ai_time / self.ai_move_count) if self.ai_move_count else 0
        msg = (f"游戏结束\n黑棋: {b}\n白棋: {w}\n{result}\n\n"
               f"AI 总用时: {self.total_ai_time:.2f}s\nAI 平均每步: {avg:.2f}s")
        self.log_msg("=== 游戏结束 ===")
        self.log_msg(f"黑{b} : 白{w}  {result}")
        messagebox.showinfo("游戏结束", msg)

    def new_game(self):
        self.board = ReversiBoard()
        self.board.current_player = BLACK
        self.total_ai_time = 0.0
        self.ai_move_count = 0
        self.log.delete("1.0", tk.END)
        self.draw_board()
        self.update_info()
        if self.board.current_player == self.ai_player:
            self.set_ai_state("thinking")
            self.root.after(self.cfg.AI_THINK_DELAY, self.ai_turn)
        else:
            self.set_ai_state("waiting")


if __name__ == "__main__":
    root = tk.Tk()
    app = ReversiGUI(root)
    root.mainloop()
