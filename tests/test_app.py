def test_root_redirects_to_static_index(client):
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == expected_location


def test_get_activities_returns_activity_data(client):
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert expected_activity in response.json()
    assert "participants" in response.json()[expected_activity]


def test_signup_adds_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "new.student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity}"}
    assert email in client.get("/activities").json()[activity]["participants"]


def test_duplicate_signup_is_rejected_without_adding_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"
    original_participants = client.get("/activities").json()[activity]["participants"]

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"
    assert client.get("/activities").json()[activity]["participants"] == original_participants


def test_signup_for_unknown_activity_returns_not_found(client):
    # Arrange
    activity = "Unknown Club"
    email = "new.student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_removes_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity}"}
    assert email not in client.get("/activities").json()[activity]["participants"]


def test_unregistering_missing_participant_returns_not_found(client):
    # Arrange
    activity = "Chess Club"
    email = "not.registered@mergington.edu"
    original_participants = client.get("/activities").json()[activity]["participants"]

    # Act
    response = client.delete(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"
    assert client.get("/activities").json()[activity]["participants"] == original_participants


def test_unregister_for_unknown_activity_returns_not_found(client):
    # Arrange
    activity = "Unknown Club"
    email = "new.student@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_without_email_returns_validation_error(client):
    # Arrange
    activity = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity}/signup")

    # Assert
    assert response.status_code == 422


def test_signup_with_malformed_email_returns_validation_error(client):
    # Arrange
    activity = "Chess Club"
    email = "not-an-email"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 422


def test_unregister_with_malformed_email_returns_validation_error(client):
    # Arrange
    activity = "Chess Club"
    email = "not-an-email"

    # Act
    response = client.delete(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 422