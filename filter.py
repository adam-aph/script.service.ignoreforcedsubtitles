import xbmc
import xbmcaddon
import xbmcvfs
import os
import sys
import json as simplejson

__addon__ = xbmcaddon.Addon()
__addonversion__ = __addon__.getAddonInfo('version')
__addonid__ = __addon__.getAddonInfo('id')
__addonname__ = __addon__.getAddonInfo('name')
__addonPath__ = __addon__.getAddonInfo('path')
__addonResourcePath__ = xbmcvfs.translatePath(os.path.join(__addonPath__, 'resources', 'lib'))
__addonIconFile__ = xbmcvfs.translatePath(os.path.join(__addonPath__, 'resources', 'icon.png'))
sys.path.append(__addonResourcePath__)

LOG_DEBUG = False
monitor = xbmc.Monitor()

def log_message(message, level=xbmc.LOGDEBUG):
    if LOG_DEBUG:
        for line in message.splitlines():
            xbmc.log(msg="{0}: {1}".format(__addonname__.encode("utf-8"), line.encode("utf-8")), level=level)

class SubtitleFilteredPlayer(xbmc.Player):
    def __init__(self):
        log_message('__init__')
        self.subtitles = []
        self.selected_sub = []
        xbmc.Player.__init__(self)

    def onAVStarted(self):
        log_message('onAVStarted')
        self.get_subtitles()
        self.process_subtitles()

    def process_subtitles(self):
        if 'language' in self.selected_sub and len(self.subtitles) > 1:
            preferred_language = self.selected_sub['language']
            log_message('preferred language: [' + preferred_language + ']')
            for sub in self.subtitles:
                log_message('found subtitle: [' + str(sub['index']) + '] ===>' + str(sub))
                ## finds first subtitle stream of the same language as already selected but which is NOT marked as forced
                if sub['language'] == preferred_language and not (sub['isforced'] is True or sub['name'].lower().find('forced') != -1):
                    self.setSubtitleStream(sub['index'])
                    log_message('subtitle changed')
                    break

    ## based on https://github.com/ace20022/service.LanguagePreferenceManager/
    def get_subtitles(self):
        activePlayers = '{"jsonrpc": "2.0", "method": "Player.GetActivePlayers", "id": 1}'
        json_query = xbmc.executeJSONRPC(activePlayers)
        json_response = simplejson.loads(json_query)
        activePlayerID = json_response['result'][0]['playerid']
        details_query_dict = {"jsonrpc": "2.0", "method": "Player.GetProperties", "params": {"properties":
                                ["currentsubtitle", "subtitles"], "playerid": activePlayerID}, "id": 1}
        details_query_string = simplejson.dumps(details_query_dict)
        json_query = xbmc.executeJSONRPC(details_query_string)
        json_response = simplejson.loads(json_query)

        if 'result' in json_response and json_response['result'] != None:
            self.selected_sub = json_response['result']['currentsubtitle']
            self.subtitles = json_response['result']['subtitles']
        log_message('json_response: [' + str(json_response) + ']')

class FilteredPlayerRunner:
    player = SubtitleFilteredPlayer()
    while not monitor.abortRequested():
        monitor.waitForAbort(1)
    del player
