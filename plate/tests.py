# tests/test_plate.py
class PlateTests(TestCase):
  def setUp(self):
    self.user = User.objects.create_user(username='testuser', password='12345')
    self.recipe_data = {
      'user': self.user,
      'nombre': 'Test Recipe',
      'tipo': 'almuerzo',
      'tiempo': '30 minutos',
      'dificultad': 'fácil',
      'ingredientes': ['ingredient1', 'ingredient2'],
      'instrucciones': 'Test instructions'
    }

  def test_recipe_creation(self):
    """Test recipe creation"""
    recipe = FoodRecipe.objects.create(**self.recipe_data)
    self.assertEqual(recipe.nombre, 'Test Recipe')
    self.assertEqual(recipe.tipo, 'almuerzo')

  def test_recipe_update(self):
    """Test recipe update"""
    recipe = FoodRecipe.objects.create(**self.recipe_data)
    recipe.tiempo = '45 minutos'
    recipe.save()
    self.assertEqual(recipe.tiempo, '45 minutos')

  def test_recipe_view(self):
    """Test recipe view access"""
    recipe = FoodRecipe.objects.create(**self.recipe_data)
    response = self.client.get(reverse('recipe_detail', args=[recipe.id]))
    self.assertEqual(response.status_code, 200)