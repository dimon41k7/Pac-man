import pygame
import math
import os

from field import Field
from settings import *

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.w, self.h = screen.get_size()
        self.font = pygame.font.SysFont(None, 28)
        self.font_big = pygame.font.SysFont(None, 80)
        self.font_btn = pygame.font.SysFont(None, 42)

    def draw_pacman(self, x, y, direction, color):
        cx = x * size + size // 2
        cy = y * size + size // 2
        radius = size // 2 - 5

        angle = {
            "right": 0,
            "left": math.pi,
            "up": -math.pi / 2,
            "down": math.pi / 2
        }[direction]

        pygame.draw.circle(self.screen, color, (cx, cy), radius)

        mouth = math.pi / 4
        p1 = (cx, cy)
        p2 = (cx + radius * math.cos(angle - mouth),
              cy + radius * math.sin(angle - mouth))
        p3 = (cx + radius * math.cos(angle + mouth),
              cy + radius * math.sin(angle + mouth))

        pygame.draw.polygon(self.screen, BG_COLOR, [p1, p2, p3])
    
    def draw_enemies(self, enemies):
        for enemy in enemies:
            cx = enemy.x * size + size // 2
            cy = enemy.y * size + size // 2

            pygame.draw.circle(self.screen, ENEMY_COLOR, (cx, cy),size // 2 - 8)

    def draw_field(self, field, player, color):
        for y, row in enumerate(field.grid):
            for x, cell in enumerate(row):
                px, py = x * size, y * size

                if cell == "🟧":
                    pygame.draw.rect(self.screen, WALL_COLOR, (px, py, size, size))
                elif cell == "🔸":
                    pygame.draw.circle(self.screen, DOT_COLOR,
                        (px + size // 2, py + size // 2), 6)
                elif cell == "➕":
                    pygame.draw.circle(
                        self.screen,
                        (0, 255, 0),
                        (px + size // 2, py + size // 2),
                        8
                    )
                elif cell == "👻":
                    pygame.draw.circle(
                        self.screen,
                        (200, 200, 255),
                        (px + size // 2, py + size // 2),
                        10
                    )

        self.draw_pacman(player.x, player.y, player.direction, color)
    
    def draw_ui(self, player, time, level_number):
        text = (
            f"Життів: {player.lives}   "
            f"Кроків: {player.steps}   "
            f"Зібрано: {player.collected}   "
            f"Час: {time}   "
            f"Карта: {level_number}"
        )
        surface = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(surface, (10, 10))
    
    def draw_text(self, text, x, y):
        surf = self.font.render(text, True, (255,255,255))
        rect = surf.get_rect(center=(x, y))
        self.screen.blit(surf, rect)
        return rect

    def draw_menu(self):
        mouse_pos = pygame.mouse.get_pos()
        title = self.font_big.render("PAC-MAN", True, (255, 200, 0))
        title_rect = title.get_rect(center=(self.w // 2, 120))
        self.screen.blit(title, title_rect)

        btn_w = 260
        btn_h = 60
        start_y = 240
        gap = 80

        btn_start = pygame.Rect(self.w // 2 - btn_w // 2, start_y, btn_w, btn_h)
        btn_wardrobe = pygame.Rect(self.w // 2 - btn_w // 2, start_y + gap, btn_w, btn_h)
        btn_records = pygame.Rect(self.w // 2 - btn_w // 2, start_y + gap * 2, btn_w, btn_h)
        btn_profile = pygame.Rect(self.w // 2 - btn_w // 2, start_y + gap * 3, btn_w, btn_h)
        btn_exit = pygame.Rect(self.w // 2 - btn_w // 2, start_y + gap * 4, btn_w, btn_h)
        

        self._draw_button(btn_start, "Нова гра", mouse_pos)
        self._draw_button(btn_wardrobe, "Гардероб", mouse_pos)
        self._draw_button(btn_records, "Рекорди", mouse_pos)
        self._draw_button(btn_profile, "Профіль", mouse_pos)
        self._draw_button(btn_exit, "Вихід", mouse_pos)
        

        return btn_start, btn_wardrobe, btn_records, btn_profile, btn_exit

    def draw_wardrobe(self, colors, selected):
        mouse_pos = pygame.mouse.get_pos()

        title = self.font_big.render("ГАРДЕРОБ", True, (255, 200, 0))
        title_rect = title.get_rect(center=(self.w // 2, 120))
        self.screen.blit(title, title_rect)

        rects = []
        box_size = 60
        spacing = 20
        cols = 5

        total_width = cols * box_size + (cols - 1) * spacing
        start_x = self.w // 2 - total_width // 2
        start_y = 260

        for i, color in enumerate(colors):
            row = i // cols
            col = i % cols

            x = start_x + col * (box_size + spacing)
            y = start_y + row * (box_size + spacing)

            rect = pygame.Rect(x, y, box_size, box_size)

            if rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, (255, 255, 255), rect.inflate(6, 6), 2)

            pygame.draw.rect(self.screen, color, rect)

            if i == selected:
                pygame.draw.rect(self.screen, (255, 255, 255), rect, 4)

            rects.append(rect)

        btn_back = pygame.Rect(self.w // 2 - 130, 500, 260, 60)
        self._draw_button(btn_back, "Назад", mouse_pos)

        return rects, btn_back


    def _draw_button(self, rect, text, mouse_pos):
        if rect.collidepoint(mouse_pos):
            color = (255, 230, 120) 
        else:
            color = (255, 200, 0) 

        pygame.draw.rect(self.screen, color, rect, border_radius=12)
        pygame.draw.rect(self.screen, (0,0,0), rect, 3, border_radius=12)

        txt = self.font_btn.render(text, True, (0,0,0))
        txt_rect = txt.get_rect(center=rect.center)
        self.screen.blit(txt, txt_rect)
    
    def draw_game_over(self, title_text):
        mouse = pygame.mouse.get_pos()

        title = self.font_big.render(title_text, True, (255, 60, 60))
        self.screen.blit(title, title.get_rect(center=(self.w//2, 140)))

        btn_restart = pygame.Rect(self.w//2 - 130, 300, 260, 60)
        btn_exit = pygame.Rect(self.w//2 - 130, 380, 260, 60)

        self._draw_button(btn_restart, "Нова гра", mouse)
        self._draw_button(btn_exit, "Вихід", mouse)

        return btn_restart, btn_exit
    
    def draw_profile(self, player_name):
        self.screen.fill(BG_COLOR)

        title = self.font_big.render("ПРОФІЛЬ", True, (255, 200, 0))
        self.screen.blit(title, title.get_rect(center=(self.w // 2, 100)))

        box = pygame.Rect(self.w//2 - 200, 200, 400, 60)
        pygame.draw.rect(self.screen, (60, 60, 60), box, border_radius=10)
        pygame.draw.rect(self.screen, (255, 200, 0), box, 2, border_radius=10)

        name_surface = self.font.render(
            player_name if player_name else "Введи ім'я...",
            True,
            (255, 255, 255)
        )
        self.screen.blit(name_surface, (box.x + 15, box.y + 18))

        hint = self.font.render(
            "ENTER — зберегти | ESC — назад",
            True,
            (180, 180, 180)
        )
        self.screen.blit(hint, hint.get_rect(center=(self.w // 2, 420)))

    def draw_records(self, records):
        self.screen.fill(BG_COLOR)

        title = self.font_big.render("РЕКОРДИ", True, (255, 200, 0))
        self.screen.blit(title, title.get_rect(center=(self.w // 2, 80)))

        y = 150
        if not records:
            txt = self.font.render("Рекордів поки немає", True, (200, 200, 200))
            self.screen.blit(txt, txt.get_rect(center=(self.w // 2, y)))
        else:
            for r in records[-10:][::-1]:
                line = f"{r['name']} | Карта {r['level']} | {r['time']} сек"
                txt = self.font.render(line, True, (255, 255, 255))
                self.screen.blit(txt, (100, y))
                y += 30

        hint = self.font.render("ESC — назад у меню", True, (180, 180, 180))
        self.screen.blit(hint, hint.get_rect(center=(self.w // 2, 520)))
    
    def draw_game_buttons(self, field):
        btn_w, btn_h = 160, 45
        gap = 20

        cell = 64

        field_width = len(field.grid[0]) * cell
        field_height = len(field.grid) * cell

        field_x = (self.w - field_width) // 2
        field_y = 120

        buttons_y = field_y + field_height + 20

        restart = pygame.Rect(
            field_x,
            buttons_y,
            btn_w,
            btn_h
        )

        exit_btn = pygame.Rect(
            field_x + btn_w + gap,
            buttons_y,
            btn_w,
            btn_h
        )

        mouse_pos = pygame.mouse.get_pos()
        self._draw_button(restart, "Заново", mouse_pos)
        self._draw_button(exit_btn, "В меню", mouse_pos)

        return restart, exit_btn
    
    def draw_warning(self, text, color):
        box = pygame.Rect(self.w//2 - 260, self.h - 120, 520, 60)
        pygame.draw.rect(self.screen, color, box, border_radius=12)

        msg = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(
            msg,
            msg.get_rect(center=box.center)
        )