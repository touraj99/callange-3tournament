from django.contrib import admin

from .models import Member, UserAnswer, Question, Tournament, ResultMember

admin.site.register(Member)
admin.site.register(UserAnswer)
admin.site.register(Question)
admin.site.register(Tournament)
admin.site.register(ResultMember)
