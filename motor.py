import socket
import json
import RPi.GPIO as GPIO
import time
import threading

servo_pin = 18  # 12
red_pin = 22  # 15
yellow_pin = 27  # 13
green_pin = 23  # 16
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)
GPIO.setup(red_pin, GPIO.OUT)
GPIO.setup(yellow_pin, GPIO.OUT)
GPIO.setup(green_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)  # 50Hz (서보모터 PWM 동작을 위한 주파수)

pwm.start(5.0)  # 서보의 0도 위치(0.6ms)이동:값 3.0은 pwm주기인 20ms의 3%를 의미하므로,0.6ms됨.


def motor_on():
    pwm.ChangeDutyCycle(5.0)  # 0 degree
    GPIO.output(red_pin, GPIO.HIGH)  # 빨간불
    GPIO.output(yellow_pin, GPIO.LOW)
    GPIO.output(green_pin, GPIO.LOW)

    pwm.ChangeDutyCycle(9.0)  # 90 degree
    time.sleep(9.0)
    pwm.ChangeDutyCycle(5.0)  # 0 degree
    time.sleep(1.5)

    GPIO.output(red_pin, GPIO.LOW)
    GPIO.output(yellow_pin, GPIO.HIGH)  # 노란불
    GPIO.output(green_pin, GPIO.LOW)
    time.sleep(1.5)

    GPIO.output(red_pin, GPIO.LOW)
    GPIO.output(yellow_pin, GPIO.LOW)
    GPIO.output(green_pin, GPIO.HIGH)  # 초록불


def motor_on2():
    time.sleep(10.0)
    pwm.ChangeDutyCycle(5.0)# 0 degree
    GPIO.output(red_pin, GPIO.HIGH) #빨간불
    GPIO.output(yellow_pin, GPIO.LOW)
    GPIO.output(green_pin, GPIO.LOW)

    pwm.ChangeDutyCycle(9.0)   # 90 degree
    time.sleep(9.0)
    pwm.ChangeDutyCycle(5.0)   # 0 degree
    time.sleep(1.5)

    GPIO.output(red_pin, GPIO.LOW)
    GPIO.output(yellow_pin, GPIO.HIGH) #노란불
    GPIO.output(green_pin, GPIO.LOW)
    time.sleep(1.5)

    GPIO.output(red_pin, GPIO.LOW)
    GPIO.output(yellow_pin, GPIO.LOW)
    GPIO.output(green_pin, GPIO.HIGH) #초록불

def Recv(client_sock):
    json_object = {"id": 5, "label": 0, "timee": 0}
    send_data = json.dumps(json_object)
    client_sock.send(send_data.encode())
    while (True):
        try:

            data = client_sock.recv(1024)
            json_data = json.loads(data.decode())

            print('Received from ' + ':', json_data)

            if (json_data.get("motor") == 1):
                print('motor operate')
                thread1 = threading.Thread(target=motor_on)
                thread1.start()
            elif (json_data.get("motor") == 2):
                print('10 seconds delay, motor operate')
                thread2 = threading.Thread(target=motor_on2)
                thread2.start()

        except ValueError as e:
            continue
            GPIO.cleanup()


client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
svrIP = "192.168.45.34"
client_sock.connect((svrIP, 9999))
print('Connected to ' + svrIP)
thread1 = threading.Thread(target=Recv, args=(client_sock,))
thread1.start()

