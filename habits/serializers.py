from rest_framework import serializers

from habits.models import Habit, HabitLog


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = (
            "id",
            "title",
            "description",
            "frequency",
            "start_date",
            "end_date",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class HabitLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitLog
        fields = (
            "id",
            "habit",
            "date",
            "completed",
            "created_at",
        )
        read_only_fields = (
            "id",
            "created_at",
        )
        
    def validate_habit(self, value):
        request = self.context["request"]

        if value.user != request.user:
            raise serializers.ValidationError(
                "You can only use your own habits."
            )

        return value