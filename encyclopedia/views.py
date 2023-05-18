from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django import forms
import random
import markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": [entry for entry in util.list_entries()] # list of entries
    })


def entry_detail(request, entry):
    content = util.get_entry(entry) # gets md file

    if content is None: # checks entry validity, 404 if doesn't exist
        raise Http404("Entry doesn't exist")

    html_content = markdown.markdown(content) # converts md to html

    return render(request, "encyclopedia/entry_detail.html", {
        "entry": entry,
        "content": html_content,
    })


def search(request):
    query = request.GET.get('q', '') # get query

    entry = util.get_entry(query) # get matching encyclopedia query
    if entry:
        return redirect('entry_detail', entry=query) # redirect to query page
    else:
        matches = [entry for entry in util.list_entries() if query.lower() in entry.lower()] # list of matches

        return render(request, "encyclopedia/search.html", { 
            "query": query,
            "entries": matches,
        })
    

class NewPageForm(forms.Form): # makes a new page form that inherits from forms
    title = forms.CharField(label="Title") 
    content = forms.CharField(label="Content", widget=forms.Textarea) 

class EditPageForm(forms.Form):
    content = forms.CharField(label="Content", widget=forms.Textarea) 

def create_page(request):
    if request.method == 'POST': 
        form = NewPageForm(request.POST) # make form object

        if form.is_valid(): # check validity of form 
            title = form.cleaned_data["title"] 
            content = form.cleaned_data["content"] 

            if util.get_entry(title) is not None: # check if title exists
                return render(request, "encyclopedia/error.html", {
                    "message": "An entry with that title already exists."
                })
            
            util.save_entry(title, content) # save entry

            return redirect('entry_detail', entry=title)
        
    else: # get method
        form = NewPageForm()

        return render(request, "encyclopedia/create_page.html", {
            "form": form
        })
    

def edit_page(request, entry):
    content = util.get_entry(entry)

    if request.method == 'POST':
        form = EditPageForm(request.POST) # make edit form object
        if form.is_valid(): # check validity of form
            new_content = form.cleaned_data["content"] # select new content
            util.save_entry(entry, new_content) # save edited file
            return redirect("entry_detail", entry=entry)    
    else:
        form = EditPageForm(initial={"content": content})

    return render(request, "encyclopedia/edit_page.html", {
        "entry": entry,
        "form": form,
    })


def random_page(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return redirect('entry_detail', entry=random_entry)