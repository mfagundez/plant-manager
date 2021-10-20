#######
# Mail sender
#
# Module to send emails using [MailJet](https://www.mailjet.com/) service
#######
import mailjet_rest

class mail_sender:

    mailjet = ''

    # Sets the client's api key and secret
    def __init__(self, api_key, api_secret):
        self.mailjet = mailjet_rest.Client(auth=(api_key, api_secret), version='v3.1')

    # Sends an email with provided data
    def send_email(self, mailfrom, mailfrom_name, mailto, cc, bcc, subject, message):
        data = {
        'Messages': [
            {
            "From": {
                "Email": mailfrom,
                "Name": mailfrom_name
            },
            "To": [
                {
                "Email": mailto
                }
            ],
            "Cc": [
                {
                "Email": cc
                }
            ],
            "Bcc": [
                {
                "Email": bcc
                }
            ],
            "Subject": subject,
            "HTMLPart": message
            }
        ]
        }
        # A None value is required to avoid cc and/or bcc fields.
        if (cc == None):
            data['Messages'][0].pop('Cc', None)
        if (bcc == None):
            data['Messages'][0].pop('Bcc', None)
            
        # Call mailjet api to send email
        result = self.mailjet.send.create(data=data)

        # According to https://dev.mailjet.com/email/reference/overview/errors/ 
        if(result.status_code != 200):
            print ("An error occurred: " + str(result.status_code))
            print (result.json())
            raise ConnectionError(result)
        return result
