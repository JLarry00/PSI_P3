import os
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from song_models.models import Song, SongUser

class Command(BaseCommand):
    help = "Populate database by scanning the media directory for song files."

    def handle(self, *args, **options):
        # 1. Limpieza de datos
        self.stdout.write("Cleaning existing data...")
        SongUser.objects.all().delete()
        Song.objects.all().delete()
        User.objects.all().delete()

        # 2. Usuarios base y superusuario
        user1 = User.objects.create_user(username="user1", password="user1password")
        user2 = User.objects.create_user(username="user2", password="user2password")
        User.objects.create_superuser(username="alumnodb", email="alumnodb@example.com", password="alumnodb")
        self.stdout.write(self.style.SUCCESS("Users and superuser 'alumnodb' created."))

        # 3. Escaneo dinámico de la carpeta media
        media_path = settings.MEDIA_ROOT
        if not os.path.exists(media_path):
            self.stdout.write(self.style.ERROR(f"Directory not found: {media_path}"))
            return

        # Buscamos todos los archivos .mp3 para usarlos como base
        audio_files = [f for f in os.listdir(media_path) if f.endswith('.mp3')]
        
        created_songs = []
        
        # Mapeo opcional para categorías/idiomas específicos basados en el artista
        metadata_map = {
            "Alan Jackson": {"language": "EN", "category": "COUNTRY"},
            "ABBA": {"language": "EN", "category": "POP"},
            "Bee Gees": {"language": "EN", "category": "POP"},
        }

        self.stdout.write(f"Scanning {media_path} for songs...")

        for audio_name in audio_files:
            # El nombre base suele ser "Artista - Título"
            base_name = os.path.splitext(audio_name)[0]
            
            try:
                artist, title = [part.strip() for part in base_name.split('-', 1)]
            except ValueError:
                artist, title = "Unknown", base_name

            # Buscamos archivos relacionados (.lrc y fotos)
            lrc_file = f"{base_name}.lrc"
            # Buscamos imagen (puede ser .jpg o .png)
            image_file = next((f for f in os.listdir(media_path) 
                             if f.startswith(base_name) and f.lower().endswith(('.jpg', '.png'))), "")

            # Obtener metadatos del mapa o usar valores por defecto
            meta = metadata_map.get(artist, {"language": "EN", "category": "POP"})

            song = Song.objects.create(
                title=title,
                artist=artist,
                language=meta["language"],
                category=meta["category"],
                audio_file=audio_name,
                lrc_file=lrc_file if os.path.exists(os.path.join(media_path, lrc_file)) else "",
                background_image=image_file
            )
            created_songs.append(song)
            self.stdout.write(self.style.SUCCESS(f"Detected and created: {artist} - {title}"))

        # 4. Crear relaciones SongUser
        self.stdout.write("Creating SongUser relations...")
        for i, song in enumerate(created_songs):
            SongUser.objects.create(
                song=song,
                user=user1 if i % 2 == 0 else user2,
                correct_guesses=i + 5,
                wrong_guesses=i
            )

        self.stdout.write(self.style.SUCCESS("Database population completed successfully."))
