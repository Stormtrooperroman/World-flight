from PIL import Image, ImageDraw
import noise
import random
import numpy as np



MAP_SIZE = (1024, 768)
SCALE = 256
EXPO_HEIGHT = 2
COLORS = {
    "grass" : (236,255,253),
    "forest" : (194, 217, 223),
    "sand" : (227, 236, 234),
    "water" : (212, 241, 249),
    "rock" : (139, 137, 137),
    "snow" : (255, 250, 250)
}

lut_vectors = (
    (-1, 1), (0, 1), (1, 1),
    (-1, 0),         (1, 0),
    (-1, -1), (0, -1), (1, -1)
)

def update_point(coords, seed):
    return noise.snoise2(coords[0]/SCALE,
                          coords[1]/SCALE,
                          octaves=6,
                          persistence=0.5,
                          lacunarity=2,
                          repeatx=MAP_SIZE[0],
                          repeaty=MAP_SIZE[1],
                          base=330
                         )


def normalize(input_map, minimum, maximum, expo):
    scale = maximum - minimum
    output_map = np.zeros(MAP_SIZE)
    for x in range(MAP_SIZE[0]):
        for y in range(MAP_SIZE[1]):
            output_map[x][y] = ((input_map[x][y] - minimum)/scale)**expo
    return output_map

def generate_heightmap():
    seed = int(random.random()*1000)
    minimum = 0
    maximum = 0
    heightmap = np.zeros(MAP_SIZE)

    for x in range(MAP_SIZE[0]):
        for y in range(MAP_SIZE[1]):
            new_value = update_point((x, y), seed)
            heightmap[x][y] = new_value
            if new_value < minimum:
                minimum = new_value
            if new_value > maximum:
                maximum = new_value
    print("Height map generated with seed:", seed)
    return normalize(heightmap, minimum, maximum, EXPO_HEIGHT)

def out_of_bounds(coord):
    if coord[0] < 0 or coord[0] >= MAP_SIZE[0]:
        return True
    if coord[1] < 0 or coord[1] >= MAP_SIZE[1]:
        return True
    return False

def generate_slopemap(heightmap):
    slopemap = np.zeros(MAP_SIZE)
    minimum = 0
    maximum = 0

    for x in range(MAP_SIZE[0]):
        for y in range(MAP_SIZE[1]):
            
            slope = 0
            for vector in lut_vectors:
                coord = (x+vector[0], y+vector[1])
                if out_of_bounds(coord):
                    continue
                slope += abs(heightmap[x][y]-heightmap[coord[0]][coord[1]])
            slope = slope/8
            slopemap[x][y] = slope
            if slope < minimum:
                minimum = slope
            if slope > maximum:
                maximum = slope
    print("Slopemap generated")
    return normalize(slopemap, minimum, maximum, 1)

def get_color(height, slope):
    if height > 0.2 and height < 0.9 and slope > 0.45:
       return COLORS["rock"]
    if height <= 0.2:
        return COLORS["water"]
    elif height > 0.2 and height <= 0.225:
        return COLORS["sand"]
    elif height > 0.225 and height <= 0.45:
        return COLORS["grass"]
    elif height > 0.45 and height <= 0.85:
        return COLORS["forest"]
    elif height > 0.85 and height <= 0.9:
        return COLORS["rock"]
    elif height > 0.9:
        return COLORS["snow"]


def export_norm_map(norm_map, filename):
    image = Image.new('RGB', MAP_SIZE, 0)
    draw = ImageDraw.ImageDraw(image)

    for x in range(MAP_SIZE[0]):
        for y in range(MAP_SIZE[1]):
            color = int(norm_map[x][y]*255)
            draw.point((x, y), (color, color, color))
    image.save(filename) 
    print(filename, "saved")
    return

def export_texture(heightmap, slopemap, filename):
    image = Image.new('RGB', MAP_SIZE, 0)
    draw = ImageDraw.ImageDraw(image)
    for x in range(MAP_SIZE[0]):
        for y in range(MAP_SIZE[1]):
            draw.point((x, y), get_color(heightmap[x][y], slopemap[x][y]))
    image.save(filename)
    print(filename, "saved")
    return

def main():
    heightmap = generate_heightmap()
    slopemap = generate_slopemap(heightmap)
    export_norm_map(heightmap, "img/heightmap.png")
    export_norm_map(slopemap, "img/slopemap.png")
    export_texture(heightmap, slopemap, "img/texture.png")

if __name__ == "__main__":
    main()