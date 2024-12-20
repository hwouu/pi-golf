# src/utils/joystick.py
try:
    import board
    import digitalio
    from adafruit_rgb_display import st7789
    USE_GPIO = True
except (ImportError, NotImplementedError):
    USE_GPIO = False

class Joystick:
    def __init__(self):
        if USE_GPIO:
            # TFT 디스플레이 설정
            self.cs_pin = digitalio.DigitalInOut(board.CE0)
            self.dc_pin = digitalio.DigitalInOut(board.D25)
            self.reset_pin = digitalio.DigitalInOut(board.D24)
            self.BAUDRATE = 24000000

            self.spi = board.SPI()
            self.disp = st7789.ST7789(
                self.spi,
                height=240,
                y_offset=80,
                rotation=180,
                cs=self.cs_pin,
                dc=self.dc_pin,
                rst=self.reset_pin,
                baudrate=self.BAUDRATE,
            )

            # 버튼 설정
            self.button_5 = digitalio.DigitalInOut(board.D5)  # #5 버튼
            self.button_6 = digitalio.DigitalInOut(board.D6)  # #6 버튼
            self.button_L = digitalio.DigitalInOut(board.D27)  # 조이스틱 왼쪽
            self.button_R = digitalio.DigitalInOut(board.D23)  # 조이스틱 오른쪽
            self.button_U = digitalio.DigitalInOut(board.D17)  # 조이스틱 위
            self.button_D = digitalio.DigitalInOut(board.D22)  # 조이스틱 아래
            self.button_C = digitalio.DigitalInOut(board.D4)   # 조이스틱 중앙

            for button in [self.button_5, self.button_6, self.button_L, 
                         self.button_R, self.button_U, self.button_D, self.button_C]:
                button.direction = digitalio.Direction.INPUT

            # 백라이트 설정
            self.backlight = digitalio.DigitalInOut(board.D26)
            self.backlight.switch_to_output()
            self.backlight.value = True

            # 디스플레이 크기
            self.width = self.disp.width
            self.height = self.disp.height