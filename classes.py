from scipy.spatial import Voronoi
from random import randint, seed
from datetime import datetime
import cv2
import numpy as np

seed(datetime.now())

class Point:
    def __init__(self, img_width, img_height):
        self.coordinates = (randint(0, img_width), randint(0, img_height))
        self.color = (randint(0, 256),
                    randint(0, 256),
                    randint(0, 256),
                    255)

    def mutate(self, alpha=0.5):
        if randint(0, 100) < alpha*100: # mutating color
            r = min(255, max(0, self.color[0] + int(randint(-25, 25))))
            
            g = min(255, max(0, self.color[1] + int(randint(-25, 25))))
            
            b = min(255, max(0, self.color[2] + int(randint(-25, 25))))
            
            self.color = (r, g, b, 255)
        else: # mutating points
            self.coordinates = (self.coordinates[0] + int(randint(-15, 15)), 
             self.coordinates[1] + int(randint(-15, 15)))

class VoronoiDiagram:
    def __init__(self, size, pts, bg_color=(0, 0, 0)):
        self.img_width, self.img_height = size
        self.points = [Point(self.img_width, self.img_height) for _ in range(pts)]
        self.bg_color = (*bg_color, 255)
    
    @property
    def num_pts(self):
        return len(self.points)

    def mutate(self, alpha=0.5):
        self.points[randint(0, self.num_pts-1)].mutate(alpha=0.5)
        

    def draw(self):
        image = np.zeros((self.img_height, self.img_width, 3), dtype='uint8')
        
        vor = Voronoi([p.coordinates for p in self.points], qhull_options="Qc")

        for i in range(self.num_pts):
            region = vor.point_region[i]
            polygon = []
            can_draw = True
            for vertex in vor.regions[region]:
                if vertex == -1:
                    can_draw = False
                    break
                polygon.append(vor.vertices[vertex])
            if can_draw:
                cv2.fillPoly(image, pts = np.int32([np.array([polygon])]), color = self.points[i].color)
        return image
