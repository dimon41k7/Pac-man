import pygame
import time
import math
import random
import os
import pickle

from field import Field
from physics import Physics
from renderer import Renderer
from input import Input
from player import Player
from enemy import Enemy
from record import *
from settings import *


def is_enemy_at(x: int, y: int) -> bool:
    positions = [(e.x, e.y) for e in enemies]
    return (x, y) in positions

def test_is_enemy_at():
    class Dummy:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    global enemies
    enemies = [Dummy(2, 3)]

    assert is_enemy_at(2, 3) is True
    assert is_enemy_at(0, 0) is False


test_is_enemy_at()

pygame.init()
screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Pac-Man")
clock = pygame.time.Clock()

renderer = Renderer(screen)
input_handler = Input()

MENU = "menu"
GAME = "game"
WARDROBE = "wardrobe"
RECORD = "record"
WIN = "win"
GAME_OVER = "game_over"
PROFILE = "profile"

LEVEL_FILES = [
    "level1.txt",
    "level2.txt",
    "level3.txt",
    "level4.txt",
    "level5.txt",]

FILE = "records.bin"
PROFILE_FILE = "profile.txt"

level_start_time = 0
current_time = 0

state = MENU
running = True

color = PACMAN_COLORS[0]
timer = 0
delay = 15


typing_name = False

btn_restart = None
btn_exit = None

warning_no_name = False
warning_timer = 0
get_elapsed_time = None

btn_restart = None
btn_exit = None

def log_call(func):
    def wrapper(*args, **kwargs):
        print(f"Виклик функції: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@log_call
def start_new_game():
    global field, physics, player, enemies, timer, current_level, level_start_time, current_time, get_elapsed_time, game_timer

    game_timer = make_game_timer()
    level_start_time = time.time()
    current_time = 0
    get_elapsed_time = create_level_timer()

    level_index = random.randint(0, len(LEVEL_FILES) - 1)
    current_level = level_index + 1
    level_path = os.path.join("levels", LEVEL_FILES[level_index])

    grid, player_pos = Field.load_level(level_path)
    field = Field(grid)
    physics = Physics()
    timer = 0

    player = Player(*player_pos, player_name)



    enemies = []
    for _ in range(2):
        while True:
            ex = random.randint(1, len(grid[0]) - 2)
            ey = random.randint(1, len(grid) - 2)
            if field.grid[ey][ex] == "🔸":
                enemies.append(
                    Enemy(ex, ey, random.choice(["horizontal", "vertical"]))
                )
                break



def is_level_complete(field):
    remaining = {
        cell
        for row in field.grid
        for cell in row
    }
    return "🔸" not in remaining


def load_records():
    try:
        with open(FILE, "rb") as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError):
        return []


def save_record(name, /, level_number, *, time_sec):
    records = load_records()

    for r in records:
        if r["level"] == level_number:
            if time_sec < r["time"]:
                r["time"] = time_sec
                r["name"] = name
            break
    else:
        records.append({
            "level": level_number,
            "name": name,
            "time": time_sec
        })

    with open(FILE, "wb") as f:
        pickle.dump(records, f)

def create_level_timer():
    start_time = level_start_time

    def get_elapsed():
        nonlocal start_time
        return int(time.time() - start_time)

    return get_elapsed

