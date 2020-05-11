# Stock Monitor
Your stock viewer to check your portfolio from Robinhood

## Setup

1. git clone this repository

2. Run this command in your terminal to install necessary packages<br/>cd robinhood_tracker/lib && pip3 install -r requirements.txt

2. Make sure you add the following env variables
* user - Robinhood login email address
* pass - Robinhood login password
* qr - Robinhood qr code<br>
To use qr code authentication you must enable Two-Factor Authentication. Follow steps:
* Login to your Robinhood Web App.
* Go to Account -> Settings
* Turn on Two-Factor Authentication.
* Select “Authentication App”
* Click “Can’t Scan It?”, and copy the 16-character QR code.
<br>
Alternatively you can also run this code without Two-Factor Authentication but it will require you to enter the Verification code each and every-time. To do this simply remove the qr_code part in:
* [challenge_type](https://github.com/vignesh1793/robinhood_tracker/blob/master/robinhood.py#L12) can be changed to "sms" if you prefer to receive 2FA code to your mobile number instead.

Click to learn more about [pyrh](https://pypi.org/project/pyrh/)
