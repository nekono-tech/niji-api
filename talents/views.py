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