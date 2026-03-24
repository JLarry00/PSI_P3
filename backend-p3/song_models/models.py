from django.db import models
from django.contrib.auth.models import User
# Añade estas importaciones para las señales
from django.db.models.signals import post_save
from django.dispatch import receiver


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

    class Meta:
        unique_together = ('song', 'user')

    @classmethod
    def create_or_update(cls, song, request, **kwargs):
        """
        Crea un SongUser si no existe para la pareja song/user.
        El usuario se obtiene de la sesión (request.user).
        Si existe, actualiza los campos con los valores proporcionados en kwargs.
        Devuelve la instancia y un booleano created (True si se creó, False si se actualizó).
        """
        user = getattr(request, "user", None)
        if user is None or not user.is_authenticated:
            raise ValueError("No authenticated user in session.")
        obj, created = cls.objects.get_or_create(song=song, user=user, defaults=kwargs)
        if not created:
            updated = False
            for key, value in kwargs.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
                    updated = True
            if updated:
                obj.save()
        return obj, created
    
    # api -> coger usuario de la sesion

@receiver(post_save, sender=SongUser)
def update_song_play_count(sender, instance, created, **kwargs):
    if created:
        song = instance.song
        song.number_times_played += 1
        song.save()