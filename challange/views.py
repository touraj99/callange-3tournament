from django.shortcuts import render
import random
from .models import Member, UserAnswer, Question, Tournament, ResultMember
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from time import time
import datetime as dt


def home(request):
    datas = []
    datas2 = []
    datas3 = []
    cash = {}
    counter = 1
    isCorrect = [0, 0, 0]
    answerCounter = [0, 0, 0]
    allq = [0, 0, 0]
    TournamentIdObj1 = Tournament.objects.only('id').get(id=1)
    TournamentIdObj2 = Tournament.objects.only('id').get(id=2)
    TournamentIdObj3 = Tournament.objects.only('id').get(id=3)
    allMember = Member.objects.all()
    for member in allMember:
        memberIdObj = Member.objects.only('id').get(id=member.id)
        allUserAnswer = UserAnswer.objects.filter(member=memberIdObj).order_by('time')
        for answer in allUserAnswer:
            if answer.question.tournament.id == 1:
                answerCounter[0] += 1
                if answer.iscorrect:
                    isCorrect[0] += 1
                allq[0] = answer.question.tournament.howmany
            if answer.question.tournament.id == 2:
                answerCounter[1] += 1
                if answer.iscorrect:
                    isCorrect[1] += 1
                allq[1] = answer.question.tournament.howmany
            if answer.question.tournament.id == 3:
                answerCounter[2] += 1
                if answer.iscorrect:
                    isCorrect[2] += 1
                allq[2] = answer.question.tournament.howmany
        if answerCounter[0] != 0:
            cash["index"] = counter
            cash["name"] = member.name
            cash["phone"] = member.phone
            cash["pCode"] = member.personalCode

            cash["allQ"] = allq[0]
            cash["allA"] = answerCounter[0]
            cash["correctA"] = str(isCorrect[0])
            datas.append(cash)
            cash = {}
        if answerCounter[1] != 0:
            cash["index"] = counter
            cash["name"] = member.name
            cash["phone"] = member.phone
            cash["pCode"] = member.personalCode

            cash["allQ"] = allq[1]
            cash["allA"] = answerCounter[1]
            cash["correctA"] = isCorrect[1]
            datas2.append(cash)
            cash = {}
        if answerCounter[2] != 0:
            cash["index"] = counter
            cash["name"] = member.name
            cash["phone"] = member.phone
            cash["pCode"] = member.personalCode

            cash["allQ"] = allq[2]
            cash["allA"] = answerCounter[2]
            cash["correctA"] = isCorrect[2]
            datas3.append(cash)
            cash = {}
        isCorrect = [0, 0, 0]
        answerCounter = [0, 0, 0]
        allq = [0, 0, 0]
        cash = {}
        counter += 1
    context = {
        "datas": ResultMember.objects.filter(tournament=TournamentIdObj1),
        "datas2": ResultMember.objects.filter(tournament=TournamentIdObj2),
        "datas3": ResultMember.objects.filter(tournament=TournamentIdObj3),
    }
    return render(request, 'adminDashboard.html', context)


def tbl(request):
    return render(request, 'pages/tables/simple.html')


def loginPage(request):
    return render(request, 'login.html')


def sendCode(request):
    phone = request.POST['phone']
    frmt_date = dt.datetime.utcfromtimestamp(time()).strftime("%Y-%m-%d %H:%M:%S")
    isAvailable = Tournament.objects.filter(
                    end__gt=frmt_date,
                    start__lt=frmt_date
                    )
    if not isAvailable:
        return JsonResponse({"result": False, "status": 403}, status=403)
    else:
        try:
            user = Member.objects.get(phone=phone)
            code = random.randint(1000, 9999)
            user.verifcode = str(code)
            user.save()
            # todo send sms

            return JsonResponse({"result": True}, status=200)
        except Exception as e:
            return JsonResponse({"result": False}, status=400)


def checkCode(request):
    phone = request.POST['phone']
    code = request.POST['code']
    try:
        user = Member.objects.get(phone=phone, verifcode=code)
        if user.isadmin:
            return JsonResponse({"result": False}, status=400)
        else:
            login(request, user)
            return JsonResponse({"result": True}, status=200)
    except Exception as e:
        return JsonResponse({"result": False}, status=402)


