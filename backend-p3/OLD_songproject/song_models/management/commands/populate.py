from pathlib import Path

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File
from django.core.management.base import BaseCommand

from song_models.models import Song, SongUser


class Command(BaseCommand):
    help = "Populate the database with sample users, songs and song-user relations."

    def handle(self, *args, **options):
        self.stdout.write("Cleaning existing data...")

        # Delete existing data to avoid duplicates
        SongUser.objects.all().delete()
        Song.objects.all().delete()
        User.objects.all().delete()

        self.stdout.write("Creating users...")
        user1 = User.objects.create_user(username="user1", password="user1password")
        user2 = User.objects.create_user(username="user2", password="user2password")
        admin = User.objects.create_superuser(
            username="alumnodb",
            email="alumnodb@example.com",
            password="alumnodb",
        )

        self.stdout.write(
            f"Created users: {user1.username}, {user2.username}, superuser {admin.username}"
        )

        # Directory where the provided media files are located
        project_root = Path(settings.BASE_DIR)
        media_source_dir = project_root / "media"

        if not media_source_dir.exists():
            self.stdout.write(
                self.style.ERROR(f"Media directory not found: {media_source_dir}")
            )
            return

        self.stdout.write(f"Using media files from: {media_source_dir}")

        songs_data = [
            {
                "title": "Super Trouper",
                "artist": "ABBA",
                "language": "EN",
                "category": "POP",
                "audio": "ABBA - Super Trouper.mp3",
                "lrc": "ABBA - Super Trouper.lrc",
                "image": "ABBA - Super Trouper.jpg",
            },
            {
                "title": "Here In The Real World",
                "artist": "Alan Jackson",
                "language": "EN",
                "category": "COUNTRY",
                "audio": "Alan Jackson - Here In The Real World.mp3",
                "lrc": "Alan Jackson - Here In The Real World.lrc",
                "image": "Alan Jackson - Here In The Real World.jpg",
            },
            {
                "title": "Don't Forget to Remember",
                "artist": "Bee Gees",
                "language": "EN",
                "category": "POP",
                "audio": "Beegees - Don't Forget to Remember.mp3",
                "lrc": "Beegees - Don't Forget to Remember.lrc",
                "image": "Beegees - Don't Forget to Remember.png",
            },
        ]

        created_songs = []

        self.stdout.write("Creating songs...")

        for data in songs_data:
            try:
                audio_path = media_source_dir / data["audio"]
                lrc_path = media_source_dir / data["lrc"]
                image_path = media_source_dir / data["image"]

                if not (audio_path.exists() and lrc_path.exists() and image_path.exists()):
                    self.stdout.write(
                        self.style.WARNING(
                            f"Skipping song '{data['title']}' because one or more files are missing."
                        )
                    )
                    continue

                with audio_path.open("rb") as audio_file, lrc_path.open(
                    "rb"
                ) as lrc_file, image_path.open("rb") as image_file:
                    song = Song.objects.create(
                        title=data["title"],
                        artist=data["artist"],
                        language=data["language"],
                        category=data["category"],
                        audio_file=File(audio_file, name=audio_path.name),
                        lrc_file=File(lrc_file, name=lrc_path.name),
                        background_image=File(image_file, name=image_path.name),
                    )
                    created_songs.append(song)
                    self.stdout.write(
                        self.style.SUCCESS(f"Created song: {song.artist} - {song.title}")
                    )
            except Exception as exc:  # noqa: BLE001
                self.stdout.write(
                    self.style.ERROR(
                        f"Error creating song '{data['title']}': {exc!r}"
                    )
                )

        self.stdout.write("Creating SongUser relations...")

        for index, song in enumerate(created_songs):
            SongUser.objects.create(
                song=song,
                user=user1 if index % 2 == 0 else user2,
                correct_guesses=index + 1,
                wrong_guesses=0,
            )

        self.stdout.write(self.style.SUCCESS("Database population completed successfully."))