# src/sprites/gauge.py
import pygame
import math
from ..config import *

class PowerGauge(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.active = False
        self.angle = 0  # 바늘의 현재 각도
        self.power = 0  # 현재 파워 값
        
        # 게이지 배경 - 부채꼴 모양으로 그리기
        self.image = pygame.Surface((100, 100), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        
        # 색상 구분된 부채꼴 그리기
        self.colors = [
            (255, 0, 0),    # 빨강
            (255, 165, 0),  # 주황
            (255, 255, 0),  # 노랑
            (0, 255, 0)     # 초록
        ]
        
        # 각 색상 구역의 크기
        self.section_angle = 90 / len(self.colors)
        
    def draw_gauge(self, surface, pos):
        # 배경 부채꼴 그리기
        radius = 40
        start_angle = -45  # 시작 각도
        
        for i, color in enumerate(self.colors):
            section_start = math.radians(start_angle + (i * self.section_angle))
            section_end = math.radians(start_angle + ((i + 1) * self.section_angle))
            
            pygame.draw.arc(surface, color, (pos[0]-radius, pos[1]-radius, radius*2, radius*2),
                          section_start, section_end, 5)
        
        # 바늘 그리기
        angle_rad = math.radians(self.angle - 45)  # -45도에서 시작
        needle_length = radius - 5
        end_pos = (pos[0] + math.cos(angle_rad) * needle_length,
                  pos[1] + math.sin(angle_rad) * needle_length)
        pygame.draw.line(surface, (255, 255, 255), pos, end_pos, 3)
        
    def update(self):
        if self.active:
            # 바늘을 일정 속도로 회전
            self.angle = (self.angle + POWER_GAUGE_SPEED) % 90
            # 파워 값 계산 (0-100)
            self.power = (self.angle / 90) * 100
            
    def get_power(self):
        # 현재 파워 값 반환
        return self.power