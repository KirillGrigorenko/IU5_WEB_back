from .models import Group,Lesson, LessonGroup
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.exceptions import BadRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.utils.dateparse import parse_date, parse_time
from django.utils.timezone import now
from django.utils import timezone
from django.db import connection
from django.core.exceptions import ValidationError
from rest_framework.decorators import *
from rest_framework.response import Response
from main_screen.serializers import *


USER_ID = 1


@api_view(['GET'])
def get_group(request, id: int):
    """
    Получение одной группы по ID
    """
    group = get_object_or_404(Group, id=id, status='Действует')
    serializer = AllGroupsSerializer(group)
    return Response(serializer.data)


@api_view(['GET'])
def groups_list(request):
    """
    Страница списка услуг = групп + фильтр по курсу
    """
    srch_course = request.query_params.get('srch_course')
    if srch_course and srch_course != '0':
        filtered_groups = Group.objects.filter(status='Действует', course__icontains=srch_course).order_by('id')
    else:
        filtered_groups = Group.objects.filter(status='Действует').order_by('id')

    req = Lesson.objects.filter(lecturer_id=USER_ID, status=Lesson.LessonStatus.DRAFT).first()

    serialazer = AllGroupsSerializer(filtered_groups, many=True)

    return Response(
        {'groups': serialazer.data,
        'groups_in_lesson': (get_groups_in_lesson(req.id) if req is not None else 0),
        'request_id': (req.id if req is not None else 0)}
    )

    return render(request, 'groups.html', {
        'data': {
            'groups': filtered_groups,
            'groups_in_lesson': (get_groups_in_lesson(req.id) if req is not None else 0),
            'groups_title': srch_course,
            'request_id': (req.id if req is not None else 0),
        },
    })

@api_view(['POST'])
def create_group(request):
    """
    Добавление новой группы
    """
    serializer = AllGroupsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)  # Created
    return Response(serializer.errors, status=400)  # Bad Request

@api_view(['PUT'])
def update_group(request, id: int):
    """
    Обновление данных группы (услуги) по ID
    """
    group = get_object_or_404(Group, id=id)
    serializer = AllGroupsSerializer(group, data=request.data, partial=True)  # partial=True → частичное обновление

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)
    
    return Response(serializer.errors, status=400)


def get_groups_in_lesson(lesson_id: int) -> int:
    """
    Получение количества услуг = групп, связанных с определённым заявкой = занятием по его id
    """
    return LessonGroup.objects.filter(lesson_id=lesson_id).count()


def get_lesson(request, id: int):
    """
    Получение страницы заявки
    """
    lesson = get_object_or_404(Lesson, id=id)
    if lesson.status == Lesson.LessonStatus.DELETED:
        raise Http404("Lesson not found")
    return render(request, 'lesson.html',
                  {'data': get_lesson_data(id)})


def add_group_to_lesson(request):
    """
    Добавление услуги = группы в заявку = занятие
    """
    if request.method != "POST":
        return redirect('groups')
    data = request.POST
    group_id = data.get("add_to_lesson")
    
    if group_id is not None:
       lesson_id = get_or_create_user(USER_ID)
       add_item_to_request(lesson_id, group_id)
    return groups_list(request)

def add_item_to_request(lesson_id: int, group_id: int):
    """
    Добавление услуги = группа в заявку = занятие
    """
    if not LessonGroup.objects.filter(lesson_id=lesson_id, group_id=group_id).exists():
        lesson = LessonGroup(lesson_id=lesson_id, group_id=group_id)
        lesson.save()


def get_or_create_user(user_id: int) -> int:
    """
    Если у пользователя есть заявка в статусе DRAFT (корзина), возвращает её Id.
    Если нет - создает и возвращает id созданной заявки
    """
    old_req = Lesson.objects.filter(lecturer_id=USER_ID,
                                                    status=Lesson.LessonStatus.DRAFT).first()
    if old_req is not None:
        return old_req.id

    new_req = Lesson(lecturer_id=USER_ID, status=Lesson.LessonStatus.DRAFT)
    new_req.save()
    return new_req.id

def delete_lesson(lesson_id: int):
    """
    Удаление заявки = занятия по id
    """
    raw_sql = "UPDATE lessons SET status=%s WHERE id=%s "
    with connection.cursor() as cursor:
        cursor.execute(raw_sql, ('Удалён', lesson_id,))

def remove_lesson_request(request, id: int):
    """
    Удаление услуги = группы из заявки
    """
    if request.method != "POST":
        return redirect('get_lesson')

    data = request.POST
    action = data.get("request_action")
    if action == "delete_lesson":
        delete_lesson(id)
        return redirect('groups_list')
    return get_lesson(request, id)

def get_lesson_data(lesson_id: int):
    """
    Формирование данных из заявки = занятия
    """
    req = Lesson.objects.filter(~Q(status=Lesson.LessonStatus.DELETED),
                                                id=lesson_id).first()
    if req is None:
        return {
            'id': lesson_id,
            'groups': [],
            'req_id': lesson_id,
        }

    groups = LessonGroup.objects.filter(lesson_id=lesson_id).select_related('group')
    return {
        'id': lesson_id,
        'groups': groups,
        'req_id': lesson_id,
    }




def update_headboy(request, id: int):
    """
    Сохранение заявки = занятия FORMED + староста + audience
    """

    lesson = get_object_or_404(Lesson, id=id)


    if request.method == 'POST':
        action = request.POST.get('request_action')
        selected_group_id = request.POST.get('selected_group')
        if action == 'update_headboy' and selected_group_id:
            selected_group = get_object_or_404(LessonGroup, id=selected_group_id)
            lesson_groups = LessonGroup.objects.filter(lesson=lesson)
            lesson_groups.update(headboy=selected_group.group.headboy)

            return redirect('get_lesson', id=id)

    return redirect('get_lesson', id=id)
