import pygame
import sys

pygame.init()

# === Constants ===
WIDTH, HEIGHT = 800, 600
MIN_FPS, MAX_FPS = 1, 100
n = 40
BAR_WIDTH = WIDTH//n
running = False
fps = MAX_FPS//2
clock = pygame.time.Clock()


nums = [225, 141, 348, 367, 58, 382, 201, 216, 473, 164, 227, 18, 301, 281, 196, 331, 187, 373, 296, 299, 423, 82, 28, 174, 18, 132, 275, 51, 386, 484, 477, 350, 179, 465, 126, 492, 379, 433, 295, 473]
NUMS = nums[:]
i, j = 0, 0
min_idx = 0
key = None



# --sort functions---

def bubble_sort():
    global i, j, running

    if i < n-1:
        if j < n-i-1:
            if nums[j] > nums[j+1]:
                nums[j], nums[j+1] = nums[j+1], nums[j]
            j += 1
        else:
            j = 0
            i += 1
    else:
        running = False


def selection_sort():
    global i, j, min_idx, running

    if i < n-1:
        if j == 0:
            min_idx = i
            j = i+1

        if j < n:
            if nums[j] < nums[min_idx]:
                min_idx = j
            j += 1
        else:
            nums[i], nums[min_idx] = nums[min_idx], nums[i]
            i += 1
            j = 0
    else:
        running = False

def insertion_sort():
    global i, j, key, running

    if i == 0:
        i = 1
        j = i  

    if i < n:
        if j == i:
            key = nums[i]
            j = i-1

        if j >= 0 and nums[j] > key:
            nums[j+1] = nums[j]
            j -= 1
        else:
            nums[j+1] = key
            i += 1
            j = i   
    else:
        running = False




current_sort = bubble_sort



BG_COLOR = (30, 30, 30)
GRID_COLOR = (60, 60, 60)
CELL_COLOR = (0, 200, 0)
BUTTON_BG = (70, 70, 70)
BUTTON_ACTIVE = (100, 150, 100)
BUTTON_TEXT = (255, 255, 255)
SLIDER_BG = (100, 100, 100)
SLIDER_FG = (0, 180, 0)

# Buttons
BUTTON_W, BUTTON_H = 90, 35
BUTTON_PADDING = 10
BUTTON_Y = HEIGHT - BUTTON_H - 10
SORT_W, SORT_H = 150, 35
SORT_Y = HEIGHT - SORT_H - 45

btn_start_rect = pygame.Rect(10, BUTTON_Y, BUTTON_W, BUTTON_H)
btn_pause_rect = pygame.Rect(10+BUTTON_W+BUTTON_PADDING, BUTTON_Y, BUTTON_W, BUTTON_H)
btn_reset_rect = pygame.Rect(10+2*(BUTTON_W+BUTTON_PADDING), BUTTON_Y, BUTTON_W, BUTTON_H)
btn_bubble_sort_rect = pygame.Rect(10, SORT_Y, SORT_W, SORT_H)
btn_selection_sort_rect = pygame.Rect(10+SORT_W+BUTTON_PADDING, SORT_Y, SORT_W, SORT_H)
btn_insertion_sort_rect = pygame.Rect(10+2*(SORT_W+BUTTON_PADDING), SORT_Y, SORT_W, SORT_H)


SLIDER_X = 10 + 5*(BUTTON_W + BUTTON_PADDING)
SLIDER_Y = BUTTON_Y + BUTTON_H//2 - 5
SLIDER_W = 150
SLIDER_H = 10
slider_rect = pygame.Rect(SLIDER_X, SLIDER_Y, SLIDER_W, SLIDER_H)
handle_x = SLIDER_X + SLIDER_W // 2
dragging_slider = False



screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Algorithm Visualizer")
font = pygame.font.SysFont(None, 22)


