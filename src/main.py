import argparse
import sys
import time

import cv2

from detector import FaceDetector
from blur import blur_regions
from tracker import FaceTracker


def parse_args():
    parser = argparse.ArgumentParser(
        description="Detect and blur faces in a video for anonymization."
    )
    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument(
        "--input", type=str, help="Path to an input video file."
    )
    source_group.add_argument(
        "--webcam", action="store_true", help="Use the default webcam as input."
    )

    parser.add_argument(
        "--output", type=str, required=True, help="Path to save the output video."
    )
    parser.add_argument(
        "--blur-strength",
        type=int,
        default=99,
        help="Gaussian blur kernel size (odd number). Default: 99.",
    )
    parser.add_argument(
        "--min-neighbors",
        type=int,
        default=5,
        help="Higher values reduce false positives. Default: 5.",
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Show a live preview window while processing (requires a display).",
    )
    parser.add_argument(
        "--grace-period",
        type=int,
        default=8,
        help="Frames to keep blurring a face after detection briefly "
        "misses it, to prevent flicker. Default: 8.",
    )
    parser.add_argument(
        "--no-smoothing",
        action="store_true",
        help="Disable temporal smoothing and use raw per-frame detections.",
    )

    return parser.parse_args()


def get_video_source(args):
    if args.webcam:
        return cv2.VideoCapture(0)
    return cv2.VideoCapture(args.input)


def main():
    args = parse_args()

    cap = get_video_source(args)
    if not cap.isOpened():
        print("Error: could not open video source.", file=sys.stderr)
        sys.exit(1)

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(args.output, fourcc, fps, (width, height))

    detector = FaceDetector(min_neighbors=args.min_neighbors)
    tracker = None if args.no_smoothing else FaceTracker(grace_period=args.grace_period)

    frame_count = 0
    faces_detected_total = 0
    start_time = time.time()

    print(f"Processing video... (source: {'webcam' if args.webcam else args.input})")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        raw_boxes = detector.detect(frame)
        faces_detected_total += len(raw_boxes)

        boxes_to_blur = tracker.update(raw_boxes) if tracker else raw_boxes

        processed_frame = blur_regions(frame, boxes_to_blur, blur_strength=args.blur_strength)

        writer.write(processed_frame)

        if args.preview:
            cv2.imshow("Face Blur Anonymizer - Preview", processed_frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                print("Preview interrupted by user.")
                break

        frame_count += 1
        if frame_count % 30 == 0:
            print(f"  Processed {frame_count} frames...")

    elapsed = time.time() - start_time

    cap.release()
    writer.release()
    if args.preview:
        cv2.destroyAllWindows()

    print("\nDone.")
    print(f"Frames processed : {frame_count}")
    print(f"Total faces found: {faces_detected_total}")
    print(f"Time elapsed     : {elapsed:.2f} seconds")
    print(f"Output saved to  : {args.output}")


if __name__ == "__main__":
    main()