from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import DietSerializer
from .models import Diet
from connection import execute_raw_sql2

class DietCreateView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            serializer = DietSerializer(data=request.data)
            if serializer.is_valid():
                validated_data = serializer.validated_data
                exercises_data = validated_data.pop('exercises', [])
                suggested_goals_data = validated_data.pop('suggested_goals', [])

                with transaction.atomic():
                    # Insert Diet using raw SQL
                    insert_diet_query = """
                        INSERT INTO diet_diet (weight_goal, duration, description, consultation_interval, consultation_unit)
                        VALUES (%s, %s, %s, %s, %s)
                        RETURNING id
                    """
                    diet_params = [
                        validated_data['weight_goal'],
                        validated_data['duration'],
                        validated_data['description'],
                        validated_data.get('consultation_interval', None),
                        validated_data.get('consultation_unit', None)
                    ]
                    result = execute_raw_sql2(insert_diet_query, diet_params)
                    diet_id = result[0]['id']

                    # Insert Exercises using raw SQL
                    for exercise_data in exercises_data:
                        insert_exercise_query = """
                            INSERT INTO diet_exercise (name, reps, sets, diet_id)
                            VALUES (%s, %s, %s, %s)
                        """
                        exercise_params = [
                            exercise_data['name'],
                            exercise_data['reps'],
                            exercise_data['sets'],
                            diet_id
                        ]
                        execute_raw_sql2(insert_exercise_query, exercise_params)

                    # Insert Suggested Goals using raw SQL
                    for suggested_goal_data in suggested_goals_data:
                        if isinstance(suggested_goal_data, dict):
                            goal = suggested_goal_data.get('goal')
                        elif isinstance(suggested_goal_data, str):
                            goal = suggested_goal_data
                        else:
                            raise ValueError(f"Unexpected type for suggested_goal_data: {type(suggested_goal_data)}")

                        insert_goal_query = """
                            INSERT INTO diet_suggestedgoal (goal, diet_id)
                            VALUES (%s, %s)
                        """
                        goal_params = [
                            goal,
                            diet_id
                        ]
                        execute_raw_sql2(insert_goal_query, goal_params)

                    return Response({"message": "Diet created successfully", "diet_id": diet_id}, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
