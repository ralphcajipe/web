from django.shortcuts import render
from . import util

import markdown2
import random


def convert_md_to_html(title):
    """
    Convert the Markdown content of the given entry title to HTML.
    If the entry doesn't exist, return None.
    """
    content = util.get_entry(title)
    if content is None:
        return None
    else:
        to_markdown = markdown2.Markdown()
        return to_markdown.convert(content)


def index(request):
    """
    Render the index page with a list of all encyclopedia entries.
    """
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    """
    Render the page for the given entry title.
    If the entry doesn't exist, render the error page.
    """
    content = convert_md_to_html(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "Sorry, but the page you requested could not be found."
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content
        })


def search(request):
    """
    Render the search result page with a list of entries that contain the query.
    If an exact match is found, render the page for that entry.
    """
    if request.method == "POST":
        query = request.POST.get("q")
        content = convert_md_to_html(query)
        if content is not None:
            return render(request, "encyclopedia/entry.html", {
                "title": query,
                "content": content
            })
        else:
            entries = util.list_entries()
            recomendations = [
                entry for entry in entries if query.lower() in entry.lower()]
            return render(request, "encyclopedia/result.html", {
                "recomendations": recomendations
            })


def create(request):
    """
    Render the create page to allow users to create a new entry.
    If a page with the same title already exists, render the error page.
    """
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        if title in util.list_entries():
            return render(request, "encyclopedia/error.html", {
                "message": "Sorry, but the page you requested already exists."
            })
        else:
            util.save_entry(title, content)
            content = convert_md_to_html(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": content
            })
    return render(request, "encyclopedia/create.html")


def edit(request):
    """
    Render the edit page to allow users to edit an existing entry.
    """
    if request.method == "POST":
        title = request.POST.get("title")
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })


def save(request):
    """
    Save the edited content of an entry and render the page for that entry.
    """
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        util.save_entry(title, content)
        new_content = convert_md_to_html(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": new_content
        })


def rand(request):
    """
    Render a random entry page.
    """
    entries = util.list_entries()
    entry = random.choice(entries)
    content = convert_md_to_html(entry)
    return render(request, "encyclopedia/entry.html", {
        "title": entry,
        "content": content
    })
