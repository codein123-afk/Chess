from pathlib import Path

import pygame

import os

IMAGE_DIR = Path(__file__).resolve().parent / "images"

def load_piece(path, size):

    filename = os.path.basename(path)

    image = pygame.image.load(str(IMAGE_DIR / filename))

    return pygame.transform.scale(image, (size, size))