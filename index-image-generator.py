import numpy
import cv2
import matplotlib.pyplot as plt
import skyfield
import os

thresh = 10
for filename in os.listdir("imgs"):
  print(thresh)
  filename = "image_001.jpg"
  im = cv2.cv2.imread(f"imgs/{filename}").astype(numpy.float)
  dst, im = cv2.cv2.threshold(im, thresh, -2, cv2.cv2.THRESH_TOZERO)
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
  ci[ci == numpy.inf] = -2
  ci = numpy.nan_to_num(ci)
  savi[savi == 0] = min([min(i) for i in savi])
  ndwi[ndwi == 0] = min([min(i) for i in ndwi])
  ci[ci == 0] = min([min(i) for i in ci])


  plt.imsave(f"vegetation_{thresh}.jpg", savi, cmap=plt.cm.Greens)
  plt.imsave(f"water_{thresh}.jpg", ndwi, cmap=plt.cm.Blues)
  plt.imsave(f"chlorophyll_{thresh}.jpg", ci, cmap=plt.cm.Reds)
  thresh += 5
