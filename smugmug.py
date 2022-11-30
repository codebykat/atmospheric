import requests
from requests_oauthlib import OAuth1, OAuth1Session
import keyring
from os import getlogin
import webbrowser
import json

import config

API_BASE = "https://api.smugmug.com/api/v2/"
REQUEST_TOKEN_URL = "https://api.smugmug.com/services/oauth/1.0a/getRequestToken"
AUTHORIZE_URL = "https://api.smugmug.com/services/oauth/1.0a/authorize"
ACCESS_TOKEN_URL = "https://api.smugmug.com/services/oauth/1.0a/getAccessToken"
UPLOAD_URL = "https://upload.smugmug.com/"

class Smugmug:
	def __init__(self):
		self.tokens = None

	def login(self):
		# see if we have a valid token stored
		if self.tokens:
				return OAuth1(client_key=config.SMUGMUG_API_KEY,
					client_secret=config.SMUGMUG_API_SECRET,
					resource_owner_key=self.tokens['oauth_token'],
					resource_owner_secret=self.tokens['oauth_token_secret'])

		# attempt to retrieve stored token from keyring
		tokens = keyring.get_password("smugmug_api_tokens", getlogin())
		if tokens:
			oauth_tokens = json.loads(tokens)
			self.tokens = oauth_tokens
			return OAuth1(client_key=config.SMUGMUG_API_KEY,
						client_secret=config.SMUGMUG_API_SECRET,
						resource_owner_key=oauth_tokens['oauth_token'],
						resource_owner_secret=oauth_tokens['oauth_token_secret'])

		# no tokens found - fetch tokens from API
		request_token_params = {"oauth_callback": "oob"}
		oauth = OAuth1Session(config.SMUGMUG_API_KEY, client_secret=config.SMUGMUG_API_SECRET)
		fetch_response = oauth.fetch_request_token(REQUEST_TOKEN_URL, params=request_token_params)
		resource_owner_key = fetch_response.get('oauth_token')
		resource_owner_secret = fetch_response.get('oauth_token_secret')

		authorization_params = {"Access": "Full", "Permissions": "Modify" }
		authorization_url = oauth.authorization_url(AUTHORIZE_URL, params=authorization_params)
		webbrowser.open(authorization_url)

		code = input('Code: ')
		oauth = OAuth1Session(config.SMUGMUG_API_KEY,
							client_secret=config.SMUGMUG_API_SECRET,
							resource_owner_key=resource_owner_key,
							resource_owner_secret=resource_owner_secret,
							verifier=code)
		oauth_tokens = oauth.fetch_access_token(ACCESS_TOKEN_URL)

		# todo error handling
		keyring.set_password("smugmug_api_tokens", getlogin(), json.dumps(oauth_tokens))
		self.tokens = oauth_tokens

		return OAuth1(client_key=config.SMUGMUG_API_KEY,
					client_secret=config.SMUGMUG_API_SECRET,
					resource_owner_key=oauth_tokens['oauth_token'],
					resource_owner_secret=oauth_tokens['oauth_token_secret'])

	def get_username(self):
		with requests.Session() as s:
			s.auth = self.login()
			s.headers = {"accept": "application/json"}
			s.params = {"_verbosity":"1"}

			# authuser returns something with Node = /api/v2/node/x4vCQ User->Uris->Node

	def get_albums(self):
		with requests.Session() as s:
			s.auth = self.login()
			s.headers = {"accept": "application/json"}
			s.params = {"_verbosity":"1"}

			# useralbums UserAlbums /api/v2/user/wirehead!albums
			#
			album_search_params = {"Scope": "/api/v2/folder/user/wirehead/Clouds",
								"_filter": "Title,AlbumKey,NodeID",
								"_filteruri": "Node,AlbumImages"}
			# r = requests.get("%salbum!search" % API_BASE, auth=auth, headers=HEADERS, params=album_search_params)
			response = s.get("%s!authuser" % API_BASE, params={"_expand":"UserAlbums"})
			# r = requests.get("%salbum" % API_BASE, auth=auth, headers=HEADERS, params={"_verbosity":"1"})
			# print(r.json())
			# r = requests.get("%suser/wirehead!albums" % API_BASE, auth=auth, headers=HEADERS, params={"_verbosity":"1"})
			print(json.dumps(response.json(), indent=3))

	def upload_to_album(self, file, albumUri):
		# https://api.smugmug.com/api/v2/doc/reference/upload.html
		title = ""
		caption = ""
		with requests.Session() as s:
			s.auth = self.login()
			s.headers = {"X-Smug-ResponseType": "JSON",
				"X-Smug-AlbumUri": albumUri,
				"X-Smug-FileName": file.name,
				"X-Smug-Title": title,
				"X-Smug-Caption": caption,
				"X-Smug-Latitude": "",
				"X-Smug-Longitude": "",
				"X-Smug-Version": "v2",
				"Content-MD5": "The MD5 digest of the media, base64-encoded"}
