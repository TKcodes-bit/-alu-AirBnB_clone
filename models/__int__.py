#!/usr/bin/python3
"""Initialize the models package and create a unique FileStorage instance."""

from models.engine.file_storage import FileStorage

# Create storage instance
storage = FileStorage()
# Reload objects from file.json, if it exists
storage.reload()

