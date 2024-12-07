# tests/test_perfil.py
class ProfileTests(TestCase):
  def setUp(self):
    self.user = User.objects.create_user(
      username='testuser',
      email='test@example.com',
      password='testpass123'
    )

  def test_user_profile_creation(self):
    """Test user profile is created"""
    self.assertTrue(self.user.profile)
    self.assertEqual(self.user.email, 'test@example.com')

  def test_profile_update(self):
    """Test profile update"""
    profile = self.user.profile
    profile.height = 170
    profile.weight = 70
    profile.goal = 'mantener'
    profile.save()
    
    self.assertEqual(profile.height, 170)
    self.assertEqual(profile.weight, 70)
    self.assertEqual(profile.goal, 'mantener')

  def test_login_view(self):
    """Test login functionality"""
    response = self.client.post(reverse('login'), {
      'username': 'testuser',
      'password': 'testpass123'
    })
    self.assertEqual(response.status_code, 302)  # Redirect after login
  def setUp(self):
    self.recipe_data = {
      'nombre': 'Test Recipe',
      'tipo': 'almuerzo',
      'tiempo': '30 minutos',
      'dificultad': 'fácil'
    }

# tests/test_perfil.py
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from perfil.models import Profile

class ProfileTests(TestCase):
  def setUp(self):
        self.client = Client()
    self.user = User.objects.create_user( # Create a user
      username='testuser',
      email='test@example.com',
      password='testpass123'
    )

    def test_profile_creation(self):
        """Test that profile is created automatically when user is created"""
        profile = Profile.objects.get(user=self.user)
        self.assertIsNotNone(profile)

    def test_profile_fields(self):
        """Test profile fields are saved correctly"""
    profile = self.user.profile
        profile.height = 175
    profile.weight = 70
        profile.gender = 'M'
        profile.goal = 'bajar'
        profile.weekly_exercise_hours = 5
        profile.smoker = False
        profile.save()
        
        updated_profile = Profile.objects.get(user=self.user)
        self.assertEqual(updated_profile.height, 175)
        self.assertEqual(updated_profile.weight, 70)
        self.assertEqual(updated_profile.gender, 'M')
        self.assertEqual(updated_profile.goal, 'bajar')
        self.assertEqual(updated_profile.weekly_exercise_hours, 5)
        self.assertFalse(updated_profile.smoker)
        
    def test_profile_edit_view(self):
        """Test profile edit view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        
    def test_profile_edit_post(self):
        """Test profile update through POST request"""
        self.client.login(username='testuser', password='testpass123')
        data = {
            'height': 180,
            'weight': 75,
            'gender': 'M',
            'goal': 'mantener',
            'weekly_exercise_hours': 3,
            'smoker': True
        }
        response = self.client.post(reverse('profile'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        
        # Verify changes were saved
        updated_profile = Profile.objects.get(user=self.user)
        self.assertEqual(updated_profile.height, 180)
        self.assertEqual(updated_profile.weight, 75)
        self.assertEqual(updated_profile.gender, 'M')
        self.assertTrue(updated_profile.smoker)
        
    def test_imc_calculation(self):
        """Test IMC calculation"""
        profile = self.user.profile
        profile.height = 170  # cm
        profile.weight = 70   # kg
    profile.save()
    
        # IMC = weight / (height in meters)^2
        expected_imc = round(70 / ((170/100) ** 2), 2)
        self.assertEqual(profile.calculate_imc(), expected_imc)
        
    def test_signup_view(self):
        """Test signup functionality"""
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'password_confirm': 'newpass123',
            'gender': 'M'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful signup
        self.assertTrue(User.objects.filter(username='newuser').exists())