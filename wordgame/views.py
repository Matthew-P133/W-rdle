from itertools import zip_longest
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render
from django.shortcuts import render,redirect
from django.views.generic import FormView, UpdateView, View

from wordgame.forms import UserForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from wordgame.models import Challenge, Statistics, Game
from .forms import UserProfileForm

from itertools import zip_longest
import re

# Create your views here.



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

def leaderboard(request):
    list = ['-score', 'games_played', 'games_won']
    Scoreboard = Statistics.objects.filter(visible = True).order_by(*list)
    return render(request, 'wordgame/leaderboard.html', {'Scoreboard': Scoreboard})

# def show_leaderboard(request):
#     context_dict = {}

#     try:
#         score = Statistics.objects.get()
#         context_dict['score'] = score
#     except Statistics.DoesNotExist:
#         context_dict['score'] = None
#     return render(request, 'wordgame/leaderboard.html', context=context_dict)


def game(request):
    
    # if not logged in the challenge given is always the same example
    if not request.user.is_authenticated:
        challenge = Challenge.objects.all()[0]
        context_dict = {'challenge': challenge}
        return render(request, 'wordgame/game.html', context=context_dict)
        
    # user logged in so their next challenge is presented
    else:
        user = User.objects.get(username=request.user.username)
        user_statistics = Statistics.objects.get(user=user)
        challenge = user_statistics.next_challenge
        context_dict = {'challenge': challenge}
        return render(request, 'wordgame/game.html', context=context_dict)

class UserProfileView(LoginRequiredMixin, UpdateView):
    form_class = UserProfileForm
    template_name = 'wordgame/userprofile.html'
    model = User
    success_url = reverse_lazy('wordgame:userprofile')

    def get_object(self, queryset=None):
        instance = self.request.user
        if self.request.method == 'GET':
            instance.password = None
        return instance

    def get_initial(self):
        initial = super(UserProfileView, self).get_initial()
        initial['photo'] = self.request.user.userprofile.photo
        initial['sex'] = self.request.user.userprofile.sex
        return initial

    def form_valid(self, form):
        # print(self.request.method)
        self.request.user.refresh_from_db()
        o_password = self.request.user.password
        instance = form.save(commit=False)
        print(form.cleaned_data)
        if not form.cleaned_data['password']:
            instance.password = o_password
        else:
            instance.set_password(form.cleaned_data['password'])
        instance.email = form.cleaned_data['email']
        instance.username = form.cleaned_data['username']
        instance.save()
        profile = self.request.user.userprofile
        profile.sex = form.cleaned_data['sex']
        profile.photo = form.cleaned_data['photo']
        profile.save()
        return redirect(self.get_success_url())

class CheckGuessView(View):
    def post(self, request):
        # extract information from request
        word = request.POST['word']
        guess = request.POST['guess']
        number_guesses = int(request.POST['number_guesses'])

        # cleanse input to be only A-Z
        word = re.sub(r'[^A-Z]', '', word.upper())
        guess = re.sub(r'[^A-Z]', '', guess.upper())

        # compare guess to target word
        output = validate(word, guess)

        # save result to database if player was successful (and is logged in)
        if output['success']:
            user = request.user
            if user.is_authenticated:
                save_result(user, number_guesses)

        if request.user.is_authenticated: 
            output['logged_in'] = 1
        else:
            output['logged_in'] = 0

        return JsonResponse(output)

def validate(word, guess):

    formatting = []
    output = {'guess': guess, 'formatting':formatting}

    for pair in zip_longest(word, guess):
        if pair[0] == pair[1]:
                formatting.append('green')
        else:
            if (pair[1] and pair[1] in word):
                formatting.append('yellow')
            else:
                if (pair[1]):
                    formatting.append('grey')

    if word == guess:
        output['success'] = True
    else:
        output['success'] = False 

    # TODO if successful guess, update database

    return output

def save_result(user, number_guesses):

    user_statistics = Statistics.objects.get(user=user)
    challenge = user_statistics.next_challenge
    challenge_ID = challenge.id

    user_statistics.games_won += 1
    user_statistics.win_streak += 1
    user_statistics.next_challenge = Challenge.objects.get(id=challenge_ID+1)
    user_statistics.save()

    game = Game.objects.get_or_create(user=user, challenge=challenge)[0]
    game.successful = True
    game.guesses = number_guesses
    game.save()
