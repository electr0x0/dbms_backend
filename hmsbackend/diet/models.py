from django.db import models

class Exercise(models.Model):
    name = models.CharField(max_length=255)
    reps = models.IntegerField()
    sets = models.IntegerField()
    diet = models.ForeignKey('Diet', related_name='exercises', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class SuggestedGoal(models.Model):
    goal = models.CharField(max_length=255)
    diet = models.ForeignKey('Diet', related_name='suggested_goals', on_delete=models.CASCADE)

    def __str__(self):
        return self.goal


class Diet(models.Model):
    UNIT_CHOICES = [
        ('weeks', 'Weeks',),
        ('days', 'Days'),
        ('months', 'Months')
    ]

    weight_goal = models.FloatField()
    duration = models.IntegerField()
    description = models.TextField()
    consultation_interval = models.IntegerField(blank=True, null=True)
    consultation_unit = models.CharField(max_length=10, choices=UNIT_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"Diet Plan: {self.weight_goal} kg over {self.duration} days"


