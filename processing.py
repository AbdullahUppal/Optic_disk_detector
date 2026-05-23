import cv2 as cv
import numpy as np

def pre_process(image, vessel, resize=None):
   
    if resize:
        image = resize_image(image)
        vessel = resize_image(vessel)

    equalized_img = cv.equalizeHist(image)
    equalized_vessel = cv.equalizeHist(vessel)

    return equalized_img, equalized_vessel

def resize_image(image):
    width ,height = image.shape[:2]

    new_width = 600
    new_height = int(height * (new_width / width))

    resized_img = cv.resize(image, (new_width, new_height), interpolation=cv.INTER_AREA)

    return resized_img

def identify_candidate_area(image, vessel_map):
    
    _, updated_img = cv.threshold(image, 245, 255, type=cv.THRESH_BINARY)
    _, updated_vessel = cv.threshold(vessel_map, 80, 255, type=cv.THRESH_BINARY)

    candidate_area = cv.bitwise_and(updated_img, updated_vessel)
    cv.imshow("canddate_region", candidate_area)
    cv.waitKey()

    # testing for best threshold
    # cv.imshow("original_img", image)
    # cv.imshow("thresholded_img", updated_img)
    # cv.imshow("orig_vessel", vessel_map)
    # cv.imshow("threshold_vessel", updated_vessel)
    # cv.waitKey(0)

# Update it's implementation to get biggest white ares.
    def ccaf(imgstr, Vset, value):
        img1 = cv.imread(imgstr, 0)
        label = np.zeros((img1.shape[0], img1.shape[1], 3), dtype='int')
        # label = cv.imread(imgstr)
        for x in range(0, img1.shape[0]-1):
            for y in range(0, img1.shape[1]-1):
                if img1[x][y] in Vset:
                    if img1[x-1][y] in Vset or img1[x][y-1] in Vset:
                        label[x][y] = value
                    else:
                        label[x][y] = value
        return np.uint8(label)
    
if __name__ == "__main__":

    RESIZE = 1

    vessel = cv.imread("Blood vessels/1ffa92e4-8d87-11e8-9daf-6045cb817f5b._bin_seg.png", cv.IMREAD_GRAYSCALE)

    image = cv.imread("Fundus image/01ffa92e4-8d87-11e8-9daf-6045cb817f5b..JPG")

    # best possible channel for further processing 
    # cv.imshow("Image",image)
    # cv.imshow("ImageC1", image[:,:,0])
    # cv.imshow("ImageC2", image[:,:,1])
    # cv.imshow("ImageC3",image[:,:,2])
    # cv.waitKey(0)
    # cv.destroyAllWindows()
    image = image[:,:,2]

    if RESIZE:
        vessel = resize_image(vessel)

    processed_img, processed_vessel = pre_process(image, vessel, resize=RESIZE)

    identify_candidate_area(image=processed_img, vessel_map=vessel)





    
