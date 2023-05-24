import smtplib
from email_content import email_content
from decide_positions import decidePositions
from decide_candidates import decideCandidates
from datetime import date
import config

def send_email():
    # Call functions to get positions and buy plan for other stocks
    position_df = decidePositions()  
    buy_plan = decideCandidates() 

    # Email configuration
    sender_email = config.sender_email
    receiver_email = '773977192@qq.com'
    password = config.password

    # Formatting the report
    positions_df_str = position_df.to_string(index=False)
    buy_plan_str = '\n'.join([f"Ticker: {ticker}, Shares: {shares}" for ticker, shares in buy_plan])

    # Email content
    email_text = email_content.format(
        positions_df=positions_df_str,
        buy_plans=buy_plan_str,
        date=date.today()
    )

    email_text = f'Subject: Stocks Report\n\n{email_text}'

    with smtplib.SMTP_SSL('smtp.163.com', 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, email_text)

send_email()
