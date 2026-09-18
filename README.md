# Face Blur Anonymizer

Name: Arnav Sharma 
Reg Number: 24BAI10576

A command-line tool that automatically detects and blurs human faces
in a video, producing an anonymized copy of the footage. It can
process a video file or a live webcam feed.

## How It Works

1.Each frame of the video is read using OpenCV.
2.A pre-trained Haar Cascade classifier scans the frame (converted to grayscale) for regions matching facial patterns.
3.A temporal smoothing step ("tracker") remembers recently-seen face positions for a short grace period, so a face that briefly fails to be detected on one or two frames doesn't cause the blur to flicker on and off.
4.A strong Gaussian blur is applied to each detected (or recently tracked) face region, while the rest of the frame is left untouched.
5.The processed frames are written to a new output video file.

## Project Structure

```
face-blur-anonymizer/
├── README.md
├── requirements.txt
├── src/
│   ├── detector.py    # Face detection logic (Haar Cascade)
│   ├── tracker.py      # Temporal smoothing to prevent blur flicker
│   ├── blur.py         # Applies Gaussian blur to detected regions
│   └── main.py         # CLI entry point
├── sample_input/       # Place input videos here
└── output/             # Processed videos are saved here
```

## Requirements

- Python 3.8 or higher
- pip

## Setup Instructions

1. **Clone the repository**

   ```bash
   git clone https://github.com/<uditraghuvanshi99811>/<face-blur-anonymizer>.git
   cd <face-blur-anonymizer>
   ```

2. **(Recommended) Create a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   This installs:
   - `opencv-python` — used for video I/O, face detection, and blurring
   - `numpy` — used for frame array operations

## Usage

### Process a video file

```bash
python src/main.py --input sample_input/your_video.mp4 --output output/result.mp4
```

### Use your webcam as input

```bash
python src/main.py --webcam --output output/webcam_result.mp4
```

Press `q` to stop early if you're using `--preview` (see below).

### Optional flags

| Flag              | Description                                                        | Default |
|-------------------|----------------------------------------------------------------------|---------|
| `--blur-strength` | Gaussian blur kernel size (higher = more blurred). Must be odd.    | 99      |
| `--min-neighbors` | Higher values reduce false-positive detections.                    | 5       |
| `--grace-period`  | Frames to keep blurring a face after detection briefly misses it (prevents flicker). | 8 |
| `--no-smoothing`  | Disable temporal smoothing and use raw per-frame detections.        | off     |
| `--preview`       | Show a live preview window while processing (requires a display).  | off     |

Example with custom settings:

```bash
python src/main.py --input sample_input/your_video.mp4 --output output/result.mp4 --blur-strength 55 --min-neighbors 6
```

## Output

The tool prints a summary after processing:

```
Frames processed : 150
Total faces found: 142
Time elapsed     : 4.32 seconds
Output saved to  : output/result.mp4
```

The processed video is saved at the path given by `--output`.

## Notes & Limitations

Detection uses OpenCV's built-in haarcascade_frontalface_default.xml classifier, which works best on faces that are reasonably front-facing and well-lit. Extreme angles, heavy occlusion, or poor lighting can reduce detection accuracy.
--preview requires a graphical display and will not work in a headless terminal/server environment — omit it for pure CLI use.
The tool does not require internet access; the Haar Cascade file ships with the opencv-python package.
## License

This project was built for academic coursework submission.
