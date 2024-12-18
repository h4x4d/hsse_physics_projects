import pygame
import math
import numpy as np
import random
import matplotlib.pyplot as plt
from fontTools.unicodedata import block

h = 1  # spatial step width
k = 0.05  # time step width
dimx = 200  # width of the simulation domain
dimy = 200  # height of the simulation domain
cellsize = 1  # display size of a cell in pixel
staticBlocks = [
    [dimx // 2 + 40, dimy // 2 - 40, dimx // 2 + 42, dimy // 2 + 40],
    [dimx // 2 + 1, dimy // 2 - 40, dimx // 2 + 40, dimy // 2 - 38],
    [dimx // 2 - 42, dimy // 2 - 40, dimx // 2 - 40, dimy // 2 + 40],
    [dimx // 2 - 40, dimy // 2 - 40, dimx // 2 - 1, dimy // 2 - 38],
    # [dimx // 2 - 5, dimy // 2 + 45, dimx // 2 + 5, dimy // 2 + 55],
    # [0, 9, dimx-1, 10],
    # [dimx // 2 - 40, dimy // 2 + 38, dimx // 2 + 40 , dimy // 2 + 40],
    # [0, 8, dimx-1, 9],
]
# а давайте запускать не волну из одной точки а волну гаусовым распределением в 2д на 10 клеток
sz = 10
sigma = 1.2 # отклонение взято от балды
xx, yy = np.meshgrid(range(-sz, sz), range(-sz, sz))
gauss_peak = np.zeros((sz, sz))
gauss_peak = 1 / (sigma*2*math.pi) * (math.sqrt(2*math.pi)) * np.exp(- 0.5 * ((xx**2+yy**2)/(sigma**2)))

def put_gauss_peak(u, x : int, y : int, height):
    w,h = gauss_peak.shape
    w = int(w/2)
    h = int(h/2)      
    u[0:2, x-w:x+w, y-h:y+h] += height * gauss_peak


def init_simulation():
    u = np.zeros((3, dimx, dimy))  # The three-dimensional simulation grid
    c = 0.6  # The "original" wave propagation speed
    alpha = np.full((dimx, dimy), ((c * k) / h) ** 2)  # Use NumPy full for constant alpha
    return u, alpha


        
def update1(u, alpha):
    u[2], u[1] = u[1], u[0].copy()  # Avoid extra copying, reassign layers directly
    u[0, 1:dimx - 1, 1:dimy - 1] = (
            alpha[1:dimx - 1, 1:dimy - 1]
            * (
                    u[1, 0:dimx - 2, 1:dimy - 1]  # Left neighbors
                    + u[1, 2:dimx, 1:dimy - 1]  # Right neighbors
                    + u[1, 1:dimx - 1, 0:dimy - 2]  # Top neighbors
                    + u[1, 1:dimx - 1, 2:dimy]  # Bottom neighbors
                    - 4 * u[1, 1:dimx - 1, 1:dimy - 1]  # Current cell
            )
    )
    u[0, 1:dimx - 1, 1:dimy - 1] += 2 * u[1, 1:dimx - 1, 1:dimy - 1] - u[2, 1:dimx - 1, 1:dimy - 1]
    u[0, 1:dimx - 1, 1:dimy - 1] *= (0.995 ** k)
    
def update2(u, alpha):
    "аналогичен update1 но использует дискретный оператор лапласа с точностью до O(x^4)"
    u[2], u[1] = u[1], u[0].copy()  # Avoid extra copying, reassign layers directly
    
    u[0, 2:dimx-2, 2:dimy-2]  = alpha[2:dimx-2, 2:dimy-2]\
                                    * ( -  1 * u[1, 2:dimx-2, 0:dimy-4]
                                        + 16 * u[1, 2:dimx-2, 1:dimy-3]                                       

                                        -  1 * u[1, 0:dimx-4, 2:dimy-2]  
                                        + 16 * u[1, 1:dimx-3, 2:dimy-2]
                                        - 60 * u[1, 2:dimx-2, 2:dimy-2]  
                                        + 16 * u[1, 3:dimx-1, 2:dimy-2] 
                                        -  1 * u[1, 4:dimx,   2:dimy-2]

                                        + 16 * u[1, 2:dimx-2, 3:dimy-1]                                         
                                        - 1  * u[1, 2:dimx-2, 4:dimy]    
                                        ) / 12 \
                                    + 2*u[1, 2:dimx-2, 2:dimy-2] \
                                    -   u[2, 2:dimx-2, 2:dimy-2] 
    
    u[0, 1:dimx - 1, 1:dimy - 1] *= (0.995 ** k)


def add_static(u, blocks):
    for block in blocks:
        add_static_block(u, block)


def add_static_block(u, cords):
    u[0, cords[0]:cords[2], cords[1]:cords[3]] = 0


def render_static(blocks, pixeldata):
    for block in blocks:
        pixeldata[block[0]:block[2], block[1]:block[3], 1] = 0


def place_raindrops(u):
    if random.random() < 0.0002:
        x = random.randrange(5, dimx - 5)
        y = random.randrange(5, dimy - 5)
        put_gauss_peak(u, x, y, 120)


def center_wave(u, x, y, v):
    u[0, x, y] = v


def render_arr(x_cords, y_cords):
    plt.plot(x_cords, y_cords)

    # naming the x axis
    plt.xlabel('T time')
    # naming the y axis
    plt.ylabel('U moment')

    # function to show the plot
    plt.show()


def main():
    pygame.init()
    display = pygame.display.set_mode((dimx * cellsize, dimy * cellsize))
    pygame.display.set_caption("Solving the 2D Wave Equation")

    u, alpha = init_simulation()
    pixeldata = np.zeros((dimx, dimy, 3), dtype=np.uint8)

    center_wave(u, dimx // 2, dimy // 2, 100) 

    # put_gauss_peak(u, int(dimx/2), int(dimy/2), 3000)
    clock = pygame.time.Clock()

    x_cords = [0]
    y_cords = [0]
    dt = 0.05
    max_time = 600

    while dt < max_time:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # place_raindrops(u)  # Uncomment if you want random raindrops
        update1(u, alpha)
        add_static(u, staticBlocks)

        x_cords.append(dt)
        y_cords.append(u[0, dimx // 2, dimy // 2])
        dt += k

        # Vectorized update of pixel data
        pixeldata[1:dimx, 1:dimy, 0] = np.clip(u[0, 1:dimx, 1:dimy] + 128, 0, 255)
        pixeldata[1:dimx, 1:dimy, 1] = np.clip(u[1, 1:dimx, 1:dimy] + 128, 0, 255)
        pixeldata[1:dimx, 1:dimy, 2] = np.clip(u[2, 1:dimx, 1:dimy] + 128, 0, 255)
        render_static(staticBlocks, pixeldata)

        surf = pygame.surfarray.make_surface(pixeldata)
        display.blit(pygame.transform.scale(surf, (dimx * cellsize, dimy * cellsize)), (0, 0))
        pygame.display.update()

        clock.tick(60 / k)  # Limit to 60 frames per second

    render_arr(x_cords, y_cords)


main()
