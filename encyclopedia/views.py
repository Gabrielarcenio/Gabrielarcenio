from django.shortcuts import render, redirect
from markdown2 import Markdown
from . import util  # Importa o módulo util
import random

markdowner = Markdown()

def index(request):
    entries = util.list_entries()
    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })

def entry(request, title):
    content = util.get_entry(title)
    if content is None:
        # Retorna uma página de erro com status 404
        return render(request, "encyclopedia/error.html", {
            "message": "A página solicitada não foi encontrada."
        }, status=404)
    else:
        content_html = markdowner.convert(content)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content_html
        })


def search(request):
    query = request.GET.get('q')
    entries = util.list_entries()

    if query:
        if query in entries:
            return entry(request, query)
        
        matching_entries = [entry for entry in entries if query.lower() in entry.lower()]
        return render(request, "encyclopedia/search_results.html", {
            "entries": matching_entries,
            "query": query
        })
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": entries
        })

def new_page(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        # Verifica se a página já existe
        if util.get_entry(title):
            return render(request, "encyclopedia/error.html", {
                "message": "A página com este título já existe."
            })

        # Salva a nova entrada
        util.save_entry(title, content)

        # Redireciona para a nova entrada
        return redirect('entry', title=title)  # Certifique-se de que o redirecionamento está correto

    # Renderiza o formulário para criar uma nova página
    return render(request, "encyclopedia/new_page.html")

def edit_page(request, title):
    if request.method == "POST":
         # Se o formulário for enviado, salva as alterações
        content = request.POST.get("content")
        util.save_entry(title, content)
        return redirect('entry', title=title)
    # Se o método for GET, exibe o formulário com o conteúdo existente
    content = util.get_entry(title)
    return render(request, "encyclopedia/edit_page.html", {
        "title": title,
        "content": content
    })

def random_page(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return redirect('entry', title=random_entry)