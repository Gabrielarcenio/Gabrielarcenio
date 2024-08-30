from django.test import TestCase, Client
from django.urls import reverse
from . import util

class EncyclopediaTests(TestCase):

    def setUp(self):
        """Configure o cliente de teste e adicione entradas iniciais."""
        self.client = Client()
        # Crie algumas entradas de teste
        util.save_entry("Python", "# Python\nPython é uma linguagem de programação poderosa.")
        util.save_entry("Django", "# Django\nDjango é um framework web para Python.")

    def test_index_page(self):
        """Testa se a página inicial é exibida corretamente."""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python")
        self.assertContains(response, "Django")

    def test_entry_page(self):
        """Testa se uma entrada específica é exibida corretamente."""
        response = self.client.get(reverse('entry', args=['Python']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python é uma linguagem de programação poderosa.")

    def test_entry_page_not_found(self):
        """Testa se uma mensagem de erro é exibida quando uma entrada não existe."""
        response = self.client.get(reverse('entry', args=['NonExistentPage']))
        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "A página solicitada não foi encontrada.")

    def test_search_exact_match(self):
        """Testa se a pesquisa exata redireciona para a página correta."""
        response = self.client.get(reverse('search'), {'q': 'Python'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python é uma linguagem de programação poderosa.")

    def test_search_partial_match(self):
        """Testa se a pesquisa parcial lista todas as entradas correspondentes."""
        response = self.client.get(reverse('search'), {'q': 'Py'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python")

    def test_create_new_page(self):
        """Testa se uma nova entrada pode ser criada corretamente."""
        response = self.client.post(reverse('new_page'), {
            'title': 'JavaScript',
            'content': '# JavaScript\nJavaScript é uma linguagem de programação de scripts.'
        })
        self.assertEqual(response.status_code, 302)  # Redirecionamento após criação
        # Verifica se a nova entrada aparece na página de visualização
        response = self.client.get(reverse('entry', args=['JavaScript']))
        self.assertContains(response, "JavaScript é uma linguagem de programação de scripts.")

    def test_edit_page(self):
        """Testa se uma entrada existente pode ser editada."""
        response = self.client.post(reverse('edit_page', args=['Python']), {
            'content': '# Python\nPython é uma linguagem incrível para ciência de dados.'
        })
        self.assertEqual(response.status_code, 302)  # Redirecionamento após edição
        # Verifica se o conteúdo editado aparece na página de visualização
        response = self.client.get(reverse('entry', args=['Python']))
        self.assertContains(response, "Python é uma linguagem incrível para ciência de dados.")

    def test_random_page(self):
        """Testa se a funcionalidade de página aleatória redireciona para uma entrada existente."""
        response = self.client.get(reverse('random_page'))
        self.assertEqual(response.status_code, 302)
        # Verifica se o redirecionamento é para uma página válida
        redirected_url = response.url
        self.assertTrue(redirected_url.startswith('/wiki/'))
        entry_title = redirected_url.split('/')[-2]
        # Verifica se o título da entrada existe
        self.assertIsNotNone(util.get_entry(entry_title))

def test_entry_page_not_found(self):
    """Testa se uma mensagem de erro é exibida quando uma entrada não existe."""
    response = self.client.get(reverse('entry', args=['NonExistentPage']))
    self.assertEqual(response.status_code, 404)
    self.assertContains(response, "A página solicitada não foi encontrada.", status_code=404)


