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
from django.core.exceptions import ValidationError
from django.utils import timezone


def groups_func(request):
    query = request.GET.get('srch_course', '')
    if query and query != '0':
        filtered_groups = Group.objects.filter(status='Действует', course__icontains=query).order_by('id')
    else:
        filtered_groups = Group.objects.filter(status='Действует').order_by('id')

    # Проверяем наличие активного урока
    active_lesson = Lesson.objects.filter(status=Lesson.LessonStatus.DRAFT).first()

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
                    name="Ваш предмет",
                )
                req_call_count = 0  # Начинаем с 0, так как новая заявка только что создана

            # Проверяем, не добавлена ли группа в заявку
            if LessonGroup.objects.filter(lesson=active_lesson, group=group).exists():
                messages.warning(request, "Группа уже добавлена в текущую заявку.")
            else:
                LessonGroup.objects.create(lesson=active_lesson, group=group)
                messages.success(request, "Группа успешно добавлена.")
                req_call_count += 1  # Увеличиваем количество групп в заявке
 
    # Отправляем данные в шаблон
    return render(request, 'groups.html', {
        'data': {
            'page_name': 'Группы',
            'groups': filtered_groups,
            'ReqCallCount': req_call_count,
            'active_lesson': active_lesson,
        },
    })


def info(request, id):
    group = get_object_or_404(Group, pk=id) 
    return render(request, 'info_group.html', {
        'data': {
            'group': group  
        }
    })



def get_schedule(request, order_id):
    # Получаем Lesson по ID
    lesson = get_object_or_404(Lesson, id=order_id)

    if lesson.status != Lesson.LessonStatus.DRAFT:
        raise Http404("Страница не найдена")

    related_groups = LessonGroup.objects.filter(lesson=lesson)

    # Определяем текущую дату и время
    today = timezone.now()  # Текущая дата и время
    today_date_input = today.strftime('%Y-%m-%d')  # Формат для <input type="date">
    now_time = today.strftime('%H:%M')  # Только время

    if request.method == 'POST':
        # Обрабатываем изменение информации о группе (Здание и аудитория)
        audience = request.POST.get('audience')
        building = request.POST.get('building')

        if audience and building:
            # Обновляем информацию для всех групп, связанных с заявкой
            for lesson_group in related_groups:
                lesson_group.audience = audience
                lesson_group.building = building
                lesson_group.save()

            # Добавляем уведомление о том, что все группы были обновлены
            messages.success(request, f"Все группы в заявке были успешно обновлены.")

        # Обрабатываем удаление группы
        remove_group_id = request.POST.get('remove_group_id')
        if remove_group_id:
            lesson_group = get_object_or_404(LessonGroup, id=remove_group_id, lesson=lesson)
            lesson_group.delete()

            # Добавляем уведомление об удалении
            messages.success(request, f"Группа {lesson_group.group} была успешно удалена из заявки.")

        # Сохраняем изменения и меняем статус заявки на FORMED только при нажатии на кнопку "Сохранить заявку"
        if 'save_lesson' in request.POST:

            name = request.POST.get('name', lesson.name)
            time = request.POST.get('time', lesson.time)
            date = request.POST.get('date', lesson.date)

            if not time or not date:
                messages.error(request, "Нельзя сохранить заявку: не указаны время и дата урока.")
                return redirect(request.path)

        # Не работает проверка на дату и время, ибо оно всегда есть, по умолчанию
        
            missing_fields = related_groups.filter(audience='', building='')
            if missing_fields.exists():
                messages.error(request, "Нельзя сохранить заявку: не заданы аудитория и здание для всех групп.")
                return redirect(request.path)
            
            lesson.name = name
            lesson.time = time
            lesson.date = date

            if lesson.status == Lesson.LessonStatus.DRAFT:
                lesson.formation_datetime = timezone.now()
            # Меняем статус заявки на FORMED
            lesson.status = Lesson.LessonStatus.FORMED
            lesson.save()

            # Добавляем уведомление о сохранении заявки
            messages.success(request, "Заявка успешно сохранена и изменена на статус 'Сформирована'.")

            # Перенаправляем на страницу поиска групп
            return redirect('groups_search')  # Перенаправление на страницу 'groups_search'

    # Передаем данные в шаблон
    context = {
        'lesson': lesson,
        'related_groups': related_groups,
        'today_date_input': today_date_input,      # Для <input type="date">
        'now_time': now_time,                     # Для времени
    }
    return render(request, 'schedule.html', context)
