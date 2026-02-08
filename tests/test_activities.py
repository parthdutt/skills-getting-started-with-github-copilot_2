"""
Tests for FastAPI activities endpoints
"""

import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint"""
    
    def test_get_activities_returns_all_activities(self, client, reset_activities):
        """Test that GET /activities returns all available activities"""
        response = client.get("/activities")
        assert response.status_code == 200
        data = response.json()
        
        # Check that all activities are returned
        assert len(data) == 9
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Basketball" in data
    
    def test_get_activities_returns_activity_details(self, client, reset_activities):
        """Test that activity details are correctly formatted"""
        response = client.get("/activities")
        data = response.json()
        
        chess_club = data["Chess Club"]
        assert chess_club["description"] == "Learn strategies and compete in chess tournaments"
        assert chess_club["schedule"] == "Fridays, 3:30 PM - 5:00 PM"
        assert chess_club["max_participants"] == 12
        assert "michael@mergington.edu" in chess_club["participants"]
        assert "daniel@mergington.edu" in chess_club["participants"]
    
    def test_get_activities_participants_count(self, client, reset_activities):
        """Test that participant counts are correct"""
        response = client.get("/activities")
        data = response.json()
        
        assert len(data["Chess Club"]["participants"]) == 2
        assert len(data["Programming Class"]["participants"]) == 2
        assert len(data["Basketball"]["participants"]) == 1


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint"""
    
    def test_signup_new_participant(self, client, reset_activities):
        """Test signing up a new participant"""
        response = client.post(
            "/activities/Basketball/signup",
            params={"email": "newstudent@mergington.edu"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Signed up newstudent@mergington.edu for Basketball"
    
    def test_signup_adds_participant_to_activity(self, client, reset_activities):
        """Test that signup actually adds participant to activity"""
        client.post(
            "/activities/Basketball/signup",
            params={"email": "newstudent@mergington.edu"}
        )
        
        response = client.get("/activities")
        data = response.json()
        assert "newstudent@mergington.edu" in data["Basketball"]["participants"]
        assert len(data["Basketball"]["participants"]) == 2
    
    def test_signup_nonexistent_activity(self, client, reset_activities):
        """Test signing up for a nonexistent activity"""
        response = client.post(
            "/activities/Nonexistent Club/signup",
            params={"email": "student@mergington.edu"}
        )
        
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Activity not found"
    
    def test_signup_duplicate_participant(self, client, reset_activities):
        """Test that duplicate signups are rejected"""
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": "michael@mergington.edu"}
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data["detail"]
    
    def test_signup_multiple_activities(self, client, reset_activities):
        """Test that a student can sign up for multiple activities"""
        # Sign up new student to first activity
        response1 = client.post(
            "/activities/Basketball/signup",
            params={"email": "versatile@mergington.edu"}
        )
        assert response1.status_code == 200
        
        # Sign up same student to another activity
        response2 = client.post(
            "/activities/Tennis Club/signup",
            params={"email": "versatile@mergington.edu"}
        )
        assert response2.status_code == 200
        
        # Verify both signups succeeded
        response = client.get("/activities")
        data = response.json()
        assert "versatile@mergington.edu" in data["Basketball"]["participants"]
        assert "versatile@mergington.edu" in data["Tennis Club"]["participants"]


class TestUnregisterFromActivity:
    """Tests for DELETE /activities/{activity_name}/unregister endpoint"""
    
    def test_unregister_existing_participant(self, client, reset_activities):
        """Test unregistering an existing participant"""
        response = client.delete(
            "/activities/Chess Club/unregister",
            params={"email": "michael@mergington.edu"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Unregistered michael@mergington.edu from Chess Club"
    
    def test_unregister_removes_participant(self, client, reset_activities):
        """Test that unregister actually removes participant from activity"""
        client.delete(
            "/activities/Chess Club/unregister",
            params={"email": "michael@mergington.edu"}
        )
        
        response = client.get("/activities")
        data = response.json()
        assert "michael@mergington.edu" not in data["Chess Club"]["participants"]
        assert len(data["Chess Club"]["participants"]) == 1
        assert "daniel@mergington.edu" in data["Chess Club"]["participants"]
    
    def test_unregister_nonexistent_activity(self, client, reset_activities):
        """Test unregistering from a nonexistent activity"""
        response = client.delete(
            "/activities/Nonexistent Club/unregister",
            params={"email": "student@mergington.edu"}
        )
        
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Activity not found"
    
    def test_unregister_nonparticipant(self, client, reset_activities):
        """Test unregistering someone not signed up for the activity"""
        response = client.delete(
            "/activities/Chess Club/unregister",
            params={"email": "noone@mergington.edu"}
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "not signed up" in data["detail"]
    
    def test_unregister_then_signup_again(self, client, reset_activities):
        """Test that a participant can re-register after unregistering"""
        # Unregister
        response1 = client.delete(
            "/activities/Chess Club/unregister",
            params={"email": "michael@mergington.edu"}
        )
        assert response1.status_code == 200
        
        # Re-register
        response2 = client.post(
            "/activities/Chess Club/signup",
            params={"email": "michael@mergington.edu"}
        )
        assert response2.status_code == 200
        
        # Verify re-registration succeeded
        response = client.get("/activities")
        data = response.json()
        assert "michael@mergington.edu" in data["Chess Club"]["participants"]


class TestIntegration:
    """Integration tests for signup and unregister workflows"""
    
    def test_full_signup_and_unregister_cycle(self, client, reset_activities):
        """Test complete signup and unregister workflow"""
        email = "integration@mergington.edu"
        activity = "Art Studio"
        
        # Get initial state
        response = client.get("/activities")
        initial_count = len(response.json()[activity]["participants"])
        
        # Sign up
        signup_response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert signup_response.status_code == 200
        
        # Verify signup
        response = client.get("/activities")
        after_signup = len(response.json()[activity]["participants"])
        assert after_signup == initial_count + 1
        
        # Unregister
        unregister_response = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email}
        )
        assert unregister_response.status_code == 200
        
        # Verify unregister
        response = client.get("/activities")
        final_count = len(response.json()[activity]["participants"])
        assert final_count == initial_count
    
    def test_root_redirect(self, client):
        """Test that root endpoint redirects to static index.html"""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"
