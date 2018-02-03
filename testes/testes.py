import matplotlib.pyplot as plt
import cmath
import pygame
import time
white = (255, 255, 255)
grey = (50, 50, 50)
black = (0, 0, 0)
orange = (255, 165, 0)
red = (255, 0, 0)

scale = 3
w_size = 1000

scale = scale * 2
block = int(w_size // scale // 2)
w, h = int(2 * scale * block), int(scale * block)
color_s = orange
color_g = red

def g(s):
    return 2 * (s + 3) / ((s + 2) * (s**2 + 2*s + 2))

def calcpoint(p, c):
    return ((p[0] - c[0])/block, (p[1] - c[1])/block)

def getcomplex(p):
    return p[0] + p[1]*1j

def s_map(s):
    return (block*s.real + w/4, block*s.imag + h/2)

def g_map(gs):
    return (block*gs.real + 3*w/4 - 0, block*gs.imag + h/2)

pygame.init()


screen = pygame.display.set_mode((w, h))
done = False
collect = False


s_center = (w/4, h/2)
g_center = (3*w/4, h/2)


s_List = []
g_List = []
first = False
nyquist = False
supernyquist = False

while not done:
    screen.fill((0,0,0))

    for wi in range(- w//block//4, w//block//4):
        pygame.draw.line(screen, grey, (s_center[0] + wi * block, 0), (s_center[0] + wi * block, h), 1)
        pygame.draw.line(screen, grey, (g_center[0] + wi * block, 0), (g_center[0] + wi * block, h), 1)

    for hi in range(- h//block//2, h//block//2):
        pygame.draw.line(screen, grey, (0, s_center[1] + hi*block), (w, s_center[1] + hi*block), 1)

    pygame.draw.line(screen, white, (10, h / 2), (w / 2 - 10, h / 2), 2)
    pygame.draw.line(screen, white, (w / 4, 10), (w / 4, h - 10), 2)
    pygame.draw.line(screen, white, (w / 2 + 10, h / 2), (w - 10, h / 2), 2)
    pygame.draw.line(screen, white, (3 * w / 4, 10), (3 * w / 4, h - 10), 2)
    pygame.draw.line(screen, white, (w/2, 0), (w/2, h), 2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            collect = True
            first = True
        if event.type == pygame.MOUSEBUTTONUP:
            collect = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_g]:
        nyquist = True
    elif keys[pygame.K_s]:
        supernyquist = True

    if first:
        s_List = []
        g_List = []
        first = False
    if nyquist:
        s_List = []
        g_List = []

        for wp in range(-10000, 10000):
            s = getcomplex(calcpoint((w/4, h/2 + wp), s_center))
            s_point = s_map(s)
            s_List.append(s_point)
            gs = g(s)
            g_point = g_map(gs)
            g_List.append(g_point)
        nyquist = False

    if supernyquist:
        s_List = []
        g_List = []

        for wp in range(-scale*block//2, scale*block//2):
            for hp in range(-scale*block//2, scale*block//2):
                try:
                    s = getcomplex(calcpoint((w/4 + hp, h/2 + wp), s_center))
                    s_point = s_map(s)
                    s_List.append(s_point)
                    gs = g(s)
                    g_point = g_map(gs)
                    g_List.append(g_point)
                except:
                    pass
        supernyquist = False

    if collect:
        try:
            mousepos = pygame.mouse.get_pos()
            if (mousepos[0] < w/2):
                s = getcomplex(calcpoint(mousepos, s_center))
                s_point = s_map(s)
                s_List.append(s_point)
                gs = g(s)
                g_point = g_map(gs)
                g_List.append(g_point)
        except:
            pass


    if (len(g_List) > 0):

        ps = (int(s_List[-1][0]), int(s_List[-1][1]))
        pg = (int(g_List[-1][0]), int(g_List[-1][1]))
        pygame.draw.circle(screen, color_s, ps, 5, 0)
        if(pg[0] > w/2):
            pygame.draw.circle(screen, color_g, pg, 5, 0)
        if (len(g_List) > 1):
            for i in range(1, len(g_List)):
                p2g = (int(g_List[i][0]), int(g_List[i][1]))
                p1g = (int(g_List[i - 1][0]), int(g_List[i - 1][1]))
                p2s = (int(s_List[i][0]), int(s_List[i][1]))
                p1s = (int(s_List[i - 1][0]), int(s_List[i - 1][1]))
                pygame.draw.line(screen, color_s, p1s, p2s, 3)
                if (p2g[0] > w/2 and p1g[0] > w/2):
                    pygame.draw.line(screen, color_g, p1g, p2g, 3)

    pygame.display.flip()
