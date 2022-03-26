# -*- coding: utf-8 -*-
import sys
from xbmc import executebuiltin

executebuiltin("ActivateWindow(Videos,%s)" % sys.listitem.getProperty("nemesis_browse_params"))