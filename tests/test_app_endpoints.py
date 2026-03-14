"""API endpoint tests for src/app.py using pytest and TestClient."""

import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture(autouse=True)
def restore_activities_state():
    """Restore the in-memory activities state around each test."""
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(copy.deepcopy(original))


@pytest.fixture
def client():
    """Return FastAPI test client."""
    return TestClient(app)


class TestGetActivities:
    def test_get_activities_returns_200(self, client):
        # Arrange / Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    def test_get_activities_contains_required_fields(self, client):
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert response.status_code == 200
        assert "Chess Club" in data
        for activity in data.values():
            assert required_fields.issubset(activity.keys())


class TestSignupForActivity:
    def test_signup_success(self, client):
        # Arrange
        activity = "Chess Club"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(f"/activities/{activity}/signup", params={"email": email})

        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Signed up {email} for {activity}"
        assert email in activities[activity]["participants"]

    def test_signup_nonexistent_activity(self, client):
        # Arrange
        activity = "Nonexistent"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(f"/activities/{activity}/signup", params={"email": email})

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_signup_duplicate(self, client):
        # Arrange
        activity = "Chess Club"
        email = "michael@mergington.edu"

        # Act
        response = client.post(f"/activities/{activity}/signup", params={"email": email})

        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Student already signed up for this activity"


class TestRemoveParticipant:
    def test_remove_participant_success(self, client):
        # Arrange
        activity = "Chess Club"
        email = "michael@mergington.edu"

        # Act
        response = client.delete(f"/activities/{activity}/signup", params={"email": email})

        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Removed {email} from {activity}"
        assert email not in activities[activity]["participants"]

    def test_remove_nonexistent_activity(self, client):
        # Arrange
        activity = "Nonexistent"
        email = "student@mergington.edu"

        # Act
        response = client.delete(f"/activities/{activity}/signup", params={"email": email})

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_remove_participant_not_found(self, client):
        # Arrange
        activity = "Chess Club"
        email = "unknown@mergington.edu"

        # Act
        response = client.delete(f"/activities/{activity}/signup", params={"email": email})

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Participant not found in activity"

