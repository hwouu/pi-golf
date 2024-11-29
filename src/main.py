# src/main.py
from PIL import Image, ImageDraw
import pygame
import sys
import math
import os
import time
from enum import Enum
from config import *
from sprites.gauge import PowerGauge
from utils.image_loader import ImageLoader
from utils.joystick import Joystick, USE_GPIO

class GameState(Enum):
   READY = "READY"       # 시작 상태
   AIMING = "AIMING"     # 조준 중
   POWER = "POWER"       # 파워 게이지 조절 중
   SHOT = "SHOT"         # 공이 날아가는 중
   SUCCESS = "SUCCESS"   # 홀인원/버디 성공
   FAIL = "FAIL"        # 실패 (시도 횟수 초과)

class Game:
   def __init__(self):
       if USE_GPIO:
           self.joystick = Joystick()
           self.image = Image.new("RGB", (self.joystick.width, self.joystick.height))
           self.image_draw = ImageDraw.Draw(self.image)  # draw -> image_draw로 변경
       else:
           pygame.init()
           self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
           pygame.display.set_caption("Pi Golf")
       
       self.clock = pygame.time.Clock()
       self.running = True
       
       # 게임 상태 초기화
       self.game_state = GameState.READY
       self.shot_count = 0
       self.max_shots = 3
       self.score = 0
       
       # 게임 오브젝트 초기화
       self.power_gauge = PowerGauge()
       self.ball_position = pygame.Vector2(90, WINDOW_HEIGHT - 20)
       self.ball_velocity = pygame.Vector2(0, 0)
       self.ball_in_motion = False
       self.aim_angle = INITIAL_ANGLE
       self.flag_position = pygame.Vector2(HOLE_POSITION, WINDOW_HEIGHT - 40)
       
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
       
       # 월드 생성 (pygame 모드용)
       if not USE_GPIO:
           self.world = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT), pygame.SRCALPHA)
       self.camera = pygame.Vector2(0, 0)

   def handle_events(self):
       if USE_GPIO:
           if self.game_state == GameState.READY or self.game_state == GameState.AIMING:
               if not self.joystick.button_U.value:  # 위쪽
                   self.aim_angle = max(self.aim_angle - ANGLE_CHANGE_SPEED, MIN_ANGLE)
               if not self.joystick.button_D.value:  # 아래쪽
                   self.aim_angle = min(self.aim_angle + ANGLE_CHANGE_SPEED, MAX_ANGLE)
               if not self.joystick.button_5.value:  # #5 버튼으로 변경 (이전의 A 버튼 대신)
                   self.game_state = GameState.POWER
                   self.power_gauge.start_oscillation()
               elif self.power_gauge.oscillating:  # #5 버튼을 뗐을 때 
                    power, angle = self.power_gauge.stop_oscillation()
                    self.shoot_ball(power)
                    self.game_state = GameState.SHOT
       else:
           for event in pygame.event.get():
               if event.type == pygame.QUIT:
                   self.running = False
               elif event.type == pygame.KEYDOWN:
                   if event.key == pygame.K_ESCAPE:
                       self.running = False
                   elif event.key == pygame.K_l and (self.game_state == GameState.READY or self.game_state == GameState.AIMING):
                       self.game_state = GameState.POWER
                       self.power_gauge.start_oscillation()
               elif event.type == pygame.KEYUP:
                   if event.key == pygame.K_l and self.game_state == GameState.POWER:
                       power, angle = self.power_gauge.stop_oscillation()
                       self.shoot_ball(power)
                       self.game_state = GameState.SHOT

           if self.game_state == GameState.READY or self.game_state == GameState.AIMING:
               keys = pygame.key.get_pressed()
               if keys[pygame.K_UP]:
                   self.aim_angle = max(self.aim_angle - ANGLE_CHANGE_SPEED, MIN_ANGLE)
               if keys[pygame.K_DOWN]:
                   self.aim_angle = min(self.aim_angle + ANGLE_CHANGE_SPEED, MAX_ANGLE)

   def shoot_ball(self, power):
       self.shot_count += 1
       angle_rad = math.radians(self.aim_angle)
       initial_speed = power * BALL_POWER_BASE
       self.ball_velocity.x = math.cos(angle_rad) * initial_speed
       self.ball_velocity.y = -math.sin(angle_rad) * initial_speed
       self.ball_in_motion = True

   def update_game_state(self):
       if self.game_state == GameState.SHOT:
           if not self.ball_in_motion:
               if abs(self.ball_position.x - self.flag_position.x) < WIN_DISTANCE:
                   self.game_state = GameState.SUCCESS
                   self.calculate_score()
               elif self.shot_count >= self.max_shots:
                   self.game_state = GameState.FAIL
               else:
                   self.game_state = GameState.AIMING

   def calculate_score(self):
       if self.shot_count == 1:
           self.score = 100  # 홀인원
       elif self.shot_count == 2:
           self.score = 50   # 버디
       else:
           self.score = 25   # 파

   def update(self):
       self.power_gauge.update()
       
       if self.ball_in_motion:
           # 공의 물리 업데이트
           self.ball_velocity.y += GRAVITY * GRAVITY_SCALE
           self.ball_position += self.ball_velocity
           
           # 바닥 충돌 체크
           if self.ball_position.y > WINDOW_HEIGHT - 20:
               self.ball_position.y = WINDOW_HEIGHT - 20
               self.ball_velocity.y = 0
               self.ball_in_motion = False
           
           # 카메라 업데이트
           target_x = max(0, self.ball_position.x - WINDOW_WIDTH/3)
           self.camera.x += (target_x - self.camera.x) * CAMERA_SMOOTH
       
       self.update_game_state()

   def draw_tft(self):
       try:
           # TFT 디스플레이용 그리기
           self.image = Image.new("RGB", (self.joystick.width, self.joystick.height))
           self.image_draw = ImageDraw.Draw(self.image)
           
           # 배경 색상
           self.image_draw.rectangle((0, 0, self.joystick.width, self.joystick.height), 
                             fill=(135, 206, 235))
           
           # 배경 타일링
           sky_width = self.images['sky'].width
           num_tiles = (WORLD_WIDTH // sky_width) + 2
           
           for i in range(num_tiles):
               x_pos = i * sky_width - int(self.camera.x % sky_width)
               # PIL 이미지 붙여넣기
               self.image.paste(self.images['sky'], (x_pos, 0))
               self.image.paste(self.images['mountains'], 
                              (x_pos, WINDOW_HEIGHT - self.images['mountains'].height))
               self.image.paste(self.images['ground'],
                              (x_pos, WINDOW_HEIGHT - self.images['ground'].height))
           
           # 깃발 그리기
           flag_x = int(self.flag_position.x - self.camera.x)
           flag_y = int(self.flag_position.y)
           self.image.paste(self.images['flag'], (flag_x, flag_y))
           
           # 골퍼 그리기
           golfer_y = WINDOW_HEIGHT - self.images['golfer'].height - 10
           self.image.paste(self.images['golfer'], (50, golfer_y))
           
           # 골프공 그리기
           ball_x = int(self.ball_position.x - self.camera.x - self.images['ball'].width/2)
           ball_y = int(self.ball_position.y - self.images['ball'].height/2)
           self.image.paste(self.images['ball'], (ball_x, ball_y))
           
           # 조준선 그리기
           if self.game_state in [GameState.READY, GameState.AIMING]:
               start_pos = (int(self.ball_position.x - self.camera.x), 
                           int(self.ball_position.y))
               angle_rad = math.radians(self.aim_angle)
               end_pos = (int(start_pos[0] + math.cos(angle_rad) * 50),
                         int(start_pos[1] + math.sin(angle_rad) * 50))
               self.image_draw.line([start_pos, end_pos], fill=(255, 0, 0), width=2)
           
           # TFT 디스플레이 업데이트
           self.joystick.disp.image(self.image)
       except Exception as e:
           print(f"Draw TFT error: {e}")

   def draw_pygame(self):
       # Pygame용 그리기
       self.screen.fill(SKY_BLUE)
       self.world.fill((0, 0, 0, 0))
       
       # 배경 타일링
       sky_width = self.images['sky'].get_width()
       num_tiles = (WORLD_WIDTH // sky_width) + 2
       
       for i in range(num_tiles):
           x_pos = i * sky_width - (self.camera.x % sky_width)
           self.world.blit(self.images['sky'], (x_pos, 0))
           self.world.blit(self.images['mountains'], 
                         (x_pos, WINDOW_HEIGHT - self.images['mountains'].get_height()))
           self.world.blit(self.images['ground'],
                         (x_pos, WINDOW_HEIGHT - self.images['ground'].get_height()))
       
       # 깃발 그리기
       flag_pos = (self.flag_position.x - self.camera.x, self.flag_position.y)
       self.world.blit(self.images['flag'], flag_pos)
       
       # 골퍼 그리기
       golfer_y = WINDOW_HEIGHT - self.images['golfer'].get_height() - 10
       self.world.blit(self.images['golfer'], (50, golfer_y))
       
       # 골프공 그리기
       ball_pos = (self.ball_position.x - self.images['ball'].get_width()/2,
                  self.ball_position.y - self.images['ball'].get_height()/2)
       self.world.blit(self.images['ball'], ball_pos)
       
       # 조준선 그리기
       if self.game_state in [GameState.READY, GameState.AIMING]:
           start_pos = (int(self.ball_position.x), int(self.ball_position.y))
           angle_rad = math.radians(self.aim_angle)
           end_pos = (int(start_pos[0] + math.cos(angle_rad) * 50),
                     int(start_pos[1] + math.sin(angle_rad) * 50))
           pygame.draw.line(self.world, (255, 0, 0), start_pos, end_pos, 2)
       
       # 월드를 화면에 그리기
       self.screen.blit(self.world, (-self.camera.x, 0))
       
       # 파워 게이지 그리기
       gauge_pos = (WINDOW_WIDTH - 80, 20)
       self.power_gauge.draw(self.screen, gauge_pos)
       
       # 게임 상태 표시
       if self.game_state in [GameState.SUCCESS, GameState.FAIL]:
           font = pygame.font.Font(None, 36)
           text = f"Score: {self.score}" if self.game_state == GameState.SUCCESS else "Game Over"
           text_surface = font.render(text, True, (255, 255, 255))
           text_rect = text_surface.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
           self.screen.blit(text_surface, text_rect)
       
       pygame.display.flip()

   def run(self):
       while self.running:
           self.handle_events()
           self.update()
           if USE_GPIO:
               self.draw_tft()
           else:
               self.draw_pygame()
           
           if not USE_GPIO:
               self.clock.tick(FPS)
           else:
               time.sleep(1/FPS)
       
       if not USE_GPIO:
           pygame.quit()
       sys.exit()

if __name__ == '__main__':
   game = Game()
   game.run()