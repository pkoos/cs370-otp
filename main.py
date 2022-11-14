import base64
import qrcode
import pyotp
import itertools
import time
import pyglet
import sys
from dotenv import dotenv_values

# from pyglet.window import Window

# class AuthenticatorWindow(Window):


secret = str()
otp_issuer = str()
otp_digits = int()
otp_period = int()
config = dict()

def otp_string(name, issuer, digits, period):
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

def generate_file_name(name):
	print("generate_file_name")
	at_loc = name.find("@")
	
	print(f"at_loc: {at_loc}")

	return f"{name[:at_loc]}_qrcode.png"

def generate_qr():
	return "--generate-qr"

def get_otp():
	return "--get-otp"

def assign_env_values():
	global config
	global secret
	global otp_issuer
	global otp_digits
	global otp_period

	config = dotenv_values()

	secret = config["SECRET"]
	otp_issuer = config["COMPANY_NAME"]
	otp_digits = config["DIGITS"]
	otp_period = config["PERIOD"]

	# print(f"[otp_issuer: {otp_issuer}] [otp_digits: {otp_digits} characters] [otp_period: {otp_period} seconds]")

def main():
	command = process_args(sys.argv)

	print("past the guard clauses")

	assign_env_values()
	config = dotenv_values('.env')
	print(f"config: {config}")

	print(f"after config: [otp_issuer: {otp_issuer}] [otp_digits: {otp_digits} characters] [otp_period: {otp_period} seconds]")
	if command == generate_qr():
		print("generating a QR Image")

		name = input("What is your email address?")
		totp_uri = otp_string(name, otp_issuer, otp_digits, otp_period)
		print(totp_uri)

		file_name = generate_file_name(name)
		print(f"file_name: {file_name}")

		qrcode_image = qrcode.make(totp_uri)
		qrcode_image.save(file_name)

		print(f"QR Code generated in file [{file_name}]")

	elif command == get_otp():
		print("getting a one time token")
		encoded_secret = base64.b32encode(bytes(secret, 'ascii'))
		one_time_code = pyotp.TOTP(encoded_secret, interval=30)
		for val in itertools.count(1):
				print(f"{val:2}: {one_time_code.now()}")
				time.sleep(30)

if __name__ == "__main__":
	main()
