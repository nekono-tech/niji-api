from rest_framework import serializers

from talents.models import Talent


class TalentSerializer(serializers.ModelSerializer):
    """
    にじさんじのタレント情報をシリアライズするクラス
    """
    class Meta:
        model = Talent
        fields = '__all__'