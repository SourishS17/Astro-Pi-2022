import numpy
import cv2
import matplotlib.pyplot as plt
#from orbit import ISS
import skyfield
import os

for filename in os.listdir("imgs"):
  print(filename)
  im = cv2.cv2.imread(f"imgs/{filename}").astype(numpy.float)
  dst, im = cv2.cv2.threshold(im, 30, -2, cv2.cv2.THRESH_TOZERO)
  dst, im = cv2.cv2.threshold(im, 220, -2, cv2.cv2.THRESH_TRUNC)
  #BGR Ordering
  # B = NIR
  # NIR, G, R
  height, width, channels = im.shape
  NIR, green, red = cv2.cv2.split(im)
  numpy.seterr(divide="ignore", invalid="ignore")
  def vegetation(n, r):
    return ((n - r) / (n + r + 0.428)) * (1 + 0.428)
  def water(n, g):
    return (g - n) / (g + n)
  def chlorophyll(n, r):
    return (n / r) - 1

  L = 0.428
  savi = (((NIR - red) / (NIR + red + L)) * (1 + L))
  ndwi = numpy.nan_to_num((green - NIR) / (green + NIR))
  ci = (NIR / red) - 1
  ci[ci == numpy.inf] = 0
  ci = numpy.nan_to_num(ci)

  #plt.imsave("vegetation.jpg", savi, cmap=plt.cm.Greens)
  #plt.imsave("water.jpg", ndwi, cmap=plt.cm.Blues)
  #plt.imsave("chlorophyll.jpg", ci, cmap=plt.cm.Reds)
  av_savi = sum([sum(i) for i in savi]) / numpy.count_nonzero(savi)
  av_ndwi = sum([sum(i) for i in ndwi]) / numpy.count_nonzero(ndwi)
  av_ci = sum([sum(i) for i in ci]) / numpy.count_nonzero(ci)
  print(av_savi, av_ndwi, av_ci)
