import smtplib
from datetime import date
import config
import os

from decision import Decision

class Report:
    def __init__(self):
        self.email_content = None

    def send_email(self):
        email_text = self._compose_email()
        print(email_text)

        # Email configuration
        sender_email = config.sender_email
        password = config.password
        receiver_email = '773977192@qq.com'

        # Send email
        with smtplib.SMTP_SSL('smtp.163.com', 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, email_text)

    def _format_email(self):
        self.email_content = '''
        Stocks Report

        Positions plans:
        {position_sell}
        {position_buy}

        Buy plans:
        {buy_plans}

        {date}
        '''

    def _compose_email(self):
        # Call functions to get plans for positions and other stocks
        decision = Decision()
        positions_sell, positions_buy = decision.update_portfolio()
        buy_plan = decision.screen_new_candidates()

        # sender_email = os.getenv("SENDER_EMAIL")
        # receiver_email = '773977192@qq.com'
        # password = os.getenv("PASSWORD")

        # Formatting the report
        if len(positions_sell) == 0:
            position_sell_plan = 'No sell plan for holding positions.'
        else:
            position_sell_plan = '\n'.join([f'Ticker: {ticker}, Quantity: {
                sell_quantity}' for ticker, sell_quantity in positions_sell])

        if len(positions_buy) == 0:
            position_buy_plan = 'No buy plan for holding positions.'
        else:
            position_buy_plan = '\n'.join([f'Ticker: {ticker}, Quantity: {
                buy_quantity}' for ticker, buy_quantity in positions_buy])

        if len(buy_plan) == 0:
            buy_plan_str = 'No buy plan for other stocks.'
        else:
            buy_plan_str = '\n'.join([f"Ticker: {ticker}, Quantity: {
                quantity}" for ticker, price, quantity in buy_plan])

        self._format_email()

        # Email content
        email_text = self.email_content.format(
            position_sell=position_sell_plan,
            position_buy=position_buy_plan,
            buy_plans=buy_plan_str,
            date=date.today()
        )

        email_text = f'Subject: Stocks Report\n\n{email_text}'
        return email_text


if __name__ == '__main__':
    report = Report()
    report.send_email()
