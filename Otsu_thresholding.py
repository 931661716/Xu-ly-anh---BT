from PIL import Image
import os, sys
import numpy as np

def total_pix(image):
  size = image.size[0] * image.size[1]
  return size

def histogramify(image):
  grayscale_array = []
  for w in range(0,image.size[0]):
    for h in range(0,image.size[1]):
      intensity = image.getpixel((w,h))
      grayscale_array.append(intensity)

  total_pixels = image.size[0] * image.size[1]
  bins = range(0,257)
  img_histogram = np.histogram(grayscale_array, bins)
  return img_histogram


def otsu(image):
  hist = histogramify(image)
  total = total_pix(image)
  current_max, threshold = 0, 0
  sumT, sumF, sumB = 0, 0, 0
  for i in range(0,256):
    sumT += i * hist[0][i]
  weightB, weightF = 0, 0
  varBetween, meanB, meanF = 0, 0, 0
  for i in range(0,256):
    weightB += hist[0][i]
    weightF = total - weightB
    if weightF == 0:
      break
    sumB += i*hist[0][i]
    sumF = sumT - sumB
    meanB = sumB/weightB
    meanF = sumF/weightF
    varBetween = weightB * weightF
    varBetween *= (meanB-meanF)*(meanB-meanF)
    if varBetween > current_max:
      current_max = varBetween
      threshold = i 
  print ("threshold is:", threshold)
  threshold(threshold, image) 
  return threshold

#Basic Thresholding

def threshold(t, image):
  intensity_array = []
  for w in range(0,image.size[1]):
    for h in range(0,image.size[0]):
      intensity = image.getpixel((h,w))
      if (intensity <= t):
        x = 0
      else:
        x = 255
      intensity_array.append(x)
  image.putdata(intensity_array)
  image.show()  
  
#

try:
  img = Image.open(sys.argv[1])
  img.load()
  img.show()
  bw = img.convert('L')
  otsu(bw)
except IOError:                                                                   
  print ("Unable to open file. Please try another format or check spelling.")