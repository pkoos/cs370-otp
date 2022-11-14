# CS370 OTP

## External Dependencies

- `pyotp`
- `python-dotenv`
- `qrcode`

Run the following command to install dependencies:

    pip install pyotp python-dotenv qrcode[pil]


## Application Setup

This application uses a .env file to store all of the settings used to generate the Google otpauth URI. A sample .env file is included with the project. Prior to running the program, rename `.env.example` to simply `.env`.

## Running the Application

There are two main pieces of functionality within the application: generating a QRCode and displaying the one-time password.

### Generating a QR Code

Use the following command to generate a QRCode:

    python3 main.py --generate-qr

The application will ask you to input a name to use within Google Authenticator. This does not need to be an email address.

Once the name is input, a file will be created with the QR Code.

### Displaying the one-time password

Use the following command to generate a one-time password:

    python3 main.py --get-otp

This will output the current one-time password, and every 30 seconds will display a new password. To exit the application, use `Ctrl+C`.

## Implementation Summary

The following program was implemented around the usage of a dotenv file. A dotenv file is typically used to store secrets or environment information that should not be committed into GitHub. Since this application has a secret, it made sense to use a dotenv file in the implementation. With the .env file and changing the secret, there is an assumption that the number of digits in the secret itself is a multiple of 5. It is also assumed that the value of digits is either 6 or 8, and that the value of period is 30, 60, or 90.

The otpauth URI is very formuliac, and as such I created a function and used formatted strings to fill the information. Most of the information is grabbed from the .env file, however the user is able to input what account the QRCode is generated for. The `qrcode` library was used for QRCode generation.

The one-time password generation was accomplished with the `pyotp` library. I base32 encode the secret from the .env file, and then display the code at intervals based on otp_period.