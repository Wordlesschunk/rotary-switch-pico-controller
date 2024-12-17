import time
import board
import digitalio

import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

try:
    # Setup the keyboard
    keyboard = Keyboard(usb_hid.devices)

    # Set up the LED pin (change 'board.LED' to your specific GPIO pin if needed)
    LED = digitalio.DigitalInOut(board.LED)
    LED.direction = digitalio.Direction.OUTPUT

    # Set up GPIO pins 1 to 10 as inputs (first switch inputs)
    signal_pins_1 = []
    for i in range(1, 11):  # GP1 to GP10
        pin = digitalio.DigitalInOut(getattr(board, f"GP{i}"))
        pin.direction = digitalio.Direction.INPUT
        pin.pull = digitalio.Pull.DOWN
        signal_pins_1.append(pin)

    # Set up GPIO pins 11 to 20 as inputs (second switch inputs)
    signal_pins_2 = []
    for i in range(11, 21):  # GP11 to GP20
        pin = digitalio.DigitalInOut(getattr(board, f"GP{i}"))
        pin.direction = digitalio.Direction.INPUT
        pin.pull = digitalio.Pull.DOWN
        signal_pins_2.append(pin)

    print("Waiting for signals on GPIO pins 1 to 20...")

    # Variables to store the previous state of the signal pins and the last active pin
    previous_signals_1 = [False] * 10  # For pins 1–10
    previous_signals_2 = [False] * 10  # For pins 11–20
    last_active_pin_1 = None  # Last active pin for first switch
    last_active_pin_2 = None  # Last active pin for second switch

    while True:
        # Read the signals for GPIO pins 1–10 (first switch)
        for i, pin in enumerate(signal_pins_1):
            current_signal = pin.value

            # If the signal on any pin changes from low to high
            if current_signal and not previous_signals_1[i]:
                LED.value = not LED.value
                print(f"LED {'ON' if LED.value else 'OFF'} (Current Selected Value: GP{i+1})")

                # Determine if the current pin is greater or less than the last active pin
                if last_active_pin_1 is not None:
                    if i > last_active_pin_1:
                        keyboard.press(Keycode.G)  # Press the 't' key
                        print("Typed 'G'")
                    else:
                        keyboard.press(Keycode.T)  # Press the 'g' key
                        print("Typed 'T'")
                else:
                    print("No previous pin to compare.")

                keyboard.release_all()
                last_active_pin_1 = i

            # Update the previous signal state for the current pin
            previous_signals_1[i] = current_signal

        # Read the signals for GPIO pins 11–20 (second switch)
        for i, pin in enumerate(signal_pins_2):
            current_signal = pin.value

            # If the signal on any pin changes from low to high
            if current_signal and not previous_signals_2[i]:
                LED.value = not LED.value
                print(f"LED {'ON' if LED.value else 'OFF'} (Current Selected Value: GP{i+11})")

                # Determine if the current pin is greater or less than the last active pin
                if last_active_pin_2 is not None:
                    if i > last_active_pin_2:
                        keyboard.press(Keycode.J)  # Press the 'w' key
                        print("Typed 'J'")
                    else:
                        keyboard.press(Keycode.U)  # Press the 's' key
                        print("Typed 'U'")
                else:
                    print("No previous pin to compare.")

                keyboard.release_all()
                last_active_pin_2 = i

            # Update the previous signal state for the current pin
            previous_signals_2[i] = current_signal

        time.sleep(0.1)  # Small delay to debounce and avoid excessive CPU usage

except KeyboardInterrupt:
    print("Script interrupted by user.")
except Exception as e:
    print(f"An error occurred: {e}")
    
finally:
    LED.value = False  # Turn off the LED on exit
    print("Exiting script. LED is OFF.")