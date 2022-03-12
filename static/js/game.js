

$(document).ready(function() {
    

    $('form').submit(function(event) {
        
        event.preventDefault();

        var form = $(this);
        var actionUrl = form.attr('action');

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
        guessedWord()
    }
}

function guessedWord() {
    alert('Well done, you guessed the word. TODO...');
}
