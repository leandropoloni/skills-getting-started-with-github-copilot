from urllib.parse import quote

from src.app import activities


def test_get_activities_returns_activity_data(client):
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert data["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_adds_participant(client):
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    response = client.post(
        f"/activities/{quote(activity_name)}/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in activities[activity_name]["participants"]


def test_signup_duplicate_returns_400(client):
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.post(
        f"/activities/{quote(activity_name)}/signup",
        params={"email": email},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"
    assert activities[activity_name]["participants"].count(email) == 1


def test_signup_full_activity_returns_400(client):
    activity_name = "Tiny Club"
    activities[activity_name] = {
        "description": "A tiny club for testing capacity",
        "schedule": "Fridays, 1:00 PM - 2:00 PM",
        "max_participants": 1,
        "participants": ["member@mergington.edu"],
    }
    email = "newstudent@mergington.edu"

    response = client.post(
        f"/activities/{quote(activity_name)}/signup",
        params={"email": email},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"
    assert email not in activities[activity_name]["participants"]


def test_remove_participant(client):
    activity_name = "Chess Club"
    email = "daniel@mergington.edu"

    response = client.delete(
        f"/activities/{quote(activity_name)}/participants",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity_name}"
    assert email not in activities[activity_name]["participants"]


def test_remove_missing_participant_returns_404(client):
    activity_name = "Chess Club"
    email = "missing@mergington.edu"

    response = client.delete(
        f"/activities/{quote(activity_name)}/participants",
        params={"email": email},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
