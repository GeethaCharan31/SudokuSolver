import time
import pygame
from grid import Grid
from darkmode import DarkMode

# everything related to display
size = 9
WIDTH, HEIGHT = 60 * (size + 5), 60 * (size)
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Solver")
pygame_icon = pygame.image.load('images/sudoku.png')
pygame.display.set_icon(pygame_icon)

FPS = 60

dm = DarkMode(False)

pygame.font.init()


def time_format(secs):
    s = secs % 60
    m = secs // 60
    h = m // 60

    return str(h) + ":" + str(m) + ":" + str(s)


def draw_to_win(win, grid, playing_time,completed):
    if dm.get_mode():
        win.fill((18,18,18))
        text_color = (255, 255, 255)  # white
    else:
        text_color = (0, 0, 0)  # black
        win.fill((255, 255, 255))

    # Time
    lg_fnt = pygame.font.SysFont("comicsans", 40)
    text = lg_fnt.render("Time: " + time_format(playing_time), 1, (255, 0, 0))
    win.blit(text, (620, 20))

    # Instructions
    md_fnt = pygame.font.SysFont("comicsans", 31)
    sm_fnt = pygame.font.SysFont("comicsans", 24)
    text = md_fnt.render("Instructions", 1, text_color)
    win.blit(text, (560, 70))
    text = sm_fnt.render("* No common number in a row", 1, text_color)
    win.blit(text, (560, 100))
    text = sm_fnt.render("* No common number in a column", 1, text_color)
    win.blit(text, (560, 120))
    text = sm_fnt.render("* No common number in a sub grid", 1, text_color)
    win.blit(text, (560, 140))

    text = md_fnt.render("To Visualize", 1, text_color)
    win.blit(text, (560, 170))
    text = sm_fnt.render("press escape key", 1, text_color)
    win.blit(text, (560, 200))

    text = sm_fnt.render("Dark Mode - Press 'd'", 1, text_color)
    win.blit(text, (560, 240))
    text = sm_fnt.render("Light Mode - Press 'l'", 1, text_color)
    win.blit(text, (560, 260))

    if completed:
        solvedImg=pygame.image.load("images/solved.png")
        win.blit(solvedImg, (565, 280))
    grid.draw()

def main():
    grid = Grid(9, 9, 540, 540, win,dm)

    clock = pygame.time.Clock()  # object for clock
    key = None
    start_time = time.time()
    completed=False
    run = True
    while run:  # basic while loop
        clock.tick(FPS)  # set to 60 FPS
        playing_time = round(time.time() - start_time)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_KP1:
                    key = 1
                if event.key == pygame.K_KP2:
                    key = 2
                if event.key == pygame.K_KP3:
                    key = 3
                if event.key == pygame.K_KP4:
                    key = 4
                if event.key == pygame.K_KP5:
                    key = 5
                if event.key == pygame.K_KP6:
                    key = 6
                if event.key == pygame.K_KP7:
                    key = 7
                if event.key == pygame.K_KP8:
                    key = 8
                if event.key == pygame.K_KP9:
                    key = 9
                if event.key == pygame.K_BACKSPACE:
                    grid.clear_cell()
                    key = None
                if event.key == pygame.K_ESCAPE:
                    grid.solve_gui()
                if event.key == pygame.K_d:
                    dm.set_mode(True)
                if event.key == pygame.K_l:
                    dm.set_mode(False)
                if event.key == pygame.K_RETURN:
                    i, j = grid.selected
                    if grid.cells[i][j].temp != 0:
                        if grid.place(grid.cells[i][j].temp):
                            print("Success")
                        else:
                            print("Wrong")
                        key = None

                        if grid.is_finished():
                            print("Game Over")
                            completed=True

            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                clicked = grid.click(position)
                if clicked:
                    grid.select_cell(clicked[0], clicked[1])
                    key = None

        if grid.selected and key != None:
            grid.sketch(key)

        draw_to_win(win, grid, playing_time,completed)
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
