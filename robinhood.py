import os
import sys

from pyrh import Robinhood
from lib.stock_code import stock_code

u = os.getenv('user')
p = os.getenv('pass')
q = os.getenv('qr')

if not u or not p or not q:
    print("Check your env variables. It should be set as:\n\n'user=<login email>'\n'pass=<password>'\n'qr=<qr_code>'")
    sys.exit()

rh = Robinhood()
rh.login(username=u, password=p, qr_code=q)

raw_result = (rh.positions())
result = raw_result['results']
share_code = dict(stock_code())

print('Your portfolio:')
for data in result:
    share_id = str(data['instrument'].split('/')[-2])
    buy = data['average_buy_price']
    shares_count = data['quantity'].split('.')[0]
    for key, value in share_code.items():
        if str(value) in share_id:
            share_name = key
            print(f'You bought {shares_count} shares of {share_name} at ${buy} per share')


def account_user_id():
    ac = rh.get_account()
    user = ac['user_id']
    return user


def portfolio_value():
    port = rh.portfolios()
    current_value = port['equity']
    return current_value


df = portfolio_value()
print(f'\nThe current value of all your shares in total is: ${df}')
