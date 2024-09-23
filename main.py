import pygame
import redis

import trail_generator

import sys
import time


# colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GRAY = (100, 100, 100)


r = redis.Redis()
pygame.init()
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.NOFRAME)
screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
WINDOW_W, WINDOW_H = screen.get_size()
pygame.display.set_caption("Simple Pygame")

x_coord, y_coord = [], []

# target
ball_radius = 7
ball_x = WINDOW_W // 2
ball_y = WINDOW_H // 2
# ball_speed_x = 1
# ball_speed_y = 1

start_button_width = 100
start_button_height = 50
start_button_x = (WINDOW_W // 2) - (start_button_width // 2)
start_button_y = (WINDOW_H // 2) - (start_button_height // 2)

reset_button_width = 100
reset_button_height = 50
reset_button_x = start_button_width + start_button_x + 20
reset_button_y = WINDOW_H - 70

font = pygame.font.Font(None, 14)
clock = pygame.time.Clock()

ticks = 0
simulation_started = False
fullscreen = False
countdownTick = 0
task1_started = False
task2_started = False
render_countdown = False
render_finish_msg = False

def StartTask1Button(_screen):
    font = pygame.font.Font(None, 48)
    pygame.draw.rect(_screen, RED, (start_button_x, start_button_y, start_button_width, start_button_height))
    text = font.render(f"Start", True, BLACK)
    text_rect = text.get_rect(center=(start_button_x + start_button_width // 2, start_button_y + start_button_height // 2))
    _screen.blit(text, text_rect)


def CounterText(_screen, count: str):
    font = pygame.font.Font(None, 108)
    text = font.render(count, True, (255, 255, 255))
    text_rect = text.get_rect(center=(WINDOW_W // 2, WINDOW_H // 2))
    _screen.blit(text, text_rect)

def toggle_fullscreen():
    global fullscreen, screen, WINDOW_W, WINDOW_H
    fullscreen = not fullscreen
    if fullscreen:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((WINDOW_W, WINDOW_H), pygame.RESIZABLE)
    WINDOW_W, WINDOW_H = screen.get_size()


def PreTask1(_screen):
    font = pygame.font.Font(None, 108)
    text = font.render("Task #1: Follow the Target!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WINDOW_W // 2, WINDOW_H // 3))
    _screen.blit(text, text_rect)
    
    StartTask1Button(_screen)


def FinishedMsg(_screen):
    font = pygame.font.Font(None, 108)
    text = font.render("Finish!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WINDOW_W // 2, WINDOW_H // 2))
    _screen.blit(text, text_rect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if start_button_x < mouse_pos[0] < start_button_x + start_button_width and start_button_y < mouse_pos[1] < start_button_y + start_button_height:
                if not task1_started:
                    task1_started = True
                    x_coord, y_coord = trail_generator.generate_trail(WINDOW_W, WINDOW_H)
                    ball_x, ball_y = x_coord[0], y_coord[0]
                if not render_countdown:
                    render_countdown = True
        # elif event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_F11:
        #         toggle_fullscreen()
        elif event.type == pygame.VIDEORESIZE:
            if not fullscreen:
                width, height = event.size
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

    if simulation_started:
        if ticks == len(x_coord):
            render_finish_msg = True
            simulation_started = False
            ticks = 0
        else:
            ball_x = x_coord[ticks]
            ball_y = y_coord[ticks]
            r.publish("MovingTarget", f"{ball_x};{ball_y};{int(time.time_ns()/10e3)}")
            ticks += 1

    screen.fill(GRAY)
    pygame.draw.circle(screen, RED, (int(ball_x), int(ball_y)), ball_radius)
    
    if not task1_started:
        PreTask1(screen)
    
    if render_finish_msg:
        FinishedMsg(screen)
        if countdownTick > 36:
            render_finish_msg = False
            countdownTick = 0
            ball_radius = 0
        countdownTick += 1
    
    if render_countdown:
        counter_text = ["Ready", "3", "2", "1", "Start!"]
        CounterText(screen, counter_text[countdownTick // 36])
        countdownTick += 1
        if countdownTick == 5*36:
            countdownTick = 0
            render_countdown = False
            simulation_started = True

    pygame.display.flip()
    clock.tick(24)