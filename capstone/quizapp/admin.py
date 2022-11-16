from django.contrib import admin
from .models import Answer, Question, Quiz, Final, User
# Register your models here.


class AnswerInLine(admin.TabularInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInLine]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)

admin.site.register(Quiz)
admin.site.register(Final)
admin.site.register(User)

