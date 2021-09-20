#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import random
import math

SCREEN_DIM = (800, 600)


class Vec2d:

    def __init__(self, point):
        self.x = point[0]
        self.y = point[1]

    def __sub__(self, other):
        """"возвращает разность двух векторов"""
        return Vec2d((self.x - other.x, self.y - other.y))

    def __add__(self, other):
        """возвращает сумму двух векторов"""
        return Vec2d((self.x + other.x, self.y + other.y))

    def __len__(self):
        """возвращает длину вектора"""
        return math.sqrt(self.x * self.x + self.y * self.y)

    def __mul__(self, k):
        """возвращает произведение вектора на число"""
        return Vec2d((self.x * k, self.y * k))

    def int_pair(self):
        """возвращает кортеж из двух целых чисел
        (текущие координаты вектора)"""
        return (int(self.x), int(self.y))

    def vec(self):
        """возвращает пару координат, определяющих вектор (координаты точки
        конца вектора), координаты начальной точки вектора совпадают с началом
        системы координат (0, 0)"""
        return (self.x, self.y)

    def __str__(self):
        return f"Vector(x:{self.x}, y:{self.y})"


class Polyline:

    def __init__(self):
        self.points = []
        self.speeds = []

    def add_or_delete(self, point, id):
        """ Adding new point to list. If new point near than 10 pixels from
        existing point we think we want to delete it"""
        if id < len(self.points):
            points = self.points[id]
            speeds = self.speeds[id]
            for p in points:
                (x, y) = p.vec()
                if abs(x - point[0]) <= 10 and abs(y - point[1]) <= 10:
                    print(f"New point {point} near {p} -> removing")
                    points.remove(p)
                    return
            points.append(Vec2d((point[0], point[1])))
            speeds.append(Vec2d((random.random(), random.random())))
        else:
            self.points.append([Vec2d((point[0], point[1]))])
            self.speeds.append([Vec2d((random.random(), random.random()))])

    def set_points(self, knots_speeds):
        """функция перерасчета координат опорных точек"""
        for i, speed in knots_speeds.items():
            if i < len(self.points):
                points = self.points[i]
                speeds = self.speeds[i]
                for p in range(len(points)):
                    # changing point coordinates
                    points[p] = points[p] + speeds[p] * speed
                    # getting point and speed coordinates
                    (x, y) = points[p].vec()
                    (sx, sy) = speeds[p].vec()
                    # if we out of bounds -> go back
                    if x > SCREEN_DIM[0] or x < 0:
                        speeds[p] = Vec2d((-sx, sy))
                    if y > SCREEN_DIM[1] or y < 0:
                        speeds[p] = Vec2d((sx, -sy))

    def draw_points(self, width=3, color=(255, 255, 255)):
        """функция отрисовки точек на экране"""
        for points in self.points:
            for p in points:
                pygame.draw.circle(gameDisplay, color, p.int_pair(), width)


class Knot(Polyline):

    def __init__(self, count):
        super().__init__()
        self.line_points = []
        self.count = count

    def __get_point__(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg] * alpha + \
            self.__get_point__(points, alpha, deg - 1) * (1 - alpha)

    def __get_points__(self, base_points):
        alpha = 1 / self.count
        res = []
        for i in range(self.count):
            res.append(self.__get_point__(base_points, i * alpha))
        return res

    def __get_knot__(self):
        self.line_points = []
        for points in self.points:
            line_points = []
            if len(points) < 3:
                return
            for i in range(-2, len(points) - 2):
                ptn = []
                ptn.append((points[i] + points[i + 1]) * 0.5)
                ptn.append(points[i + 1])
                ptn.append((points[i + 1] + points[i + 2]) * 0.5)

                line_points.extend(self.__get_points__(ptn))
            self.line_points.append(line_points)

    def add_or_delete(self, point, id):
        super().add_or_delete(point, id)
        self.__get_knot__()

    def set_points(self, knots_speeds):
        super().set_points(knots_speeds)
        self.__get_knot__()

    def draw_line(self, width=3, color=(255, 255, 255)):
        for line_points in self.line_points:
            for p_n in range(-1, len(line_points) - 1):
                pygame.draw.line(gameDisplay,
                                 color,
                                 line_points[p_n].int_pair(),
                                 line_points[p_n + 1].int_pair(),
                                 width)


def draw_help():
    """функция отрисовки экрана справки программы"""
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = []
    data.append(["F1", "Show Help"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play"])
    data.append(["Num+", "More points"])
    data.append(["Num-", "Less points"])
    data.append([",", "Decreasing speed"])
    data.append([".", "Increasing speed"])
    data.append(["u", "Switch to next line"])
    data.append(["j", "Switch to previous line"])
    data.append(["", ""])
    data.append([str(steps), "Current points"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
        (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * i))


if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    steps = 35
    working = True
    knot = Knot(steps)
    show_help = False
    pause = True
    knot_id = 0
    knots_speeds = {knot_id: 1}
    hue = 0
    color = pygame.Color(0)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    knot = Knot(steps)
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_u:
                    knot_id += 1
                    if knot_id not in knots_speeds:
                        knots_speeds[knot_id] = 1
                if event.key == pygame.K_j:
                    knot_id -= 1 if knot_id > 0 else 0
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0
                if event.key == pygame.K_PERIOD:
                    knots_speeds[knot_id] += 1
                if event.key == pygame.K_COMMA:
                    knots_speeds[knot_id] -= 1
                    # if speed < 0 -> points goes in oposit direction
            if event.type == pygame.MOUSEBUTTONDOWN:
                knot.add_or_delete(event.pos, knot_id)

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)

        knot.draw_points()
        knot.draw_line(3, color)

        if not pause:
            knot.set_points(knots_speeds)
        if show_help:
            draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
