import cv2 as cv

def pre_process(image, resize=None):
   
    if resize:
        image = resize_image(image)

    equalized_img = cv.equalizeHist(image)

    return equalized_img

def resize_image(image):
    width ,height = image.shape[:2]

    new_width = 600
    new_height = int(height * (new_width / width))

    resized_img = cv.resize(image, (new_width, new_height), interpolation=cv.INTER_AREA)

    return resized_img

def identify_candidate_area(image, vessel_map):
    
    ret, updated_img = cv.threshold(image, 255, type=cv.THRESH_OTSU)
    cv.imshow("thresholded_img", updated_img)
    cv.waitKey(0)

if __name__ == "__main__":

    RESIZE = 0

    image = cv.imread("C:/Users/au001/Documents/Projects\ML DIP/optic_disk_detector/Fundus image/01ffa92e4-8d87-11e8-9daf-6045cb817f5b..JPG")

    vessel = cv.imread("C:/Users/au001/Documents/Projects\ML DIP/optic_disk_detector/Blood vessels/1ffa92e4-8d87-11e8-9daf-6045cb817f5b._bin_seg.png")

    if RESIZE:
        vessel = resize_image(vessel)

    processed_img = pre_process(image, resize=RESIZE)

    identify_candidate_area(image=processed_img, vessel_map=vessel)





    
