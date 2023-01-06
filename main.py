from machine import Pin
import network
import random
import socket
import sys
import time
import uasyncio

from config import WIFI_SSID, WIFI_PASS

def reset_led(pin):
    led = Pin(pin, Pin.OUT)
    led.on()
    time.sleep(0.1)
    led.off()
    return led

LEDS = {
    'system': { "left": 'LED' },
    "darth": { "left": 6, "right": 7 },
    "tie": { "left": 8, "right": 9 },
    "cannon": { "left": 10, "right": 11 }
}

for fighter in LEDS:
    if fighter == 'system': continue
    LEDS[fighter]['pin_left'] = reset_led(LEDS[fighter]['left'])
    LEDS[fighter]['pin_right'] = reset_led(LEDS[fighter]['right'])

LEDS['system']['pin_left'] = reset_led(LEDS['system']['left'])
print(LEDS)

wlan = network.WLAN(network.STA_IF)

def connect_to_network():
    wlan.active(True)
    wlan.config(pm = 0xa11140)  # Disable power-save mode
    wlan.connect(WIFI_SSID, WIFI_PASS)

    max_wait = 20
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)

    if wlan.status() != 3:
        raise RuntimeError('network connection failed')
    else:
        print('connected')
        status = wlan.ifconfig()
        print('ip = ' + status[0])


async def blink(pin, count, speed):
    for i in range(0, count*2):
        pin.toggle()
        await uasyncio.sleep_ms(speed)
        #time.sleep(speed/1000)

async def blink2(pin1, pin2, count, speed):
    pin1.off()
    pin2.off()
    for i in range(0, count*2):
        pin1.toggle()
        await uasyncio.sleep_ms(speed)
        pin2.toggle()
        #time.sleep(speed/1000)
    await uasyncio.sleep_ms(speed)
    pin1.off()
    pin2.off()
    print(f'finished blink2 for {pin1} and {pin2}')

async def pewpew(fighter, count, speed):
    await uasyncio.sleep_ms(random.randint(200,400))
    uasyncio.create_task(blink2(LEDS[fighter]['pin_left'], LEDS[fighter]['pin_right'], count, speed))
    print(f'finished setting up pewpew for {fighter}')


async def serve_client(reader, writer):
    print("Client connected")
    request_line = await reader.readline()
    print("Request:", request_line)
    # We are not interested in HTTP request headers, skip them
    while await reader.readline() != b"\r\n":
        pass

    request = str(request_line)
    do_pewpew = request.find('/api/v1/pewpew')
    print('do_pewpew', do_pewpew)

    response = '{"status": "ok"}'
    writer.write('HTTP/1.0 202 OK\r\nContent-type: application/json\r\n\r\n')
    writer.write(response)
    await writer.drain()
    await writer.wait_closed()
    print("Client disconnected")

    if do_pewpew > 0:
        uasyncio.create_task(pewpew('darth', 8, 100))
        uasyncio.create_task(pewpew('tie', 8, 100))
        uasyncio.create_task(pewpew('cannon', 8, 100))


async def heartbeat():
    reset_led('LED')

async def main():
    connect_to_network()
    uasyncio.create_task(uasyncio.start_server(serve_client, "0.0.0.0", 80))
    while True:
        await heartbeat()
        await uasyncio.sleep(2)

print('starting main')
try:
    uasyncio.run(main())
finally:
    uasyncio.new_event_loop()

