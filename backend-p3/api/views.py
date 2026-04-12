from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from song_models.models import Song, SongUser

from .serializers import SongSerializer, SongUserSerializer


class CustomPagination(PageNumberPagination):
    page_size = 3


SongPagination = CustomPagination


class SongViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Song.objects.all().order_by("id")
    serializer_class = SongSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    @action(detail=False, methods=["get"])
    def random(self, request):
        song = Song.objects.order_by("?").first()
        if song is None:
            return Response(
                {"detail": "No songs available"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.get_serializer(song)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def top(self, request):
        raw_n = request.query_params.get("n", "3")
        try:
            n = int(raw_n)
        except (TypeError, ValueError):
            return Response(
                {"detail": "Invalid n parameter"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if n < 1:
            return Response(
                {"detail": "n must be greater than 0"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        songs = Song.objects.order_by("-number_times_played", "id")[:n]
        serializer = self.get_serializer(songs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def search(self, request):
        title = request.query_params.get("title") or request.query_params.get("tilte")
        if not title:
            return Response(
                {"detail": "title query parameter is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        songs = Song.objects.filter(title__icontains=title).order_by("id")
        if not songs.exists():
            return Response(
                {"detail": "No songs found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(songs, many=True)
        return Response(serializer.data)


class SongUserViewSet(viewsets.ModelViewSet):
    serializer_class = SongUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SongUser.objects.filter(user=self.request.user).order_by("id")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
