import cv2
import numpy as np
import math 

import Shared

def detect_package():

      current_pos = Shared.data.current_pos
      frame = np.copy(Shared.data.frame)

      text = "Detecting Package"
      cv2.putText(frame, text, (300, 50), cv2.FONT_HERSHEY_SIMPLEX,
          1, (0, 255, 0), 2)

      hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

      # HSV range for red box
      lower_red = np.array([114, 90, 100])
      upper_red = np.array([180, 255, 255])

      # only find pixels in image which fall into specified colour range
      maskhsv = cv2.inRange(hsv, lower_red, upper_red)
      # Gaussian to remove noisy region
      mask = cv2.medianBlur(maskhsv, 5)
      # Connect pixels
      kernel = np.ones((5, 5), np.uint8)
      mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
      maskBGR = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
      # 8-way pixel connectivity - centre pixel connected to its 8 neighbours
      connectivity = 8
      # Finds all connected pixels within binary maskhsv image
      output = cv2.connectedComponentsWithStats(mask, connectivity, cv2.CV_8U)
      # number of blobs in image seen with required colour
      num_labels = output[0]
      # Labels of blobs
      labels = output[1]
      # The location and size of bounding box of blobs
      stats = output[2]
      # The centroid of each bounding box
      centroids = output[3]
      max_area = 0
      index = -1
      max_centroid = [-1,-1]

      # Find the maximum blob in image
      for i in range(1, num_labels):
          statarea = stats[i, cv2.CC_STAT_AREA]
          if statarea > max_area:
              max_area = statarea
              index = i

      if index > -1:
          # Mask out everything outside box which bounds blob
          x_left = stats[index, cv2.CC_STAT_LEFT]
          y_top = stats[index, cv2.CC_STAT_TOP]
          width = stats[index, cv2.CC_STAT_WIDTH]
          height = stats[index, cv2.CC_STAT_HEIGHT]
          statarea = stats[index, cv2.CC_STAT_AREA]
          centroid = centroids[index]
          ROI = mask[y_top:y_top+height,x_left:x_left+width]
          mask = np.zeros_like(mask)
          mask[y_top:y_top+height,x_left:x_left+width] = ROI

          # Find bounding shape around collection of pixels.
          cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
          cont_sorted = sorted(cnts[0], key=lambda z: cv2.contourArea(z), reverse=True)
          peri = cv2.arcLength(cont_sorted[0], True)
          approx = cv2.approxPolyDP(cont_sorted[0], 0.04 * peri, True)
          area = cv2.contourArea(approx)

          alt = current_pos[2]
          box_area_small = get_size(0.15, 0.155, alt)
          box_area_large = get_size(0.21, 0.270, alt)
          if area > 0.5 * box_area_small and area < 1.8 * box_area_large:
              # Draw polygon around blob
              cv2.drawContours(maskBGR, [approx], -1, (0, 0, 255), 3)
              # Only send pixel centroid if area of blob is the right size
              max_centroid = centroid

      Shared.data.pixel_pos[0] = max_centroid[0]
      Shared.data.pixel_pos[1] = max_centroid[1]

      Shared.data.frame_image_recognition = frame

      return

def get_size(sidea, sideb, height):
    height = abs(height)
    if height < 0.3:
        return Shared.data.video_height * Shared.data.video_width
    else:
        img_v = 2 * height * math.tan(Shared.data.FOVV / 2)
        side_pixela = sidea * Shared.data.video_height / img_v
        side_pixelb = sideb * Shared.data.video_height / img_v
        return side_pixela * side_pixelb
