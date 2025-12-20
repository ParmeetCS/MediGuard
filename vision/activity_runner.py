"""
Activity Runner Module
Handles the execution of timed physical activities for health assessment.
Segments frames based on activity duration for separate analysis.
"""

import time
import numpy as np
from typing import List, Generator, Optional

# Define standard activity durations and metadata
ACTIVITY_CONFIG = {
    "sit_to_stand": {
        "duration": 30,
        "description": "Sit comfortably, then stand up fully and sit back down. Repeat."
    },
    "short_walk": {
        "duration": 45,
        "description": "Walk forward a few paces, turn around, and walk back."
    },
    "steady_hands": {
        "duration": 30,
        "description": "Hold your hands steady in front of you."
    }
}

def run_activity(activity_name: str, camera_generator, duration_seconds: int = None) -> List[np.ndarray]:
    """
    Runs a specified activity by capturing frames for a set duration from the provided stream.
    
    Args:
        activity_name (str): Identifier for the activity (e.g., 'sit_to_stand').
        camera_generator (generator): The live frame generator from camera.py.
        duration_seconds (int, optional): Override duration. If None, uses default config.
        
    Returns:
        List[np.ndarray]: A list of captured frames corresponding to the activity.
    """
    
    # Get configuration safely
    config = ACTIVITY_CONFIG.get(activity_name, {})
    
    # Determine actual duration to run
    duration = duration_seconds if duration_seconds is not None else config.get("duration", 5)
    
    captured_frames = []
    start_time = time.time()
    
    print(f"Starting activity: {activity_name} for {duration} seconds.")
    
    try:
        # Loop through the generator
        for frame in camera_generator:
            # Check elapsed time
            elapsed = time.time() - start_time
            if elapsed >= duration:
                break
            
            if frame is not None:
                # Store frame for later analysis
                captured_frames.append(frame)
            
            # Note: We rely on the caller to handle the generator's state if they want to
            # continue using it, but typically a new stream or loop is managed at the UI level.
            # However, for this runner, we just consume what we need.
            
    except Exception as e:
        print(f"Error executing activity {activity_name}: {e}")
        
    final_count = len(captured_frames)
    print(f"Activity '{activity_name}' finished. Captured {final_count} frames.")
    
    return captured_frames

def get_activity_info(activity_name: str) -> dict:
    """Helper to get metadata about an activity."""
    return ACTIVITY_CONFIG.get(activity_name, {
        "duration": 5, "description": "Unknown Activity"
    })
