#Henry Thomas
#Dakota Crowder
#Evolutionary Computing A412
#April 24, 2018
#Handwritten Letter Feature Vector Generator

from PIL import Image, ImageOps, ImageChops
import os

def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)

def getBitstring(img):
    bitstring = ''
    rgb_img = img.convert('RGB')
    for i in range(50):
        for j in range(50):
            r, g, b = rgb_img.getpixel((i, j))
            if r + g + b > 700:
                bitstring += '0'
            else:
                bitstring += '1'
    return bitstring

def reformat(dataDir):
    letters = []
    folders = os.listdir(dataDir)
    for folder in folders:
        letters.append(os.listdir('%s\\%s' % (dataDir, folder)))
    if not os.path.exists('newDataset'):
        os.makedirs('newDataset')        
        
    for j in range(26):
        print(j+1)
        for i in range(55):
            img = Image.open('%s\\%s\\%s' % (dataDir, folders[j], letters[j][i]))
            trimmed = trim(img)
            trimmed.thumbnail((50, 50))

            h = int((50 - trimmed.size[0])/2)
            v = int((50 - trimmed.size[1])/2)

            formatted = Image.new("RGB", (50, 50), 'white')
            formatted.paste(trimmed, (h, v))
            formatted.save('newDataset\\%s_%s.jpg' % (j+1, i+1))

if __name__ == '__main__':
    dataDir = 'dataset'
    newDataDir = 'newDataset'
    reformat(dataDir)