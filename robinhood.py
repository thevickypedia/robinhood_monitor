"""/**
 * Author:  Vignesh Sivanandha Rao
 * Created:   05.08.2020
 *
 **/"""
from datetime import datetime, timedelta, date
from json import loads
from math import fsum
from os import environ, mkdir, path
from shutil import rmtree
from sys import exit
from time import perf_counter

import matplotlib.pyplot as plt
from pandas import read_html as reader
from pyrh import Robinhood
from requests import get
from twilio.rest import Client

from lib.emailer import Emailer


def market_status():
    url = 'https://www.nasdaqtrader.com/trader.aspx?id=Calendar'
    holidays_list = list(reader(url)[0][0])
    today = date.today().strftime("%B %d, %Y")
    if today in holidays_list:
        print(f'{today}: The markets are closed today.')
    else:
        return True


def watcher():
    global graph_msg, graph_min, graph_max
    rh = Robinhood()
    rh.login(username=rh_user, password=rh_pass, qr_code=rh_qr)
    raw_result = rh.positions()
    result = raw_result['results']
    shares_total = []
    port_msg = f"Your portfolio ({rh.get_account()['account_number']}):\n"
    loss_output = 'Loss:'
    profit_output = 'Profit:'
    loss_total = []
    profit_total = []
    graph_msg = None  # initiates a variable graph_msg as None for looped condition below
    n = 0
    n_ = 0
    for data in result:
        share_id = str(data['instrument'].split('/')[-2])
        buy = round(float(data['average_buy_price']), 2)
        shares_count = int(data['quantity'].split('.')[0])
        if shares_count != 0:
            n = n + 1
            n_ = n_ + shares_count
        else:
            continue
        raw_details = rh.get_quote(share_id)
        share_name = raw_details['symbol']
        call = raw_details['instrument']
        share_full_name = loads(get(call).text)['simple_name']
        total = round(shares_count * float(buy), 2)
        shares_total.append(total)
        current = round(float(raw_details['last_trade_price']), 2)
        current_total = round(shares_count * current, 2)
        difference = round(float(current_total - total), 2)
        if difference < 0:
            loss_output += (
                f'\n{share_full_name}:\n{shares_count} shares of {share_name} at ${buy} Currently: ${current}\n'
                f'Total bought: ${total} Current Total: ${current_total}'
                f'\nLOST ${-difference}\n')
            loss_total.append(-difference)
        else:
            profit_output += (
                f'\n{share_full_name}:\n{shares_count} shares of {share_name} at ${buy} Currently: ${current}\n'
                f'Total bought: ${total} Current Total: ${current_total}'
                f'\nGained ${difference}\n')
            profit_total.append(difference)
        if graph_min and graph_max:
            graph_min = float(graph_min)
            graph_max = float(graph_max)
            if difference > graph_max or difference < -graph_min:
                time_now = datetime.now()
                metrics = time_now - timedelta(days=7)
                numbers = []
                historic_data = (rh.get_historical_quotes(share_name, '10minute', 'week'))
                historical_values = historic_data['results'][0]['historicals']
                for close_price in historical_values:
                    numbers.append(round(float(close_price['close_price']), 2))
                fig, ax = plt.subplots()
                if difference > graph_max:
                    plt.title(f"Stock Price Trend for {share_full_name}\nShares: {shares_count}  Profit: ${difference}")
                elif difference < graph_min:
                    plt.title(f"Stock Price Trend for {share_full_name}\nShares: {shares_count}  LOSS: ${-difference}")
                plt.xlabel(f"1 Week trend with 10 minutes interval from {metrics.strftime('%m-%d %H:%M')} to "
                           f"{time_now.strftime('%m-%d %H:%M')}")
                plt.ylabel('Price in USD')
                ax.plot(numbers, linewidth=1.5)
                if not path.isdir('img'):
                    mkdir('img')
                fig.savefig(f"img/{share_full_name}.png", format="png")
                plt.close()  # close plt to avoid memory exception when more than 20 graphs are generated
                # stores graph_msg only if a graph is generated else graph_msg remains None
                if not graph_msg:  # used if not to avoid storing the message repeatedly
                    graph_msg = f"Attached are the graphs for stocks which exceeded a profit of " \
                                f"${graph_max} or deceeded a loss of ${graph_min}"
        elif not graph_msg:  # used elif not to avoid storing the message repeatedly
            graph_msg = "Add the env variables for <graph_min> and <graph_max> to include a graph of previous " \
                        "week's trend."

    lost = round(fsum(loss_total), 2)
    gained = round(fsum(profit_total), 2)
    port_msg += f'The below values will differ from overall profit/loss if shares were purchased ' \
                f'with different price values.\nTotal Profit: ${gained}\nTotal Loss: ${lost}\n'
    net_worth = round(float(rh.equity()), 2)
    output = f'Total number of stocks purchased: {n}\n'
    output += f'Total number of shares owned: {n_}\n\n'
    output += f'Current value of your total investment is: ${net_worth}\n'
    total_buy = round(fsum(shares_total), 2)
    output += f'Value of your total investment while purchase is: ${total_buy}\n'
    total_diff = round(float(net_worth - total_buy), 2)
    if total_diff < 0:
        output += f'Overall Loss: ${total_diff}'
    else:
        output += f'Overall Profit: ${total_diff}'
    yesterday_close = round(float(rh.equity_previous_close()), 2)
    two_day_diff = round(float(net_worth - yesterday_close), 2)
    output += f"\n\nYesterday's closing value: ${yesterday_close}"
    if two_day_diff < 0:
        output += f"\nCurrent Dip: ${two_day_diff}"
    else:
        output += f"\nCurrent Spike: ${two_day_diff}"
    if not graph_msg:  # if graph_msg was not set above
        graph_msg = f"You have not lost more than ${graph_min} or gained more than " \
                    f"${graph_max} to generate a graph."

    return port_msg, profit_output, loss_output, output, graph_msg


