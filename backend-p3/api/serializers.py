from rest_framework import serializers

from song_models.models import Song, SongUser


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = "__all__"


class SongUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongUser
        fields = "__all__"
        read_only_fields = ("user", "played_at")
