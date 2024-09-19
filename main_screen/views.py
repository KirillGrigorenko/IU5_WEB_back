from django.shortcuts import render
from datetime import date

groups = [
{'id':1, 'image':"http://127.0.0.1:9000/lab1/photo1.jpeg", 'group_name':"IU5-51B", 'group_desc':"Сомнительно"},
{'id':2, 'image':"http://127.0.0.1:9000/lab1/photo1.jpeg", 'group_name':"IU5-52B", 'group_desc':"Но окэй"},
{'id':3, 'image':"http://127.0.0.1:9000/lab1/photo1.jpeg", 'group_name':"IU5-53B", 'group_desc':"Я понимаю"},
{'id':4, 'image':"http://127.0.0.1:9000/lab1/photo1.jpeg", 'group_name':"IU5-54B", 'group_desc':"Что он делает"},
{'id':5, 'image':"http://127.0.0.1:9000/lab1/photo1.jpeg", 'group_name':"IU5-55B", 'group_desc':"Но я не принимаю"},
{'id':6, 'image':"http://127.0.0.1:9000/lab1/photo1.jpeg", 'group_name':"IU5-55B", 'group_desc':"НDEQW"}
]

orders = [
    {'order_id': 1, 'order_date': '17.09.2024', 'groups':[
        {'id':1, 'image':"http://127.0.0.1:9000/lab1/photo1.jpeg", 'group_name':"IU5-51B", 'group_desc':"Сомнительно"},
        {'id':2, 'image':"http://127.0.0.1:9000/lab1/photo1.jpeg", 'group_name':"IU5-52B", 'group_desc':"Но окэй"},]},
    {'order_id': 2, 'order_date': '16.09.2024', 'groups':[
        {'id':4, 'image':"http://127.0.0.1:9000/lab1/photo1.jpeg", 'group_name':"IU5-51B", 'group_desc':"Сомнительно"},
        {'id':5, 'image':"http://127.0.0.1:9000/lab1/photo1.jpeg", 'group_name':"IU5-52B", 'group_desc':"Но окэй"},]}

]

index_photos = [
    {'id':1, 'image':"http://127.0.0.1:9000/lab1/bmstu.png", 'alt': "bmstu.png"},
    {'id':2, 'image':"http://127.0.0.1:9000/lab1/search.png", 'alt': "search.png"},
    {'id':3, 'image':"http://127.0.0.1:9000/lab1/dashboard.png", 'alt': "dashboard.png"},
    {'id':4, 'image':"http://127.0.0.1:9000/lab1/photo1.jpeg", 'alt': "photo1.jpeg"}
]

def hello(request):
    query = request.GET.get('q')
    if query:
        filtered_groups = [
            group for group in groups
             if query.lower() in group['group_name'].lower()
            #if group['group_name'].lower().startswith(query.lower())
            ]
    else:
        filtered_groups = groups
    return render(request, 'card.html', 
    { 'data': {
        'page_name': 'Группы',
        'groups' : filtered_groups,
        'index_photo' : index_photos
    }})


def info(request, id):
    group = next((gr for gr in groups if gr['id'] == id), None)
    return render(request, 'info.html', {'data': {'group': group, 'index_photo':index_photos}})


def GetBin(request, order_id):
    order = next((order for order in orders if order['order_id'] == order_id), None)
    if order is None:
        return render(request, '404.html', status=404)
    return render(request, 'bin.html', {'data': order['groups']})


# Create your views here.
