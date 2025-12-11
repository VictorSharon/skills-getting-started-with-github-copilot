"""Tests for the Mergington High School API endpoints."""
import pytest
from tests.conftest import client


def test_get_activities(client):
    """Test retrieving all activities."""
    response = client.get("/activities")
    assert response.status_code == 200
    
    activities = response.json()
    assert isinstance(activities, dict)
    assert "Chess Club" in activities
    assert "Programming Class" in activities
    assert "Tennis Club" in activities
    
    # Verify activity structure
    chess_club = activities["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)


def test_signup_success(client):
    """Test successful signup for an activity."""
    response = client.post(
        "/activities/Tennis%20Club/signup?email=new_student@example.com"
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "new_student@example.com" in data["message"]
    assert "Tennis Club" in data["message"]
    
    # Verify participant was added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert "new_student@example.com" in activities["Tennis Club"]["participants"]


def test_signup_already_registered(client):
    """Test signup fails when student is already registered."""
    response = client.post(
        "/activities/Chess%20Club/signup?email=michael@mergington.edu"
    )
    assert response.status_code == 400
    data = response.json()
    assert "Already signed up" in data["detail"]


def test_signup_activity_not_found(client):
    """Test signup fails when activity doesn't exist."""
    response = client.post(
        "/activities/Nonexistent%20Activity/signup?email=student@example.com"
    )
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_signup_activity_full(client):
    """Test signup fails when activity is at max capacity."""
    # Get an activity that's full (we'll artificially fill Tennis Club)
    from src.app import activities
    activities["Tennis Club"]["max_participants"] = 1
    activities["Tennis Club"]["participants"] = ["existing@example.com"]
    
    response = client.post(
        "/activities/Tennis%20Club/signup?email=another@example.com"
    )
    assert response.status_code == 400
    data = response.json()
    assert "Activity is full" in data["detail"]


def test_unregister_success(client):
    """Test successful unregistration from an activity."""
    # First, signup
    client.post("/activities/Tennis%20Club/signup?email=test@example.com")
    
    # Then unregister
    response = client.post(
        "/activities/Tennis%20Club/unregister?email=test@example.com"
    )
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered" in data["message"]
    assert "test@example.com" in data["message"]
    
    # Verify participant was removed
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert "test@example.com" not in activities["Tennis Club"]["participants"]


def test_unregister_not_registered(client):
    """Test unregister fails when student is not registered."""
    response = client.post(
        "/activities/Chess%20Club/unregister?email=nonexistent@example.com"
    )
    assert response.status_code == 400
    data = response.json()
    assert "Not registered" in data["detail"]


def test_unregister_activity_not_found(client):
    """Test unregister fails when activity doesn't exist."""
    response = client.post(
        "/activities/Nonexistent%20Activity/unregister?email=student@example.com"
    )
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_signup_and_unregister_workflow(client):
    """Test complete workflow: signup, verify, unregister, verify."""
    email = "workflow@example.com"
    activity = "Robotics Club"
    
    # Initial check
    activities_before = client.get("/activities").json()
    assert email not in activities_before[activity]["participants"]
    
    # Signup
    signup_response = client.post(
        f"/activities/{activity.replace(' ', '%20')}/signup?email={email}"
    )
    assert signup_response.status_code == 200
    
    # Verify signup
    activities_after_signup = client.get("/activities").json()
    assert email in activities_after_signup[activity]["participants"]
    
    # Unregister
    unregister_response = client.post(
        f"/activities/{activity.replace(' ', '%20')}/unregister?email={email}"
    )
    assert unregister_response.status_code == 200
    
    # Verify unregister
    activities_after_unregister = client.get("/activities").json()
    assert email not in activities_after_unregister[activity]["participants"]


def test_multiple_signups_same_activity(client):
    """Test multiple different students can signup for the same activity."""
    activity = "Art Studio"
    emails = ["student1@example.com", "student2@example.com", "student3@example.com"]
    
    for email in emails:
        response = client.post(
            f"/activities/{activity.replace(' ', '%20')}/signup?email={email}"
        )
        assert response.status_code == 200
    
    # Verify all are registered
    activities = client.get("/activities").json()
    for email in emails:
        assert email in activities[activity]["participants"]


def test_activity_spots_available(client):
    """Test that spots available is correctly calculated."""
    activity = "Drama Club"
    
    activities = client.get("/activities").json()
    drama = activities[activity]
    max_participants = drama["max_participants"]
    current_participants = len(drama["participants"])
    
    assert max_participants == 25
    assert current_participants == 0
    assert (max_participants - current_participants) == 25
