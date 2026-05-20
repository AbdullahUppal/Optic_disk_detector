import cv2 as cv
import numpy as np
import os

def extract_optic_disc(fundusloc, vesseloc):
    fundus_image = cv.imread("Fundus image/" + fundusloc, 0)
    vessel_map = cv.imread("Blood vessels/" + vesseloc, 0)

    # Step 2: Bright Region Extraction
    fundus_image = cv.resize(fundus_image,(500, 500))
    # cv.imshow("fundimg", fundus_image)
    vessel_map = cv.resize(vessel_map,(500,500))

    # cv.imshow("vessimg",vessel_map)
    # cv.waitKey()
    equalized_image = cv.equalizeHist(fundus_image)
    # cv.imshow("eqimg", equalized_image)
    # cv.waitKey()
    # Step 3: Candidate Region Identification
    # Simple thresholding (replace 127 with a suitable value)
    ret, thresh = cv.threshold(equalized_image, 245, 255, cv.THRESH_BINARY)
    # cv.imshow("threhhold", thresh)
    # cv.waitKey()
    # Step 4: Refining Optic Disc Candidate
    # Morphological opening with small kernel (replace 3 with a suitable size)
    kernel = np.ones((7, 7), np.uint8)
    opened_image = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel)
    # cv.imshow("openedimg",opened_image)
    # cv.waitKey()
    # Blood vessel map integration
    candidate_regions = cv.bitwise_and(opened_image, vessel_map)
    # cv.imshow("candidate", candidate_regions)
    # cv.waitKey()

    # min_val, max_val, min_loc, max_loc = cv.minMaxLoc(candidate_regions)
    # print(min_loc,min_val,max_val,max_loc)
    # Draw a circle around the brightest pixel location (potentially the optic disc)
    resized_image = cv.resize(cv.imread("Fundus image/" + fundusloc),(500, 500))
    contours, _ = cv.findContours(candidate_regions, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        moments = cv.moments(contour)
        if moments["m00"] != 0:
            cx = int(moments["m10"] / moments["m00"])
            cy = int(moments["m01"] / moments["m00"])

            # Get intensity value at centroid location
            # intensity = resized_image[cy, cx]  # Assuming 'grayscale_image' is your original image
            # print("intensity: ", intensity)
            # if np.any(intensity > 252):
                # print(f"Filtered Bright Region Centroid: ({cx}, {cy})")


    circle_radius = 50  # Adjust the radius of the circle as needed
    cv.circle(resized_image, (cx, cy), circle_radius, (255, 0, 0), 2)
    # cv.imshow("circled image", resized_image)
    # cv.waitKey()
    return resized_image


fundus = os.listdir("Fundus image/")
vessel = os.listdir("Blood vessels/")

# Example usage (assuming you have loaded fundus_image and vessel_map)
for x in range(0,len(fundus)):
    print(fundus[x])
    print(vessel[x])
    output = extract_optic_disc(fundus[x], vessel[x])
    cv.imshow("Output/"+fundus[x],output)
    cv.imwrite("Output/"+fundus[x], output)
cv.waitKey()