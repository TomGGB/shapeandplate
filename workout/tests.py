# tests/test_workout.py
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from workout.models import ExerciseRoutine, ExerciseProgress

class WorkoutTests(TestCase):
  def setUp(self):
    self.user = User.objects.create_user(username='testuser', password='12345')
    self.client = Client()
    self.client.login(username='testuser', password='12345')

  def test_calculate_imc(self):
    """Test IMC calculation"""
    test_cases = [
      {'height': 170, 'weight': 70, 'expected': 24.22},
      {'height': 180, 'weight': 80, 'expected': 24.69},
      {'height': 165, 'weight': 55, 'expected': 20.20}
    ]
    
    for case in test_cases:
      height_m = case['height'] / 100
      calculated_imc = round(case['weight'] / (height_m * height_m), 2)
      self.assertEqual(calculated_imc, case['expected'])

  def test_exercise_routine_creation(self):
    """Test exercise routine creation"""
    routine_data = {
      'user': self.user,
      'tipo': 'strength',
      'duracion': '30 minutos',
      'dificultad': 'intermedio'
    }
    routine = ExerciseRoutine.objects.create(**routine_data)
    self.assertEqual(routine.user, self.user)
    self.assertEqual(routine.tipo, 'strength')

  def test_workout_view_access(self):
    """Test access to workout view"""
    response = self.client.get(reverse('workout'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'workout.html')

  def test_exercise_progress(self):
    """Test exercise progress tracking"""
    routine = ExerciseRoutine.objects.create(
      user=self.user,
      tipo='strength',
      duracion='30 minutos'
    )
    progress = ExerciseProgress.objects.create(
      routine=routine,
      completed=True,
      time_spent=25
    )
    self.assertTrue(progress.completed)
    self.assertEqual(progress.time_spent, 25)