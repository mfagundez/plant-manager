
import mailjet_rest

class mail_sender:

    mailjet = ''

    def __init__(self, api_key, api_secret):
        self.mailjet = mailjet_rest.Client(auth=(api_key, api_secret), version='v3.1')

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
            "TextPart": message
            }
        ]
        }
        if (cc == None):
            data['Messages'][0].pop('Cc', None)
        if (bcc == None):
            data['Messages'][0].pop('Bcc', None)
            
        result = self.mailjet.send.create(data=data)
        if(result.status_code != 200):
            print ("An error occurred: " + str(result.status_code))
            print (result.json())
            raise ConnectionError(result)
        return result
