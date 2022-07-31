from django.contrib import admin

from .models import Exam, ExamAttempts, Question, TargetExamType, User, Profile, Answer, Option
# Register your models here.

admin.site.register(User)
admin.site.register(TargetExamType)
admin.site.register(Profile)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Option)
admin.site.register(Exam)
admin.site.register(ExamAttempts)