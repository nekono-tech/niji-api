from django.urls import path

from .views import TalentIndexView

urlpatterns = [
    # タレント情報一覧取得API
    path('/', TalentIndexView.as_view(), name='talent.index'),
]