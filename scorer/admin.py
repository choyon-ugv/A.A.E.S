from django.contrib import admin

from .models import Question, TakeTest,Evaluation,StudentMarks

admin.site.register(Question)

@admin.register(TakeTest)
class TestAdmin(admin.ModelAdmin):
    list_display = ['title','status','duration']

@admin.register(StudentMarks)
class StudentMarkAdmin(admin.ModelAdmin):
    list_display = ['name','student_id','total_marks']
    search_fields = ['name','student_id']
    list_filter = ['exam'] 

@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ['question','marks','similarity']
    list_filter = ['test']


