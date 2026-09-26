from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from datetime import timedelta
from .models import Task


User = get_user_model()


class TaskAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="user@example.com",
            phone_number="09120000001",
            password="TestPassword123!",
        )

        self.other_user = User.objects.create_user(
            username="otheruser",
            email="other@example.com",
            phone_number="09120000002",
            password="TestPassword123!",
        )

        self.list_url = "/api/v1/tasks/"

        self.client.force_authenticate(user=self.user)

    def test_create_task(self):
        data = {
            "title": "Complete Phase 3",
            "description": "Finish task management API",
            "priority": "HIGH",
            "status": "TODO",
            "due_date": timezone.localdate(),
        }

        response = self.client.post(
            self.list_url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        task = Task.objects.get(title="Complete Phase 3")

        self.assertEqual(task.user, self.user)
        self.assertEqual(task.priority, "HIGH")
        self.assertEqual(task.status, "TODO")
        
        
    def test_unauthenticated_user_cannot_access_tasks(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
        
        
        
    def test_task_is_created_for_authenticated_user(self):
        data = {
            "title": "My Task",
            "description": "This task belongs to me",
            "priority": "HIGH",
            "status": "TODO",
            "due_date": timezone.localdate(),
            "user": self.other_user.id,
        }
    
        response = self.client.post(
            self.list_url,
            data,
            format="json",
        )
    
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
    
        task = Task.objects.get(title="My Task")
    
        self.assertEqual(task.user, self.user)
        self.assertNotEqual(task.user, self.other_user)
        
    def test_user_can_only_see_own_tasks(self):
        Task.objects.create(
            user=self.user,
            title="My Task",
            due_date=timezone.localdate(),
        )

        Task.objects.create(
            user=self.other_user,
            title="Other User Task",
            due_date=timezone.localdate(),
        )

        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

        self.assertEqual(
            response.data[0]["title"],
            "My Task",
        )
        
    def test_tasks_are_filtered_by_date(self):
        today = timezone.localdate()
        tomorrow = today + timezone.timedelta(days=1)

        Task.objects.create(
            user=self.user,
            title="Today's Task",
            due_date=today,
        )

        Task.objects.create(
            user=self.user,
            title="Tomorrow's Task",
            due_date=tomorrow,
        )

        response = self.client.get(
            self.list_url,
            {"date": today},
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
            response.data[0]["title"],
            "Today's Task",
        )
        
        
    def test_tasks_default_to_today(self):
        today = timezone.localdate()
        tomorrow = today + timedelta(days=1)

        Task.objects.create(
            user=self.user,
            title="Today's Task",
            due_date=today,
        )

        Task.objects.create(
            user=self.user,
            title="Tomorrow's Task",
            due_date=tomorrow,
        )

        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

        self.assertEqual(
            response.data[0]["title"],
            "Today's Task",
        )
        
    def test_user_can_update_own_task(self):
        task = Task.objects.create(
            user=self.user,
            title="Old Title",
            priority="MEDIUM",
            due_date=timezone.localdate(),
        )

        response = self.client.patch(
            f"{self.list_url}{task.id}/",
            {
                "title": "Updated Title",
                "priority": "HIGH",
            },
            format="json",
        )
        

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        task.refresh_from_db()

        self.assertEqual(
            task.title,
            "Updated Title",
        )

        self.assertEqual(
            task.priority,
            "HIGH",
        )
        
    def test_user_cannot_update_other_users_task(self):
        task = Task.objects.create(
            user=self.other_user,
            title="Other User Task",
            priority="MEDIUM",
            due_date=timezone.localdate(),
        )

        response = self.client.patch(
            f"{self.list_url}{task.id}/",
            {
                "title": "Hacked Title",
                "priority": "URGENT",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

        task.refresh_from_db()

        self.assertEqual(
            task.title,
            "Other User Task",
        )

        self.assertEqual(
            task.priority,
            "MEDIUM",
        )
        
    def test_user_can_delete_own_task(self):
        task = Task.objects.create(
            user=self.user,
            title="Task To Delete",
            priority="MEDIUM",
            due_date=timezone.localdate(),
        )

        response = self.client.delete(
            f"{self.list_url}{task.id}/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Task.objects.filter(id=task.id).exists(),
        )