import pygame
import datetime
import sys
import os

# =====================
# 設定
# =====================
WINDOW_W, WINDOW_H = 1080, 600
BG_COLOR = (18, 18, 18)
CARD_BG = (30, 30, 30)
TEXT_COLOR = (230, 230, 230)
SPLIT_COLOR = (10, 10, 10)
FLIP_DURATION = 0.4
MUSIC_DIR = "music"
IMG_DIR = "assets/ui"
BTN_SIZE = 80
pygame.mixer.pre_init(44100, -16, 2, 512)

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WINDOW_W, WINDOW_H), pygame.RESIZABLE)
pygame.display.set_caption("PataPata_clock")
clock = pygame.time.Clock()

# =====================
# フォント
# =====================
def get_font(size):
    try:
        return pygame.font.Font("Inter-Regular.otf", size)
    except:
        return pygame.font.Font(None, size)

# =====================
# 音楽プレイヤー
# =====================
class MusicPlayer:
    def __init__(self, music_dir):
        self.playlist = [
            os.path.join(music_dir, f)
            for f in os.listdir(music_dir)
            if f.lower().endswith((".wav", ".mp3"))
            and os.path.isfile(os.path.join(music_dir, f))
        ]

        self.playlist.sort()
        self.index = 0
        self.paused = False

        if not self.playlist:
            print("⚠ 音楽ファイルなし")
            return

        self._load_current()

    def _load_current(self):
        path = self.playlist[self.index]
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
            print("再生:", path)
        except pygame.error as e:
            print("⚠ 読み込み失敗:", path)
            print(e)
            self._skip()

    def _skip(self):
        if len(self.playlist) <= 1:
            print("再生可能な曲がありません")
            return
        self.index = (self.index + 1) % len(self.playlist)
        self._load_current()

    def next(self):
        if not self.playlist:
            return
        pygame.mixer.music.stop()
        self.index = (self.index + 1) % len(self.playlist)
        self._load_current()


        if self.playlist:
            pygame.mixer.music.load(self.playlist[self.index])
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play()

    def toggle(self):
        if self.paused:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()
        self.paused = not self.paused

    def next(self):
        if not self.playlist:
            return
        self.index = (self.index + 1) % len(self.playlist)
        pygame.mixer.music.load(self.playlist[self.index])
        pygame.mixer.music.play()
        self.paused = False

    def prev(self):
        if not self.playlist:
            return
        self.index = (self.index - 1) % len(self.playlist)
        pygame.mixer.music.load(self.playlist[self.index])
        pygame.mixer.music.play()
        self.paused = False

