# -*- coding: utf-8 -*-
import xbmc
from threading import Thread
from modules import service_functions
from modules.settings_reader import make_settings_dict
from modules.kodi_utils import set_property, clear_property, logger

class NemesisMonitor(xbmc.Monitor):
	def __init__ (self):
		xbmc.Monitor.__init__(self)
		logger('Nemesis', 'Main Monitor Service Starting')
		logger('Nemesis', 'Settings Monitor Service Starting')
		self.startUpServices()
	
	def startUpServices(self):
		threads = []
		functions = (service_functions.DatabaseMaintenance().run, service_functions.TraktMonitor().run)
		for item in functions: threads.append(Thread(target=item))
		while not self.abortRequested():
			try: service_functions.InitializeDatabases().run()
			except: pass
			try: service_functions.CheckSettingsFile().run()
			except: pass
			try: service_functions.SyncMyAccounts().run()
			except: pass
			[i.start() for i in threads]
			try: service_functions.ClearSubs().run()
			except: pass
			try: service_functions.ViewsSetWindowProperties().run()
			except: pass
			try: service_functions.AutoRun().run()
			except: pass
			try: service_functions.ReuseLanguageInvokerCheck().run()
			except: pass
			break

	def onScreensaverActivated(self):
		set_property('nemesis_pause_services', 'true')

	def onScreensaverDeactivated(self):
		clear_property('nemesis_pause_services')

	def onSettingsChanged(self):
		clear_property('nemesis_settings')
		xbmc.sleep(50)
		refreshed = make_settings_dict()

	def onNotification(self, sender, method, data):
		if method == 'System.OnSleep': set_property('nemesis_pause_services', 'true')
		elif method == 'System.OnWake': clear_property('nemesis_pause_services')


NemesisMonitor().waitForAbort()

logger('Nemesis', 'Settings Monitor Service Finished')
logger('Nemesis', 'Main Monitor Service Finished')