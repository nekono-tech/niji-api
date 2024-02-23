from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from talents.models import Talent
from talents.serializers import TalentSerializer


class TalentIndexView(APIView):
    """
    タレント情報一覧取得API
    """
    def get_queryset(self):
        return Talent.objects.all()

    def get(self, request, *args, **kwargs):
        talents = self.get_queryset()
        return Response(data=TalentSerializer(talents, many=True).data)


class TalentDetailView(APIView):
    """
    タレント情報詳細取得API
    """
    def get(self, request, *args, **kwargs):
        talent_id = kwargs.get('talent_id')
        talent = get_object_or_404(Talent, pk=talent_id)
        return Response(data=TalentSerializer(talent).data)
