// {% csrf_token %}
$(document).ready(function () {
    $('#verifCode').css('display','none');

    $('#sendCode').on('click', function() {
        if ($(this).html() == "ارسال کد") {
            var phone = $('#phone').val();
            $.ajax({
                url: 'challenge/sendCode',
                type: 'POST',
                headers: { 'X-CSRFToken': $("input[name='csrfmiddlewaretoken']").val() },
                dataType: 'json',
                data: {
                    phone: phone
                },
                success: function (response) {
                    if (response.result) {
                        $('#verifCode').css('display', 'block');
                        $('#sendCode').html("تایید کد");
                        $('.timer').startTimer();
                    }else{
                        alert("error");
                    }
                },
                error: function (response) {
                    if (response.status == 403) {
                        alert("در حال حاضر مسابقه ای برگزار نمیشود.")
                    } else {
                        alert("خطایی رخ داده لطفا با مسئول مربوطه تماس حاصل فرمایید.");
                    }
                }
            });
        } else if ($(this).html() == "تایید کد"){
            var phone = $('#phone').val();
            var code = "";
            for (let index = 1; index < 5; index++) {
                code += $('#validCode' + index).val();
            }
            $.ajax({
                url: 'challenge/checkCode',
                type: 'POST',
                headers: { 'X-CSRFToken': $("input[name='csrfmiddlewaretoken']").val() },
                dataType: 'json',
                data: {
                    phone: phone,
                    code: code
                },
                success: function (response) {
                    if (response.valid) {
                        location.href = "/adminDashboard/1";    
                    }else{
                        location.href = "/questions";
                    }
                },
                error: function (response) {
                    alert("کد اشتباه است.");
                }
            });
        }
    });
    $('#continue').on('click', function () {
        var answer ="";
        var qid = $('#qid').val();
        var inputType = $('.answers');
        if (inputType.attr('type')=="radio") {
            answer = $('input[name=answers]:checked').val();
        }else{
            $("input[name='answers[]']:checked").each(function () {
                answer += $(this).val() + "-";
            });
        }

        $.ajax({
            url: 'submitanswer',
            type: 'POST',
            headers: { 'X-CSRFToken': $("input[name='csrfmiddlewaretoken']").val() },
            dataType: 'json',
            data: {
                qid: qid,
                answer: answer
            },
            success: function () {
                location.reload();
            },
            error: function () {
                alert("خطای سیستمی");
            }
        });
    });
    
    $('#resendCode').on('click', function(){
        var phone = $('#phone').val();
        $.ajax({
            url: 'challenge/resendCode',
            type: 'POST',
            headers: { 'X-CSRFToken': $("input[name='csrfmiddlewaretoken']").val() },
            dataType: 'json',
            data: {
                phone: phone
            },
            success: function (response) {
                if (response.result) {
                    $("#mainBtn").removeClass("col-7");
                    $("#mainBtn").addClass("col-10");
                    $('#resendBtn').css('display', 'none');
                    $('.timer').empty();
                    $('.timer').startTimer();
                } else {
                    alert("error");
                }
            },
            error: function (response) {
                if (response.status == 403) {
                    alert("در حال حاضر مسابقه ای برگزار نمیشود.")
                } else {
                    alert("خطایی رخ داده لطفا با مسئول مربوطه تماس حاصل فرمایید.");
                }
            }
        });
    });

    jQuery(".validCode").on('keyup', function (e) {
        var pressedKey = e.key;
        var codeindex = e.currentTarget.attributes.codeindex.value;
        if (pressedKey == 'Backspace' || pressedKey == 'Delete') {
            jQuery(this).val('');
            if (codeindex > 1) {
                codeindex--;
                jQuery(".validCode[codeindex='" + codeindex + "']").focus();
            }
        } else {
            codeindex++;
            var el = jQuery(".validCode[codeindex='" + codeindex + "']").get(0);
            el.focus();
            el.setSelectionRange && el.setSelectionRange(0, 0);
        }
    });
});