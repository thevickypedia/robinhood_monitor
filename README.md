# Stock Monitor
Your stock viewer to check your portfolio from Robinhood

## Setup

1. git clone this repository

2. Run this command in your terminal to install necessary packages<br/>cd robinhood_tracker/lib && pip3 install -r requirements.txt

2. Make sure you add the following env variables
* user - Robinhood login email address
* pass - Robinhood login password
* [challenge_type](https://github.com/vignesh1793/robinhood_tracker/blob/master/robinhood.py#L12) can be changed to "sms" if you prefer to receive 2FA code to your mobile number instead.

Note: The script may be considered useless as currently it requires 2 factor authentication every time you run it. This is because currently Robinhood does not support API hence there is no security token to be used.<br>I will try to build a cached session around it to bypass MFA for multiple runs and possibly include more features in the future.

Click to learn more about [pyrh](https://pypi.org/project/pyrh/)