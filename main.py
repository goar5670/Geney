import cv2
import numpy as np

from copy import deepcopy
from random import randint

from classes import VoronoiDiagram

targetName = 'sample00.png'

target = cv2.imread(f'testingImages/{targetName}')

size = (target.shape[1], target.shape[0])

num_pts = 1300

def mse(imageA, imageB):
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err

def score(x: VoronoiDiagram) -> float:
    return mse(x.draw(), target)

def mutate(x: VoronoiDiagram, alpha=0.5) -> VoronoiDiagram:
    z = deepcopy(x)
    z.mutate(alpha=alpha)
    return z

def summarize(gen, v):
    if gen%100 == 0:
        print(f'{targetName}', gen, score(v))
    if gen%1000 == 0:
        cv2.imwrite(f'output/{targetName}_GEN_%06d.png' % gen, v.draw())

def evolve(v: VoronoiDiagram, start, end):
    s = score(v)
    gen = start
    while gen < end:
        v1 = mutate(v)
        v2 = mutate(v)
        s1 = score(v1)
        s2 = score(v2)
        if s < s1 and s < s2:
            v = v
            s = s
        elif s1 < s2:
            v = v1
            s = s1
        else:
            v = v2
            s = s2
        gen += 1
        summarize(gen, v)
    return v

v = VoronoiDiagram(size, num_pts, bg_color=(255, 255, 255))

v = evolve(v, 0, 100000)