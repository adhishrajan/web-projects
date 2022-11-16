from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from . import util
from markdown2 import Markdown
from django.urls import reverse
import random
from django import forms
from .forms import EditPageForm, NewForm, SearchForm


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    markdowner = Markdown()
    entry1 = util.get_entry(entry)
    if entry1 is None:
        return render(request, "encyclopedia/noEntry.html", {
            "entryTitle": entry
        })
    else:
        return render(request, "encyclopedia/entry.html",{
            "entry": markdowner.convert(entry1),
            "entryTitle": entry
        })

def search(request):
    #Get value that was submitted in search bar
    x = request.GET.get('q','')
    #If value searched is already an entry:
    if (util.get_entry(x) is not None):
        return HttpResponseRedirect(reverse("entry", kwargs= {'entry': x })) 
    else: 
        entryList = []
        for entry in util.list_entries():
            if x.upper() in entry.upper():
                entryList.append(entry)
        return render(request, "encyclopedia/search.html", {
            "entries": entryList,
            "search": True,
            "x": x
        })

def edit(request, entry):
    content = util.get_entry(entry.strip())
    if request.method == "POST":
        #Get new content in form
        content = request.POST.get("content").strip()
        #Save new content in form
        util.save_entry(entry, content)
        return redirect("entry", entry = entry) 
    return render(request, "encyclopedia/edit.html", {'content': content,'entryTitle': entry})


def newEntry(request):
    markdowner = Markdown()
    if request.method == "POST":
        entryNew = NewForm(request.POST) 
        if entryNew.is_valid():
            title = entryNew.cleaned_data["title"]
            body = entryNew.cleaned_data["body"]
            entries = util.list_entries()
            for entry in entries:
                #if entry already exists
                if entry.lower() == title.lower():
                    return render(request, "encyclopedia/newEntry.html", {
                        "form": SearchForm(),
                        "NewForm": NewForm(),
                        "error": "Entry Exists Already, please Retry"
                    })
            #Creating new entry and saving it
            newEntryTitle = "# " + title
            newEntryBody = "\n" + body
            newEntryFull = newEntryTitle + newEntryBody
            util.save_entry(title, newEntryFull)
            entry = util.get_entry(title)
            return render(request, "encyclopedia/newEntryShow.html", {
                "success": True,
                "title": title,
                "entry": markdowner.convert(entry),
                "form": SearchForm()
            })
    return render(request, "encyclopedia/newEntry.html", {
        "form": SearchForm(),
        "NewForm": NewForm()
    })

    
def entryFail(request):
     x = request.GET.get('q','')
     return render(request, "encyclopedia/noEntry.html", {
        "entryTitle": x 
    })

def randomPage(request):
    markdowner = Markdown()
    entryList = util.list_entries()
    entryChoice = util.get_entry(random.choice(entryList))
    return render(request, "encyclopedia/randomPage.html", {
        "randomPage": randomPage,
        "entryChoice": markdowner.convert(entryChoice)
    })
