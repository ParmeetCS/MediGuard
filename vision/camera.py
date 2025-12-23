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
    camera = None
    
    try:
        # Open default webcam
        camera = cv2.VideoCapture(0)
        
        if not camera.isOpened():
            print("Error: Could not access webcam.")
            yield None
            return

        # Set generic resolution
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Stream loop
        while True:
            success, frame = camera.read()
            
            if not success:
                print("Failed to read frame.")
                break
                
            # Convert BGR (OpenCV default) to RGB (Streamlit requirement)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Yield the frame to the consumer
            yield rgb_frame
            
            # Minimal sleep to control frame rate if strictly necessary, 
            # though usually the read() blocks enough.
            time.sleep(0.01)

    except Exception as e:
        print(f"Stream error: {e}")
        yield None

    finally:
        # Cleanup
        if camera is not None:
            camera.release()
            print("Camera resource released.")
