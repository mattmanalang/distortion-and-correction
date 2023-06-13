from .interpolation import interpolation
from dip import *
import math

class Distort:
    def __init__(self):
        pass

    def distortion(self, image, k):
        """Applies distortion to the image
                image: input image
                k: distortion Parameter
                return the distorted image"""

        # Initialize output image with the same size as the input image
        distorted_image = zeros(image.shape, uint8)
        
        # Image center is ((number of rows)//2, (number of columns)//2)
        img_center_i_j = array([(image.shape[0]/2), (image.shape[1]/2)])
        img_center_ic_jc = array([0,0], int)

        # Lambdas for calculating
        distance_from_center = lambda pixel: math.sqrt(sum((pixel - img_center_ic_jc)**2))
        change_to_center_coords = lambda coords: coords - img_center_i_j
        change_to_origin_coords = lambda coords: coords + img_center_i_j
        distort = lambda pixel: (pixel / (1 + (k * distance_from_center(pixel))))
        round_off = lambda coord: array([round(coord[0]), round(coord[1])], int)

        # For each pixel...
        for row in range (image.shape[0]):
          for col in range (image.shape[1]):
            # Distortion operations
            curr_pixel_i_j = array([row, col], int)
            curr_pixel_ic_jc = change_to_center_coords(curr_pixel_i_j)
            distorted_icd_jcd = distort(curr_pixel_ic_jc)
            distorted_id_jd = round_off(change_to_origin_coords(distorted_icd_jcd))

            # Copying the pixel value
            distorted_image[distorted_id_jd[0]][distorted_id_jd[1]] = image[row][col]
        return distorted_image

    def correction_naive(self, distorted_image, k):
        """Applies correction to a distorted image by applying the inverse of the distortion function
        image: the input image
        k: distortion parameter
        return the corrected image"""

        # Create naive corrected image with the same size as the input (distorted) image
        corrected_image = zeros(distorted_image.shape, uint8)
        # Image center coordinates
        img_center_i_j = array([(distorted_image.shape[0]/2), (distorted_image.shape[1]/2)])
        img_center_ic_jc = array([0,0], int)

        # Lambdas for calculating
        distance_from_center = lambda pixel: math.sqrt(sum((pixel - img_center_ic_jc)**2))
        change_to_center_coords = lambda coords: coords - img_center_i_j
        change_to_origin_coords = lambda coords: coords + img_center_i_j
        inverse_distortion = lambda pixel: (pixel * (1 + (k * distance_from_center(pixel))))
        round_off = lambda coord: array([round(coord[0]), round(coord[1])], int)

        out_of_x_bounds = lambda coords: True if (coords[0] < 0 or coords[0] >= corrected_image.shape[0]) else False
        out_of_y_bounds = lambda coords: True if (coords[1] < 0 or coords[1] >= corrected_image.shape[1]) else False

        # For each pixel...
        for row in range (distorted_image.shape[0]):
          for col in range (distorted_image.shape[1]):
            # Naive correction operations
            curr_pixel_id_jd = array([row, col], int)
            curr_pixel_icd_jcd = change_to_center_coords(curr_pixel_id_jd)
            correction_ic_jc = inverse_distortion(curr_pixel_icd_jcd)
            correction_i_j = round_off(change_to_origin_coords(correction_ic_jc))

            # Copying the pixel value
            if (out_of_x_bounds(correction_i_j) or out_of_y_bounds(correction_i_j)):
              continue

            corrected_image[correction_i_j[0]][correction_i_j[1]] = distorted_image[row][col]
        return corrected_image

    def correction(self, distorted_image, k, interpolation_type):
        """Applies correction to a distorted image and performs interpolation
                image: the input image
                k: distortion parameter
                interpolation_type: type of interpolation to use (nearest_neighbor, bilinear)
                return the corrected image"""
        

        # Create corrected output image with the same dims as the input (distorted) image
        corrected_image = zeros(distorted_image.shape, uint8)
        img_center_i_j = array([corrected_image.shape[0]/2, corrected_image.shape[1]/2])
        img_center_ic_jc = array([0,0], int)

        # Lambda Calculations
        distance_from_center = lambda coords: math.sqrt(sum((coords - img_center_ic_jc)**2))
        change_to_center_coords = lambda coords: coords - img_center_i_j
        change_to_origin_coords = lambda coords: coords + img_center_i_j
        distort = lambda pixel: pixel / (1 + (k * distance_from_center(pixel)))
        round_off = lambda coord: array([round(coord[0]), round(coord[1])], int)
        get_intensities = lambda pixel: distorted_image[pixel[0]][pixel[1]]


        # Using the specified correction type
        """If nearest_neighbor, linear, bilinear, then [...]"""
        for row in range (corrected_image.shape[0]):
          for col in range (corrected_image.shape[1]):
            pixel_i_j = array([row, col], int)
            pixel_ic_jc = change_to_center_coords(pixel_i_j)
            pixel_icd_jcd = distort(pixel_ic_jc)
            pixel_id_jd = change_to_origin_coords(pixel_icd_jcd)

            if (interpolation_type == "bilinear"):
              interpolater = interpolation()
              # Find the four nearest neighbors
              # Point = (i, j)
              NW_point = (math.floor(pixel_id_jd[0]), math.ceil(pixel_id_jd[1]))
              I_NW = get_intensities(NW_point)
              NE_point = (math.ceil(pixel_id_jd[0]), math.ceil(pixel_id_jd[1]))
              I_NE = get_intensities(NE_point)
              SW_point = (math.floor(pixel_id_jd[0]), math.floor(pixel_id_jd[1]))
              I_SW = get_intensities(SW_point)
              SE_point = (math.ceil(pixel_id_jd[0]), math.floor(pixel_id_jd[1]))
              I_SE = get_intensities(SE_point)

              # Copy the pixel value
              corrected_image[row][col] = interpolater.bilinear_interpolation(pixel_id_jd, NW_point, I_NW, NE_point, I_NE, SW_point, I_SW, SE_point, I_SE)
              
            else: # interpolation_type == "nearest_neighbor"
              pixel_inn_jnn = round_off(pixel_id_jd)
              # Copy the pixel value
              corrected_image[row][col] = distorted_image[pixel_inn_jnn[0]][pixel_inn_jnn[1]]
            
        return corrected_image
