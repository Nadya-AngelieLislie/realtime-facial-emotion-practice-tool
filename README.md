# Real-Time Facial Emotion Practice Tool

> A webcam app that scores how well you act out a chosen emotion.

## Overview

- Solo desktop app that helps users practice facial expressions on cue, like a mirror that scores your acting.

## Data / Scope

- Live webcam frames analysed by a pre-trained facial-emotion-recognition model (FER library), predicting emotions such as happy, sad, angry and surprised.

## Workflow

- OpenCV captures webcam frames in real time and feeds them to the emotion model.
- Majority voting over recent frames smooths noisy predictions and reduces flicker.
- Tkinter GUI lets users pick a target emotion and see live feedback.

## Results

- Post-session gallery shows moments where the detected emotion missed the target.
- Screenshots and logs of mismatched attempts are saved automatically for review.
- A complete feedback loop, not just a bare model demo.

## Tech Stack

Python, OpenCV, FER library, Tkinter

## Repository Structure

```
latihan_untuk_aktor.py   Desktop app: webcam capture, FER emotion detection, Tkinter UI
requirements.txt
```

## How to Run

```bash
pip install -r requirements.txt
python latihan_untuk_aktor.py
```
Needs a webcam. Tkinter ships with the standard Python installer.

## Team

Individual project.

## Notes

- Mismatch screenshots are saved locally during a session and are git-ignored.

## Author

Nadya Angelie Lislie, BINUS University (Computer Science and Statistics). [LinkedIn](https://www.linkedin.com/in/nadya-angelie-lislie/) | [GitHub](https://github.com/Nadya-AngelieLislie)

## Continuous Integration

GitHub Actions (`.github/workflows/ci.yml`) runs `ruff` and `pytest` repository-health checks on every push; run them locally with `make lint test`.
