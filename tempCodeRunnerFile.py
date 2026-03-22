import pygame
import sys
import random

pygame.init()

# === Constants ===
WIDTH, HEIGHT = 1280, 720
MIN_FPS, MAX_FPS = 1, 100
N_MIN, N_MAX = 5, 150
n = 40
BAR_WIDTH = WIDTH/n

running = False
fps = MAX_FPS//2
clock = pygame.time.Clock()


nums = [random.randint(1, 500) for _ in range(n)]
NUMS = nums[:]

i, j = 0, 0
min_idx = 0
key = None
merge_gen = None



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


# --- merge sort functions ---

def merge_sort_gen(arr, l, r):
    if l>=r:
        return 
    
    mid = (l+r)//2

    yield from merge_sort_gen(arr, l, mid)
    yield from merge_sort_gen(arr, mid+1, r)

    temp = []
    i, j, = l, mid+1

    while i<=mid and j<=r:
        if arr[i] <= arr[j]:
            temp.append(arr[i])
            i+=1
        else:
            temp.append(arr[j])
            j+=1
        
        yield
    
    while i<=mid:
        temp.append(arr[i])
        i+=1
        yield

    while j<=r:
        temp.append(arr[j])
        j+=1
        yield
    
    for k in range(len(temp)):
        arr[l+k] = temp[k]
        yield
    

def start_merge_sort():
    global merge_gen, running
    merge_gen = merge_sort_gen(nums, 0, n-1)

def merge_sort():
    global merge_gen, running
    try:
        next(merge_gen)
    except StopIteration:
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
SORT_Y = HEIGHT - SORT_H - 50

btn_start = pygame.Rect(10, BUTTON_Y, BUTTON_W, BUTTON_H)
btn_pause = pygame.Rect(10+BUTTON_W+BUTTON_PADDING, BUTTON_Y, BUTTON_W, BUTTON_H)
btn_reset = pygame.Rect(10+2*(BUTTON_W+BUTTON_PADDING), BUTTON_Y, BUTTON_W, BUTTON_H)
btn_generate = pygame.Rect(10+3*(BUTTON_W+BUTTON_PADDING), BUTTON_Y, BUTTON_W, BUTTON_H)
btn_bubble_sort = pygame.Rect(10, SORT_Y, SORT_W, SORT_H)
btn_selection_sort = pygame.Rect(10+SORT_W+BUTTON_PADDING, SORT_Y, SORT_W, SORT_H)
btn_insertion_sort = pygame.Rect(10+2*(SORT_W+BUTTON_PADDING), SORT_Y, SORT_W, SORT_H)
btn_merge_sort = pygame.Rect(10+3*(SORT_W+BUTTON_PADDING), SORT_Y, SORT_W, SORT_H)


SLIDER_X = 10 + 6*(BUTTON_W + BUTTON_PADDING)-30
SLIDER_Y = BUTTON_Y + BUTTON_H//2 - 5
SLIDER_W = 150
SLIDER_H = 10
slider_rect = pygame.Rect(SLIDER_X, SLIDER_Y, SLIDER_W, SLIDER_H)
handle_x = SLIDER_X + SLIDER_W // 2
dragging_slider = False
dragging_n_slider = False

N_SLIDER_X=10 + 4*(BUTTON_W + BUTTON_PADDING)-30
N_SLIDER_Y=BUTTON_Y + BUTTON_H//2 - 5
N_SLIDER_W=150
n_slider_rect=pygame.Rect(N_SLIDER_X,N_SLIDER_Y,N_SLIDER_W,10)
n_handle_x=N_SLIDER_X+(n-N_MIN)/(N_MAX-N_MIN)*N_SLIDER_W
dragging_n_slider=False



screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sorting Algorithm Visualizer")
font = pygame.font.SysFont(None, 22)

def gen_grid():
    global nums, NUMS, BAR_WIDTH
    BAR_WIDTH = WIDTH/n
    nums=[random.randint(1,500) for _ in range(n)]
    NUMS = nums[:]

def draw_grid():
    for k in range(n):
        x = int(BAR_WIDTH*k)
        pygame.draw.rect(screen, (0,0,255), (x, HEIGHT-nums[k]-100, int(BAR_WIDTH), nums[k]))

def reset_grid():
    global i, j, nums, running, min_idx, key, merge_gen
    i=0
    j=0
    min_idx = 0
    key = None
    merge_gen = None
    nums = NUMS[:]
    running = False

