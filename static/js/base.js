$(document).ready(function () {
    $('ul').find('a').each(function () {
            if (this.href == document.location.href) {
                $(this).css({"background-color":"rgb(8, 157, 184)","border-radius":"30px"}); 
                $(this).hover(function(){
                $(this).css("color","black");
                },function(){
                $(this).css("color","white");
            });
            }
        });
    
});