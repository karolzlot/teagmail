# -*- coding: utf-8 -*-
from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

def auth():
	""" Authenticates user from a token.json file enabling
		get request from the Google APIs """
	store = file.Storage('token.json')
	creds = store.get()
	if not creds or creds.invalid:
		flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
		creds = tools.run_flow(flow, store)
	return build('gmail', 'v1', http=creds.authorize(Http()))

SCOPES = 'https://www.googleapis.com/auth/gmail.modify'  # TODO move to conf file

if __name__ == '__main__':
	auth()