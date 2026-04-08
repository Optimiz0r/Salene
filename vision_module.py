#!/usr/bin/env python3
"""
Simple Vision Module for SALENE
Captures frames, detects faces, provides context.
"""
import cv2
import numpy as np
from pathlib import Path
from datetime import datetime

# Model paths
MODEL_PATH = "/home/optimizor/models/face_detector.caffemodel"
CONFIG_PATH = "/home/optimizor/models/face_detector.prototxt"

class VisionModule:
    """Simple vision for SALENE - captures and analyzes camera frames"""
    
    def __init__(self, device: int = 0):
        self.device = device
        self.face_net = None
        self._load_face_detector()
        
    def _load_face_detector(self):
        """Load DNN face detector"""
        if Path(MODEL_PATH).exists() and Path(CONFIG_PATH).exists():
            try:
                self.face_net = cv2.dnn.readNetFromCaffe(CONFIG_PATH, MODEL_PATH)
                print("✅ Face detector loaded")
            except Exception as e:
                print(f"⚠️  Face detector failed: {e}")
                self.face_net = None
        else:
            print("⚠️  Face detector models not found")
    
    def check_camera(self) -> tuple:
        """Check if camera is available"""
        cap = cv2.VideoCapture(self.device)
        available = cap.isOpened()
        if available:
            ret, _ = cap.read()
            cap.release()
            return available, "Camera accessible"
        cap.release()
        return False, "Camera not available"
    
    def capture(self, save_path: str = None) -> dict:
        """
        Capture frame and analyze.
        
        Returns:
            dict with success, faces count, context, image_path
        """
        cap = cv2.VideoCapture(self.device)
        if not cap.isOpened():
            return {
                'success': False,
                'error': 'Cannot open camera',
                'faces': 0,
                'context': 'No camera available.',
                'image_path': None
            }
        
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            return {
                'success': False,
                'error': 'Cannot capture frame',
                'faces': 0,
                'context': 'Camera opened but frame capture failed.',
                'image_path': None
            }
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Default save path
        if save_path is None:
            save_path = f"/tmp/salene_vision_{timestamp}.jpg"
        
        # Analyze
        faces = self._detect_faces(frame)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        brightness = np.mean(gray)
        
        # Draw boxes on frame
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # Save annotated frame
        cv2.imwrite(save_path, frame)
        
        # Build context
        num_faces = len(faces)
        context_parts = [f"I see {num_faces} face(s)."]
        
        if brightness < 40:
            context_parts.append("The room is quite dark.")
        elif brightness < 80:
            context_parts.append("The lighting is moderate.")
        else:
            context_parts.append("The room is well lit.")
        
        if num_faces > 0:
            context_parts.append(f"Detected {num_faces} person(s) in frame.")
        
        return {
            'success': True,
            'faces': num_faces,
            'brightness': float(brightness),
            'context': " ".join(context_parts),
            'image_path': save_path,
            'timestamp': timestamp
        }
    
    def _detect_faces(self, frame: np.ndarray) -> list:
        """Detect faces in frame using DNN"""
        if self.face_net is None:
            return []
        
        h, w = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
                                    (300, 300), (104.0, 177.0, 123.0))
        self.face_net.setInput(blob)
        detections = self.face_net.forward()
        
        faces = []
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                faces.append((startX, startY, endX-startX, endY-startY))
        
        return faces


# Simple test
if __name__ == "__main__":
    import sys
    print("🔍 Testing SALENE Vision Module...")
    
    vision = VisionModule()
    available, msg = vision.check_camera()
    
    if not available:
        print(f"❌ {msg}")
        print("\nCamera may need:")
        print("  - USB passthrough (VM)")
        print("  - Video group membership: sudo usermod -a -G video $USER")
        print("  - Logout/login for group changes")
        sys.exit(1)
    
    print(f"✅ {msg}")
    print("\n📸 Capturing frame...")
    
    result = vision.capture()
    
    if result['success']:
        print(f"✅ Capture successful!")
        print(f"   Faces: {result['faces']}")
        print(f"   Brightness: {result['brightness']:.1f}")
        print(f"   Context: {result['context']}")
        print(f"   Saved to: {result['image_path']}")
    else:
        print(f"❌ Capture failed: {result['error']}")
