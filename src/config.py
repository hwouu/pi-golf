# src/config.py
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
POWER_GAUGE_SPEED = 3  # 게이지 바늘 회전 속도
MAX_POWER = 100
BALL_SPEED = 5
GRAVITY = 9.8

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