"""
Camera Streaming Module
This module provides a generator for live webcam streaming.
It is designed to be consumed by a Streamlit loop to display real-time video.
"""

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    cv2 = None

import time
import sys
from typing import Generator, Optional
import numpy as np

def camera_stream() -> Generator[Optional[np.ndarray], None, None]:
    """
    Generator that yields frames from the webcam.
    
    Yields:
        np.ndarray: RGB frame from the webcam.
    
    Usage:
        for frame in camera_stream():
            if frame is not None:
                st.image(frame)
    """
    # Check if OpenCV is available
    if not CV2_AVAILABLE:
        print("Error: OpenCV (cv2) is not available.")
        yield None
        return
    
    camera = None
    
    try:
        # Try different camera backends for Windows compatibility
        if sys.platform == 'win32':
            # Try DirectShow backend first for better Windows compatibility
            camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            if not camera.isOpened():
                print("DirectShow failed, trying default backend...")
                camera = cv2.VideoCapture(0)
        else:
            camera = cv2.VideoCapture(0)
        
        if not camera.isOpened():
            print("Error: Could not access webcam. Please check:")
            print("  1. Camera is connected and not in use by another app")
            print("  2. Camera permissions are granted")
            print("  3. Camera drivers are installed")
            yield None
            return

        # Set generic resolution
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Set buffer size to reduce latency
        camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        
        # Warm up the camera (read a few frames to stabilize)
        for _ in range(5):
            camera.read()
        
        print("Camera initialized successfully")
        
        # Stream loop
        while True:
            success, frame = camera.read()
            
            if not success or frame is None:
                print("Failed to read frame.")
                # Try to recover
                time.sleep(0.1)
                continue
                
            # Convert BGR (OpenCV default) to RGB (Streamlit requirement)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Yield the frame to the consumer
            yield rgb_frame
            
            # Minimal sleep to control frame rate
            time.sleep(0.01)

    except Exception as e:
        print(f"Stream error: {e}")
        import traceback
        traceback.print_exc()
        yield None

    finally:
        # Cleanup
        if camera is not None:
            camera.release()
            print("Camera resource released.")
