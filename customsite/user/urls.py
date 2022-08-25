from django.urls import path
from user import views
from django.conf.urls.static import static
from django.conf import settings # settings.py 파일임

app_name = "User"

urlpatterns = [
    # 로그인 및 회원가입 및 PW
    path('login/', views.login, name='user_login'),
    path('logout/',  views.logout, name='user_logout'),
    path('register/', views.register, name="user_register"),
    path('find/', views.find_pw, name="find_pw"), # Pw 찾는페이지
    path('chpw/<str:email>/', views.chpw, name="chpw"), # Pw 변경페이지

    # 매거진
    path('list/', views.magazine_list, name="magazine_list"),
    path('detail/<int:pk>/', views.magazine_detail, name="magazine_detail"), 
    path('update/<int:pk>/', views.magazine_update, name="magazine_update"),
    path('write/', views.magazine_write, name="magazine_write"),
    path('delete/', views.magazine_delete, name="magazine_delete"),

    # mypage -------------------------------------------------------------------------------
    path('mypage/', views.mypage, name="mypage"),
    path('login/api/', views.api_login, name="api_login"),
    path('mypage/modify/check/', views.info_modify, name="info_modify"),
    path('mypage/modify/detail/', views.info_modify_detail, name="info_modify_detail"),
]
# MEDIA 경로 추가
urlpatterns += static(  # 정규표현식 사용가능
    settings.MEDIA_URL,
    document_root = settings.MEDIA_ROOT
)