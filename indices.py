import numpy
import cv2
import matplotlib.pyplot as plt
#from orbit import ISS
#import skyfield
import os
from exif import Image



def get_decimal_coordinates(info):
    for key in ['Latitude', 'Longitude']:
        if 'GPS'+key in info and 'GPS'+key+'Ref' in info:
            e = info['GPS'+key]
            ref = info['GPS'+key+'Ref']
            info[key] = ( e[0][0]/e[0][1] +
                          e[1][0]/e[1][1] / 60 +
                          e[2][0]/e[2][1] / 3600
                        ) * (-1 if ref in ['S','W'] else 1)

    if 'Latitude' in info and 'Longitude' in info:
        return [info['Latitude'], info['Longitude']]

#get_decimal_coordinates(exif['GPSInfo'])
def q(s):
  e=s
  g = ( e[0][0]/e[0][1] +
              e[1][0]/e[1][1] / 60 +
              e[2][0]/e[2][1] / 3600
            )
  return g


import piexif
g="latitude,longitude,SAVI,NDWI,CI"
for filename in os.listdir("imgs"):
  print(filename)
  exif_dict = piexif.load("imgs/"+filename)
  # Extract thumbnail and save it, if exists
  thumbnail = exif_dict.pop('thumbnail')
  if thumbnail is not None:
      with open('thumbnail.jpg', 'wb') as f:
          f.write(thumbnail)

  # Iterate through all the other ifd names and print them
  for ifd in exif_dict:
      for tag in exif_dict[ifd]:
          tag_name = piexif.TAGS[ifd][tag]["name"]
          tag_value = exif_dict[ifd][tag]
          if isinstance(tag_value, bytes):
              tag_value = tag_value[:10]
          if tag_name == "GPSLatitude":
            a=tag_value
          if tag_name == "GPSLongitude":
            b=tag_value
          if tag_name == "GPSLatitudeRef":
            if tag_value.decode()=="S":aa=-1
            else:aa=1
          if tag_name == "GPSLongitudeRef":
            if tag_value.decode()=="W":bb=-1
            else:bb=1
  a,b=q(a),q(b)      
  a,b=a*aa,b*bb    

  #print(a,b)
  im = cv2.cv2.imread(f"imgs/{filename}").astype(numpy.float)
  dst, im = cv2.cv2.threshold(im, 30, -2, cv2.cv2.THRESH_TOZERO)
  dst, im = cv2.cv2.threshold(im, 190, -2, cv2.cv2.THRESH_TRUNC)
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

  #IMGS!!!!! If you need yo check. These make the background appear a moderate colour (the background is set to 0 and some values are negative, so this appears as a middleish colour)
  #plt.imsave("vegetation.jpg", savi, cmap=plt.cm.Greens)
  #plt.imsave("water.jpg", ndwi, cmap=plt.cm.Blues)
  #plt.imsave("chlorophyll.jpg", ci, cmap=plt.cm.Reds)
  #av_savi = min([min(i) for i in [j for j in savi]])
  av_savi = sum([sum(i) for i in savi]) / numpy.count_nonzero(savi)
  av_ndwi = sum([sum(i) for i in ndwi]) / numpy.count_nonzero(ndwi)
  av_ci = sum([sum(i) for i in ci]) / numpy.count_nonzero(ci)
  g+=f"\n{a},{b},{av_savi},{av_ndwi},{av_ci}"
  #print(g)  

  print("")
  

f = open("results.csv","w")
f.write(g)
f.close()
