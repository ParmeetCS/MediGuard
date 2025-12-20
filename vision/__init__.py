"""
Vision module for MediGuard Drift AI
Camera-based health monitoring and feature extraction
"""

from .camera import camera_stream
from .feature_extraction import extract_features

__all__ = ['camera_stream', 'extract_features']
