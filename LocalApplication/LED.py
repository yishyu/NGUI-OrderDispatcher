import time
import board
import neopixel

class LEDManager():
    def __init__(self):
        # Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
        # NeoPixels must be connected to D10, D12, D18 or D21 to work.
        pixel_pin = board.D18
        # The number of NeoPixels
        num_pixels = 4
        # The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
        # For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
        ORDER = neopixel.GRBW
        self.pixels = neopixel.NeoPixel(
            pixel_pin, num_pixels, auto_write=False, brightness=1, pixel_order=ORDER
        )
        self.pixels.fill(0)
        self.leds = {"#ff0000": (0, 0xff0000), "#00ff00": (1, 0x00ff00), "#0000ff": (2, 0x0000ff), "#6a0dad": (3, 0x6a0dad)}

    def light_up_led(self, color):
        self.pixels.fill(0)
        self.pixels[self.leds[color][0]] = self.leds[color][1]
        self.pixels.show()

if __name__ == "__main__":
    led_manager = LEDManager()
    led_manager.light_up_led("#ff0000")
    time.sleep(0.5)
    led_manager.light_up_led("#00ff00")
    time.sleep(0.5)
    led_manager.light_up_led("#0000ff")
    time.sleep(0.5)
    led_manager.light_up_led("#6a0dad")
