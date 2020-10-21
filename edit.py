import math
import copy
from pgm import *

def averaging(image):
        H = len(image)
        W = len(image[0])
        out = [[0 for i in range(W)] for j in range(H)]
        for i in range(H):
                for j in range(W):
                        if i == 0 or i == H - 1 or j == 0 or j == W - 1:
                                out[i][j] == image[i][j]
                        else:
                                out[i][j] = int((image[i-1][j-1] + image[i-1][j] + image[i-1][j+1] + image[i][j-1] + image[i][j] + image[i][j+1] + image[i+1][j-1] + image[i+1][j] + image[i+1][j+1])/9)
        return out

def edge_detection(image):
        H = len(image)
        W = len(image[0])
        b_out = [[0 for i in range(W+2)] for j in range(H+2)]
        out = [[0 for i in range(W)] for j in range(H)]
        def hdif(image, i, j):
                return (image[i-1][j-1] - image[i-1][j+1]) + 2*(image[i][j-1] - image[i][j+1]) + (image[i+1][j-1] - image[i+1][j+1])
        def vdif(image, i, j):
                return (image[i-1][j-1] - image[i+1][j-1]) + 2*(image[i-1][j] - image[i+1][j]) + (image[i-1][j+1] - image[i+1][j+1])
        def grad(image, i, j):
                return int(math.sqrt(hdif(image, i, j)*hdif(image, i, j) + vdif(image, i, j)*vdif(image, i, j)))
        for m in range(H+2):
                b_out[m][0] = 0
                b_out[m][W+1] = 0
        for n in range(W+2):
                b_out[0][n] = 0
                b_out[H+1][n] = 0
        for m in range(1, H+1):
                for n in range(1, W+1):
                        b_out[m][n] = image[m-1][n-1]
        for i in range(H):
                for j in range(H):
                        out[i][j] = grad(b_out, i+1, j+1)
        return out

def normal(image):
        b = 0
        for i in image:
                for j in i:
                        if j > b:
                                b = j
        for i1 in range(len(image)):
                for j1 in range(len(image[0])):
                        image[i1][j1] = image[i1][j1] * 255//b
        return image

def threshold(image, threshold):
        for i in range(len(image)):
                for j in range(len(image[0])):
                        if image[i][j] >= threshold:
                                image[i][j] = 255
                        elif image[i][j] < threshold:
                                image[i][j] = 0
        return image

def minEnergy(image):
        H = len(image)
        W = len(image[0])
        edge = edge_detection(image)
        out = copy.deepcopy(image)
        MinEnergy = [[0 for i in range(W)] for j in range(H)]
        for i in range(H):
                for j in range(W):
                        if i == 0:
                                MinEnergy[i][j] = edge[i][j]
                        elif j == 0:
                                MinEnergy[i][j] = edge[i][j] + min(MinEnergy[i-1][j], MinEnergy[i-1][j+1])
                        elif j == W - 1:
                                MinEnergy[i][j] = edge[i][j] + min(MinEnergy[i-1][j-1], MinEnergy[i-1][j])
                        else:
                                MinEnergy[i][j] = edge[i][j] + min(MinEnergy[i-1][j-1], MinEnergy[i-1][j], MinEnergy[i-1][j+1])
        '''def MinEnergy(image, i, j):
                if i == 0:
                        return edge[i][j]
                elif j == 0:
                        return edge[i][j] + min(MinEnergy(image, i-1, j), MinEnergy(image, i-1, j+1))
                elif j == W - 1:
                        return edge[i][j] + min(MinEnergy(image, i-1, j-1), MinEnergy(image, i-1, j))
                else:
                        return edge[i][j] + min(MinEnergy(image, i-1, j-1), MinEnergy(image, i-1, j), MinEnergy(image, i-1, j+1))'''
        '''def min_path(image, i, j):
                if j == 0:
                        if MinEnergy(image, i-1, j) = (min(MinEnergy(image, i-1, j), MinEnergy(image, i-1, j+1))):
                                
                elif j == W - 1:
                        m = image[i-1].index(min(MinEnergy(image, i-1, j-1), MinEnergy(image, i-1, j)))
                else:
                        m = image[i-1].index(min(MinEnergy(image, i-1, j-1), MinEnergy(image, i-1, j), MinEnergy(image, i-1, j+1)))
                if i == 1:
                        return [m]
                else:
                        return [m] + min_path(image, i-1, m)'''
        n_min = [0]
        for n in range(W):
                if MinEnergy[H-1][n] < MinEnergy[H-1][n_min[0]]:
                        n_min = [n]
                elif MinEnergy[H-1][n] == MinEnergy[H-1][n_min[0]]:
                        n_min += [n]
                else:
                        continue

        def paint(image, o_image, i, j):
                o_image[i][j] = 255
                if i != 0:
                        if j == 0:
                                x = min(MinEnergy[i-1][j], MinEnergy[i-1][j+1])
                                for k in range(j, j+2):
                                        if MinEnergy[i-1][k] == x:
                                                paint(image, o_image, i-1, k)
                        elif j == len(image[0]) - 1:
                                x = min(MinEnergy[i-1][j-1], MinEnergy[i-1][j])
                                for k in range(j-1, j+1):
                                        if MinEnergy[i-1][k] == x:
                                                paint(image, o_image, i-1, k)
                        else:
                                x = min(MinEnergy[i-1][j-1], MinEnergy[i-1][j], MinEnergy[i-1][j+1])
                                for k in range(j-1, j+2):
                                        if MinEnergy[i-1][k] == x:
                                                paint(image, o_image, i-1, k)
        '''paths = []
        for n in n_min:
                paths.append(min_path(image, H-1, n))
        for path in paths:
                p = H - 1
                for q in path:
                        out[p][q] = 255
                        p -= 1'''
        for n in n_min:
                paint(edge, out, H-1, n)
        return out
