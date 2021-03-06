import ts3lib, ts3defines, datetime
from ts3plugin import ts3plugin
from pytsonui import setupUi
from PythonQt.QtGui import *
from configparser import ConfigParser
from os import path

class NoX(ts3plugin):
    name = "BanBypasser (NoX)"
    apiVersion = 21
    requestAutoload = False
    version = "1.0"
    author = "Bluscream"
    description = "Fights for you against admin abuse!"
    offersConfigure = True
    commandKeyword = ""
    infoTitle = None
    iconPath = path.join(ts3lib.getPluginPath(), "pyTSon", "scripts", "NoX", "icons")
    menuItems = [(ts3defines.PluginMenuType.PLUGIN_MENU_TYPE_GLOBAL, 0, "Change Identity", "")]
    hotkeys = []
    debug = False
    ini = path.join(ts3lib.getPluginPath(), "pyTSon", "scripts", "NoX", "settings.ini")
    cfg = ConfigParser()
    dlg = None

    def __init__(self):
        if path.isfile(self.ini):
            self.cfg.read(self.ini)
        else:
            self.cfg['general'] = { "cfgversion": "1", "debug": "False", "enabled": "True", "channelpw": "123", "serverpw": "123", "anticrash": "True" }
            self.cfg['antimove'] = { "enabled": "True", "delay": "0"}
            self.cfg['antichannelkick'] = { "enabled": "True", "delay": "0"}
            self.cfg['antichannelban'] = { "enabled": "True", "delay": "0"}
            self.cfg['antiserverkick'] = { "enabled": "True", "delay": "0"}
            self.cfg['antiserverban'] = { "enabled": "True", "delay": "0"}
            self.cfg['antichanneldelete'] = { "enabled": "True", "delay": "0"}
            self.cfg['lastconnection'] = { "ip": "127.0.0.1", "port": "9987", "channelid": "0", "channelname": "Default Channel", "nickname": "TeamspeakUser", "phoneticnick": "", "metaData": "" }
            with open(self.ini, 'w') as configfile:
                self.cfg.write(configfile)
        ts3lib.logMessage(self.name+" script for pyTSon by "+self.author+" loaded from \""+__file__+"\".", ts3defines.LogLevel.LogLevel_INFO, "Python Script", 0)
        if self.debug: ts3lib.printMessageToCurrentTab('[{:%Y-%m-%d %H:%M:%S}]'.format(datetime.now())+" [color=orange]"+self.name+"[/color] Plugin for pyTSon by [url=https://github.com/"+self.author+"]"+self.author+"[/url] loaded.")

    def configure(self, qParentWidget):
        try:
            if not self.dlg:
                self.dlg = SettingsDialog(self)
            self.dlg.show()
            self.dlg.raise_()
            self.dlg.activateWindow()
        except: from traceback import format_exc;ts3lib.logMessage(format_exc(), ts3defines.LogLevel.LogLevel_ERROR, "PyTSon", 0)

    def onMenuItemEvent(self, schid, atype, menuItemID, selectedItemID):
        if atype == ts3defines.PluginMenuType.PLUGIN_MENU_TYPE_GLOBAL:
            if menuItemID == 0: self.reconnect(schid)

    def onConnectStatusChangeEvent(self, schid, newStatus, errorNumber):
        if newStatus == ts3defines.ConnectStatus.STATUS_CONNECTION_ESTABLISHED:
            (error, ip) = ts3lib.getConnect(schid, channelID, ts3defines.ChannelProperties.CHANNEL_DESCRIPTION)

class SettingsDialog(QDialog):
    def __init__(self, this, parent=None):
        self.this = this
        super(QDialog, self).__init__(parent)
        setupUi(self, path.join(ts3lib.getPluginPath(), "pyTSon", "scripts", "NoX", "settings.ui"))
        self.setWindowTitle("%s Settings" % this.name)
        self.chk_debug.setChecked(this.cfg.getboolean("general", "debug"))