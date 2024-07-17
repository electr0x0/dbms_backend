# serializers.py

from rest_framework import serializers
from .models import Diet, Exercise, SuggestedGoal

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['name', 'reps', 'sets']

class SuggestedGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuggestedGoal
        fields = ['goal']

class DietSerializer(serializers.ModelSerializer):
    exercises = ExerciseSerializer(many=True, required=False)
    suggested_goals = serializers.ListField(child=serializers.CharField(), required=False)

    class Meta:
        model = Diet
        fields = ['weight_goal', 'duration', 'description', 'exercises', 'consultation_interval', 'consultation_unit', 'suggested_goals']

    def create(self, validated_data):
        exercises_data = validated_data.pop('exercises', [])
        suggested_goals_data = validated_data.pop('suggested_goals', [])

        diet = Diet.objects.create(**validated_data)

        for exercise_data in exercises_data:
            Exercise.objects.create(diet=diet, **exercise_data)

        for goal in suggested_goals_data:
            print(goal, "baal")
            SuggestedGoal.objects.create(diet=diet, goal=goal)

        return diet
