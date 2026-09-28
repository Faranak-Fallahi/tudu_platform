from habits.models import Habit, HabitLog
from habits.serializers import HabitSerializer, HabitLogSerializer
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HabitLogViewSet(viewsets.ModelViewSet):
    serializer_class = HabitLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return HabitLog.objects.filter(
            habit__user=self.request.user
        )

    def perform_create(self, serializer):
        habit = serializer.validated_data["habit"]

        if habit.user != self.request.user:
            

            raise PermissionDenied(
                "You can only create logs for your own habits."
            )

        serializer.save()