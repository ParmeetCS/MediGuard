"""
Person Detection Module
Uses OpenCV's built-in person detection with HOG (Histogram of Oriented Gradients)
to detect and draw bounding boxes around people in video frames.
"""

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    cv2 = None

import numpy as np
from typing import List, Tuple, Optional


class PersonDetector:
    """
    Person detector using OpenCV's HOG descriptor and SVM classifier
    """
    
    def __init__(self):
        """Initialize the HOG person detector"""
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        
        # Detection parameters
        self.win_stride = (8, 8)
        self.padding = (16, 16)
        self.scale = 1.05
        self.confidence_threshold = 0.5
    
    def detect_person(self, frame: np.ndarray) -> List[Tuple[int, int, int, int, float]]:
        """
        Detect person in the frame
        
        Args:
            frame: Input frame in RGB or BGR format
        
        Returns:
            List of tuples containing (x, y, w, h, confidence) for each detection
        """
        try:
            # Convert to grayscale if needed
            if len(frame.shape) == 3:
                gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            else:
                gray = frame
            
            # Detect people
            (rects, weights) = self.hog.detectMultiScale(
                gray,
                winStride=self.win_stride,
                padding=self.padding,
                scale=self.scale
            )
            
            # Filter by confidence
            detections = []
            for (x, y, w, h), weight in zip(rects, weights):
                if weight > self.confidence_threshold:
                    detections.append((x, y, w, h, weight))
            
            return detections
        
        except Exception as e:
            print(f"Detection error: {e}")
            return []
    
    def draw_boxes(self, frame: np.ndarray, detections: List[Tuple[int, int, int, int, float]], 
                    color: Tuple[int, int, int] = (0, 255, 0), thickness: int = 3) -> np.ndarray:
        """
        Draw bounding boxes around detected persons
        
        Args:
            frame: Input frame
            detections: List of (x, y, w, h, confidence) tuples
            color: RGB color for the box (default: green)
            thickness: Box line thickness
        
        Returns:
            Frame with bounding boxes drawn
        """
        frame_copy = frame.copy()
        
        for (x, y, w, h, confidence) in detections:
            # Draw rectangle
            cv2.rectangle(frame_copy, (x, y), (x + w, y + h), color, thickness)
            
            # Add confidence label
            label = f"Person: {confidence:.2f}"
            label_y = y - 10 if y - 10 > 10 else y + 20
            
            # Draw label background
            (label_w, label_h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            cv2.rectangle(frame_copy, (x, label_y - label_h - 5), (x + label_w, label_y + 5), color, -1)
            
            # Draw label text
            cv2.putText(frame_copy, label, (x, label_y), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        return frame_copy
    
    def process_frame(self, frame: np.ndarray, draw_boxes: bool = True) -> Tuple[np.ndarray, int]:
        """
        Process a single frame: detect person and optionally draw boxes
        
        Args:
            frame: Input frame
            draw_boxes: Whether to draw bounding boxes
        
        Returns:
            Tuple of (processed frame, number of persons detected)
        """
        detections = self.detect_person(frame)
        
        if draw_boxes and len(detections) > 0:
            frame = self.draw_boxes(frame, detections)
        
        return frame, len(detections)


def camera_stream_with_detection() -> 'Generator':
    """
    Generator that yields frames with person detection
    
    Yields:
        Tuple of (frame with boxes, person count)
    """
    detector = PersonDetector()
    camera = None
    
    try:
        camera = cv2.VideoCapture(0)
        
        if not camera.isOpened():
            print("Error: Could not access webcam.")
            yield None, 0
            return

        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        while True:
            success, frame = camera.read()
            
            if not success:
                break
            
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process frame with detection
            processed_frame, person_count = detector.process_frame(rgb_frame)
            
            yield processed_frame, person_count

    except Exception as e:
        print(f"Stream error: {e}")
        yield None, 0

    finally:
        if camera is not None:
            camera.release()
            print("Camera resource released.")
