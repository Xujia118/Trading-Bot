import smtplib
from email_content import email_content
from decide_positions import decidePositions
from decide_candidates import decideCandidates
from datetime import date
import config

def send_email():
    # Call functions to get plans for positions and other stocks
    position_sell, position_buy = decidePositions()  
    buy_plan = decideCandidates() 

    # Email configuration
    sender_email = config.sender_email
    receiver_email = '773977192@qq.com'
    password = config.password

    # Formatting the report
    if len(position_sell) == 0:
        position_sell_plan = 'No sell plan for holding positions.'
    else:
        position_sell_plan = '\n'.join([f'Ticker: {ticker}, Quantity: {sell_quantity}' for ticker, sell_quantity in position_sell])

    if len(position_buy) == 0:
        position_buy_plan = 'No buy plan for holding positions.'
    else:
        position_buy_plan = '\n'.join([f'Ticker: {ticker}, Quantity: {buy_quantity}' for ticker, buy_quantity in position_buy])

    buy_plan_str = '\n'.join([f"Ticker: {ticker}, Quantity: {quantity}" for ticker, price, quantity in buy_plan])    

    # Email content
    email_text = email_content.format(
        position_sell = position_sell_plan,
        position_buy = position_buy_plan,
        buy_plans = buy_plan_str,
        date=date.today()
    )

    email_text = f'Subject: Stocks Report\n\n{email_text}'

    with smtplib.SMTP_SSL('smtp.163.com', 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, email_text)

send_email()