def draw_grid():
    for k in range(n):
        pygame.draw.rect(screen, (0,0,255), (k*BAR_WIDTH, HEIGHT-nums[k]-100, BAR_WIDTH-2, nums[k]))

def reset_grid():
    global i, j, nums, running, min_idx, key
    i=0
    j=0
    min_idx = 0
    key = None
    nums = NUMS[:]
    running = False

def draw_buttons():
    pygame.draw.rect(screen, BUTTON_ACTIVE if running else BUTTON_BG, btn_start_rect)
    text_start = font.render("Start", True, BUTTON_TEXT)
    screen.blit(text_start, text_start.get_rect(center=btn_start_rect.center))

    pygame.draw.rect(screen, BUTTON_BG if running else BUTTON_ACTIVE, btn_pause_rect)
    text_pause = font.render("Pause", True, BUTTON_TEXT)
    screen.blit(text_pause, text_pause.get_rect(center=btn_pause_rect.center))

    pygame.draw.rect(screen, BUTTON_BG, btn_reset_rect)
    text_reset = font.render("Reset", True, BUTTON_TEXT)
    screen.blit(text_reset, text_reset.get_rect(center=btn_reset_rect.center))

    pygame.draw.rect(screen, BUTTON_ACTIVE if current_sort == bubble_sort else BUTTON_BG, btn_bubble_sort_rect)
    text_bubble = font.render("BUBBLE SORT", True, BUTTON_TEXT)
    screen.blit(text_bubble, text_bubble.get_rect(center=btn_bubble_sort_rect.center))

    pygame.draw.rect(screen, BUTTON_ACTIVE if current_sort == selection_sort else BUTTON_BG, btn_selection_sort_rect)
    text_selection = font.render("SELECTION SORT", True, BUTTON_TEXT)
    screen.blit(text_selection, text_selection.get_rect(center=btn_selection_sort_rect.center))

    pygame.draw.rect(screen, BUTTON_ACTIVE if current_sort == insertion_sort else BUTTON_BG, btn_insertion_sort_rect)
    text_insertion = font.render("INSERTION SORT", True, BUTTON_TEXT)
    screen.blit(text_insertion, text_insertion.get_rect(center=btn_insertion_sort_rect.center))

    pygame.draw.rect(screen, SLIDER_BG, slider_rect)
    pygame.draw.circle(screen, SLIDER_FG, (handle_x, SLIDER_Y + SLIDER_H//2), 8)

    fps_text = font.render(f"{fps} FPS", True, BUTTON_TEXT)
    screen.blit(fps_text, (SLIDER_X + SLIDER_W + 10, SLIDER_Y - 8))


while True:
    screen.fill(BG_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mx, my = event.pos
                if btn_start_rect.collidepoint(mx,my): running = True
                elif btn_pause_rect.collidepoint(mx,my): running = False
                elif btn_reset_rect.collidepoint(mx,my): reset_grid()
                elif btn_bubble_sort_rect.collidepoint(mx,my):
                    current_sort = bubble_sort
                    running = False
                    reset_grid()
                elif btn_selection_sort_rect.collidepoint(mx,my):
                    current_sort = selection_sort
                    running = False
                    reset_grid()
                elif btn_insertion_sort_rect.collidepoint(mx,my):
                    current_sort = insertion_sort
                    running = False
                    reset_grid()
                elif slider_rect.collidepoint(mx,my):
                    dragging_slider = True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging_slider = False

        elif event.type == pygame.MOUSEMOTION:
            if dragging_slider:
                handle_x = max(SLIDER_X, min(SLIDER_X + SLIDER_W, event.pos[0]))
                ratio = (handle_x - SLIDER_X) / SLIDER_W
                fps = int(MIN_FPS + ratio * (MAX_FPS - MIN_FPS))

    # Draw
    draw_grid()
    draw_buttons()

    # Update game state
    if running:
        current_sort()

    pygame.display.flip()
    clock.tick(fps)

    
    