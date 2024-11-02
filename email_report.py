import smtplib
from email_content import email_content
import decide_positions 
import decide_candidates
from datetime import date

def send_email():
    # Call functions to get plans for positions and other stocks
    positions_sell, positions_buy = decide_positions.decide_positions_actions()
    buy_plan = decide_candidates.decide_candidates() 

    # Formatting the report
    if len(positions_sell) == 0:
        position_sell_plan = 'No sell plan for holding positions.'
    else:
        position_sell_plan = '\n'.join([f'Ticker: {ticker}, Quantity: {sell_quantity}' for ticker, sell_quantity in positions_sell])

    if len(positions_buy) == 0:
        position_buy_plan = 'No buy plan for holding positions.'
    else:
        position_buy_plan = '\n'.join([f'Ticker: {ticker}, Quantity: {buy_quantity}' for ticker, buy_quantity in positions_buy])

    if len(buy_plan) == 0:
        buy_plan_str = 'No buy plan for other stocks.'
    else:
        buy_plan_str = '\n'.join([f"Ticker: {ticker}, Quantity: {quantity}" for ticker, price, quantity in buy_plan])    

    # Email content
    report = email_content.format(
        position_sell = position_sell_plan,
        position_buy = position_buy_plan,
        buy_plans = buy_plan_str,
        date=date.today()
    )

    report = f'Subject: Stocks Report\n\n{report}'
    print(report)

if __name__ == '__main__':
    send_email()
