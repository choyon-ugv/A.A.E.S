from django.db import models

# Create your models here.


class Question(models.Model):
    question_text = models.TextField(blank=True,null=True)
    correct_answer = models.TextField(blank=True,null=True)

    def __str__(self):
        return f'{self.question_text[:30]}'
    
class TakeTest(models.Model):
    status = models.BooleanField(default=False) 
    title = models.CharField(max_length=100) 
    question= models.ManyToManyField(Question) 
    duration = models.CharField(max_length=3,blank=True) 

    def __str__(self):
        return self.title 
    

class Evaluation(models.Model):
    test = models.ForeignKey(TakeTest,on_delete=models.CASCADE,blank=True,null=True) 
    question = models.ForeignKey(Question, on_delete=models.CASCADE ) 
    marks = models.PositiveIntegerField(default=0) 
    similarity = models.CharField(max_length=5) 

    class Meta:
        verbose_name_plural= 'Evaluation'
        verbose_name = 'Evaluation'


    def __str__(self):
        return f'{self.question}- {self.marks}'

class StudentMarks(models.Model):
    exam = models.ForeignKey(TakeTest,on_delete=models.CASCADE) 
    name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=100)
    student_marks = models.ManyToManyField(Evaluation) 
    total_marks = models.PositiveIntegerField(default=0)
    
    @property
    def get_total(self):
        self.total_marks =  sum([mark.marks for mark in self.student_marks.all()])
        self.save()
        return self.total_marks

    def __str__(self):
        return f'StudentMarks of {self.name} id {self.student_id} ' 
    