# pico-w-api-async

controlling a Lego light kit with a Raspberry Pi Pico W via an API call to the Pico

This project was started with a desire to turn a Briksmax light kit for the Lego kit "Death Star Trench Run" (kit #75329) controlled by a Raspberry Pi to attach to a Twitch chatbot command called !pewpew.

Here it is in action:

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">Successful stream tonight, albeit with some pretty newb soldering skills, but our !pewpew chat command works great!<br>Now to get the RPi Pico to run the code without needing to be plugged into the PC... <a href="https://t.co/tBpbERUAuz">pic.twitter.com/tBpbERUAuz</a></p>&mdash; w. ian douglas 🇨🇦🇺🇸🥑🎙️ (@iandouglas736) <a href="https://twitter.com/iandouglas736/status/1611237264490901505?ref_src=twsrc%5Etfw">January 6, 2023</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

## requirements

- Raspberry Pi Pico W with header pins soldered on (at a minimum you only need to solder the pins you'll actually use)
  - for me that was:
    - pin 9, 10, 11, 12, 14, 15 for the 6 LEDs I want to blink
    - pin 13 for the ground that all LEDs will share
    - pine 38 and 40 to power the trench run lights that will always stay on (5 of them)
  - soldering the tiny Bricksmax wires to larger female socket ends to connect to the Pico's pins was the hardest part of the project
    - if I had to do this over again, I might strip more of the wires, wrap the wire all around the Pico's connector and solder it directly onto the Pico connector pad instead of dealing with pins and sockets
- Micropython installed

## code

put your wifi credentials in config.py

there are a few helper methods defined in main.py to reset LEDs, make two of them blink in an alternating pattern, and more

