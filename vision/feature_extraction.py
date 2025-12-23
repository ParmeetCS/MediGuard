"""
Feature Extraction Module
This module extracts numerical motion and posture features from video frames.
Uses basic computer vision techniques without machine learning.
"""

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    cv2 = None

import numpy as np
import random
from typing import List, Dict, Union

def extract_features(frames: List[np.ndarray], activity_name: str = "general") -> Dict[str, Union[float, int, str, list]]:
    """
    Extract comprehensive motion and posture features from video frames.
    
    Args:
        frames (list): List of video frames as NumPy arrays in RGB format.
        activity_name (str): The name of the activity being analyzed.
    
    Returns:
        dict: Dictionary containing extracted features including:
            - movement_speed (float): 0-1 normalized intensity
            - stability (float): 0-1 inverse of jitter
            - posture_deviation (float): 0-1 spatial variance
            - motion_smoothness (float): 0-1 consistency of velocity
            - micro_movements (float): 0-1 small involuntary motions
            - range_of_motion (float): 0-1 spatial coverage
            - acceleration_variance (float): 0-1 change in speed patterns
            - sit_to_stand_time (float): Transition time in seconds
            - frame_by_frame_motion (list): Motion intensity per frame for graphing
            - temporal_data (list): List of dicts with timestamp and metrics
    """
    response = {
        "movement_speed": 0.0,
        "stability": 0.0,
        "posture_deviation": 0.0,
        "motion_smoothness": 0.0,
        "micro_movements": 0.0,
        "range_of_motion": 0.0,
        "acceleration_variance": 0.0,
        "sit_to_stand_time": 0.0,
        "frame_count": 0,
        "frame_by_frame_motion": [],
        "temporal_data": [],
        "status": "error",
        "message": "Invalid input"
    }
    
    if not frames or len(frames) < 2:
        response["message"] = "Insufficient frames"
        return response
    
    try:
        gray_frames = [cv2.cvtColor(f, cv2.COLOR_RGB2GRAY) for f in frames]
        
        diffs = []
        centers_of_motion = []
        frame_motion_data = []
        
        # Frame-by-frame analysis
        for i in range(len(gray_frames) - 1):
            diff = cv2.absdiff(gray_frames[i], gray_frames[i+1])
            mean_diff = np.mean(diff)
            diffs.append(mean_diff)
            
            # Store per-frame motion for graphing
            frame_motion_data.append({
                'frame': i,
                'motion_intensity': mean_diff,
                'timestamp': i / 30.0  # Assuming 30 FPS
            })
            
            # Center of motion with threshold
            _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
            M = cv2.moments(thresh)
            if M["m00"] > 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                centers_of_motion.append((cX, cY))
            else:
                prev = centers_of_motion[-1] if centers_of_motion else (0, 0)
                centers_of_motion.append(prev)

        diff_array = np.array(diffs)
        
        # 1. Movement Speed
        avg_movement_raw = np.mean(diff_array)
        movement_speed = min(avg_movement_raw / 50.0, 1.0)
        
        # 2. Motion Smoothness
        if len(diff_array) > 1:
            velocity_changes = np.abs(np.diff(diff_array))
            smoothness_raw = np.std(velocity_changes)
            motion_smoothness = max(0.0, min(1.0, 1.0 - (smoothness_raw / 15.0)))
        else:
            motion_smoothness = 0.0

        # 3. Stability
        movement_variance = np.var(diff_array)
        stability = max(0.0, min(1.0, 1.0 - (movement_variance / 500.0)))

        # 4. Posture Deviation
        if centers_of_motion:
            com_array = np.array(centers_of_motion)
            if len(com_array) > 1:
                var_x = np.var(com_array[:, 0])
                var_y = np.var(com_array[:, 1])
                total_spatial_var = np.sqrt(var_x + var_y)
                posture_deviation = min(total_spatial_var / 150.0, 1.0)
            else:
                posture_deviation = 0.0
        else:
            posture_deviation = 0.0
            
        # 5. Micro-movements (small involuntary motions)
        small_movements = diff_array[diff_array < np.percentile(diff_array, 25)]
        if len(small_movements) > 0:
            micro_intensity = np.mean(small_movements)
            micro_movements = min(micro_intensity / 10.0, 1.0)
        else:
            micro_movements = 0.0
            
        # 6. Range of Motion (spatial coverage)
        if centers_of_motion and len(centers_of_motion) > 1:
            com_array = np.array(centers_of_motion)
            x_range = np.max(com_array[:, 0]) - np.min(com_array[:, 0])
            y_range = np.max(com_array[:, 1]) - np.min(com_array[:, 1])
            total_range = np.sqrt(x_range**2 + y_range**2)
            range_of_motion = min(total_range / 200.0, 1.0)
        else:
            range_of_motion = 0.0
            
        # 7. Acceleration Variance (change in motion patterns)
        if len(diff_array) > 2:
            acceleration = np.diff(np.diff(diff_array))
            accel_var = np.var(acceleration)
            acceleration_variance = min(accel_var / 100.0, 1.0)
        else:
            acceleration_variance = 0.0
            
        # 8. Sit-to-Stand Time
        sit_stand_time = 0.0
        if activity_name == "sit_to_stand" and len(diff_array) > 0:
            threshold = np.max(diff_array) * 0.4
            active_frames = np.sum(diff_array > threshold)
            sit_stand_time = round(active_frames / 30.0, 2)

        return {
            "movement_speed": round(movement_speed, 2),
            "stability": round(stability, 2),
            "posture_deviation": round(posture_deviation, 2),
            "motion_smoothness": round(motion_smoothness, 2),
            "micro_movements": round(micro_movements, 2),
            "range_of_motion": round(range_of_motion, 2),
            "acceleration_variance": round(acceleration_variance, 2),
            "sit_to_stand_time": sit_stand_time,
            "frame_count": len(frames),
            "frame_by_frame_motion": [round(x, 2) for x in diffs],
            "temporal_data": frame_motion_data,
            "status": "success",
            "message": "Analysis complete"
        }
        
    except Exception as e:
        response["message"] = str(e)
        return response

def generate_mock_features() -> dict:
    """Generate realistic mock data compatible with the enhanced format."""
    num_frames = 150
    base_motion = random.uniform(10, 30)
    motion_data = [base_motion + random.uniform(-5, 5) for _ in range(num_frames)]
    
    return {
        "movement_speed": round(random.uniform(0.3, 0.8), 2),
        "stability": round(random.uniform(0.6, 0.9), 2),
        "posture_deviation": round(random.uniform(0.1, 0.4), 2),
        "motion_smoothness": round(random.uniform(0.5, 0.85), 2),
        "micro_movements": round(random.uniform(0.1, 0.3), 2),
        "range_of_motion": round(random.uniform(0.4, 0.7), 2),
        "acceleration_variance": round(random.uniform(0.2, 0.5), 2),
        "sit_to_stand_time": round(random.uniform(1.2, 2.5), 2),
        "frame_count": num_frames,
        "frame_by_frame_motion": [round(x, 2) for x in motion_data],
        "temporal_data": [
            {'frame': i, 'motion_intensity': motion_data[i], 'timestamp': i/30.0}
            for i in range(num_frames)
        ],
        "status": "success",
        "message": "Mock data generated"
    }
