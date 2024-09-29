from django.shortcuts import render, redirect
from datetime import date

groups = [
{'id':1, 'image':"http://127.0.0.1:9000/lab1/facultet/ИУ5.svg", 'group_fac':"ИУ", 'group_kaf':5, 'group_course':"3", 'group_count':"3", 'contact':"Власов А.А.", 'contact_phone':"79156734835"},
{'id':4, 'image':"http://127.0.0.1:9000/lab1/facultet/ИУ5.svg", 'group_fac':"ИУ", 'group_kaf':5, 'group_course':"3", 'group_count':"5", 'contact':"Кузьмин Д.А.", 'contact_phone':"79190108127"},
{'id':3, 'image':"http://127.0.0.1:9000/lab1/facultet/ИУ1.svg", 'group_fac':"ИУ", 'group_kaf':1, 'group_course':"3", 'group_count':"3", 'contact':"Беляев И.А.", 'contact_phone':"79858888218"},
{'id':5, 'image':"http://127.0.0.1:9000/lab1/facultet/ИУ4.png", 'group_fac':"ИУ", 'group_kaf':4, 'group_course':"2", 'group_count':"3", 'contact':"Нагапетян В.С.", 'contact_phone':"79854605879"},
{'id':2, 'image':"http://127.0.0.1:9000/lab1/facultet/ИУ4.png", 'group_fac':"ИУ", 'group_kaf':4, 'group_course':"4", 'group_count':"3", 'contact':"Григоренко К.Д.", 'contact_phone':"79166431639"},
{'id':6, 'image':"http://127.0.0.1:9000/lab1/facultet/ИУ8.png", 'group_fac':"ИУ", 'group_kaf':8, 'group_course':"4", 'group_count':"2", 'contact':"Канев А.И.", 'contact_phone':""}
]

orders = [
    {'order_id': 1, 'order_date': "2024-09-21 17:00:00", 'classroom':"515ю", 'info': "asmentus wine tastes the same as i remember", 'groups':[
        {'id':1},
        {'id':2}]},
    {'order_id': 2, 'order_date': "2024-09-21 17:00:00", 'classroom':"515ю", 'info': "asmentus wine tastes the same as i remember", 'groups':[
        {'id':3},
        {'id':4}]},
    {'order_id': 3, 'order_date': "2024-10-01 08:00:00", 'classroom':"502ю", 'info': "asmentus wine tastes the same as i remember", 'groups':[
        {'id':2},
        {'id':5}]},
    {'order_id': 4, 'order_date': "2024-10-03 10:00:00", 'classroom':"404", 'info': "asmentus wine tastes the same as i remember", 'groups':[
        {'id':3},
        {'id':4},
        {'id':1}]},
]

def groups_func(request):
    query = request.GET.get('srch_group')
    if query:
        filtered_groups = [
            group for group in groups
             if query.lower() in group['group_name'].lower()
            #if group['group_name'].lower().startswith(query.lower())
            ]
    else:
        filtered_groups = groups
    return render(request, 'groups.html', 
    { 'data': {
        'page_name': 'Группы',
        'groups' : filtered_groups,
    }})


def info(request, id):
    group = next((gr for gr in groups if gr['id'] == id), None)
    return render(request, 'info_group.html', {'data': {'group': group}})


def get_schedule(request, order_id):
    order = next((order for order in orders if order['order_id'] == order_id), None) 
    if order is None:
        return render(request, '404.html', status=404)
    return render(request, 'schedule.html', {'data': {'groups': groups, 'this': order}})


# Create your views here.
