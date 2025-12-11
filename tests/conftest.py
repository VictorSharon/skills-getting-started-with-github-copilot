import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Fixture to provide a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to initial state before each test."""
    from src.app import activities
    
    # Store original activities
    original = {
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
        "Tennis Club": {
            "description": "Learn tennis skills and compete in matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 16,
            "participants": []
        },
        "Basketball Team": {
            "description": "Competitive basketball team for school tournaments",
            "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 15,
            "participants": []
        },
        "Drama Club": {
            "description": "Stage acting, script writing, and theatrical performances",
            "schedule": "Saturdays, 10:00 AM - 12:00 PM",
            "max_participants": 25,
            "participants": []
        },
        "Art Studio": {
            "description": "Painting, drawing, sculpture, and mixed media arts",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": []
        },
        "Robotics Club": {
            "description": "Build and program robots for competitions",
            "schedule": "Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 14,
            "participants": []
        },
        "Science Club": {
            "description": "Explore physics, chemistry, and biology through experiments",
            "schedule": "Fridays, 3:30 PM - 4:30 PM",
            "max_participants": 22,
            "participants": []
        }
    }
    
    # Clear and reset
    activities.clear()
    activities.update(original)
    
    yield
    
    # Cleanup after test
    activities.clear()
    activities.update(original)
