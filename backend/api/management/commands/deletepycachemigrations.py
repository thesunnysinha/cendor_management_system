import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    """Django command to delete migration and __pycache__ directories"""

    def handle(self, *args, **options):
        project_directory = settings.BASE_DIR

        app_directories = [
            app for app in os.listdir(project_directory)
            if os.path.isdir(os.path.join(project_directory, app))
        ]

        for app in app_directories:
            app_directory = os.path.join(project_directory, app)
            self.delete_nested_directories(app_directory)

    def delete_nested_directories(self, directory):
        migrations_directory = os.path.join(directory, "migrations")
        pycache_directory = os.path.join(directory, "__pycache__")

        self.delete_directory(migrations_directory)
        self.delete_directory(pycache_directory)

        # Traverse subdirectories
        for root, dirs, files in os.walk(directory):
            for dir_name in dirs:
                subdirectory = os.path.join(root, dir_name)
                migrations_directory = os.path.join(subdirectory, "migrations")
                pycache_directory = os.path.join(subdirectory, "__pycache__")

                self.delete_directory(migrations_directory)
                self.delete_directory(pycache_directory)

    def delete_directory(self, directory):
        if os.path.exists(directory):
            shutil.rmtree(directory)
            self.stdout.write(self.style.SUCCESS(f"Deleted: {directory}"))
        else:
            self.stdout.write(self.style.ERROR(f"Directory not found: {directory}"))
