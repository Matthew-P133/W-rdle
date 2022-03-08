from django.shortcuts import render
from django.shortcuts import render,redirect
from wordgame.forms import UserForm
from django.urls import reverse
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from wordgame.models import Challenge, Statistics

# Create your views here.

def game(request):
    return render(request, 'wordgame/game.html')

def register(request):
    registered = False
    if request.method == 'POST': 
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(request,'wordgame/register.html',context = {'user_form': user_form,'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('wordgame:game'))
            else:
                return render(request,'wordgame/login.html',{'msg':'Your wordgame account is disabled.'})
        else:
            return render(request,'wordgame/login.html',{'msg':'Wrong username or password.'})
    else:
        return render(request, 'wordgame/login.html')

@login_required
def restricted(request):
    return render(request,'wordgame/restricted.html')

# Use the login_required() decorator to ensure only those logged in can
# access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return redirect(reverse('wordgame:game'))

def learderboard(request):
#     visitor_cookie_handler(request)
    list = ['-score', 'correct_rate', 'time_cost']
    Scoreboard = Statistics.objects.filter(visible = True).order_by(*list)
    return render(request, 'wordgame/leaderboard.html', {'Scoreboard': Scoreboard})

def show_learderboard(request):
    context_dict = {}

    try:
        score = Statistics.objects.get()
        context_dict['score'] = score
    except Statistics.DoesNotExist:
        context_dict['score'] = None
    return render(request, 'wordgame/leaderboard.html', context=context_dict)


def game(request):
    
    challenge = Challenge.objects.all()[0]

    context_dict = {'challenge': challenge}

    return render(request, 'wordgame/game.html', context=context_dict)

