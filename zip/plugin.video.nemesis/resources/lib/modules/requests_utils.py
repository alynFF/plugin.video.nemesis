# -*- coding: utf-8 -*-
import requests
# from modules.kodi_utils import logger

def make_session():
	session = requests.Session()
	session.mount('https://', requests.adapters.HTTPAdapter())
	return session	

def make_requests():
	return requests