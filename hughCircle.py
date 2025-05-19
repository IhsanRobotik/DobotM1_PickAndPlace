import sys
import cv2 as cv
import numpy as np

def on_trackbar_change(val):
    pass  # Callback function for trackbar (does nothing)

def main(argv):
    default_file = '20250511_124939.jpg'
    filename = argv[0] if len(argv) > 0 else default_file
    # Loads an image
    src = cv.imread(cv.samples.findFile(filename), cv.IMREAD_COLOR)
    # Check if image is loaded fine
    if src is None:
        print('Error opening image!')
        print('Usage: hough_circle.py [image_name -- default ' + default_file + '] \n')
        return -1

    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    gray = cv.medianBlur(gray, 5)

    # Create a window
    cv.namedWindow("detected circles", cv.WINDOW_NORMAL)

    # Create trackbars for parameters
    cv.createTrackbar("param1", "detected circles", 100, 200, on_trackbar_change)
    cv.createTrackbar("param2", "detected circles", 30, 100, on_trackbar_change)
    cv.createTrackbar("minRadius", "detected circles", 30, 100, on_trackbar_change)
    cv.createTrackbar("maxRadius", "detected circles", 200, 300, on_trackbar_change)

    while True:
        # Get current positions of trackbars
        param1 = cv.getTrackbarPos("param1", "detected circles")
        param2 = cv.getTrackbarPos("param2", "detected circles")
        minRadius = cv.getTrackbarPos("minRadius", "detected circles")
        maxRadius = cv.getTrackbarPos("maxRadius", "detected circles")

        # Detect circles
        rows = gray.shape[0]
        circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, rows / 8,
                                   param1=param1, param2=param2,
                                   minRadius=minRadius, maxRadius=maxRadius)

        # Copy the original image to draw circles
        display = src.copy()

        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                center = (i[0], i[1])
                # circle center
                cv.circle(display, center, 1, (0, 100, 100), 3)
                # circle outline
                radius = i[2]
                cv.circle(display, center, radius, (255, 0, 255), 3)

        # Show the image with detected circles
        cv.imshow("detected circles", display)

        # Break the loop if 'q' is pressed
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cv.destroyAllWindows()
    return 0

if __name__ == "__main__":
    main(sys.argv[1:])