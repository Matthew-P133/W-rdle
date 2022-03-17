

$(document).ready(function() {

    // reset guesses to 0 for new word
    $('#number_guesses').val(0)


    $('#show_hint').hover(
        function() {
            $('#cheat').show()
        }, function() {
            $('#cheat').hide()
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
                console.log(response);
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

    var game_end_message = "";    

    // append new message or display prompt
    if (game_finished) {
        if (valid) {
            update_game_grid(response);
            game_end_message += "Well done, you got " + guess + " in " +  $('#number_guesses').attr('value') + " guess(es).";
        } else {
            update_game_grid(response);
            game_end_message += "Oh dear. You ran out of guesses. The word was: " + guess + ".";
        }
        finish_game(logged_in, game_end_message)
    } else {
        if (valid) {
            update_game_grid(response);
        } else {
            alert("That's not a word! Please try again.");
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
    var number_guesses = parseInt($('#number_guesses').attr('value'))

    // currently displayed guesses
    messageString = $('#guesses').html();

    // update the number of guesses. (TODO - use a COOKIE for this instead)
    $('#number_guesses').val(number_guesses + 1)

    var messageAppend = '';
    for (i = 0; i < guess.length; i++) {
        messageAppend += '<span style="color:' + formatting[i] + '">' + guess.substring(i, i+1) + '</span>';
    }
    messageString = messageString + messageAppend + '<br>'

    // update display
    $('#guesses').html(messageString); 

    // clear form ready for new guess
    $('#guess').val("");
}
