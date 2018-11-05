## TeaGmail ##

python GmailApi library

[![License](https://img.shields.io/badge/License-MIT-orange.svg)](https://github.com/Charlkie/PyMail/blob/master/LICENSE)
![](https://img.shields.io/badge/Version-Alpha%200.0.1-brightgreen.svg)


If you have any question, open an issue :-)

Pull requests are welcome

Installation
------------


    pip install -i https://test.pypi.org/simple/ teagmail
    
Setup
-----

TeaGmail uses OAuth authentication

Generate a client ID and client secret https://developers.google.com/gmail/api/quickstart/python under section
**Step 1: Turn on the Gmail API**. Follow steps until you generate `credentials.json`. Save this file in your project folder




Usage - READ
------------


    from teagmail import Gmail

    Gmail = Gmail()


    def main():

        # Gets users total number of messages in all mailboxes
        msgTotal = Gmail.getUserInfo()['messagesTotal']

        # example1	 # 	Get list of all messages
        messages = Gmail.getMessages()

        # example2:    using query with syntax the same as in Gmail search box
        messages2 = messages = Gmail.getMessages(
            'subject:("Welcome to Gmail") from:(noreply@github.com) -label:mylabel')  # minus "-" means NOT

        # example3:   (only 5 messages)
        messages3 = Gmail.GetMessages().list(5, ["INBOX"])

        if messages is not None:

            for msg in messages:
                # printing messages bodies	 # simple check if it is html or text
                print(msg['html'] if 'html' in msg else msg['txt'])
                # Label_7438957439057033324 is id, not name of label
                Gmail.addLabel(msg['id'], 'Label_7438957439057033324')
                Gmail.removeLabel(msg['id'], 'INBOX')  # archive message

        labels = Gmail.listLabels()   # use this to get id of labels


    def testSend():
        """Sends email based of user input"""
        mailData = [input('Name: '), input('Recipient: '),
                    input('Subject: '), input('content: ')]

        Gmail.sendMessage(*mailData)


    if __name__ == '__main__':
        main()








## Documentation

### Methods

| **Gmail.** | Parameters | Description |
| ------------- |-------------| -----|
| GetMessages().list() | msgNum | Fetches 'msgNum' message ID's, recipient, sender name, sender email, subject and body of email in plain text or html format. |
| sendMessage() | to, from, subject, content | sends an email from users mailbox  |
| listLabels()   | ---  |  lists all labels |
| addLabel()   |  msgid, labelid |  adds label |
| removeLabel()   |  msgid, labelid |  removes label |
| getUserInfo()   | ---  |  see example above  |




****
### Parameters
****

| Parameters | Value | Description |
| ---------- | ----- | ----------- |
| MsgNum | integer | The number of messages to be queried. |
| Messages | list | list of messages returned from `getMessages.list` method. |
| format | string | text format either `default` or `raw` |
| bodies | boolean | True to collect html or plain text bodies from payload, false. for simply headers |
| types | list of strings | types of bodies to be returned, either `html` or `plain` |


**To do:**

* add removeMessege
* test if sendMessage 


Based on https://github.com/Charlkie/PyMail

Thanks to
* @Charlkie
