#!/usr/bin/python3
"""Initialize the models package and storage engine."""

from models.engine.file_storage import FileStorage

# Single storage instance for the application
storage = FileStorage()
storage.reload()

