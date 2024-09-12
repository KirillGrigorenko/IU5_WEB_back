from django.shortcuts import render
from datetime import date

groups = [
{'id':1, 'image':"http://127.0.0.1:9000/lab1/photo1.jpeg", 'group_name':"IU5-51B", 'group_desc':"Сомнительно"},
{'id':2, 'image':"http://127.0.0.1:9000/lab1/photo1.jpeg", 'group_name':"IU5-52B", 'group_desc':"Но окэй"},
{'id':3, 'image':"http://127.0.0.1:9000/lab1/photo1.jpeg", 'group_name':"IU5-53B", 'group_desc':"Я понимаю"},
{'id':4, 'image':"http://127.0.0.1:9000/lab1/photo1.jpeg", 'group_name':"IU5-54B", 'group_desc':"Что он делает"},
{'id':5, 'image':"http://127.0.0.1:9000/lab1/photo1.jpeg", 'group_name':"IU5-55B", 'group_desc':"Но я не принимаю"}]

def hello(request):
    return render(request, 'card.html', 
    { 'data': {
        'page_name': 'Группы',
        'group' : groups
    }})

# Create your views here.
