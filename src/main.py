# src/main.py
import pygame
import sys
from config import *
from utils.image_loader import ImageLoader

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Pi Golf")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # 이미지 로드
        self.images = {
            'sky': ImageLoader.load_image(IMAGES['BACKGROUND']['SKY']),
            'mountains': ImageLoader.load_image(IMAGES['BACKGROUND']['MOUNTAINS']),
            'ground': ImageLoader.load_image(IMAGES['BACKGROUND']['GROUND']),
            'golfer': ImageLoader.load_image(IMAGES['PLAYER']['GOLFER']),
            'ball': ImageLoader.load_image(IMAGES['OBJECTS']['BALL']),
            'flag': ImageLoader.load_image(IMAGES['OBJECTS']['FLAG']),
            'power_gauge': ImageLoader.load_image(IMAGES['UI']['POWER_GAUGE'])
        }
        
        # 월드 생성 (SRCALPHA 추가)
        self.world = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT), pygame.SRCALPHA)
        self.camera = pygame.Vector2(0, 0)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self):
        pass

    def draw(self):
        # 화면 클리어
        self.screen.fill((135, 206, 235))  # 하늘색으로 배경 채우기
        self.world.fill((0, 0, 0, 0))  # 월드 서피스를 투명하게 초기화
        
        # 배경 레이어 그리기
        self.world.blit(self.images['sky'], (0, 0))
        print(f"Sky dimensions: {self.images['sky'].get_size()}")  # 디버깅용
        
        # 산 레이어
        mountain_y = WINDOW_HEIGHT - self.images['mountains'].get_height()
        self.world.blit(self.images['mountains'], (0, mountain_y))
        print(f"Mountains position: (0, {mountain_y})")  # 디버깅용
        
        # 땅 레이어
        ground_y = WINDOW_HEIGHT - self.images['ground'].get_height()
        self.world.blit(self.images['ground'], (0, ground_y))
        print(f"Ground position: (0, {ground_y})")  # 디버깅용
        
        # 골퍼 그리기
        golfer_y = WINDOW_HEIGHT - self.images['golfer'].get_height() - 10
        self.world.blit(self.images['golfer'], (50, golfer_y))
        print(f"Golfer dimensions: {self.images['golfer'].get_size()}")  # 디버깅용
        
        # 골프공 그리기
        ball_y = WINDOW_HEIGHT - self.images['ball'].get_height() - 5
        self.world.blit(self.images['ball'], (90, ball_y))
        
        # 월드를 화면에 그리기
        self.screen.blit(self.world, (-self.camera.x, 0))
        
        # UI는 화면에 직접 그리기 (파워 게이지)
        gauge_pos = (WINDOW_WIDTH - self.images['power_gauge'].get_width() - 20, 20)
        self.screen.blit(self.images['power_gauge'], gauge_pos)
        print(f"Power gauge dimensions: {self.images['power_gauge'].get_size()}")  # 디버깅용
        
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = Game()
    game.run()