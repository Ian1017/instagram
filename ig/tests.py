from django.test import TestCase
from .models import Editor,Profile,tags

# Create your tests here.
class EditorTestClass(TestCase):

  # Set up method
    def setUp(self):
        self.logue= Editor(first_name = 'Logue', last_name ='Hearts', email ='logue54@gmail.com')
    # Testing  instance
    def test_instance(self):
        self.assertTrue(isinstance(self.logue,Editor))
       # Testing Save Method
    def test_save_method(self):
        self.logue.save_editor()
        editors = Editor.objects.all()
        self.assertTrue(len(editors) > 0) 