from contextlib import nullcontext
import json
from itertools import zip_longest
from pickle import TRUE
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, AnonymousUser
from django.db.models import QuerySet
from django.forms import model_to_dict
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.views.generic import FormView, UpdateView, View

from wordgame.forms import UserForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from wordgame.models import Challenge, Statistics, Game, UserProfile, Dictionary
from .forms import UserProfileForm

from itertools import zip_longest
import re

# Create your views here.
def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        Pbbool = User.objects.filter(username = request.POST.get('username')).count()       
        if Pbbool >= 1:
            message = "This username has already been registered!"
            return render(request, 'wordgame/register.html',  context={'user_form': user_form,'message':message})
        if user_form.is_valid():
                user = user_form.save(commit=False)
                user.set_password(user.password)
                user.save()
                profile = UserProfile.objects.create(user = user)
                profile.save()

                user_statistics = Statistics.objects.get_or_create(user=user, next_challenge = Challenge.objects.all()[0])[0]
                user_statistics.save()

                registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(request, 'wordgame/register.html', context={'user_form': user_form,'registered': registered})

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            remember = request.POST.get('remember')
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:                
                    if not remember:
                        request.session.set_expiry(0)
                    login(request, user)
                    if str(request.user) == 'AnonymousUser':
                        username = 'Anonymous User'
                    else:
                        username = user.username
                    print('username',username)
                    return redirect(reverse('wordgame:game'), {'user': username})
                else:
                    return render(request, 'wordgame/login.html', {'msg': 'Your wordgame account is disabled.'})
            else:
                return render(request, 'wordgame/login.html', {'msg': 'Wrong username or password!'})
        return render(request, 'wordgame/login.html')
    else:
        return render(request, 'wordgame/restricted.html')

@login_required
def restricted(request):
    return render(request, 'wordgame/restricted.html')


# Use the login_required() decorator to ensure only those logged in can
# access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return redirect(reverse('wordgame:game'))


def leaderboard(request):
    if str(request.user) == 'AnonymousUser':
        data = {
			"user": "Anonymous User",
            "rank": 0,
            "score": 0,
            "avatar": 'photots/AnonymousUser.png'
        }
        return render(request, 'wordgame/leaderboard.html', data)
    queryset = list(Statistics.objects.all().order_by('-score'))
    statistics = Statistics.objects.get(user=request.user)
    try:
        userProfile = UserProfile.objects.get(user=request.user)
    except Exception:
        userProfile = UserProfile.objects.create(user=request.user)
    data = {
        "rank": queryset.index(statistics) + 1,
        "score": statistics.score,
        "avatar": userProfile.photo if userProfile.photo else 'photots/AnonymousUser.png'
    }

    return render(request, 'wordgame/leaderboard.html', data)



def get_leader_board(request):
    sort = request.GET.get('sort', None)
    queryset = Statistics.objects.filter(visible=True).order_by(sort)

    data_list = []
    for i in queryset:
        temp = model_to_dict(i)
        temp['name'] = User.objects.get(id=i.user_id).username
        data_list.append(temp)

    return JsonResponse({'data': data_list})


def game(request):

    # if not logged in the challenge given is always the same example
    if not request.user.is_authenticated:
        challenge = Challenge.objects.all()[0]
        context_dict = {'challenge': challenge, 'name': 'Anonymous User'}
        
    # user logged in so their next challenge is presented
    else:
        user = User.objects.get(username=request.user.username)
        user_statistics = Statistics.objects.get(user=user)
        challenge = user_statistics.next_challenge
        context_dict = {'challenge': challenge}

    # retain value of number_guesses cookie if reloading the same challenge, 
    # otherwise reset
    if not request.session.get('challenge'):
        request.session['challenge'] = challenge.id
    else:
        if challenge.id != request.session.get('challenge'):
            request.session['challenge'] = challenge.id
            request.session['number_guesses'] = 0

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
        id = request.POST['word_id']
        guess = request.POST['guess']
       
        # get current number of guesses from session COOKIE
        if not request.session.get('number_guesses'):
            request.session['number_guesses'] = 0
        
        number_guesses = request.session.get('number_guesses')
            
        # look up word from its ID
        word = Challenge.objects.filter(id=id)[0].word

        # cleanse input to be only A-Z
        word = re.sub(r'[^A-Z]', '', word.upper())
        guess = re.sub(r'[^A-Z]', '', guess.upper())

        # compare guess to target word
        output = validate(request, word, guess, number_guesses)

        number_guesses = request.session.get('number_guesses')

        # save result to database if game finished (and player is logged in)
        if output['game_finished']:
            user = request.user
            if user.is_authenticated:
                
                save_result(user, number_guesses, output['success'])
            request.session['number_guesses'] = 0

        if request.user.is_authenticated: 
            output['logged_in'] = 1
        else:
            output['logged_in'] = 0
        output['number_guesses'] = number_guesses

        return JsonResponse(output)


def validate(request, word, guess, number_guesses):

    # create dictionary for output
    formatting = []
    output = {'guess': guess, 'formatting': formatting}

    for i in range(12):
        formatting.append("grey")

    # check that not exceeded maximum number of guesses
    if number_guesses > 9:
        output['game_finished'] = True
        output['success'] = False
        for letter in word:
            output['guess']=word
            formatting.append('red')
        return output

    output['game_finished'] = False

    # checks if a valid English word has been entered
    if not Dictionary.objects.filter(word=guess):
        output['valid_word'] = False
        output['success'] = False
        return output

    output['valid_word'] = True
    request.session['number_guesses'] += 1

    # count the number of appearances of each letter in the target word
    letters = {}

    for letter in word:
        if letter in letters:
            letters[letter] = letters[letter] + 1
        else:
            letters[letter] = 1

    # first, highlight correctly placed letters in green
    for index, pair in enumerate(zip_longest(word, guess)):
        if pair[0] == pair[1]:
            formatting[index] = "green"
            letters[pair[1]] = letters[pair[1]] - 1
        
    # next highlight incorrectly placed, but present, letters in orange
    # if appropriate to do so (avoid highlighting a letter more times than 
    # it appears in the target)
    for index, pair in enumerate(zip_longest(word, guess)):
        if formatting[index] == "grey":
            if (pair[1] and pair[1] in word and letters[pair[1]] > 0):
                formatting[index] = "orange"
                letters[pair[1]] = letters[pair[1]] - 1

    if word == guess:
        output['success'] = True
        output['game_finished'] = True
    else:
        output['success'] = False

    return output


def save_result(user, number_guesses, success):

    # updates models (e.g. after a game has been completed)

    user_statistics = Statistics.objects.get(user=user)
    challenge = user_statistics.next_challenge
    challenge_ID = challenge.id

    game = Game.objects.get_or_create(user=user, challenge=challenge)[0]
    game.successful = success
    game.guesses = number_guesses
    game.save()


    if (success):
        user_statistics.games_won += 1
        user_statistics.win_streak += 1

    else:
        user_statistics.games_lost += 1
        user_statistics.win_streak = 0

    user_statistics.next_challenge = Challenge.objects.get(id=challenge_ID+1)
    user_statistics.save()

    

    challenge.timesPlayed = challenge.timesPlayed + 1
    if (success):
        challenge.successes += 1
    else:
        challenge.failures += 1
    challenge.save()


