"""
Utility functions for attendance system
"""

import hashlib
import secrets

def compute_image_hash(image_bytes: bytes) -> str:
    """Compute SHA-256 hash of image bytes"""
    return hashlib.sha256(image_bytes).hexdigest()

def generate_session_token() -> str:
    """Generate secure session token"""
    return secrets.token_urlsafe(32)

def format_attendance_status(status: str) -> str:
    """Format attendance status for display"""
    status_map = {
        "present": "✅ Present",
        "absent": "❌ Absent",
        "uncertain": "⚠️ Uncertain",
    }
    return status_map.get(status, status)

def compute_confidence_threshold(confidence: float) -> float:
    """Compute confidence threshold based on model confidence"""
    # Confidence 0-1, convert to 0-100
    return confidence * 100
