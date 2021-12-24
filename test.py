from PIL import Image
import matplotlib.pyplot as plt
def photo2pixelart(image, i_size, o_size):

    #read file
    img=Image.open(image)

    #convert to small image
    small_img=img.resize(i_size,Image.BILINEAR)

    #resize to output size
    res=small_img.resize(img.size, Image.NEAREST)

    #Save output image
    filename=f'test.png'
    res.save(filename)

img=Image.open('img.png')
photo2pixelart(image='img.png',i_size=(100,100),
                    o_size=img.size)