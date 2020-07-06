from django.test import TestCase
from .models import User,Profile,Comment

# Create your tests here.
class UserTestClass(TestCase):

  # Set up method
    def setUp(self):
        self.logue= User(User_name = 'Logue54',first_name='Flacko', last_name ='Hearts', email ='logue54@gmail.com')
    # Testing  instance
    def test_instance(self):
        self.assertTrue(isinstance(self.logue,Editor))
       # Testing Save Method
    def test_save_method(self):
        self.logue.save_user()
        users = User.objects.all()
        self.assertTrue(len(users) > 0) 