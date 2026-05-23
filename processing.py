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
    
    # cv.imshow("Candidate Image", candidate_area)
    final_img = identify_central_area(candidate_area)

    # cv.imshow("Final Image", final_img)
    # cv.waitKey()
    
    contours, _ = cv.findContours(final_img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        moments = cv.moments(contour)
        if moments["m00"] != 0:
            cx = int(moments["m10"] / moments["m00"])
            cy = int(moments["m01"] / moments["m00"])

    return cx,cy

    # testing for best threshold
    # cv.imshow("original_img", image)
    # cv.imshow("thresholded_img", updated_img)
    # cv.imshow("orig_vessel", vessel_map)
    # cv.imshow("threshold_vessel", updated_vessel)
    # cv.waitKey(0)

# Update it's implementation to get biggest white ares.
def identify_central_area(img1):
    Vset = 255
    label = {}
    count = 1
    # label = cv.imread(imgstr)
    for x in range(1, img1.shape[0] - 1):
        for y in range(1, img1.shape[1] - 1):
            if img1[x][y] == Vset:
                if (
                    img1[x - 1][y] == Vset or
                    img1[x][y - 1] == Vset or
                    img1[x - 1][y - 1] == Vset or
                    img1[x - 1][y + 1] == Vset
                ):
                    label[f"area_{count}"].append([x, y])
                else:
                    count += 1
                    label[f"area_{count}"] = []
                    label[f"area_{count}"].append([x, y])
    # print(label)
    largest = 0
    largest_key = ""
    for key, value in label.items():
        # print(value)
        var = len(value)
        if var > largest:
            largest_key = key
            largest = var
    final_area_img = np.zeros((img1.shape[0], img1.shape[1]), dtype=np.uint8)
    print(label[largest_key])
    for x, y in label[largest_key]:
        final_area_img[x][y] = 255

    return np.uint8(final_area_img)

    
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

    if RESIZE:
        vessel = resize_image(vessel)
        image_rbg = resize_image(image)

    image = image[:,:,2]

    processed_img, processed_vessel = pre_process(image, vessel, resize=RESIZE)

    cx, cy = identify_candidate_area(image=processed_img, vessel_map=vessel)

    cv.drawMarker(
        image_rbg,
        (cx, cy),
        (0, 0, 0),
        markerType=cv.MARKER_CROSS,
        markerSize=10,
        thickness=2,
        line_type=cv.LINE_AA,
    )
    cv.imshow("circled image", image_rbg)
    cv.waitKey()






    
