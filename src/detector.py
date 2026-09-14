"""
detector.py

Handles face detection for a single video frame using OpenCV's
pre-trained Haar Cascade classifier. Haar cascades work by scanning
the image at multiple scales for patterns of light/dark regions that
are characteristic of a face (eyes are darker than cheeks, the nose
bridge is lighter than the eye sockets, etc.).

This module is intentionally kept separate from blurring and video
I/O so each concern can be tested and understood independently.
"""

import cv2
import os


class FaceDetector:
    def __init__(self, scale_factor=1.1, min_neighbors=5, min_size=(30, 30)):
        """
        scale_factor : how much the image size is reduced at each scale
                       (smaller = more accurate, slower)
        min_neighbors: how many overlapping detections are required to
                       keep a region as a valid face (higher = fewer
                       false positives, but may miss some real faces)
        min_size     : smallest object size to consider a face (in px)
        """
        cascade_path = os.path.join(
            cv2.data.haarcascades, "haarcascade_frontalface_default.xml"
        )
        self.classifier = cv2.CascadeClassifier(cascade_path)

        if self.classifier.empty():
            raise IOError(f"Could not load cascade file from {cascade_path}")

        self.scale_factor = scale_factor
        self.min_neighbors = min_neighbors
        self.min_size = min_size

    def detect(self, frame):
        """
        Detects faces in a single BGR frame (as read by OpenCV).

        Returns a list of bounding boxes: [(x, y, w, h), ...]
        where (x, y) is the top-left corner and (w, h) is the
        width/height of the detected face region.
        """
        # Haar cascades work on grayscale images, so we convert first.
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Improves detection consistency across varying lighting.
        gray = cv2.equalizeHist(gray)

        faces = self.classifier.detectMultiScale(
            gray,
            scaleFactor=self.scale_factor,
            minNeighbors=self.min_neighbors,
            minSize=self.min_size,
        )

        return faces  # numpy array of [x, y, w, h] rows
