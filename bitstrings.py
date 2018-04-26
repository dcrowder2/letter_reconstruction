#Henry Thomas
#Dakota Crowder
#Evolutionary Computing A412
#April 24, 2018
#Handwritten Letter Bitstring Generator

from PIL import Image, ImageOps, ImageChops
import os

def bitstring(dataDir):
    filenames = os.listdir(dataDir)     
    with open('bitstrings.txt', 'w') as f: 
        for filename in filenames:
            bitstring = ''
            img = Image.open('%s\\%s' % (dataDir, filename))
            rgb_img = img.convert('RGB')
            for i in range(img.size[0]):
                for j in range(img.size[1]):
                    r, g, b = rgb_img.getpixel((i, j))
                    if r + g + b > 400:
                        bitstring += '1'
                    else:
                        bitstring += '0'
            f.write(filename[:filename.find('_')] +' ' + bitstring + '\n')
            
if __name__ == '__main__':
    dataDir = 'newDataset'
    bitstring(dataDir)