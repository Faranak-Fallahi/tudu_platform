from datetime import date

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit, HabitLog


User = get_user_model()


class HabitAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="ali",
            phone_number="09120000001",
            password="TestPass123!",
        )

        self.other_user = User.objects.create_user(
            username="reza",
            phone_number="09120000002",
            password="TestPass123!",
        )

        self.habit = Habit.objects.create(
            user=self.user,
            title="Study",
            description="Study Django",
            frequency="daily",
            start_date=date(2026, 9, 29),
            end_date=date(2026, 12, 31),
            is_active=True,
        )

        self.client.force_authenticate(user=self.user)

    def test_unauthenticated_user_cannot_access_habits(self):
        self.client.force_authenticate(user=None)

        response = self.client.get("/api/v1/habits/")

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_user_can_list_own_habits(self):
        response = self.client.get("/api/v1/habits/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Study")

    def test_user_cannot_see_other_users_habits(self):
        Habit.objects.create(
            user=self.other_user,
            title="Other Habit",
            description="Other user's habit",
            frequency="daily",
            start_date=date(2026, 9, 29),
            end_date=date(2026, 12, 31),
            is_active=True,
        )

        response = self.client.get("/api/v1/habits/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Study")

    def test_user_can_create_habit(self):
        data = {
            "title": "Exercise",
            "description": "Daily exercise",
            "frequency": "daily",
            "start_date": "2026-09-29",
            "end_date": "2026-12-31",
            "is_active": True,
        }

        response = self.client.post(
            "/api/v1/habits/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            response.data["title"],
            "Exercise",
        )

        habit = Habit.objects.get(
            id=response.data["id"]
        )

        self.assertEqual(
            habit.user,
            self.user,
        )

    def test_user_cannot_assign_habit_to_another_user(self):
        data = {
            "title": "Exercise",
            "description": "Daily exercise",
            "frequency": "daily",
            "start_date": "2026-09-29",
            "end_date": "2026-12-31",
            "is_active": True,
            "user": self.other_user.id,
        }

        response = self.client.post(
            "/api/v1/habits/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        habit = Habit.objects.get(
            id=response.data["id"]
        )

        self.assertEqual(
            habit.user,
            self.user,
        )

    def test_user_can_update_own_habit(self):
        data = {
            "title": "Updated Study",
            "description": "Updated description",
            "frequency": "weekly",
            "start_date": "2026-09-29",
            "end_date": "2027-01-31",
            "is_active": True,
        }

        response = self.client.put(
            f"/api/v1/habits/{self.habit.id}/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.habit.refresh_from_db()

        self.assertEqual(
            self.habit.title,
            "Updated Study",
        )

        self.assertEqual(
            self.habit.frequency,
            "weekly",
        )

    def test_user_cannot_update_other_users_habit(self):
        other_habit = Habit.objects.create(
            user=self.other_user,
            title="Other Habit",
            description="Other description",
            frequency="daily",
            start_date=date(2026, 9, 29),
            end_date=date(2026, 12, 31),
            is_active=True,
        )

        data = {
            "title": "Hacked Habit",
            "description": "Trying to modify another user's habit",
            "frequency": "daily",
            "start_date": "2026-09-29",
            "end_date": "2026-12-31",
            "is_active": True,
        }

        response = self.client.put(
            f"/api/v1/habits/{other_habit.id}/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

        other_habit.refresh_from_db()

        self.assertEqual(
            other_habit.title,
            "Other Habit",
        )

    def test_user_can_delete_own_habit(self):
        response = self.client.delete(
            f"/api/v1/habits/{self.habit.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Habit.objects.filter(
                id=self.habit.id
            ).exists()
        )

    def test_user_cannot_delete_other_users_habit(self):
        other_habit = Habit.objects.create(
            user=self.other_user,
            title="Other Habit",
            description="Other description",
            frequency="daily",
            start_date=date(2026, 9, 29),
            end_date=date(2026, 12, 31),
            is_active=True,
        )

        response = self.client.delete(
            f"/api/v1/habits/{other_habit.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

        self.assertTrue(
            Habit.objects.filter(
                id=other_habit.id
            ).exists()
        )


class HabitLogAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="ali",
            phone_number="09120000001",
            password="TestPass123!",
        )

        self.other_user = User.objects.create_user(
            username="reza",
            phone_number="09120000002",
            password="TestPass123!",
        )

        self.habit = Habit.objects.create(
            user=self.user,
            title="Study",
            description="Study Django",
            frequency="daily",
            start_date=date(2026, 9, 29),
            end_date=date(2026, 12, 31),
            is_active=True,
        )

        self.other_habit = Habit.objects.create(
            user=self.other_user,
            title="Other Habit",
            description="Other user's habit",
            frequency="daily",
            start_date=date(2026, 9, 29),
            end_date=date(2026, 12, 31),
            is_active=True,
        )

        self.habit_log = HabitLog.objects.create(
            habit=self.habit,
            date=date(2026, 9, 29),
            completed=False,
        )

        self.client.force_authenticate(user=self.user)

    def test_unauthenticated_user_cannot_access_habit_logs(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(
            "/api/v1/habit-logs/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_user_can_create_habit_log_for_own_habit(self):
        data = {
            "habit": self.habit.id,
            "date": "2026-09-30",
            "completed": True,
        }

        response = self.client.post(
            "/api/v1/habit-logs/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            response.data["habit"],
            self.habit.id,
        )

        self.assertTrue(
            response.data["completed"]
        )

    def test_user_cannot_create_habit_log_for_other_users_habit(self):
        data = {
            "habit": self.other_habit.id,
            "date": "2026-09-30",
            "completed": True,
        }

        response = self.client.post(
            "/api/v1/habit-logs/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_user_can_list_own_habit_logs(self):
        response = self.client.get(
            "/api/v1/habit-logs/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

        self.assertEqual(
            response.data[0]["habit"],
            self.habit.id,
        )

    def test_user_cannot_update_log_to_other_users_habit(self):
        data = {
            "habit": self.other_habit.id,
            "date": "2026-09-29",
            "completed": True,
        }

        response = self.client.put(
            f"/api/v1/habit-logs/{self.habit_log.id}/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_user_can_update_own_habit_log(self):
        data = {
            "habit": self.habit.id,
            "date": "2026-09-29",
            "completed": True,
        }

        response = self.client.put(
            f"/api/v1/habit-logs/{self.habit_log.id}/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.habit_log.refresh_from_db()

        self.assertTrue(
            self.habit_log.completed
        )

    def test_user_can_delete_own_habit_log(self):
        response = self.client.delete(
            f"/api/v1/habit-logs/{self.habit_log.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            HabitLog.objects.filter(
                id=self.habit_log.id
            ).exists()
        )

    def test_duplicate_habit_log_for_same_date_is_rejected(self):
        data = {
            "habit": self.habit.id,
            "date": "2026-09-29",
            "completed": True,
        }

        response = self.client.post(
            "/api/v1/habit-logs/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )