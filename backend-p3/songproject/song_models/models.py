from django.db import models
from django.contrib.auth.models import User


class Song(models.Model):
    LANGUAGE_CHOICES = [
        ("EN", "English"),
        ("ES", "Spanish"),
        ("FR", "French"),
        ("DE", "German"),
        ("IT", "Italian"),
        ("PT", "Portuguese"),
        ("JA", "Japanese"),
        ("ZH", "Chinese"),
    ]

    CATEGORY_CHOICES = [
        ("POP", "Pop"),
        ("ROCK", "Rock"),
        ("JAZZ", "Jazz"),
        ("HIPHOP", "Hip-Hop"),
        ("CLASSICAL", "Classical"),
        ("REGGAE", "Reggae"),
        ("LATIN", "Latin"),
        ("KPOP", "K-Pop"),
        ("COUNTRY", "Country"),
        ("BLUES", "Blues"),
        ("FOLK", "Folk"),
        ("ELECTRONIC", "Electronic"),
        ("R&B", "R&B"),
        ("SOUL", "Soul"),
        ("METAL", "Metal"),
        ("PUNK", "Punk"),
        ("ALTERNATIVE", "Alternative"),
        ("INDIE", "Indie"),
        ("GOSPEL", "Gospel"),
        ("WORLD", "World Music"),
    ]

    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES)
    audio_file = models.FileField(upload_to="")
    lrc_file = models.FileField(upload_to="")
    background_image = models.ImageField(upload_to="")
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    number_times_played = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.artist} - {self.title}"



class SongUser(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    played_at = models.DateTimeField(auto_now_add=True)
    correct_guesses = models.IntegerField(default=0)
    wrong_guesses = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.song.title}"