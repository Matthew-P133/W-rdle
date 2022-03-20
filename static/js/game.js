

$(document).ready(function() {


    // displays word if the user gets stuck
    $('#show_hint').click(
        function() {
            $('#cheat').css('display', 'block')
        }
    );

    // when user presses check guess
    $('form').submit(function(event) {
        
        // stop the default event
        event.preventDefault();

        // get information
        var form = $(this);
        var actionUrl = form.attr('action');

        // send request to back end
        $.ajax({
            type: 'POST',
            url: actionUrl,
            data: form.serialize(),
            dataType: 'json',
            success: function(response) {
                display(response);
            }
        })
    });
}); 

// update the game display
function display(response) {

    // extract information from ajax response
    var valid = response.valid_word;
    var logged_in = parseInt(response.logged_in);
    var game_finished = response.game_finished;
    var guess = response.guess;
    var number_guesses = response.number_guesses;

    var game_end_message = "";    

    // append new message or display prompt
    if (game_finished) {
        if (valid) {
            update_game_grid(response);
            game_end_message += "Well done, you got " + guess + " in " +  number_guesses + " guess(es).";
        } else {
            update_game_grid(response);
            game_end_message += "Oh dear. You ran out of guesses. The word was: " + guess + ".";
        }
        finish_game(logged_in, game_end_message)
    } else {
        if (valid) {
            update_game_grid(response);
        } else {
            alert("Sorry, that word isn't in my dictionary! Please try again.");
        }
    }  
}

function finish_game(logged_in, message) {
    if (logged_in) {
        if(alert( message + "\r\nPress OK to try the next game.")) {}
        else window.location.reload();
    } else {
        if(alert( message + "\r\nLog in to play other challenges.")) {}
        else window.location.reload();
    }
}

function update_game_grid(response) {

    // get information from response
    var guess = response.guess;
    var formatting = response.formatting;
   

    var messageAppend = '<div class="gamerow">';
    for (i = 0; i < guess.length; i++) {

        messageAppend += '<div class="tile" style="color: ' + formatting[i] + '">' + guess.substring(i, i+1) + '</div>';
        
    }
    for (i = guess.length; i < 12; i++) {
        messageAppend += '<div class="tile" style="color: grey">' + '-' + '</div>';
    }

    messageAppend += '</div>';

    // update display
    $('.gamegrid#game').append(messageAppend);

    // clear form ready for a new guess
    $('#guess').val("");
}
