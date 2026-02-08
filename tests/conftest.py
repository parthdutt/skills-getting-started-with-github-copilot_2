"""
Pytest configuration and fixtures for FastAPI tests
"""

import pytest
import sys
from pathlib import Path

# Add src directory to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fastapi.testclient import TestClient
from app import app, activities


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Reset activities to initial state before each test"""
    initial_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball": {
            "description": "Team sport focusing on shooting, dribbling, and defensive skills",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Individual and doubles tennis matches and coaching",
            "schedule": "Tuesdays and Thursdays, 3:45 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["james@mergington.edu"]
        },
        "Drama Club": {
            "description": "Theater performances and acting workshops",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 25,
            "participants": ["isabella@mergington.edu", "lucas@mergington.edu"]
        },
        "Art Studio": {
            "description": "Painting, drawing, and sculpture techniques",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["grace@mergington.edu"]
        },
        "Debate Team": {
            "description": "Competitive debate and public speaking skills",
            "schedule": "Mondays and Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 14,
            "participants": ["noah@mergington.edu", "ava@mergington.edu"]
        },
        "Science Club": {
            "description": "Hands-on experiments and scientific research projects",
            "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["ethan@mergington.edu"]
        }
    }
    
    # Clear and reset activities
    activities.clear()
    activities.update(initial_activities)
    yield
    # Clean up after test
    activities.clear()
    activities.update(initial_activities)