def load_player_name():
    try:
        with open(PROFILE_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""


def save_player_name(name):
    with open(PROFILE_FILE, "w", encoding="utf-8") as f:
        f.write(name)

player_name = load_player_name()

def make_game_timer():
    start = time.time()

    def elapsed():
        return int(time.time() - start)

    return elapsed

while running:
    screen.fill(BG_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if state == RECORD and event.key == pygame.K_ESCAPE:
                state = MENU

        if state == PROFILE and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                typing_name = False
                state = MENU

            elif event.key == pygame.K_BACKSPACE:
                player_name = player_name[:-1]

            elif event.key == pygame.K_RETURN:
                typing_name = False
                save_player_name(player_name)
                state = MENU

            else:
                if len(player_name) < 12 and event.unicode.isprintable():
                    player_name += event.unicode

        if event.type == pygame.KEYDOWN:
            if state == PROFILE and event.key == pygame.K_ESCAPE:
                state = MENU

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            if state == MENU:
                btn_start, btn_wardrobe, btn_records, btn_profile, btn_exit = renderer.draw_menu()

                if btn_start.collidepoint(mx, my):
                    if not player_name:
                        warning_no_name = True
                        warning_timer = 120 
                    else:
                        start_new_game()
                        state = GAME

                elif btn_wardrobe.collidepoint(mx, my):
                    state = WARDROBE

                elif btn_exit.collidepoint(mx, my):
                    running = False
                
                elif btn_records.collidepoint(mx, my):
                    state = RECORD
                
                elif btn_profile.collidepoint(mx, my):
                    state = PROFILE
                    typing_name = True
            
            elif state in (WIN, GAME_OVER):
                if btn_restart and btn_restart.collidepoint(mx, my):
                    start_new_game()
                    state = GAME

                elif btn_exit and btn_exit.collidepoint(mx, my):
                    state = MENU


            elif state == WARDROBE:
                color_rects, back = renderer.draw_wardrobe(PACMAN_COLORS, PACMAN_COLORS.index(color))

                for i, r in enumerate(color_rects):
                    if r.collidepoint(mx, my):
                        color = PACMAN_COLORS[i]

                if back.collidepoint(mx, my):
                    state = MENU
            
            elif state == GAME:
                if btn_restart and btn_restart.collidepoint(mx, my):
                    start_new_game()

                elif btn_exit and btn_exit.collidepoint(mx, my):
                    state = MENU

            
    if state == GAME:
        elapsed = get_elapsed_time()

        if not(0<=elapsed<=300):
            state = MENU
            continue

        dx, dy, direction = input_handler.get_direction()

        current_time = game_timer()

        if direction:
            ny = player.y + dy
            nx = player.x + dx

            if is_enemy_at(nx, ny):
                player.lose_life()
                time.sleep(0.1)
            else:
                ny, nx, moved = physics.try_move(
                    player.y, player.x, dy, dx, field
                )

                if moved:
                    field.grid[player.y][player.x] = "　"

                    if field.eat_life(ny, nx):
                        player.add_life()

                    if field.eat_resource(ny, nx):
                        player.collect()

                    field.grid[ny][nx] = "😎"
                    player.x, player.y = nx, ny
                    player.direction = direction
                    player.add_step()

                    time.sleep(0.1)
        if is_level_complete(field):
            save_record(player.name, current_level, time_sec = current_time)
            state = MENU

        timer += 1
        if timer >= delay:
            for enemy in enemies:
                if enemy.x < 0 or enemy.y < 0:
                    continue 
                enemy.move(field)
            timer = 0

        for enemy in enemies:
            if enemy.x == player.x and enemy.y == player.y:
                player.lose_life()

        if not player.is_alive:
            print(player)
            state = GAME_OVER
        
        if field.check_win():
            save_record(player.name, current_level, time_sec = current_time)
            state = WIN

    if state == MENU:
        renderer.draw_menu()

    elif state == WARDROBE:
        renderer.draw_wardrobe(PACMAN_COLORS, PACMAN_COLORS.index(color))

    elif state == GAME:
        renderer.draw_field(field, player, color)
        renderer.draw_enemies(enemies)
        renderer.draw_ui(player, current_time, current_level)
        btn_restart, btn_exit = renderer.draw_game_buttons(field)
    
    elif state == GAME_OVER:
        btn_restart, btn_exit = renderer.draw_game_over("ПОРАЗКА")

    elif state == WIN:
        btn_restart, btn_exit = renderer.draw_game_over("ПЕРЕМОГА!")
    
    elif state == PROFILE:
        renderer.draw_profile(player_name)
    
    elif state == RECORD:
        renderer.draw_records(load_records())
        
    
    if warning_no_name:
        renderer.draw_warning("Введіть ім'я у розділі «Профіль»", color = (180, 50, 50))
        warning_timer -= 1
        if warning_timer <= 0:
            warning_no_name = False    

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

