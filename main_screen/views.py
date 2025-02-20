from .models import Group,Lesson, LessonGroup
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
import os
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
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer
from django.contrib.auth.models import User
from main_screen.serializers import *
from django.conf import settings
from .minio import MinioStorage


USER_ID = 1


@api_view(['POST'])
def create_user(request):
    """
    Регистрация пользователя
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_user(request):
    """
    Обновление данных пользователя (личный кабинет)
    """
    user = request.user 
    serializer = UserSerializer(user, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(request):
    """
    Вход пользователя
    """
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Username and password required'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)

    return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout_user(request):
    """
    Выход (деавторизация)
    """
    # Удаление токена, чтобы завершить сессию
    request.auth.delete()
    # Возвращаем успешный ответ (204 - нет контента)
    return Response(status=status.HTTP_204_NO_CONTENT)

#М-М

@api_view(['DELETE'])
def delete_lesson_group(request, lesson_pk, group_pk):
    """
    Удаление группы из занятия
    """
    # Найти запись в промежуточной таблице (many-to-many)
    lesson_group = LessonGroup.objects.filter(lesson_id=lesson_pk, group_id=group_pk).first()
    
    if lesson_group is None:
        return Response("LessonGroup not found", status=status.HTTP_404_NOT_FOUND)
    
    # Удаление найденной записи
    lesson_group.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
def put_lesson_group(request, lesson_pk, group_pk):
    """
    Изменение данных о группе в занятии
    """
    # Ищем запись в таблице LessonGroup по lesson_pk и group_pk
    lesson_group = LessonGroup.objects.filter(lesson_id=lesson_pk, group_id=group_pk).first()

    if lesson_group is None:
        return Response("LessonGroup not found", status=status.HTTP_404_NOT_FOUND)

    # Если передано поле headboy в запросе, обновляем его
    if 'headboy' in request.data:
        lesson_group.headboy = request.data['headboy']

    # Сохраняем изменения
    lesson_group.save()

    return Response({"message": "LessonGroup updated successfully"}, status=status.HTTP_200_OK)

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

@api_view(['DELETE'])
def delete_group(request, id: int):
    """
    Деактивация группы
    """
    group = Group.objects.filter(id=id).first()
    if not group:
        return Response({"error": "Группа не найдена"}, status=status.HTTP_404_NOT_FOUND)

    if not group.is_active:
        return Response({"message": "Группа уже деактивирована"}, status=status.HTTP_200_OK)

    group.is_active = False
    group.save()

    return Response({"message": "Группа деактивирована"}, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_draft_lesson(request):
    """
    Создание заявки в статусе 'Черновик'
    """
    user = request.user
    if not user.is_authenticated:
        return Response({"error": "Требуется авторизация"}, status=status.HTTP_401_UNAUTHORIZED)

    lesson = Lesson.objects.create(
        lecturer=user,
        status=Lesson.LessonStatus.DRAFT
    )

    return Response({"message": "Заявка создана", "id": lesson.id}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def upload_group_image(request, id):
    """
    Загрузка изображения группы в MinIO, старое изображение заменяется
    """
    group = Group.objects.filter(id=id, is_active=True).first()
    if group is None:
        return Response({"error": "Группа не найдена"}, status=status.HTTP_404_NOT_FOUND)

    # Создание экземпляра MinioStorage с параметрами из настроек
    minio_storage = MinioStorage(
        endpoint=settings.MINIO_ENDPOINT_URL,
        access_key=settings.AWS_ACCESS_KEY_ID,
        secret_key=settings.AWS_SECRET_ACCESS_KEY,
        secure=settings.MINIO_USE_SSL
    )

    # Получаем файл изображения из запроса
    file = request.FILES.get("image")
    if not file:
        return Response({"error": "Файл изображения отсутствует"}, status=status.HTTP_400_BAD_REQUEST)

    # Определяем расширение файла и его имя
    file_extension = os.path.splitext(file.name)[1]
    file_name = f"facultet/{group.__str__()}{file_extension}"  # Сохраняем в папку facultet

    # Удаляем старое изображение, если оно есть
    if group.photo_url:
        try:
            old_file_name = group.photo_url.split("/")[-1]  # Получаем имя старого файла
            # Удаляем файл из MinIO
            file_path = f"facultet/{old_file_name}"  
            # Удаляем файл из MinIO
            minio_storage.delete_file("lab1", file_path)
        except Exception as e:
            return Response({"error": f"Ошибка удаления старого изображения: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Загружаем новое изображение
    try:
        minio_storage.load_file("lab1", file_name, file)
    except Exception as e:
        return Response({"error": f"Ошибка загрузки изображения: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Обновляем URL изображения в базе данных
    group.photo_url = f"http://{settings.MINIO_ENDPOINT_URL}/lab1/{file_name}"
    group.save()

    return Response({"message": "Изображение загружено", "photo_url": group.photo_url}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_lessons(request):
    """
    Получение списка занятий (кроме 'Удалён' и 'Черновик') с фильтрацией по статусу и диапазону даты формирования.
    """
    status_filter = request.query_params.get("status")
    formation_start = request.query_params.get("formation_start")
    formation_end = request.query_params.get("formation_end")

    # Фильтрация: исключаем 'Удалён' и 'Черновик'
    filters = ~Q(status="Удалён") & ~Q(status="Черновик")
    
    # Фильтр по статусу (если передан)
    if status_filter is not None:
        filters &= Q(status=status_filter)

    # Фильтр по диапазону дат (если передан)
    if formation_start is not None:
        filters &= Q(formation_datetime__gte=formation_start)
    if formation_end is not None:
        filters &= Q(formation_datetime__lte=formation_end)

    # Применяем фильтры
    lessons = Lesson.objects.filter(filters).select_related("lecturer", "manager")

    # Сериализация данных
    serializer = LessonSerializer(lessons, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_lesson_id(request, pk):
    filters = Q(id=pk) & ~Q(status="Удалён")
    lesson = Lesson.objects.filter(filters).prefetch_related("lessongroup_set__group").first()
    
    if lesson is None:
        return Response({"error": "Lesson not found"}, status=status.HTTP_404_NOT_FOUND)

    lesson_data = LessonSerializer(lesson).data
    lesson_groups = LessonGroupSerializer(lesson.lessongroup_set.all(), many=True).data
    lesson_data["groups"] = lesson_groups

    return Response(lesson_data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def update_lesson(request, pk):
    """
    Изменение данных занятия по ID
    """
    lesson = Lesson.objects.filter(id=pk).first()  # Находим занятие по ID

    if lesson is None:
        return Response("Lesson not found", status=status.HTTP_404_NOT_FOUND)

    # Сериализуем и передаем данные из запроса
    serializer = LessonSerializer(lesson, data=request.data, partial=True)  # partial=True для частичного обновления

    if serializer.is_valid():  # Если данные валидны
        serializer.save()  # Сохраняем изменения
        return Response(serializer.data, status=status.HTTP_200_OK)  # Возвращаем обновленные данные
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Возвращаем ошибки

@api_view(['PUT'])
def form_lesson(request, pk):
    """
    Формирование заявки на занятие
    """
    lesson = Lesson.objects.filter(id=pk, status=Lesson.LessonStatus.DRAFT).first()

    if lesson is None:
        return Response("Lesson not found or already formed", status=status.HTTP_400_BAD_REQUEST)

    # Проверка обязательных полей
    if lesson.formation_datetime is None:
        return Response("formation_datetime is required", status=status.HTTP_400_BAD_REQUEST)
    
    if lesson.lecturer is None:
        return Response("lecturer is required", status=status.HTTP_400_BAD_REQUEST)

    # Проверка других полей, если нужно
    if not lesson.name:
        return Response("name is required", status=status.HTTP_400_BAD_REQUEST)

    if not lesson.time:
        return Response("time is required", status=status.HTTP_400_BAD_REQUEST)

    if not lesson.date:
        return Response("date is required", status=status.HTTP_400_BAD_REQUEST)

    if not lesson.building:
        return Response("building is required", status=status.HTTP_400_BAD_REQUEST)

    if not lesson.audience:
        return Response("audience is required", status=status.HTTP_400_BAD_REQUEST)

    # Если все обязательные поля заполнены
    lesson.status = Lesson.LessonStatus.FORMED
    lesson.formation_datetime = timezone.now()  # Дата формирования
    lesson.save()

    serializer = LessonSerializer(lesson)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def update_lesson_status(request, pk):
    """
    Завершение или отклонение заявки модератором.
    Проставляется модератор и дата завершения.
    """
    lesson = Lesson.objects.filter(id=pk).first()

    if lesson is None:
        return Response("Lesson not found", status=status.HTTP_404_NOT_FOUND)

    if lesson.status in [Lesson.LessonStatus.COMPLETED, Lesson.LessonStatus.REJECTED]:
        return Response("Lesson is already completed or rejected", status=status.HTTP_400_BAD_REQUEST)

    status_filter = request.data.get("status")
    moderator_id = request.data.get("moderator")  # ID модератора из запроса

    if status_filter not in [Lesson.LessonStatus.COMPLETED, Lesson.LessonStatus.REJECTED]:
        return Response("Invalid status", status=status.HTTP_400_BAD_REQUEST)

    if not moderator_id:
        return Response("Moderator is required", status=status.HTTP_400_BAD_REQUEST)

    # Проставляем статус, модератора и дату завершения
    lesson.status = status_filter
    lesson.moderator_id = moderator_id  # Устанавливаем модератора
    lesson.completion_datetime = timezone.now()  # Проставляем дату завершения вручную

    lesson.save()

    serializer = LessonSerializer(lesson)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_lesson(request, pk):
    """
    Удаление заявки (изменение статуса на 'Удалён')
    """
    lesson = Lesson.objects.filter(id=pk, status=Lesson.LessonStatus.DRAFT).first()

    if lesson is None:
        return Response("Lesson not found or already processed", status=status.HTTP_404_NOT_FOUND)

    lesson.status = Lesson.LessonStatus.DELETED
    lesson.save()

    return Response(status=status.HTTP_200_OK)



def get_groups_in_lesson(lesson_id: int) -> int:
    """
    Получение количества услуг = групп, связанных с определённым заявкой = занятием по его id
    """
    return LessonGroup.objects.filter(lesson_id=lesson_id).count()


def get_lesson(request, id: int):
    lesson = get_object_or_404(Lesson, id=id)
    """
    Получение страницы заявки
    """   
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
