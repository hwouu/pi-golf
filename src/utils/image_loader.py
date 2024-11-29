# src/utils/image_loader.py 수정
import os
from PIL import Image

class ImageLoader:
    ASSETS_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets', 'images')
    
    @staticmethod
    def load_image(path: str, scale: float = 1.0):
        """이미지를 로드하고 scale 값에 따라 크기를 조정합니다."""
        full_path = os.path.join(ImageLoader.ASSETS_PATH, path)
        print(f"Loading image from: {full_path}")
        try:
            # PIL Image로 로드하고 RGBA 모드로 변환
            image = Image.open(full_path).convert('RGBA')
            if scale != 1.0:
                new_size = (int(image.width * scale), int(image.height * scale))
                image = image.resize(new_size)
            return image
        except Exception as e:
            print(f"Couldn't load image: {path}")
            print(e)
            # 에러 발생 시 빨간색 이미지 생성
            error_image = Image.new('RGBA', (50, 50), (255, 0, 0, 255))
            return error_image