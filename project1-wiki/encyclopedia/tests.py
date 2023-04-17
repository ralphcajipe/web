from django.test import TestCase

# To run this test, run the following command:
# python manage.py test encyclopedia.tests

# Create your tests here.

class WikiTestCase(TestCase):
    def test_index(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'encyclopedia/index.html')
        self.assertContains(response, 'Django')

    def test_entry(self):
        response = self.client.get('/wiki/Django')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'encyclopedia/entry.html')
        self.assertContains(response, 'Django')
        
    def test_search(self):
        response = self.client.post('/search/', {'q': 'Django'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'encyclopedia/entry.html')
        self.assertContains(response, 'Django')
        
    def test_create(self):
        response = self.client.get('/create/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'encyclopedia/create.html')
        
    def test_edit(self):
        ...
        
    def test_random(self):
        ...
    def test_convert(self):
        ...
        
    def test_error(self):
        response = self.client.get('/wiki/Nonexistent')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'encyclopedia/error.html')
        self.assertContains(
            response, 'Sorry, but the page you requested could not be found.')

    

    