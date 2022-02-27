# ---------------------------------------
# IMPORTS
# ---------------------------------------

from picamera import PiCamera # Take images
from time import sleep # Pauses in code
from logzero import logger, logfile # Logging for debugging
from orbit import ISS # Check if dark
from skyfield.api import load # Check if dark
from datetime import datetime, timedelta # Keeping program under 3 hours
import numpy as np # To deal with images
import cv2 # To deal with images
from pathlib import Path # Ensure to use the correct paths
import os # To create a directory for images



# ---------------------------------------
# INITIALISING VARIABLES
# ---------------------------------------

# Creating initial time variables to know when to stop the program
start_time = datetime.now()
now_time = datetime.now()

# Setting up the base path to store logs/images in
base_folder = Path(__file__).parent.resolve()

# Creating a directory to store all the images in
img_dir = f"{base_folder}/imgs/"
if not(os.path.isdir(img_dir)):
   os.makedirs(img_dir)

# Variables for checking sunlight
ephemeris = load("de421.bsp")
timescale = load.timescale()

# Camera settings - max res for more precise indices
camera = PiCamera()
camera.resolution = (4056,3040)

# Setting up a logging file
logfile(base_folder/"logs.log")

# See how many times driver loop is run
count = 0

# Number images for naming
img_count = 1

# Total storage space taken by images, in Bytes
img_size = 0

# Sets comparative value for if an image has too much water/cloud
# A good range is 40-50 / 90-100
water_threshold = 43
cloud_threshold = 100



# ---------------------------------------
# FUNCTIONS
# ---------------------------------------


def light_levels():
    
    """ Checking if the ISS is in sunlight

        so that the pi only takes images where there is enough light to
        extract useful information and therefore save storage

        INPUT: nothing
        RETURN: a boolean, True if there is enough light, False otherwise
    """
    
    curr = timescale.now()
    
    if ISS.at(curr).is_sunlit(ephemeris):
        logger.info("in sun")
        return True
    
    else:
        logger.info("not in sun")
        return False
    
    
def take_image(path):
    
    """ Taking and saving an image       

        INPUT: path to save image
        RETURN: saves image, no return
    """
    
    camera.capture(path)
    logger.info(f"image {path[5:-4]} taken")
    
    
def is_useful(path):
    
    """ Checks to see if the image is over water/clouds

        so that we can delete it to save storage and processing
        because an image largely over water is useless for the task.
        The function takes the average light/darkness value and compares
        it to a known threshold to determine if the image is over water/clouds.

        INPUT: path location for image to check
        RETURN: a boolean, True if it is not over water/clouds, False otherwise
    """
    
    image = cv2.imread(path).astype(np.float)
    nir_val = np.average(image[:, :, 0])
    
    if cloud_threshold > nir_val > water_threshold:
        logger.info("image useful")
        return True
    
    else:
        logger.info("image not useful")
        return False
    
    
def loc_convert(angle):
    
    """ Turn the location coordinates into data which
        can be added to the metadata of the images

        INPUT: raw location data
        RETURN: EXIF-friendly location data
    """
    
    sign, degrees, minutes, seconds = angle.signed_dms()
    exif_angle = f"{degrees:.0f}/1,{minutes:.0f}/1,{seconds*10:.0f}/10"
    
    logger.info("location converted")
    
    return sign < 0, exif_angle


def add_metadata(lat, latr, long, longr):
    
    """ Add the metadata tags to the camera

        so that we know the location and can identify the
        area on a map when we analyse the images on Earth

        INPUT: all EXIF-friendly location data
        RETURN: metadata tags added, nothing returned
    """
    
    global camera
    
    camera.exif_tags["GPS.GPSLatitude"] = lat
    camera.exif_tags["GPS.GPSLatitudeRef"] = latr
    camera.exif_tags["GPS.GPSLongitude"] = long
    camera.exif_tags["GPS.GPSLongitudeRef"] = longr
    
    logger.info("metadata loc added")
    

  

# ---------------------------------------
# DRIVER CODE
# ---------------------------------------


while (now_time < start_time + timedelta(minutes=179)):

    now_time = datetime.now()

    # Keeping under the storage limit with a safe buffer
    if img_size > 2900000000:
        # We are approaching the limit, so the program terminates
      
        logger.error("STORAGE LIMIT EXCEEDED - TERMINATING")      
        break
      

    # Entire program is in a try-except to ensure errors don't break anything
    try:
      
      count += 1
      logger.info(f"running loop count: {count}")
      
      light = light_levels()
      
      if light:
          # There is enough light to take an image
          
          # Get location and add it to the image
          location = ISS.coordinates()
          south, exif_lat = loc_convert(location.latitude)
          west, exif_long = loc_convert(location.longitude)
          add_metadata(exif_lat,
                       "S" if south else "N",
                       exif_long,
                       "W" if west else "E")
          
          
          # Take the image and check for water
          path = f"{base_folder}/imgs/image_{str(img_count).zfill(3)}.jpg"
          take_image(path)
          useful = is_useful(path)
          
          if not(useful):
              # The image is useless
              # Wait some time before trying again
              # The img_count is not updated so that the image is overwritten
              # on the next run through as opposed to wasting time deleting it
              
              sleep(0.5)
              continue
          
          
          # Only run if the image is useful
          img_count += 1
          img_size += os.path.getsize(path)
        
          # How long to wait before taking the next photo - some overlap with previous to map out area
          sleep(10)
          
      else:
          # Wait a small amount of time before trying again
          
          sleep(2)
          continue

  
    except Exception as e:
    
      logger.error(e)
      sleep(1) # To give time for the pi to recover from errors
      img_count += 5 # To negate overwrites and make errors obvious



logger.info("\n------------\nexecution complete :D\n------------")




# END #