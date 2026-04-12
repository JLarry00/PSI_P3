from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class SongViewSetAdditionalTests(APITestCase):
    def test_top_songs_rejects_non_positive_n(self):
        response = self.client.get(reverse("songs-top"), {"n": 0})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "n must be greater than 0")
