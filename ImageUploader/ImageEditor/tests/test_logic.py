from django.test import TestCase
from ..core.views import get_image_by_url, get_image_size
from ..core.models import Img


class LogicTestCase(TestCase):
    def get_image_url_test(self):
        image_url = 'https://itblog21.ru/wp-content/uploads/2020/02/jpg_jpeg01.jpg'
        result = get_image_by_url(image_url)
        self.assertEqual(Img.objects.filter(name="jpg_jpeg01.jpg", image=True), result)