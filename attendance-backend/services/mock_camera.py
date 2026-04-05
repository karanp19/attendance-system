"""
Mock Camera Service for testing
Simulates real-time video face capture
"""

import time
import numpy as np
from PIL import Image, ImageGrab
from uuid import uuid4
from datetime import datetime

class MockCameraService:
    """
    Simulates camera face capture for testing
    Generates synthetic images with known faces
    """
    
    def __init__(self, mock_enabled: bool = True):
        self.mock_enabled = mock_enabled
        self.camera_id = f"mock_{uuid4().hex[:8]}"
    
    def capture_frame(self) -> np.ndarray:
        """
        Capture a frame (mock mode)
        Returns: numpy array with face image
        """
        if not self.mock_enabled:
            raise Exception("Camera service disabled")
        
        # Generate synthetic grayscale image
        image_size = 128
        image = np.random.randint(50, 200, size=(image_size, image_size), dtype=np.uint8)
        
        # Add a "face" region
        face_size = 64
        y, x = image_size // 2 - face_size // 2, image_size // 2 - face_size // 2
        image[y:y+face_size, x:x+face_size] = 150
        
        return image
    
    def start_capture(self, frame_callback=None, stop_callback=None):
        """Start continuous capture loop"""
        if not self.mock_enabled:
            return
        
        print(f"Mock camera started: {self.camera_id}")
        
        loop = True
        frame_count = 0
        
        while loop:
            frame = self.capture_frame()
            
            if frame_callback:
                frame_callback(frame)
            
            if stop_callback and stop_callback():
                loop = False
            
            frame_count += 1
            time.sleep(0.5)  # 2fps mock capture
        
        if stop_callback:
            print("Mock camera stopped")
    
    def stop_capture(self):
        """Stop continuous capture"""
        if not self.mock_enabled:
            return
        print("Mock camera stopped")
    
    def is_running(self):
        """Check if capture is running"""
        return self.mock_enabled
