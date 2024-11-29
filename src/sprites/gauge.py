# src/sprites/gauge.py
import pygame
import math
import sys
import os
from PIL import Image
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from config import *
from utils.image_loader import ImageLoader

class PowerGauge(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # PIL Image를 pygame Surface로 변환
        pil_image = ImageLoader.load_image(IMAGES['UI']['POWER_GAUGE'])
        if USE_GPIO:
            self.image = pil_image  # TFT 디스플레이용으로는 PIL Image 사용
        else:
            # PIL Image를 pygame Surface로 변환
            image_data = np.array(pil_image)
            self.image = pygame.surfarray.make_surface(image_data.transpose(1, 0, 2))
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
        normalized_angle = (self.angle % 90) / 90.0
        self.power = normalized_angle * 100
        return self.power, self.angle
        
    def update(self):
        if self.oscillating:
            self.angle = math.sin(pygame.time.get_ticks() * 0.003) * 45
            
    def draw(self, surface, position):
        if USE_GPIO:
            # TFT 디스플레이용 그리기
            surface.paste(self.image, position)
            # 바늘 그리기는 별도로 처리
            needle_length = 40
            angle_rad = math.radians(self.angle)
            end_pos = (
                int(position[0] + needle_length * math.cos(angle_rad)),
                int(position[1] + needle_length * math.sin(angle_rad))
            )
            ImageDraw.Draw(surface).line(
                [position, end_pos],
                fill=(255, 255, 255),
                width=3
            )
        else:
            # Pygame용 그리기
            surface.blit(self.image, position)
            needle_length = 40
            angle_rad = math.radians(self.angle)
            end_pos = (
                position[0] + needle_length * math.cos(angle_rad),
                position[1] + needle_length * math.sin(angle_rad)
            )
            pygame.draw.line(surface, (255, 255, 255), position, end_pos, 3)