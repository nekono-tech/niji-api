from rest_framework import serializers

from talents.models import Talent


class TalentSerializer(serializers.ModelSerializer):
    """
    にじさんじのタレント情報をシリアライズするクラス
    """
    class Meta:
        model = Talent
        fields = ('id', 'name', 'name_en', 'slug', 'debut_at', 'fanclub_url', 'affiliation', 'created_at', 'updated_at')