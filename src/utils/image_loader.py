# src/utils/image_loader.py
import os
import pygame

class ImageLoader:
    ASSETS_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets', 'images')
    
    @staticmethod
    def load_image(path: str, scale: float = 1.0) -> pygame.Surface:
        """이미지를 로드하고 scale 값에 따라 크기를 조정합니다."""
        full_path = os.path.join(ImageLoader.ASSETS_PATH, path)
        print(f"Loading image from: {full_path}")  # 디버깅용 로그 추가
        try:
            image = pygame.image.load(full_path).convert_alpha()
            if scale != 1.0:
                new_size = (int(image.get_width() * scale), int(image.get_height() * scale))
                image = pygame.transform.scale(image, new_size)
            print(f"Successfully loaded image: {path}")  # 성공 로그
            return image
        except pygame.error as e:
            print(f"Couldn't load image: {path}")
            print(e)
            # 에러 발생 시 표시할 기본 surface 반환
            surface = pygame.Surface((50, 50), pygame.SRCALPHA)
            surface.fill((255, 0, 0, 128))
            return surface