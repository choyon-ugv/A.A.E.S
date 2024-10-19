from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Question, TakeTest, StudentMarks 
from .machine import *
from .models import Evaluation

def take_test(request):
    try:
        test = TakeTest.objects.filter(status = True).first() 
        print('test',test)
        print('qs',test.question.all())
        print('number of input field', test.question.count())
    except:
        test = {}
        print('no test found')    
    # print('test',test) 
    context = {
        'tests':test,
        # 'questions':questions
    }
    return render(request,'main.html',context) 


def evaluate_and_store(request,id=None):
    if request.method == "POST":
        exam = TakeTest.objects.get(id=id) 

        question = exam.question.all().count()

        name = request.POST.get('name')
        student_id = request.POST.get('student_id')
        student_marks_exist = StudentMarks.objects.filter(exam=exam,student_id=student_id).exists()
        if not student_marks_exist:
            eval = StudentMarks(
                    name=name,
                    student_id=student_id,
                    exam=exam
                )
            eval.save()
        else:
            return redirect('second_time')
        answer_ = []
        for i in range (1,question+1):
            ll = request.POST.get(f'answer-{i}')
            answer_.append(ll)
        print('ans list',answer_)
        
        for index,item in enumerate(exam.question.all()): 
            print('qsn',item)
            model_answer = item.correct_answer
            user_answer = answer_[index] 

            similarity_score_percentage = int(calculate_similarity_score(model_answer, user_answer))
            marks = calculate_marks(similarity_score_percentage)   

            save_marks = Evaluation(
                question=item,
                marks=marks,
                similarity=similarity_score_percentage
                ) 
            save_marks.save() 

            # save to evaluation 
            
            eval.student_marks.add(save_marks)
            eval.total_marks = eval.get_total
            eval.save()

            
        # return redirect('/')

            


        return render(request,'thanks.html') 




def evaluate(request,id=None):
    if request.method == 'POST':
        answer = request.POST['answer_text']
        print('answer get from frontend',answer,'id is',id) 
        question = Question.objects.get(pk=int(id))
        model_answer = question.correct_answer 
        similarity_score_percentage = int(calculate_similarity_score(model_answer, answer))
        similarity_score_percentage = "{:.1f}%".format(calculate_similarity_score(model_answer, answer))
        marks = calculate_marks(similarity_score_percentage)   
        context = {
            'marks':marks,
            'score':similarity_score_percentage,
        }
        return render(request,'result.html',context)
    else:
        question_= Question.objects.get(id=id)
        return render(request,'answer.html',{'qs':question_}) 

def checkAnswer(question_,answer_,model_answer_):
    # student_answer = '''NLP stands for Natural Language Processing, which is a field of artificial intelligence that focuses on the interaction between computers and human language.'''
    # print(student_answer)
    # question = Question.objects.get(pk=1)
    # print('question',question)
    answer = answer_
    question = question_
    model_answer = model_answer_
    # model_answer = question.correct_answer
    # print('model answer',model_answer)
    similarity_score_percentage = calculate_similarity_score(model_answer, answer) 
    marks = calculate_marks(similarity_score_percentage)
    context={'marks':marks,'similarity_score_percentage':similarity_score_percentage}
    # return render(request,"check_answers/check_answer.html",context)
    print(context) 


    # return render(request,'main.html')


# def check_result(request):
#     student_id = 121
#     eval = Evaluation.objects.get(student_id=student_id)
#     # print('student eval ',eval.student_marks.all())
#     total_marks = 0
#     for item in eval.student_marks.all():
#         print(f'The question is {item.question}  and the mark is {item.marks} ')
#         total_marks +=  item.marks
#     print('total marks in this exam is ',total_marks)

    

#     return redirect('/')
    
def home(request):
    return render(request,'index.html')

def second_time(request):
    return render(request,'2nd_submission.html')