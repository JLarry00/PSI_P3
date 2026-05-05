from pathlib import Path
from tempfile import TemporaryDirectory

from django.test import SimpleTestCase, override_settings


class MediaServingTests(SimpleTestCase):
    @override_settings(DEBUG=False)
    def test_media_files_are_served_when_debug_is_disabled(self):
        with TemporaryDirectory() as temp_dir:
            sample_file = Path(temp_dir) / "sample.lrc"
            sample_file.write_text("[00:00.00] Lyrics", encoding="utf-8")

            with override_settings(MEDIA_ROOT=temp_dir):
                response = self.client.get("/media/sample.lrc")

            self.assertEqual(response.status_code, 200)
            content = b"".join(response.streaming_content).decode("utf-8")
            self.assertEqual(content, "[00:00.00] Lyrics")
