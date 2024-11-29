# src/utils/image_loader.py
import os
import pygame
from PIL import Image

class ImageLoader:
    ASSETS_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets', 'images')
    
    @staticmethod
    def load_image(path: str, scale: float = 1.0):
        """이미지를 로드하고 scale 값에 따라 크기를 조정합니다."""
        full_path = os.path.join(ImageLoader.ASSETS_PATH, path)
        print(f"Loading image from: {full_path}")
        try:
            # PIL Image로 먼저 로드
            pil_image = Image.open(full_path)
            if scale != 1.0:
                new_size = (int(pil_image.width * scale), int(pil_image.height * scale))
                pil_image = pil_image.resize(new_size)
            return pil_image
        except Exception as e:
            print(f"Couldn't load image: {path}")
            print(e)
            # 에러 발생 시 빨간색 이미지 생성
            error_image = Image.new('RGB', (50, 50), (255, 0, 0))
            return error_image