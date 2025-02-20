"""
URL configuration for iu5_web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from main_screen import views as m_s

urlpatterns = [
    path('admin/', admin.site.urls),
    path('groups/', m_s.groups_list, name='groups_list'),
    path('group_info/<int:id>/', m_s.get_group, name='get_group'),
    path('group/create/', m_s.create_group, name='create_group'),
    path('group/<int:id>/update/', m_s.update_group, name='update_group'),
    path('group/<int:id>/delete/', m_s.delete_group, name='delete_group'),
    path('lesson/create/', m_s.create_draft_lesson, name='create_draft_lesson'),
    path('group/<int:id>/upload_image/', m_s.upload_group_image, name='upload_group_image'),

    path('lessons/', m_s.get_lessons, name='get_lessons'),
    path('lessons/<int:pk>/', m_s.get_lesson_id, name='get_lesson_id'),
    path('lessons/<int:pk>/update/', m_s.update_lesson, name='update_lesson'),  # Новый путь для PUT запроса
    path('lessons/<int:pk>/form/', m_s.form_lesson, name='form_lesson'),  # Новый путь для формирования занятия
    path('lessons/<int:pk>/update_status/', m_s.update_lesson_status, name='update_lesson_status'),
    path('lessons/<int:pk>/delete/', m_s.delete_lesson, name='delete_lesson'),
    
    path('user/register/', m_s.create_user, name='register_user'),
    path("login/", m_s.login_user, name="login"),
    path('user/update/', m_s.update_user, name='update_user'),
    path('logout/', m_s.logout_user, name='logout_user'),

    path('lesson_group/<int:lesson_pk>/<int:group_pk>/delete', m_s.delete_lesson_group, name='lesson_group_delete'),
    path('lesson_group/<int:lesson_pk>/<int:group_pk>/put', m_s.put_lesson_group, name='lesson_group_put'),


    path('lesson/<int:id>/', m_s.get_lesson, name='get_lesson'),
    path('add_group_to_lesson/', m_s.add_group_to_lesson, name='add_group_to_lesson'),
    path('delete_lesson/<int:id>/', m_s.remove_lesson_request, name='remove_lesson_request'),
    path('update_headboy/<int:id>/', m_s.update_headboy, name='update_headboy'),
  

  ]

"""     
   

        main_page GET
    path('', views.get_software_list, name='software_list'), 

        add_to_lesson POST
    path('add_software_to_cart/', views.add_software_to_cart, name='add_software_to_cart'),
    
        info/group/<> GET
    path('software/<int:id>/', views.software_page, name='software'),
    
        lessons     GET
    path('install_software_request/<int:id>/', views.get_software_request, name='install_software_request'),
    
        delete_lesson POST
    path('remove_software_request/<int:id>/', views.remove_software_request, name='remove_software_request'),
]"""