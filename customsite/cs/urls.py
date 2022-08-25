from django.urls import path
from cs import views

app_name = "Cs"

urlpatterns = [
    # 공지사항
    path("write/", views.notice_write, name="notice_write"),
    path("detail/<int:pk>/", views.notice_detail, name="notice_detail"),
    path("list/", views.notice_list, name="notice_list"),
    path('update/<int:pk>/', views.notice_update, name="notice_update"),
    path('delete/', views.notice_delete, name="notice_delete"),

    # 이벤트
    path("event/write/", views.event_write, name="event_write"),
    path("event/detail/<int:pk>/", views.event_detail, name="event_detail"),
    path("event/list/", views.event_list, name="event_list"),
    path('event/update/<int:pk>/', views.event_update, name="event_update"),
    path('delete/', views.event_delete, name="event_delete"),

    # 1:1문의
    path("oto/write/", views.oto_write, name="oto_write"),
    path("oto/detail/<int:pk>", views.oto_detail, name="oto_detail"),
    path("oto/list/", views.oto_list, name="oto_list"),
    path('oto/answer/<int:pk>/', views.oto_answer, name="oto_answer"),
    path('oto_loading/', views.oto_loading, name="oto_loading"),

    # FAQ
    path("faq/write/", views.faq_write, name="faq_write"),
    path("faq/detail/<int:pk>", views.faq_detail, name="faq_detail"),
    path("faq/list/", views.faq_list, name="faq_list"),
    path('faq/update/<int:pk>/', views.faq_update, name="faq_update"),
    path('faq/delete/', views.faq_delete, name="faq_delete"),
]
