from django.shortcuts import render
QUESTIONS = [
    {
        "title": f"Title #{i}",
        "text": f"This is text for question #{i}",
        "number": i,
        "likes": i
    } for i in range(10)
]
TAGS = [
    {
        "name": f"Tag#{i}",
        "number": i
    } for i in range(10)
]
def index(request):
    return render(request, "index.html", {"questions": QUESTIONS})

def ask(request):
    return render(request, "ask.html")

def auth(request):
    return render(request, "auth.html")

def reg(request):
    return render(request, "reg.html")

def hot(request):
    return render(request, "hot.html", {"questions": QUESTIONS})

def question(request, i:int):
    return render(request, "question_page.html", {"question": QUESTIONS[i]})

def tags(request):
    return render(request, "inc/tags.html",{"tags": TAGS})
