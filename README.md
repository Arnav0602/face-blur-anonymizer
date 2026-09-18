# Face Blur Anonymizer

**Name:** Arnav Sharma
**Registration Number:** 24BAI10576

A command-line tool that automatically detects and blurs human faces in a video, producing an anonymized copy of the footage. It can process either a video file or a live webcam feed.

## How It Works

1. **Frame capture:** Each frame of the video is read using OpenCV.
2. **Face detection:** The frame is converted to grayscale, and a pre-trained Haar Cascade classifier scans it for regions matching facial patterns.
3. **Temporal smoothing:** A lightweight tracker remembers recently seen face positions for a short grace period, so a face that goes undetected for a frame or two doesn't cause the blur to flicker on and off.
4. **Blurring:** A strong Gaussian blur is applied to each detected (or recently tracked) face region, leaving the rest of the frame untouched.
5. **Output:** The processed frames are written to a new video file.

## Project Structure

```
face-blur-anonymizer/
├── README.md
├── requirements.txt
├── src/
│   ├── detector.py     # Face detection logic (Haar Cascade)
│   ├── tracker.py      # Temporal smoothing to prevent blur flicker
│   ├── blur.py         # Applies Gaussian blur to detected regions
│   └── main.py         # CLI entry point
├── sample_input/       # Place input videos here
└── output/             # Processed videos are saved here
```

## Requirements

- Python 3.8 or higher
- pip

## Setup

1. **Clone the repository**

```bash
   git clone https://github.com/uditraghuvanshi99811/face-blur-anonymizer.git
   cd face-blur-anonymizer
```

2. **Create a virtual environment** (recommended)

```bash
   python3 -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
   pip install -r requirements.txt
```

   This installs:
   - `opencv-python` — video I/O, face detection, and blurring
   - `numpy` — frame array operations

## Usage

### Process a video file

```bash
python src/main.py --input sample_input/your_video.mp4 --output output/result.mp4
```

### Use a webcam as input

```bash
python src/main.py --webcam --output output/webcam_result.mp4
```

When running with `--preview`, press `q` in the preview window to stop early.

### Optional Flags

| Flag              | Description
