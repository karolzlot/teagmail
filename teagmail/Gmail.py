# -*- coding: utf-8 -*-
""" Manipulates data from Gmail API

This module uses the Gmail API to send and recieve information from a
users mailbox.

Example usage:
	example usage can be seen within the README 
	
Todo:
	* Be able to delete specfic messages/threads from users mailbox.


"""

import os
import base64
import dateutil.parser as parser
from email.mime.text import MIMEText
#from MailLogging import debug
from authentication import auth


class Gmail:

    def __init__(self):
        self.user_id = 'me'
        self.service = auth()
        #debug.createLog()

    def getMessagesBodies(self, messagesIDs, format=None, log=False):
        """ Return a list of message data in dictionary format
        Args:
                messages (list): The returned object from the
                `getMessages` function
        """
        if 'messages' in messagesIDs:

            messagesData = []
            for msgID in messagesIDs['messages']:
                msg = self.service.users().messages().get(userId=self.user_id,
                                                          id=msgID['id'],
                                                          format=format).execute()
                messagesData.append(msg['payload'])
                messagesData[-1]['id'] = msgID['id']
                """
        if log:
            debug.writeLog(format+' message' if format else 'messages',
                           messagesData)
                    """
            return self.unpackPayload(messagesData, log=True)
        else:
            return None

    def decodeMSG(self, message):
        """ Decodes `message` paramater into utf-8
        Arg:
                message (string): base64 encoded string
        """
        msgString = base64.urlsafe_b64decode(message.encode('ASCII'))
        decoded = msgString.decode("utf-8")
        return decoded

    def unpackPayload(self, payloads, bodies=True,
                      types=['html', 'plain'], log=False, x=0, depth=0):
        """
        recurses through message parts until it find the types
        specified, then returns the decoded part and appends it to a
        list/dictionary of all messages parts

        Args:
                payloads (dictionary): The returned object from the
                `getPayload` function

                bodies (bool): True to collect html or plain text bodies
                from payload, false for simply headers

                types (:obj:`list` of :obj:`str`): types of bodies to be
                returned, either `html` or `plain`

                log (bool): True to log output to ./logs directory

                *DO NOT ALTER THE FOLLOWING PARAMETERS, THEY ARE REQUIRED
                FOR THE RECURSION*
                x (int): Specifies the index of the payloads
                depth (int): Specifies the Depth of recursion
        """
        if payloads is None:
            return None
        else:
            messageParts = []
            plain = False
            plainText = ''
            for msg in payloads:
                parts = {}
                if bodies:
                    type = msg['mimeType']
                    # Plain text
                    if type == 'text/plain' and 'plain' in types:
                        plainText = self.decodeMSG(msg['body']['data'])
                        if depth == 0:
                            parts['plain'] = plainText[:20]
                        else:
                            plain = True
                    # Html
                    elif type == 'text/html' and 'html' in types:
                        plain = False
                        body = self.decodeMSG(msg['body']['data'])
                        if depth > 0:
                            return {"html": body}
                        parts['html'] = body
                    # Other
                    elif type[10:] in ['mixed', 'alternative',
                                       'related', 'report']:
                        msgParts = msg['parts']
                        parts = self.unpackPayload(msgParts, bodies=True,
                                                   types=types, x=x, depth=depth+1)
                        if depth > 0:
                            return parts
                    # Attatchment
                    elif type[:10] == 'application':
                        pass
                # Headers
                if depth == 0:
                    #print(parts, 'X:', x)
                    parts['id'] = msg['id']
                    header = msg['headers']
                    for head in header:
                        name, value = head['name'], head['value']
                        if name == 'Date':
                            parts['dateTime'] = value
                        if name == 'Subject':
                            parts['Subject'] = value
                        if name == 'From':
                            if '<' in value:
                                FROM, EMAIL = value.split('<')
                                parts['From'] = FROM[:-1]
                                parts['From-email'] = EMAIL[:-1]
                            else:
                                parts['From-email'] = value
                messageParts.append(parts)
                x += 1
            if plain and depth > 0:
                plain = False
                return {"plain": plainText[:20]}  # TODO remove :20 ?
            # adds plain message if no html

            # TODO add msg['type']
                """
        if log:   # TODO add logging library instead
            debug.createLog(dir='logs/bodies')
            debug.writeLog("mockData" if bodies else "headers",
                           messageParts)
            if bodies:
                for (index, msg) in enumerate(messageParts):
                    if 'html' in msg:
                        debug.writeLog(str(index+1), msg['html'],
                                       'bodies/', extension="html")
                    else:
                        debug.writeLog(str(index+1), msg['plain'],
                                       'bodies/', extension="txt")
                    """
            return messageParts

    def getUserInfo(self):
        return self.service.users().labels().get(userId=self.user_id,
                                                 id="INBOX").execute()

    def getMessages(self, query=None, labelIds=[], maxResults=None):
        """
        Returns a list of messages and thread Id's for n number
        of messages
        """
        msgList = self.service.users().messages().list(userId='me',
                                                       labelIds=labelIds, q=query,  maxResults=maxResults, includeSpamTrash=True).execute()
        return self.getMessagesBodies(msgList, log=True)

    def sendMessage(self, to, from_, subject, content):
        """ Sends a messages from users mailbox """
        # create message base64 with MIMEText format
        createdMessage = self.createMessage(to, from_, subject, content)
        # sends message
        message = (self.service.users().messages().send(userId="me",
                                                        body=createdMessage).execute())

    def createMessage(self, sender, to, subject, message_text):
        """ Creates a MIME fromat email message """
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        return {'raw': base64.urlsafe_b64encode(
            message.as_bytes()).decode()}

    def addLabel(self, m_id, labelID):
        self.service.users().messages().modify(
            userId="me", id=m_id, body={'addLabelIds': [labelID]}).execute()

    def removeLabel(self, m_id, labelID):
        self.service.users().messages().modify(
            userId="me", id=m_id, body={'removeLabelIds': [labelID]}).execute()

    def listLabels(self):
        results = self.service.users().labels().list(userId='me').execute()
        return results.get('labels', [])
