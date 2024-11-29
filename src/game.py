# src/game.py
from enum import Enum

class GameState(Enum):
    READY = "READY"       # 시작 상태
    AIMING = "AIMING"     # 조준 중
    POWER = "POWER"       # 파워 게이지 조절 중
    SHOT = "SHOT"         # 공이 날아가는 중
    SUCCESS = "SUCCESS"   # 홀인원/버디 성공
    FAIL = "FAIL"        # 실패 (시도 횟수 초과)

class Game:
    def __init__(self):
        self.state = GameState.READY
        self.shot_count = 0
        self.max_shots = 3
        self.score = 0
    
    def update_game_state(self, ball_position):
        if self.state == GameState.SHOT:
            # 공이 멈췄는지 확인
            if abs(ball_position.x - HOLE_POSITION) < WIN_DISTANCE:
                self.state = GameState.SUCCESS
                self.calculate_score()
            elif self.shot_count >= self.max_shots:
                self.state = GameState.FAIL
    
    def calculate_score(self):
        if self.shot_count == 1:
            self.score = 100  # 홀인원
        elif self.shot_count == 2:
            self.score = 50   # 버디
        else:
            self.score = 25   # 파