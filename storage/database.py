"""
Database Module
Handles persistent storage of daily health records using JSON.
Supports saving and loading records by user_id.
"""

import json
import os
from typing import List, Dict, Any
from datetime import datetime

DB_FILE = os.path.join(os.path.dirname(__file__), "health_records.json")

def _load_db() -> Dict[str, List[Dict[str, Any]]]:
    """Internal helper to load the entire database."""
    if not os.path.exists(DB_FILE):
        return {}
    
    try:
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        # Return empty dict if file is corrupted or empty
        return {}

def _save_db(data: Dict[str, List[Dict[str, Any]]]):
    """Internal helper to save the entire database."""
    try:
        with open(DB_FILE, 'w') as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        print(f"Error saving database: {e}")

def save_health_record(user_id: str, record: Dict[str, Any]) -> bool:
    """
    Save a daily health record for a specific user.
    Appends the new record to the user's history.
    
    Args:
        user_id (str): Unique identifier for the user.
        record (dict): The health data to save.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    if not user_id or not record:
        return False
        
    db = _load_db()
    
    # Initialize user list if not exists
    if user_id not in db:
        db[user_id] = []
    
    # Add timestamp if missing
    if 'timestamp' not in record:
        record['timestamp'] = datetime.now().isoformat()
        
    # Append new record
    db[user_id].append(record)
    
    _save_db(db)
    return True

def load_health_records(user_id: str) -> List[Dict[str, Any]]:
    """
    Load all health records for a specific user.
    
    Args:
        user_id (str): Unique identifier for the user.
        
    Returns:
        list: List of health records, or empty list if user not found.
    """
    db = _load_db()
    return db.get(user_id, [])

# Initialize db file if it doesn't exist
if not os.path.exists(DB_FILE):
    _save_db({})
