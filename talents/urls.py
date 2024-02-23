from django.urls import path

from .views import TalentIndexView, TalentDetailView

urlpatterns = [
    # タレント情報一覧取得API
    path('/', TalentIndexView.as_view(), name='talent.index'),
    # タレント情報詳細取得API
    path('/<int:talent_id>', TalentDetailView.as_view(), name='talent.detail'),
]