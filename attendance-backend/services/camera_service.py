"""
Real Camera Service for Face Capture
Uses OpenCV and MediaPipe Face Mesh for accurate detection
"""

import cv2
import mediapipe as mp
import numpy as np
from typing import Optional, Callable, List
from datetime import datetime

class CameraService:
    """
    Real-time camera face capture service
    Uses MediaPipe Face Mesh for robust face detection
    """
    
    def __init__(self, camera_id: Optional[str] = None):
        self.camera_id = camera_id or f"camera_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.is_running = False
        self.frame_callback: Optional[Callable[[np.ndarray], None]] = None
        
        # Initialize MediaPipe
        mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = mp_face_mesh.FaceMesh(
            max_num_faces=1,
            min_detection_confidence=0.9,
            min_tracking_confidence=0.8
        )
    
    def capture_frame(self) -> Optional[np.ndarray]:
        """
        Capture a frame with detected face
        Returns: numpy array with face cropped
        """
        camera = cv2.VideoCapture(0)  # Default webcam
        if not camera.isOpened():
            camera = cv2.VideoCapture(1)  # Try second camera
        
        ret, frame = camera.read()
        camera.release()
        
        if not ret:
            return None
        
        return frame
    
    def process_frame(self, frame: np.ndarray) -> Optional[np.ndarray]:
        """
        Process frame for face detection and extraction
        Returns: cropped face image with known hash
        """
        try:
            results = self.face_mesh.process(frame)
            
            if results.multi_face_landmarks:
                # Get the first detected face
                landmarks = results.multi_face_landmarks[0]
                
                # Crop face region (approximate)
                y_min = 0
                y_max = frame.shape[0]
                x_min = 0
                x_max = frame.shape[1]
                
                # Use face landmarks for better cropping
                face_landmarks = landmarks
                x, y, w, h = self._estimate_face_bbox(face_landmarks)
                
                face_crop = frame[y:y+h, x:x+w]
                
                # Resize to model input size
                face_crop = cv2.resize(face_crop, (128, 128))
                
                return face_crop.astype(np.uint8)
        
        except Exception as e:
            print(f"Error processing frame: {e}")
            return None
    
    def _estimate_face_bbox(self, landmarks) -> tuple:
        """Estimate face bounding box from landmarks"""
        x_coords = [landmarks.x[i] for i in range(468)]
        y_coords = [landmarks.y[i] for i in range(468)]
        
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)
        
        return int(x_min * 256), int(y_min * 256), int(x_max * 256), int(y_max * 256)
    
    def start_capture(self, callback: Optional[Callable[[np.ndarray], None]] = None):
        """Start continuous capture loop"""
        self.frame_callback = callback
        
        print(f"Camera service started: {self.camera_id}")
        
        loop = True
        while loop:
            frame = self.capture_frame()
            if frame is None:
                continue
            
            face_crop = self.process_frame(frame)
            if face_crop is None:
                continue
            
            # Call callback with cropped face
            if callback:
                callback(face_crop)
            
            # Process for 1 second
            self._process_single_frame()
    
    def stop_capture(self):
        """Stop continuous capture"""
        if not self.is_running:
            return
        print("Camera service stopped")
        self.is_running = False
    
    def _process_single_frame(self):
        """Process single frame for model inference"""
        frame = self.capture_frame()
        if frame is None:
            return
        
        face_crop = self.process_frame(frame)
        if face_crop is None:
            return
        
        # Pass to model service
        try:
            from models.siamoneonnx import SiameseONNXModel
            model = SiameseONNXModel()
            embedding = model.extract_embedding(face_crop)
            confidence = model.predict(face_crop)
            print(f"Face detected, embedding: {embedding.shape}, confidence: {confidence:.2f}")
        except Exception as e:
            print(f"Model inference failed: {e}")
    
    def is_running(self):
        """Check if capture is running"""
        return self.is_running