def draw_buttons():
    pygame.draw.rect(screen, BUTTON_ACTIVE if running else BUTTON_BG, btn_start)
    pygame.draw.rect(screen, BUTTON_BG if running else BUTTON_ACTIVE, btn_pause)
    pygame.draw.rect(screen, BUTTON_BG, btn_reset)
    pygame.draw.rect(screen, BUTTON_BG, btn_generate)
    pygame.draw.rect(screen, BUTTON_ACTIVE if current_sort == bubble_sort else BUTTON_BG, btn_bubble_sort)
    pygame.draw.rect(screen, BUTTON_ACTIVE if current_sort == selection_sort else BUTTON_BG, btn_selection_sort)
    pygame.draw.rect(screen, BUTTON_ACTIVE if current_sort == insertion_sort else BUTTON_BG, btn_insertion_sort)
    pygame.draw.rect(screen, BUTTON_ACTIVE if current_sort == merge_sort else BUTTON_BG, btn_merge_sort)

    start_text = font.render("Start", True, BUTTON_TEXT)
    screen.blit(start_text, start_text.get_rect(center=btn_start.center))    
    pause_text = font.render("Pause", True, BUTTON_TEXT)
    screen.blit(pause_text, pause_text.get_rect(center=btn_pause.center))    
    reset_text = font.render("Reset", True, BUTTON_TEXT)
    screen.blit(reset_text, reset_text.get_rect(center=btn_reset.center))
    generate_text = font.render("Generate", True, BUTTON_TEXT)
    screen.blit(generate_text, generate_text.get_rect(center=btn_generate.center))
    bubble_text = font.render("BUBBLE SORT", True, BUTTON_TEXT)
    screen.blit(bubble_text, bubble_text.get_rect(center=btn_bubble_sort.center))
    selection_text = font.render("SELECTION SORT", True, BUTTON_TEXT)
    screen.blit(selection_text, selection_text.get_rect(center=btn_selection_sort.center))
    insertion_text = font.render("INSERTION SORT", True, BUTTON_TEXT)
    screen.blit(insertion_text, insertion_text.get_rect(center=btn_insertion_sort.center))
    merge_text = font.render("MERGE SORT", True, BUTTON_TEXT)
    screen.blit(merge_text, merge_text.get_rect(center=btn_merge_sort.center))

    pygame.draw.rect(screen,SLIDER_BG,slider_rect)
    pygame.draw.circle(screen,SLIDER_FG,(int(handle_x),SLIDER_Y+5),8)
    screen.blit(font.render(f"FPS:{fps}",1,BUTTON_TEXT),(SLIDER_X+160,SLIDER_Y-5))

    pygame.draw.rect(screen,SLIDER_BG,n_slider_rect)
    pygame.draw.circle(screen,SLIDER_FG,(int(n_handle_x),N_SLIDER_Y+5),8)
    screen.blit(font.render(f"N:{n}",1,BUTTON_TEXT),(N_SLIDER_X+160,N_SLIDER_Y-5))


while True:
    screen.fill(BG_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mx, my = event.pos

                if btn_start.collidepoint(mx,my): 
                    if current_sort == merge_sort and merge_gen is None:
                        start_merge_sort()
                    running = True
                elif btn_pause.collidepoint(mx,my): running = False
                elif btn_reset.collidepoint(mx,my): reset_grid()
                elif btn_generate.collidepoint(mx, my) :
                    gen_grid()
                    running = False
                elif btn_bubble_sort.collidepoint(mx,my):
                    current_sort = bubble_sort
                    running = False
                    reset_grid()
                elif btn_selection_sort.collidepoint(mx,my):
                    current_sort = selection_sort
                    running = False
                    reset_grid()
                elif btn_insertion_sort.collidepoint(mx,my):
                    current_sort = insertion_sort
                    running = False
                    reset_grid()
                elif btn_merge_sort.collidepoint(mx,my):
                    current_sort = merge_sort
                    running = False
                    reset_grid()
                elif slider_rect.collidepoint(mx,my):
                    dragging_slider = True
                elif n_slider_rect.collidepoint(mx,my):
                    dragging_n_slider = True

        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging_slider = False
                dragging_n_slider=False

        elif event.type == pygame.MOUSEMOTION:
            if dragging_slider:
                handle_x = max(SLIDER_X, min(SLIDER_X + SLIDER_W, event.pos[0]))
                ratio = (handle_x - SLIDER_X) / SLIDER_W
                fps = int(MIN_FPS + ratio * (MAX_FPS - MIN_FPS))
            
            if dragging_n_slider:
                n_handle_x=max(N_SLIDER_X,min(N_SLIDER_X+N_SLIDER_W,event.pos[0]))
                ratio=(n_handle_x-N_SLIDER_X)/N_SLIDER_W
                new_n=int(N_MIN+ratio*(N_MAX-N_MIN))

                if new_n!=n:
                    n=new_n
                    gen_grid()
        

    draw_grid()
    draw_buttons()


    if running:
        current_sort()

    pygame.display.flip()
    clock.tick(fps)

    
    