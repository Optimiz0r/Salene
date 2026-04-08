# SALENE Vision Deployment Guide

## ✅ What's Built

**Files Created:**
- `vision_module.py` - Reusable vision component (face detection, brightness analysis)
- `salene_with_vision.py` - SALENE agent with vision integration

**Features:**
- Automatically detects faces in frame
- Assesses room lighting (dark/moderate/bright)
- Adds vision context to SALENE's perception
- Gracefully degrades if camera unavailable
- Saves captured frames with timestamps

## 🔧 Camera Permission Fix (Required for Production)

The user `optimizor` is in the `video` group, but the current session doesn't have it.

**Fix:**
```bash
# Option 1: New login session (cleanest)
logout
# Then log back in

# Option 2: Switch group for single command
sg video -c "cd /home/optimizor/neurobit-project && source venv/bin/activate && python3 salene_with_vision.py"

# Option 3: Start new shell with video group
newgrp video
```

**Verify:**
```bash
python3 -c "import cv2; cap = cv2.VideoCapture(0); print('Camera:', 'OK' if cap.isOpened() else 'FAIL')"
```

## 🚀 Running SALENE with Vision

```bash
cd /home/optimizor/neurobit-project
source venv/bin/activate
python3 salene_with_vision.py
```

**Options:**
1. Say hello (captures frame, SALENE responds with what she sees)
2. Run continuous mode (60s of dream cycles with vision checks)
3. Check vision status

## 📁 Architecture

**Vision flow:**
```
User starts SALENE with Vision
         ↓
VisionModule checks camera
         ↓
SALENE interacts → Vision captures frame
         ↓
Face detection + brightness analysis
         ↓
Vision context added to prompt
         ↓
LLM generates response based on what SALENE "sees"
```

## 🎯 Next Steps for New VM Deployment

1. **Install dependencies:**
   ```bash
   pip install opencv-python
   sudo apt-get install -y libgl1  # OpenCV requirement
   ```

2. **Download face detection models:**
   ```bash
   # These should be in /home/optimizor/models/
   # If deploying fresh, download from:
   # https://github.com/opencv/opencv_3rdparty/raw/dnn_samples_face_detector_20170830/
   ```

3. **Set up camera permissions:**
   ```bash
   sudo usermod -a -G video $USER
   # Logout and login for changes
   ```

4. **Test:**
   ```bash
   python3 -c "from vision_module import VisionModule; v = VisionModule(); print(v.check_camera())"
   ```

## 📝 Code Summary

**vision_module.py** (190 lines):
- `VisionModule(device)` - Initialize with camera device (default 0)
- `check_camera()` - Returns (available, message)
- `capture(save_path)` - Captures, analyzes, returns dict with:
  - `success` (bool)
  - `faces` (count)
  - `brightness` (0-255)
  - `context` (description string)
  - `image_path` (where frame saved)

**salene_with_vision.py** (150 lines):
- Extends `ContinuousSalene`
- Overrides `interact()` to capture vision before responding
- Adds vision context to system prompt

---
**Status:** Code ready. Camera permissions need session refresh on production deploy.
