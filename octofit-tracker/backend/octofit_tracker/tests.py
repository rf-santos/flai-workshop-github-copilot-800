from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, Team, Activity, Leaderboard, Workout
from datetime import datetime


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            name="John Doe",
            email="john@example.com",
            team="Team Alpha"
        )
    
    def test_user_creation(self):
        self.assertEqual(self.user.name, "John Doe")
        self.assertEqual(self.user.email, "john@example.com")
        self.assertEqual(self.user.team, "Team Alpha")


class TeamModelTest(TestCase):
    def setUp(self):
        self.team = Team.objects.create(
            name="Team Alpha",
            description="Test team",
            captain="John Doe",
            members_count=5,
            total_points=100
        )
    
    def test_team_creation(self):
        self.assertEqual(self.team.name, "Team Alpha")
        self.assertEqual(self.team.captain, "John Doe")
        self.assertEqual(self.team.members_count, 5)


class ActivityModelTest(TestCase):
    def setUp(self):
        self.activity = Activity.objects.create(
            user_id="123",
            user_name="John Doe",
            team="Team Alpha",
            activity_type="running",
            duration=30,
            distance=5.0,
            calories=300,
            points=50,
            date=datetime.now()
        )
    
    def test_activity_creation(self):
        self.assertEqual(self.activity.user_name, "John Doe")
        self.assertEqual(self.activity.activity_type, "running")
        self.assertEqual(self.activity.duration, 30)


class LeaderboardModelTest(TestCase):
    def setUp(self):
        self.leaderboard = Leaderboard.objects.create(
            team="Team Alpha",
            total_points=500,
            total_activities=10,
            total_calories=3000,
            total_distance=50.0,
            rank=1
        )
    
    def test_leaderboard_creation(self):
        self.assertEqual(self.leaderboard.team, "Team Alpha")
        self.assertEqual(self.leaderboard.total_points, 500)
        self.assertEqual(self.leaderboard.rank, 1)


class WorkoutModelTest(TestCase):
    def setUp(self):
        self.workout = Workout.objects.create(
            name="Morning Run",
            description="A refreshing morning run",
            activity_type="running",
            difficulty="beginner",
            duration=30,
            calories_estimate=300,
            instructions=["Warm up", "Run", "Cool down"]
        )
    
    def test_workout_creation(self):
        self.assertEqual(self.workout.name, "Morning Run")
        self.assertEqual(self.workout.difficulty, "beginner")
        self.assertEqual(self.workout.duration, 30)


class APITestCases(APITestCase):
    def test_api_root(self):
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('users', response.data)
        self.assertIn('teams', response.data)
        self.assertIn('activities', response.data)
        self.assertIn('leaderboard', response.data)
        self.assertIn('workouts', response.data)
    
    def test_users_endpoint(self):
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_teams_endpoint(self):
        response = self.client.get('/api/teams/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_activities_endpoint(self):
        response = self.client.get('/api/activities/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_leaderboard_endpoint(self):
        response = self.client.get('/api/leaderboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_workouts_endpoint(self):
        response = self.client.get('/api/workouts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
