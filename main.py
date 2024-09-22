import pygame
import sys

import trail_generator

pygame.init()

width, height = 1280, 720
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("Simple Pygame")

BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)

x_coord, y_coord = trail_generator.generate_trail(width, height)

ball_radius = 7
ball_x = width // 2
ball_y = height // 2
ball_speed_x = 1
ball_speed_y = 1

button_width = 100
button_height = 50
button_x = 20
button_y = height - 70
button_color = RED

font = pygame.font.Font(None, 14)
clock = pygame.time.Clock()


ticks = 0
started = False
fullscreen = False

def draw_button(screen, color):
    pygame.draw.rect(screen, color, (button_x, button_y, button_width, button_height))
    text = font.render(f"w:{width}, h:{height}", True, BLACK)
    if started: 
        text = font.render(f"Stop", True, BLACK)
    text_rect = text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
    screen.blit(text, text_rect)


def button2(screen, color):
    global x_coord, y_coord
    
    pygame.draw.rect(screen, color, (140, button_y, button_width, button_height))
    text = font.render("New Test", True, BLACK)
    text_rect = text.get_rect(center=(140 + button_width // 2, button_y + button_height // 2))
    screen.blit(text, text_rect)
    
    x_coord, y_coord = trail_generator.generate_trail(width, height)


def toggle_fullscreen():
    global fullscreen, screen, width, height
    fullscreen = not fullscreen
    if fullscreen:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    width, height = screen.get_size()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if button_x < mouse_pos[0] < button_x + button_width and button_y < mouse_pos[1] < button_y + button_height:
                if started:
                    ticks = 0
                started = not started
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                toggle_fullscreen()
        elif event.type == pygame.VIDEORESIZE:
            if not fullscreen:
                width, height = event.size
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

    if started:
        if ticks == len(x_coord):
            ticks = 0
        ball_x = x_coord[ticks]
        ball_y = y_coord[ticks]
        ticks += 1

    if ball_x <= ball_radius or ball_x >= width - ball_radius:
        ball_speed_x = -ball_speed_x
    if ball_y <= ball_radius or ball_y >= height - ball_radius:
        ball_speed_y = -ball_speed_y

    screen.fill(BLACK)
    pygame.draw.circle(screen, YELLOW, (int(ball_x), int(ball_y)), ball_radius)
    draw_button(screen, button_color)
    
    if not started:
        button2(screen, button_color)

    pygame.display.flip()
    clock.tick(24)