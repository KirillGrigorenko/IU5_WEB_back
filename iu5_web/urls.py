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