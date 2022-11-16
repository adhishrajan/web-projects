from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Answer, Question, Quiz, Final, User, Follower
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
# Create your views here.

def index(request):
    #View for home page (active listings)
    return render(request, "quizapp/index.html")


def unfollow(request, username):
    user = User.objects.get(username=username)
    request.user.unfollow(user)
    return redirect('myquizzes', username)



def follow(request, username):
    user = User.objects.get(username=username)
    request.user.follow(user)
    return redirect('myquizzes', username)  


def newquiz(request):
    if request.method == "POST":
        #Assigning data from the form to the Lis model
        quiz1 = Quiz()
        quiz1.creator = request.user.username
        quiz1.name = request.POST.get('name')
        quiz1.subject = request.POST.get('subject')
        quiz1.questionamt = request.POST.get('questionamt')
        quiz1.passingscore = request.POST.get('passingscore')
        quiz1.difficulty = request.POST.get('difficulty')
        quiz1.time = request.POST.get('time')
        quiz1.bestscore = 0
        quiz1.bestscoreuser = "N/A"
        quiz1.save(Quiz)
        a = Quiz.objects.latest('pk').questionamt
        for i in range(a): 
            question1 = Question()
            question1.quiz = Quiz.objects.latest('pk')
            question1.body = request.POST.get(f'body{i}')
            question1.save(Question)
            answer1 = Answer()
            answer1.question = Question.objects.latest('timemade')
            answer1.body = request.POST.get(f'abody1{i}')
            if request.POST.get(f'correct1{i}'):
                answer1.correct = True
            else:
                answer1.correct = False
            answer2 = Answer()
            answer2.question = Question.objects.latest('timemade')
            answer2.body = request.POST.get(f'abody2{i}')
            if request.POST.get(f'correct2{i}'):
                answer2.correct = True
            else:
                answer2.correct = False
            answer3 = Answer()
            answer3.question = Question.objects.latest('timemade')
            answer3.body = request.POST.get(f'abody3{i}')
            if request.POST.get(f'correct3{i}'):
                answer3.correct = True
            else:
                answer3.correct = False
            answer3.save(Answer)
            answer2.save(Answer)
            answer1.save(Answer)
        
    else: 
        return render(request, "quizapp/newquiz.html")
    quizzes = Quiz.objects.all()
    return redirect('quizlist')

#View for profile page
def myquizzes(request, username):
    try:
        user = User.objects.get(username=username)
        quizzes = Quiz.objects.filter(creator=user)
        paginator = Paginator(quizzes, 10) # Show 10 contacts per page.   
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        followings = user.following.all()
        followers = user.followers.all()
        folcount = len(followers)
        quizcount = len(quizzes)
        folingcount = len(followings)
        followed = False
        empty = True
        if len(quizzes) > 0:
            empty = False
        for fer in followers:
            if request.user.username == fer.follower.username:
                followed = True
    except ObjectDoesNotExist:
        return render(request, "quizapp/dne.html")
    return render(request, "quizapp/myquizzes.html", {
        "username": username,
        "quizzes": quizzes,
        "followings": followings,
        "followers": followers,
        "followed": followed,
        "folcount": folcount,
        "quizcount": quizcount,
        "folingcount": folingcount,
        "empty": empty,
        "page_obj": page_obj
    })

  



def quizlist(request):
    quizzes = Quiz.objects.all().order_by('-timestamp')
    empty = False
    if len(quizzes) == 0:
        empty = True
    return render(request, "quizapp/quizlist.html", {
        "quizzes": quizzes,
        "empty": empty
    })

def save(request, quiz_pk):
    # if we are dealing with an ajax request
    if request.is_ajax():
        qs = []
        data = request.POST
        #transform queryDict to ordinary Dict
        data1 = dict(data.lists())
        # deleting csrf middleware token
        data1.pop('csrfmiddlewaretoken')
        # loop thru each queestion
        for i in data1.keys():
            print('key: ', i)
            q = Question.objects.get(body=i)
            qs.append(q)
        print(qs)


        user = request.user
        quiz = Quiz.objects.get(pk=quiz_pk)

        score = 0
        multiplier = 100 / quiz.questionamt
        results = []
        correctans = None
        #grabbing which answer was selected
        for j in qs:
            selected = request.POST.get(j.body)
            
            # check if answer was even selected
            if selected != "":
                answers = Answer.objects.filter(question=j)
                for k in answers:
                    # if the answer selected was one of the available answers
                    if selected == k.body:
                        # if answer is correct incrememnt score
                        if k.correct:
                            score = score + 1
                            correctans = k.body
                    elif k.correct:
                        correctans = k.body
                
                results.append({str(j): {'correct answer': correctans, 'answered': selected}})
            # if no answer was selected
            else: 
                results.append({str(j): 'not answered'})

        score1 = score * multiplier
        # if this is not the first time taking quiz, delete previous score
        if not Final.objects.filter(user=user, quiz=quiz).count() == 0:
            # if new score is better than previous score
            if Final.objects.get(user=user, quiz=quiz).score < score1:
                Final.objects.get(user=user, quiz=quiz).delete()
                Final.objects.create(quiz=quiz, user=user, score=score1)
        else:
            Final.objects.create(quiz=quiz, user=user, score=score1)  

        finals = Final.objects.filter(quiz=quiz)
        highscoreuser = None
        highscore = 0
        for final in finals:
            if final.score > highscore:
                highscore = final.score
                highscoreuser = final.user

        qqq = Quiz.objects.get(pk=quiz_pk)
        qqq.bestscore = highscore
        qqq.bestscoreuser = highscoreuser
        qqq.save()

        if score1 >= quiz.passingscore:
            return JsonResponse({'passed': True, 'score': score1, 'results': results})
        else:
            return JsonResponse({'passed': False, 'score': score1, 'results': results})


@login_required
def taken(request, username):
    user = User.objects.get(username=request.user.username)
    finals = Final.objects.filter(user=username)
    quizzes = []
    finalss = []
    for final in finals:
        f = final.quiz
        quizzes.append(f)
        finalss.append(final)
    empty = False
    if len(quizzes) == 0:
        empty = True
    paginator = Paginator(finalss, 10) # Show 10 contacts per page.   
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "quizapp/taken.html", {
        "page_obj": page_obj,
        "empty": empty,
        "finals": finalss,
    })
    



@login_required
def following(request, username):
    #View of posts made by users that the user follows
    user = User.objects.get(username=request.user.username)    
    followings = Follower.objects.filter(follower=user)
    quizzes1 = []
    for f in followings:
        quizzes = Quiz.objects.filter(creator=f.following)
        for quiz in quizzes:
            quizzes1.append(quiz)
    if len(quizzes1) == 0:
        empty = True
    else:
        empty = False
    paginator = Paginator(quizzes1, 10) # Show 10 contacts per page.   
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "quizapp/following.html", {
        "quizzes": quizzes1,
        "page_obj": page_obj,
        "empty": empty
    })

def quiz_view(request, quiz_pk):
    quiz = Quiz.objects.get(pk=quiz_pk)
    return render(request, 'quizapp/quiz.html', {
        'quiz': quiz
        
    })

def quiz_viewcont(request, quiz_pk):
    quiz = Quiz.objects.get(pk=quiz_pk)
    questions = []
    for i in quiz.getQuestions():
        answers = []
        for j in i.getAnswer():
            answers.append(j.body)
        # assigning a list of answers to a question
        questions.append({str(i): answers})
    return JsonResponse({
        'data': questions,
        'time': quiz.time
    })



def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "quizapp/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "quizapp/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "quizapp/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "quizapp/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "quizapp/register.html")

