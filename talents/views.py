from rest_framework import viewsets

from talents.models import Talent
from talents.serializers import TalentSerializer


class TalentViewSet(viewsets.ModelViewSet):
    """
    タレント情報ViewSet
    """
    queryset = Talent.objects.all()
    serializer_class = TalentSerializer
