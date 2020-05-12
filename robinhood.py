import math
import os
import sys

from pyrh import Robinhood
from lib.helper import stock_id

u = os.getenv('user')
p = os.getenv('pass')
q = os.getenv('qr')

if not u or not p or not q:
    print("Check your local environment variables. It should be set as:\n\n"
          "'user=<login_email>'\n'pass=<password>'\n'qr=<qr_code>'")
    sys.exit()

rh = Robinhood()
rh.login(username=u, password=p, qr_code=q)


def account_user_id():
    ac = rh.get_account()
    user = ac['account_number']
    return user


acc_id = account_user_id()
raw_result = (rh.positions())
result = raw_result['results']
share_code = dict(stock_id())
shares_total = []
print(f'Your portfolio ({acc_id}):\n')
for data in result:
    share_id = str(data['instrument'].split('/')[-2])
    buy = round(float(data['average_buy_price']), 2)
    shares_count = data['quantity'].split('.')[0]
    for key, value in share_code.items():
        if str(value) == share_id:
            share_name = key.split("|")[0]
            share_full_name = key.split("|")[1]
            total = round(int(shares_count) * float(buy), 2)
            shares_total.append(total)  # not used in this function
            current = round(float(rh.get_quote(share_name)['last_trade_price']), 2)
            current_total = round(int(shares_count) * current, 2)
            difference = round(float(current_total - total), 2)
            print(f'{shares_count} shares of {share_name} at ${buy} Currently: ${current}\n'
                  f'Total bought: ${total} Current Total: ${current_total}')
            if difference < 0:
                print(f'LOST ${-difference} on {share_full_name}\n')
            else:
                print(f'Gained ${difference} on {share_full_name}\n')


def portfolio_value():
    port = rh.portfolios()
    current_val = port['equity']
    current_value = round(float(current_val), 2)
    return current_value


net_worth = portfolio_value()
print(f'Current value of your total investment is: ${net_worth}')
total_buy = round(math.fsum(shares_total), 2)
print(f'Previous value of your total investment is: ${total_buy}')
total_diff = round(float(net_worth - total_buy), 2)
if total_diff < 0:
    print(f'Total Loss: ${total_diff}')
else:
    print(f'Total Profit: ${total_diff}')
