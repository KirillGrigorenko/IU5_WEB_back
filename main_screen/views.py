from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from datetime import date
from .models import Group,Lesson, LessonGroup
from django.db.models import Q
from django.core.exceptions import BadRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.utils.dateparse import parse_date, parse_time
from django.utils.timezone import now


def groups_func(request):
    query = request.GET.get('srch_course', '')
    if query and query != '0':
        filtered_groups = Group.objects.filter(status='Действует', course__icontains=query).order_by('id')
    else:
        filtered_groups = Group.objects.filter(status='Действует').order_by('id')

    # Проверяем наличие активного урока
    active_lesson = Lesson.objects.filter(status=Lesson.LessonStatus.DRAFT).first()
    flash_message = ""

    # Считаем количество групп в активной заявке
    req_call_count = LessonGroup.objects.filter(lesson=active_lesson).count() if active_lesson else 0

    if request.method == 'POST':
        group_id = request.POST.get('group_id')
        if group_id:
            group = get_object_or_404(Group, pk=group_id)

            # Создаём черновую заявку, если её нет
            if not active_lesson:
                active_lesson = Lesson.objects.create(
                    status=Lesson.LessonStatus.DRAFT,
                    name="Новая Заявка",
                )
                req_call_count = 0  # Начинаем с 0, так как новая заявка только что создана

            # Проверяем, не добавлена ли группа в заявку
            if LessonGroup.objects.filter(lesson=active_lesson, group=group).exists():
                flash_message = "Группа уже добавлена в текущую заявку."
            else:
                LessonGroup.objects.create(lesson=active_lesson, group=group)
                flash_message = "Группа успешно добавлена."
                req_call_count += 1  # Увеличиваем количество групп в заявке
 
    # Отправляем данные в шаблон
    return render(request, 'groups.html', {
        'data': {
            'page_name': 'Группы',
            'groups': filtered_groups,
            'ReqCallCount': req_call_count,
            'active_lesson': active_lesson,
        },
        'flash_message': flash_message,  # Передаем сообщение для отображения
    })



def info(request, id):
    group = get_object_or_404(Group, pk=id) 
    return render(request, 'info_group.html', {
        'data': {
            'group': group  
        }
    })

def get_schedule(request, order_id):
    lesson = get_object_or_404(Lesson, id=order_id, status=Lesson.LessonStatus.DRAFT)
    related_groups = LessonGroup.objects.filter(lesson=lesson)

    # Текущая дата и время для шаблона
    today = now()
    today_date = today.date()
    now_time = today.strftime('%H:%M')

    flash_message = ""  # Переменная для flash-сообщения

    if request.method == 'POST':
        update_type = request.POST.get('update_type', '')

        if update_type == 'formation_datetime':
            new_date = request.POST.get('formation_date', '').strip()
            new_time = request.POST.get('formation_time', '').strip()
            parsed_date = parse_date(new_date)
            parsed_time = parse_time(new_time)
            
            if parsed_date and parsed_time:
                lesson.formation_datetime = now().replace(
                    year=parsed_date.year, month=parsed_date.month, day=parsed_date.day,
                    hour=parsed_time.hour, minute=parsed_time.minute, second=0, microsecond=0
                )
                lesson.save()
                flash_message = 'Дата и время формирования успешно обновлены.'
                messages.success(request, flash_message)
            else:
                flash_message = 'Неверный формат даты или времени.'
                messages.error(request, flash_message)

    context = {
        'lesson': lesson,
        'related_groups': related_groups,
        'today_date': today_date,
        'now_time': now_time,
        'flash_message': flash_message,  # Передаем flash-сообщение в шаблон
    }

    return render(request, 'schedule.html', context)