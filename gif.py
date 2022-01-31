import os
import imageio

path = 'output/'

files =  os.listdir(path)
files.sort()

images = []

for file in files:
    if (file[-3:] == 'png'):
        images.append(imageio.imread(path+file))

imageio.mimsave(f'{path}/gif.gif', images)

# print(files)