//$(document).ready(function() {
//$('#guesses').text('');
//});

$(document).ready(function() {
    

    $('#check_btn').click(function() {
        var word;
        word = $(this).attr('data-word');
        var guess = $('#guess').val();
        console.log(guess);

        $.get('/wordgame/check_guess/', {'word': word, 'guess': guess}, function(data) {
            var msg = $('#guesses').html();

            $('#guesses').html(msg + '<br>' + data);
        })

    });

    // disable enter so that user cannot submit form directly
    $(document).keypress(
        function(event){
          if (event.which == '13') {
            event.preventDefault();
          }
      });

});