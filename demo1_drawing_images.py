from cmu_graphics import *
from PIL import Image

# For more info about the Image class, see:
# https://pillow.readthedocs.io/en/stable/reference/Image.html 

def onAppStart(app):
    # Load the PIL image
    app.image = Image.open('CSM_0.png')

    # Transpose the PIL image
    app.imageFlipped = app.image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    
    # Convert each PIL image to a CMUImage for drawing
    app.image = CMUImage(app.image)
    app.imageFlipped = CMUImage(app.imageFlipped)

def redrawAll(app):
    drawLabel('Original',200, 50, align='center', size=24)
    drawImage(app.image, 200, 200, align='center')

    drawLabel('Scaled', 500, 50, align='center', size=24)
    pilImage = app.image.image
    drawImage(app.image, 500, 200, align='center',
              width=pilImage.width//2,
              height=pilImage.height//2)

    drawLabel('Flipped', 200, 400, align='center', size=24)
    drawImage(app.imageFlipped, 200, 550, align='center')

    drawLabel('Scaled and Rotated', 500, 400, align='center', size=24)
    drawImage(app.image, 500, 550, align='center',
              rotateAngle=-60,
              width=pilImage.width//2,
              height=pilImage.height//2)

def main():
    runApp(700, 700)

if __name__ == '__main__':
    main()