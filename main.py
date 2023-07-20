import cv2
import numpy as np

img = cv2.imread('output.png')

height, width, c = img.shape

i = 0

while True:
    i += 1

    # divided the image into left and right part
    # like list concatenation we concatenated
    # right and left together
    l = img[:, :(i % width)]
    r = img[:, (i % width):]

    img1 = np.hstack((r, l))

    # this function will concatenate
    # the two matrices
    cv2.imshow('output', img1)

    if cv2.waitKey(2) == ord('q'):
        # press q to terminate the loop
        cv2.destroyAllWindows()
        break