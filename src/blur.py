"""
blur.py

Applies a strong Gaussian blur to specific regions of a frame
(the regions where faces were detected), leaving the rest of the
frame untouched.
"""

import cv2


def blur_regions(frame, boxes, blur_strength=99):
    """
    frame        : the original BGR frame (numpy array)
    boxes        : list of (x, y, w, h) bounding boxes to blur
    blur_strength: kernel size for Gaussian blur. Must be odd.
                   Larger = more heavily blurred/anonymized.

    Returns a new frame with the specified regions blurred.
    """
    # Kernel size must be odd and positive.
    if blur_strength % 2 == 0:
        blur_strength += 1

    output = frame.copy()

    for (x, y, w, h) in boxes:
        # Clip coordinates so we never index outside the frame,
        # which can happen near the edges of the image.
        x1, y1 = max(x, 0), max(y, 0)
        x2, y2 = min(x + w, frame.shape[1]), min(y + h, frame.shape[0])

        region = output[y1:y2, x1:x2]
        if region.size == 0:
            continue

        blurred_region = cv2.GaussianBlur(region, (blur_strength, blur_strength), 0)
        output[y1:y2, x1:x2] = blurred_region

    return output
