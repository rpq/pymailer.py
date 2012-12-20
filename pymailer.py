import sys
import argparse
import logging
import smtplib

import settings

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="python tls smtp command line mailer script")
    parser.add_argument('-s', '--subject', help='e-mail subject',
        required=True, type=str)
    parser.add_argument('-t', '--to_addr', help='e-mail to address',
        required=True, type=str)
    parser.add_argument('-f', '--from_addr', help='e-mail from address',
        required=True, type=str)
    parser.add_argument('-v', '--verbosity', type=int,
        help='0=none, 1=info, 2=debug, 3=smtpmessages', default=1)
    args = parser.parse_args()


    logger = logging.getLogger('pymailer.py')
    if args.verbosity == 0:
        logger.addHandler(logging.NullHandler)
    elif args.verbosity == 1:
        logging.basicConfig(level=logging.INFO)
    elif args.verbosity > 1:
        logging.basicConfig(level=logging.DEBUG)

    body = sys.stdin.read() or ''
    subject = args.subject
    to_sender = args.to_addr
    from_sender = args.from_addr

    smtp_server = settings.SERVER
    smtp_port = settings.PORT
    smtp_username = settings.USERNAME
    smtp_password = settings.PASSWORD

    server = smtplib.SMTP()
    if args.verbosity > 2:
        server.set_debuglevel(1)
    logger.info('connecting to server: {0}:{1}'.format(
        smtp_server, smtp_port))
    server.connect(smtp_server, smtp_port)
    logger.info('connected')
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(smtp_username, smtp_password)
    logger.info('logger in as: {0}'.format(smtp_username))

    # construct message with headers
    from email.MIMEText import MIMEText
    msg = MIMEText(body, 'plain')
    msg['To'] = to_sender
    msg['From'] = from_sender
    msg['Subject'] = subject

    logger.debug('from: {0}'.format(from_sender))
    logger.debug('to: {0}'.format(to_sender))
    logger.debug('mail contents:\n{0}'.format(msg.as_string()))
    server.sendmail(from_sender, to_sender, msg.as_string())
    logger.info('sent mail.')
