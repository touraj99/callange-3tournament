$(document).ready(function () {
    $('#verifCode').css('display','none');

    $('#sendCode').on('click', function() {
        if () {
            $('#verifCode').css('display', 'block');
            $(this).html("تایید کد");
            alert('alert');
            $('.timer').startTimer();
        } else if ($(this).html() == "تایید کد"){
            $.ajax({
                async: false,
                url: 'challenge/sendCode',
                type: 'POST',
                global: false,
                dataType: 'json',
                data: {
                    userid: userSelected,
                    ccode: coupon
                }
            }).done(function (response) {
                if (response.success) {
                    
                }
                else {
        
                }
            }).fail(function (failCallbacks) {
                console.log(failCallbacks);
            });

        }
        

    });
});