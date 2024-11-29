# src/config.py

try:
   import board
   import digitalio
   USE_GPIO = True
except (ImportError, NotImplementedError):
   USE_GPIO = False

# 디스플레이 설정
WINDOW_WIDTH = 240
WINDOW_HEIGHT = 240
WORLD_WIDTH = 800  # 실제 게임 월드의 너비 (200야드를 픽셀로 환산)
WORLD_HEIGHT = 240
FPS = 60

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)
SKY_BLUE = (135, 206, 235)



# 게임 설정
POWER_GAUGE_SPEED = 3     # 게이지 바늘 회전 속도
MAX_POWER = 100
BALL_SPEED = 5
GRAVITY = 9.8
GAUGE_SPEED = 3          # 게이지 바늘 움직임 속도
BALL_POWER_BASE = 0.8    # 기본 발사 세기
BALL_POWER_FACTOR = 0.3  # 공의 발사 세기 (낮출수록 덜 강하게 날아감)
GRAVITY_SCALE = 0.1      # 중력 영향력
CAMERA_SMOOTH = 0.1      # 카메라 움직임 부드러움
HOLE_POSITION = 600  # 홀 위치 (x좌표)
WIN_DISTANCE = 10    # 홀컵과 공의 거리가 이 값보다 작으면 성공

# 각도 설정
ANGLE_CHANGE_SPEED = 2   # 방향키로 각도 조절 속도
MIN_ANGLE = -60         # 최소 각도
MAX_ANGLE = 0          # 최대 각도
INITIAL_ANGLE = -45    # 시작 각도

# GPIO 버튼 설정
if USE_GPIO:
   button_U = digitalio.DigitalInOut(board.D17)
   button_D = digitalio.DigitalInOut(board.D22)
   button_L = digitalio.DigitalInOut(board.D27)
   button_R = digitalio.DigitalInOut(board.D23)
   button_A = digitalio.DigitalInOut(board.D5)
   button_B = digitalio.DigitalInOut(board.D6)
   button_C = digitalio.DigitalInOut(board.D4)

   for button in [button_U, button_D, button_L, button_R, button_A, button_B, button_C]:
       button.direction = digitalio.Direction.INPUT

# 이미지 경로
IMAGES = {
   'BACKGROUND': {
       'SKY': 'background/sky.png',
       'MOUNTAINS': 'background/mountains.png',
       'GROUND': 'background/ground.png'
   },
   'PLAYER': {
       'GOLFER': 'player/golfer.png'
   },
   'OBJECTS': {
       'BALL': 'objects/ball.png',
       'FLAG': 'objects/flag.png'
   },
   'UI': {
       'POWER_GAUGE': 'ui/power-gauge.png'
   }
}

# 입력 키 매핑
KEYS = {
   'SHOT': ['K_l', 'GPIO_5'],       # L키 또는 GPIO #5 버튼
   'LEFT': ['K_a', 'GPIO_27'],      # A키 또는 조이스틱 왼쪽
   'RIGHT': ['K_d', 'GPIO_23'],     # D키 또는 조이스틱 오른쪽
   'UP': ['K_w', 'GPIO_17'],        # W키 또는 조이스틱 위
   'DOWN': ['K_s', 'GPIO_22'],      # S키 또는 조이스틱 아래
}