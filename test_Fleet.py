from django.test import SimpleTestCase

class SimpleTests(SimpleTestCase):

    def atest_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def atest_home_page_contains_connect_html(self):
        response = self.client.get('/')
        self.assertContains(response, 'Hello World!')



