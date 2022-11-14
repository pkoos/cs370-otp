import base64
import qrcode
import pyotp
import itertools
import time
import pyglet
import sys
from dotenv import load_dotenv

# from pyglet.window import Window

# class AuthenticatorWindow(Window):


secret = "ThisIsAVeryLongPassword1!"
company_name = "Paul Ko"
email_addr = "paul@paul.paul"

def otp_string(name, issuer = company_name, digits = 6, period = 30):
	return f"otpauth://totp/{issuer}:{name}?secret={base64.b32encode(bytes(secret, 'ascii')).decode()}&issuer={issuer}&algorithm=SHA1&digits={digits}&period={period}"

def usage():
	print("::usage()")
	print("Usage: python3 main.py [ --generate-qr | --get-otp ]")

def process_args(argv):
	if len(sys.argv) < 2:
		usage()
		sys.exit(1)

	arg = sys.argv[1]

	valid_args = [generate_qr(), get_otp()]

	if arg not in valid_args:
		usage()
		sys.exit(2)
	
	return arg


def generate_qr():
	return "--generate-qr"

def get_otp():
	return "--get-otp"

def main():
	command = process_args(sys.argv)

	print("past the guard clauses")

	if command == generate_qr():
		print("generating a QR Image")

		name = input("What is your email address?")
		print(otp_string(name))
	elif command == get_otp():
		print("getting a one time token")
	

	# window = pyglet.window.Window()

	# label = pyglet.text.Label('Hello, world!',
	# 													font_name = 'Times New Roman',
	# 													font_size = 36,
	# 													x = window.width // 2, y = window.height // 2,
	# 													anchor_x = 'center', anchor_y = 'center')
	# button_image = pyglet.image.load('button.png')

	# provisioning_button = pyglet.gui.PushButton(x = window.width // 2, y = window.height // 2, pressed = button_image, depressed = button_image)

	# @window.event
	# def on_draw():
	# 	window.clear()
	# 	button_image.blit((window.width - button_image.width) // 2, (window.height - button_image.height) // 2)
		
		
	
	# pyglet.app.run()
	

	# encoded_secret = base64.b32encode(bytes(secret, 'ascii'))
	# print(f"encoded_secret: {encoded_secret}")

	# google_auth_uri = pyotp.totp.TOTP(encoded_secret, digits=8, interval=5).provisioning_uri(name=email_addr, issuer_name=company_name )
	
	# print(f"google_auth_uri: {google_auth_uri}")
	# totp = pyotp.TOTP(encoded_secret, interval=1)

	# for val in itertools.count(0):
	# 	print(f"{val:2}: {totp.now()}")
	# 	time.sleep(1)

	# 	if val == 30:
	# 		break
	
	# print("Hello World!")
	# issuer = "Paul%20Ko"
	# name = "paul@paul.paul"
	# digits = 6
	# period = 30
	# totp_string = otp_string(issuer, name, digits, period)
	# print(totp_string)

	# qrcode_image = qrcode.make(totp_string)
	# print(f"qrcode_image type: {type(qrcode_image)}")

	# qrcode_image.save("qrcode.png")

if __name__ == "__main__":
	main()
