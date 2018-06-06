import base64
from email.mime.text import MIMEText

from googleapiclient import errors


def create_message(sender, to, subject, message_text):
    """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return dict(raw=base64.urlsafe_b64encode(str(message).encode()))


def send_message(service, user_id, message):
    """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print( 'Message Id: %s' % message['id'] )
        return message
    except errors.HttpError as error:
        print( 'An error occurred: %s' % error )


create_message(sender="whileshesleepsstore@gmail.com", to="12burner@gmail.com", subject="Test", message_text="This is the test")
send_message(service="ya29.GlvSBXQZZks_huUpr2zzIbKx1AQJnYTjqpGmdXCN3e1cpe-BYpQ2WcRy8w0p7_NTJLRgQ0MlU8owdOvySjLG-LV-Wx2LwZpPLEJ8yD_zybFjQTFsraSR1nfS2DN-", user_id="12burner@gmail.com", message="This is a test")
#TODO Get this to work, find out wat "service" is