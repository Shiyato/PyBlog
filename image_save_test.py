from PIL import Image
import os
path = os.path.abspath('.')
img = Image.open('test_img.jpg')
img = img.convert('RGB')
img.resize()
img.save(path + '\\images\\test_img.jpg')
