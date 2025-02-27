from django.test import TestCase

from .models import Categoria

# Create your tests here.
class CategoriaModelTest(TestCase):
    def setUp(self):
        self.category = Categoria.objects.create(
            nombre = "Tec",
            titulo='Tecnologia',
            descripcion = 'Todo sobre tecnologia',
            slug='tec'
        )

    def test_category_creation(self):
        self.assertEqual(str(self.category),'Tec')
        self.assertEqual(self.category.titulo,'Tecnologia')