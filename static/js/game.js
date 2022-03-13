

$(document).ready(function() {

    $('#number_guesses').val(0)
    
    // when user presses check guess
    $('form').submit(function(event) {
        
        // stop the default event
        event.preventDefault();

        // get information
        var form = $(this);
        var actionUrl = form.attr('action');

        // update the number of guesses. (TODO - use a COOKIE for this instead)
        var number_guesses = parseInt($('#number_guesses').attr('value'))
        $('#number_guesses').val(number_guesses + 1)

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

    // currently displayed guesses
    messageString = $('#guesses').html();

    // extract information from ajax response
    var guess = response.guess;
    var success = response.success;
    var formatting = response.formatting;

    // append new message
    var messageAppend = '';
    for (i = 0; i < guess.length; i++) {
        messageAppend += '<span style="color:' + formatting[i] + '">' + guess.substring(i, i+1) + '</span>';
    }
    messageString = messageString + messageAppend + '<br>'

    // update display
    $('#guesses').html(messageString); 

    if (success) {
        var logged_in = parseInt(response.logged_in);
        guessedWord(logged_in)
    }
}

function guessedWord(logged_in) {
    if (logged_in) {
        if(alert('Well done, you got it in ' +  $('#number_guesses').attr('value') + ' guess(es)! Reload the page to try the next game.' )) {}
        else window.location.reload();
    } else {
        if(alert('Well done, you got it in ' +  $('#number_guesses').attr('value') + ' guess(es)! Log in to play other challenges.')) {}
        else window.location.reload();
    }
}
