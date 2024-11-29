import pygame
import math
import sys
import os

# 상위 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.config import *
from src.utils.image_loader import ImageLoader

class PowerGauge(pygame.sprite.Sprite):
  
    def __init__(self):
        super().__init__()
        self.image = ImageLoader.load_image(IMAGES['UI']['POWER_GAUGE'])
        self.rect = self.image.get_rect()
        self.active = False
        self.angle = 0
        self.power = 0
        self.oscillating = False
        self.oscillation_speed = 3
        self.needle_surface = pygame.Surface((40, 4), pygame.SRCALPHA)
        
    def start_oscillation(self):
        self.oscillating = True
        self.angle = 0
        
    def stop_oscillation(self):
        self.oscillating = False
        # 현재 각도를 기반으로 파워와 각도 계산
        normalized_angle = (self.angle % 90) / 90.0
        self.power = normalized_angle * 100
        return self.power, self.angle
        
    def update(self):
        if self.oscillating:
            # sin 함수를 사용하여 -45도에서 45도 사이를 반복
            self.angle = math.sin(pygame.time.get_ticks() * 0.003) * 45
            
    def draw(self, surface, position):
        # 게이지 배경 그리기
        surface.blit(self.image, position)
        
        # 바늘 그리기
        needle_length = 40
        angle_rad = math.radians(self.angle)
        end_pos = (
            position[0] + needle_length * math.cos(angle_rad),
            position[1] + needle_length * math.sin(angle_rad)
        )
        pygame.draw.line(surface, (255, 255, 255), position, end_pos, 3)