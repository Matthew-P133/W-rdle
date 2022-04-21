# W[]rdle 

## Introduction

A simple word-guessing game drawing inspiration from the popular online puzzle game Wordle.     

- Play a daily W[]rdle challenge: just like Wordle, but - you guessed it – the word can be any length.
- See how your skills stack up against other players: how did someone get *that* in 3 guesses!
- See your stats: make an account to view your statistics and current streak.
- Aim for glory: check how you stack up against other players on the Leaderboard.

The game is designed to be as intuitive as possible, but for further instructions see the game rules on the game page. 

## Design and Technologies

W[]rdle is built using a simple three-tier system architecture: a client (the user's browser) which displays HTML, CSS and JavaScript content; a Python/Django middleware which dynamically generates this content and interacts with the database; and a SQLite3 database to store relevant information.

When you enter a guess, the game uses JQuery and AJAX to send the guess to the server. The server then validates this guess, and returns a JSON object describing how to display the results of the guess to the user. If the guess has completed the game, the databse is updated to reflect this.

Cheating by making a number of guesses to narrow down the target and then refreshing the page in an attempt to reset the number of guesses to zero is prevented by use of a server side COOKIE to store the current number of guesses.

In the interests of expedited testing (and because the game turned out considerably harder than we anticipated) a cheat button has been included in the game rules - we are in no way liable for any damage to conscience resulting from its use.

## Usage

The application can be deployed as a Django web application.

First install dependencies. Run:

```
pip install -r requirements.txt
```

Next perform database setup and population, and perform unit tests. Run the following from the directory containing manage.py:

```
python manage.py makemigrations
python manage.py migrate
python populate_wordgame.py
python manage.py test
```

Finally, run the application on localhost:

```
python manage.py runserver
```

The application is hosted at https://matthewp133.eu.pythonanywhere.com/wordgame/ at the time of writing.

## Other notes

This web application was designed and built as part of the Internet Technology course at the University of Glasgow.

This game was built purely as an educational exercise and is in no way intended to impinge upon Wordle or any of its many existing variants.

The wordlist used to check if a guess is a valid english word was adapted from the wordlist at http://www-personal.umich.edu/~jlawler/wordlist
