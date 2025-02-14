import wx
from libs.frame_ui import FrameUI


class MainFrame(FrameUI):
    def __init__(self, parent, username, expires):
        FrameUI.__init__(self, parent)
        self.icon = wx.Icon('icon.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)
        self.username = username

        self.m_statusBar1.SetStatusWidths([-2, -2, -5])
        self.m_statusBar1.SetStatusText(username, 0)
        self.m_statusBar1.SetStatusText('过期时间：' + expires, 1)
        self.m_statusBar1.SetStatusText('技术联系：（QQ）43188540', 2)



