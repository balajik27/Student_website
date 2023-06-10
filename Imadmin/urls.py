from django.urls import path
from . import views
urlpatterns = [
    path('',views.login,name="login"),
    path('about',views.about,name="about"),
    path('announce',views.announce,name="announce"),
    path('delete_announce/<str:title>',views.delete_announce,name="delete_announce"),
    path('register/',views.register,name="register"),
    path('home',views.home,name="home"),
    path('logout/',views.logout,name="logout"),
    path('create_profile/',views.create_profile,name="create_profile"),
    path('create_subject/',views.create_subject,name = "create_subject"),
    path('material_list/<str:sub_name>',views.material_list,name="material_list"),
    path('material_upload/<str:sub>',views.material_upload , name = "material_upload"),
    path('material_list/<str:file>/<str:yr>/<str:mon>/<str:date>/<str:filename>',views.show_pdf),
    path('<str:file>/<str:yr>/<str:mon>/<str:date>/<str:filename>',views.delete,name = "delete"),
    path('<str:subject>',views.delete_all,name="delete_all"),
]