def send_email(attachment):
    print("Sending email...")
    footer_text = "\n----------------------------------------------------------------" \
                  "----------------------------------------\n" \
                  "A report on the list shares you have purchased.\n" \
                  "The data is being collected using http://api.robinhood.com/," \
                  f"\nFor more information check README.md in https://github.com/thevickypedia/robinhood_monitor"
    Emailer(access_key=access_key, secret_key=secret_key,
            sender=f"Robinhood Monitor <{sender}>", recipients=[recipient],
            title=f'Investment Summary as of {dt_string}',
            text=f'{overall_result}\n\n{port_head}\n{profit}\n{loss}\n\n{graph_msg}\n\n{footer_text}',
            attachment=attachment)
    if 'Attached' in graph_msg:  # only tries to delete if graphs have been generated
        rmtree('img')


def send_whatsapp():
    print('Sending whats app notification...')
    Client(sid, token).messages.create(
        body=f'{dt_string}\nRobinhood Report\n{overall_result}\n\nCheck your email for summary',
        from_=f"whatsapp:{send}",
        to=f"whatsapp:{receive}"
    )


if __name__ == '__main__':
    if market_status():
        if environ.get('DOCKER'):
            print('Using json file for secrets')
            from json import load

            json_file = load(open('params.json'))
            rh_user = json_file.get('user')
            rh_pass = json_file.get('pass')
            rh_qr = json_file.get('qr')
            sid = json_file.get('SID')
            token = json_file.get('TOKEN')
            send = json_file.get('SEND')
            receive = json_file.get('RECEIVE')
            sender = json_file.get('SENDER')
            access_key = json_file.get('ACCESS_KEY')
            secret_key = json_file.get('SECRET_KEY')
            current_time = datetime.now() - timedelta(hours=5)
        else:
            rh_user = environ.get('user')
            rh_pass = environ.get('pass')
            rh_qr = environ.get('qr')
            sid = environ.get('SID')
            token = environ.get('TOKEN')
            send = environ.get('SEND')
            receive = environ.get('RECEIVE')
            sender = environ.get('SENDER')
            access_key = environ.get('ACCESS_KEY')
            secret_key = environ.get('SECRET_KEY')
            current_time = datetime.now()

        recipient = rh_user

        # below are optional to get graphs for stocks that have profited more than graph_max and loss below graph_min
        graph_min = environ.get('graph_min')
        graph_max = environ.get('graph_max')

        env_vars = [rh_user, rh_pass, rh_qr, sid, token, send, receive, sender, recipient]

        if any(env_var is None for env_var in env_vars):
            exit("Check your environment variables. It should be set as:\n"
                 "'user=<login_email>'\n'pass=<password>'\n'qr=<qr_code>'\n"
                 "'SID=<twilio_sid>'\n'TOKEN=<twilio_token>'\n'SEND=<twilio_sender>'\n"
                 "'RECEIVE=<phone_number>'\n'SENDER=<emailID>'")

        dt_string = current_time.strftime("%A, %B %d, %Y %I:%M %p")
        print(f'{dt_string}')
        print('Gathering your investment details...')
        port_head, profit, loss, overall_result, graph_msg = watcher()
        send_email(attachment=True)
        send_whatsapp()
        print(f"Process Completed in {round(float(perf_counter()), 2)} seconds")