@login_required(login_url='/login')
def tournament(request):
    context = {}
    try:
        # ? find last question user logined answered
        lastQuestionAnswerd = UserAnswer.objects.filter(member=request.user.id).order_by("-id")[0]
        # ? get question info with id
        lastQuestion = Question.objects.filter(id=lastQuestionAnswerd.question.id)
        if not lastQuestion:  # ? if not found question 0%
            context["data"] = "خطای 101 رخ داده است لطفا به مسئول مربوطه اطلاع دهید."
            return render(request, 'result.html', context)
        else:
            lastQuestion = lastQuestion[0]
            # ? if user compelete one tournament
            if lastQuestion.order == lastQuestion.tournament.howmany:
                # ? find valid tournament
                frmt_date = dt.datetime.utcfromtimestamp(time()).strftime("%Y-%m-%d %H:%M:%S")
                isAvailable = Tournament.objects.filter(
                                end__gt=frmt_date,
                                start__lt=frmt_date
                                )
                if not isAvailable:  # ? if not found valid tournament
                    context["data"] = "در حال حاضر مسابقه ای در جریان نیست.لطفا در زمان مقرر وارد شوید."
                    return render(request, 'result.html', context)
                else:
                    validTournament = isAvailable[0]
                    if lastQuestionAnswerd.question.tournament.id == validTournament.id:
                        context["data"] = "با موفقیت مسابقه با پشت سر گذاشتید در صورت قبولی در آزمون فعلی اطلاع رسانی برای مسابقه بعدی از طریق پیامک انجام خواهد شد."
                        return render(request, 'result.html', context)
                    userCanContinue = ResultMember.objects.filter(
                        member=request.user.id,
                        tournament=lastQuestionAnswerd.question.tournament.id
                        )
                    if not userCanContinue:  # ? if user not any result
                        context["data"] = "خطای 102 رخ داده است لطفا با بستن و باز کردن دوباره مرورگر تلاش فرمایید در صورت عدم رفع مشکل با مسئول مربوطه ارتباط حاصل فرمایید."
                        return render(request, 'result.html', context)
                    else:
                        resultMemberCanDo = userCanContinue[0]
                        if resultMemberCanDo.valid:  # ? user have min score?
                            # ? if lastquestion tournament id not equal to
                            # ? valid touranament id near 0%
                            if lastQuestionAnswerd.question.tournament.id != validTournament.id:
                                tournamentId = validTournament.id
                                order = 0
                            else:
                                if lastQuestionAnswerd.question.tournament.id == 3:
                                    context["data"] = "شما با موفقیت هر سه مسابقه را پشت سرگذاشتید.منتظر اعلام نتایج باشید."
                                    return render(request, 'result.html', context)
                                else:
                                    context["data"] = "خطای 103 رخ داده است لطفا به مسئول مربوطه اطلاع دهید."
                                    return render(request, 'result.html', context)
                        else:
                            context["data"] = "شما امتیاز لازم برای شرکت در مسابقه بعدی را ندارید."
                            return render(request, 'result.html', context)
            else:
                tournamentId = lastQuestion.tournament.id
                order = lastQuestion.order
        # ? if cant find next question || question of this tournament complete
        try:
            nextQuestion = Question.objects.get(
                            tournament=tournamentId,
                            order=order+1
                            )
            caseList = nextQuestion.cases.split("-")
            context = {
                "text": nextQuestion.text,
                "cases": caseList,
                "id": nextQuestion.id,
                "type": nextQuestion.type
            }
            return render(request, 'touranament.html', context)
        except Exception as e:
            context["data"] = "با موفقیت مسابقه با پشت سر گذاشتید در صورت قبولی در آزمون فعلی اطلاع رسانی برای مسابقه بعدی از طریق پیامک انجام خواهد شد."
            return render(request, 'result.html', context)
    except Exception as e:
        frmt_date = dt.datetime.utcfromtimestamp(time()).strftime("%Y-%m-%d %H:%M:%S")
        isAvailable = Tournament.objects.filter(
                        end__gt=frmt_date,
                        start__lt=frmt_date,
                        id=1
                        )
        if not isAvailable:
            context["data"] = "در حال حاضر مسابقه ای در جریان نیست.لطفا در زمان مقرر وارد شوید."
            return render(request, 'result.html', context)
        else:
            nowQuestion = Question.objects.get(tournament=1, order=1)
            caseList = nowQuestion.cases.split("-")
            context = {
                "text": nowQuestion.text,
                "cases": caseList,
                "id": nowQuestion.id,
                "type": nowQuestion.type
            }
            return render(request, 'touranament.html', context)


@login_required(login_url='/login')
def submitAnswer(request):
    if request.method == 'POST':
        questinId = request.POST['qid']
        answerText = request.POST['answer']
        try:
            # ? get question info
            questionFind = Question.objects.get(id=int(questinId))
            # ? get question object just id
            questionIdObj = Question.objects.only('id').get(id=int(questinId))
            # ? get tournament object just id
            TournamentIdObj = Tournament.objects.only('id').get(id=questionFind.tournament.id)
            # ? get member object just id
            memberIdObj = Member.objects.only('id').get(id=request.user.id)
            # ? cehck if correct
            validAnswerNotSpace = questionFind.answer.replace(" ", "")
            validAnswerNotDash = validAnswerNotSpace.replace("-", "")
            userAnswerNotSpace = answerText.replace(" ", "")
            userAnswerNotDash = userAnswerNotSpace.replace("-", "")
            if validAnswerNotDash == userAnswerNotDash:
                iscorrectVal = True
            else:
                iscorrectVal = False

            userAnswerObj = UserAnswer(
                ansewertext=answerText,
                iscorrect=iscorrectVal,
                member=memberIdObj,
                question=questionIdObj
            )
            userAnswerObj.save()

            try:
                hasResult = ResultMember.objects.get(
                    member=memberIdObj,
                    tournament=TournamentIdObj
                )

                resultMember = ResultMember.objects.filter(
                    member=memberIdObj,
                    tournament=TournamentIdObj
                )
                if iscorrectVal:
                    newCorrect = hasResult.all_answer_correct+1
                else:
                    newCorrect = hasResult.all_answer_correct
                if newCorrect >= questionFind.tournament.minpoint:
                    isvalidResult = True
                else:
                    isvalidResult = False
                resultMember.update(
                    all_answer=hasResult.all_answer+1,
                    all_answer_correct=newCorrect,
                    valid=isvalidResult
                )
            except Exception as e:
                resultMemberObj = ResultMember(
                    member=memberIdObj,
                    tournament=TournamentIdObj,
                    all_answer=1,
                    all_answer_correct=1,
                    valid=False
                )
                resultMemberObj.save()
            return JsonResponse({"result": True}, status=200)
        except Exception as e:
            return JsonResponse({"result": False}, status=400)