# =====================
# パタパタ 1桁
# =====================
class FlipDigit:
    def __init__(self, val):
        self.current = val
        self.next = val
        self.anim = False
        self.t = 0
        self.font = None
        self.font_size = 0
        self.cache = {}
        self.last_size = (0, 0)

    def set(self, val):
        if val != self.current and not self.anim:
            self.next = val
            self.anim = True
            self.t = 0

    def update(self, dt):
        if self.anim:
            self.t += dt
            if self.t >= FLIP_DURATION:
                self.anim = False
                self.current = self.next

    def _surf(self, val, w, h):
        if self.last_size != (w, h):
            self.cache.clear()
            self.last_size = (w, h)

        if val in self.cache:
            return self.cache[val]

        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(surf, CARD_BG, (0, 0, w, h), border_radius=int(w * 0.1))

        fs = int(h * 0.85)
        if fs != self.font_size:
            self.font_size = fs
            self.font = get_font(fs)

        txt = self.font.render(str(val), True, TEXT_COLOR)
        rect = txt.get_rect(center=(w // 2, h // 2))
        surf.blit(txt, rect)

        self.cache[val] = surf
        return surf

    def draw(self, screen, x, y, w, h):
        cur = self._surf(self.current, w, h)
        nxt = self._surf(self.next, w, h)
        hh = h // 2

        if not self.anim:
            screen.blit(cur, (x, y))
            pygame.draw.line(screen, SPLIT_COLOR, (x, y + hh), (x + w, y + hh), 2)
            return

        t = self.t / FLIP_DURATION
        screen.blit(nxt, (x, y), (0, 0, w, hh))
        screen.blit(cur, (x, y + hh), (0, hh, w, hh))

        if t < 0.5:
            h2 = int(hh * (1 - t * 2))
            if h2 > 0:
                top = cur.subsurface((0, 0, w, hh))
                screen.blit(pygame.transform.scale(top, (w, h2)), (x, y + hh - h2))
        else:
            h2 = int(hh * ((t - 0.5) * 2))
            if h2 > 0:
                bot = nxt.subsurface((0, hh, w, hh))
                screen.blit(pygame.transform.scale(bot, (w, h2)), (x, y + hh))

        pygame.draw.line(screen, SPLIT_COLOR, (x, y + hh), (x + w, y + hh), 2)

# =====================
# 画像読み込み
# =====================
def load_img(name):
    img = pygame.image.load(os.path.join(IMG_DIR, name)).convert_alpha()
    return pygame.transform.smoothscale(img, (BTN_SIZE, BTN_SIZE))

img_prev  = load_img("prev.png")
img_play  = load_img("play.png")
img_pause = load_img("pause.png")
img_next  = load_img("next.png")

# =====================
# 初期化
# =====================
digits = [FlipDigit(0) for _ in range(4)]
last_time = ""
music = MusicPlayer(MUSIC_DIR)

# =====================
# メインループ
# =====================
running = True
while running:
    dt = clock.tick(60) / 1000

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False
        if e.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(e.size, pygame.RESIZABLE)
        if e.type == pygame.MOUSEBUTTONDOWN:
            if btn_prev.collidepoint(e.pos):
                music.prev()
            elif btn_play.collidepoint(e.pos):
                music.toggle()
            elif btn_next.collidepoint(e.pos):
                music.next()

    if not pygame.mixer.music.get_busy() and not music.paused:
        music.next()

    now = datetime.datetime.now().strftime("%H%M")
    if now != last_time:
        for i in range(4):
            digits[i].set(int(now[i]))
        last_time = now

    for d in digits:
        d.update(dt)

    screen.fill(BG_COLOR)
    W, H = screen.get_size()

    card_h = int(H * 0.45)
    card_w = int(card_h * 0.7)
    gap = int(card_w * 0.15)

    # 時計全体の幅
    total_clock_w = card_w * 4 + gap * 3 + gap
    sx = (W - total_clock_w) // 2
    BLOCK_GAP = 30
    BUTTON_H = 60
    FILENAME_H = 30

    total_block_h = card_h + BLOCK_GAP + BUTTON_H + BLOCK_GAP + FILENAME_H
    sy = (H - total_block_h) // 2
    clock_center_x = sx + total_clock_w // 2


    for i in range(4):
        px = sx + i * (card_w + gap)
        if i >= 2:
            px += gap
        digits[i].draw(screen, px, sy, card_w, card_h)

    # コロン
    colon_x = sx + card_w * 2 + gap * 2 + gap // 2
    colon_x -= int(card_w * 0.08)
    colon_font_size = int(card_h * 0.85)
    colon_font = get_font(colon_font_size)
    colon_txt = colon_font.render(":", True, TEXT_COLOR)
    colon_rect = colon_txt.get_rect(center=(colon_x, sy + card_h // 2 - 20))
    screen.blit(colon_txt, colon_rect)

    # 時計とボタンの間に白い線
    by = sy + card_h + BLOCK_GAP + 10
    pygame.draw.line(screen, (255, 255, 255), (sx, by - BLOCK_GAP//2), (sx + total_clock_w, by - BLOCK_GAP//2), 2)

    # ボタン
    by = sy + card_h + BLOCK_GAP

    bw = 100
    cx = W // 2 + int(card_w * 0.028)

    btn_prev = pygame.Rect(cx - bw - 20, by, bw, BUTTON_H)
    btn_play = pygame.Rect(cx - bw // 2, by, bw, BUTTON_H)
    btn_next = pygame.Rect(cx + 20, by, bw, BUTTON_H)

    # ボタン背景をアプリ背景色で描く
    pygame.draw.rect(screen, BG_COLOR, btn_prev, border_radius=8)
    pygame.draw.rect(screen, BG_COLOR, btn_play, border_radius=8)
    pygame.draw.rect(screen, BG_COLOR, btn_next, border_radius=8)

    # ボタン画像を上に載せる
    screen.blit(img_prev, btn_prev)
    screen.blit(img_pause if not music.paused else img_play, btn_play)
    screen.blit(img_next, btn_next)

    pygame.display.flip()

pygame.quit()
sys.exit()
