import base64
import qrcode
import pyotp
import itertools
import time
import sys
from dotenv import dotenv_values

secret = str()
otp_issuer = str()
otp_digits = int()
otp_period = int()

def otp_string(name, issuer, digits, period):
	return f"otpauth://totp/{issuer}:{name}?secret={base64.b32encode(bytes(secret, 'ascii')).decode()}&issuer={issuer}&algorithm=SHA1&digits={digits}&period={period}"

def usage():
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
	at_loc = name.find("@")
	
	filename_string = name.replace(" ", "_")

	return f"{filename_string[:at_loc]}_qrcode.png" if at_loc > -1 else f"{filename_string}_qrcode.png"

def generate_qr():
	return "--generate-qr"

def get_otp():
	return "--get-otp"

def assign_env_values():
	global secret, otp_issuer, otp_digits, otp_period

	config = dotenv_values()

	secret = config["SECRET"]
	otp_issuer = config["COMPANY_NAME"]
	otp_digits = int(config["DIGITS"])
	otp_period = int(config["PERIOD"])


def main():
	command = process_args(sys.argv)

	assign_env_values()
	dotenv_values('.env')

	if command == generate_qr():

		name = input("What is your email address?")
		totp_uri = otp_string(name, otp_issuer, otp_digits, otp_period)

		file_name = generate_file_name(name)

		qrcode_image = qrcode.make(totp_uri)
		qrcode_image.save(file_name)

		print(f"QR Code generated in file [{file_name}]")

	elif command == get_otp():
		encoded_secret = base64.b32encode(bytes(secret, 'ascii'))
		one_time_code = pyotp.TOTP(encoded_secret, interval=otp_period)
		for val in itertools.count(1):
				print(f"{val:2}: {one_time_code.now()}")
				time.sleep(otp_period)

if __name__ == "__main__":
	main()
