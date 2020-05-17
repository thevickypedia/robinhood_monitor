# Stock Monitor
Your stock viewer to check your portfolio from Robinhood

## Setup

1. git clone this repository

2. Run this command in your terminal to install necessary packages<br/>cd robinhood_tracker/lib && pip3 install -r requirements.txt

2. Make sure you add the following env variables
* user - Robinhood login email address
* pass - Robinhood login password
* qr - Robinhood MFA QR code (Check for steps in original [README.md](https://github.com/vignesh1793/robinhood_tracker/blob/master/README.md))
* ACCESS_KEY - AWS login access key
* SECRET_KEY - AWS secret key
* SENDER - sender email address (verified via AWS SES)
* RECIPIENT - receiver email address (verified via AWS SES)
<br/><br/>Optional (If you'd like to setup whats app notifications else skip these, app will still run):
* SID - S-ID from twilio
* TOKEN - Token from twilio
* SEND - sender whats app number (fromat - +1xxxxxxxxxx)
* RECEIVE - receiver whats app number (fromat - +1xxxxxxxxxx)<br><br>

To use [qr_code](https://github.com/vignesh1793/robinhood_tracker/blob/master/robinhood.py#L30) you must enable Two-Factor Authentication. Follow steps:
* Login to your Robinhood Web App.
* Go to Account -> Settings or click [me](https://robinhood.com/account/settings)
* Turn on Two-Factor Authentication.
* Select “Authentication App”
* Click “Can’t Scan It?”, and copy the 16-character QR code.

Alternatively you can also run this code without Two-Factor Authentication but it will require you to enter the Verification code each and every-time. To do this simply remove the qr_code part [here](https://github.com/vignesh1793/robinhood_tracker/blob/master/robinhood.py#L30)

You can also change the way you receive validation code from email to sms by including challenge_type="sms" in your [login](https://github.com/vignesh1793/robinhood_tracker/blob/master/robinhood.py#L30)

Click to learn more about [pyrh](https://pypi.org/project/pyrh/)
