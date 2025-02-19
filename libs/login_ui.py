# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.2.1-0-g80c4cb6)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class LoginUI
###########################################################################

class LoginUI ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"登录", pos = wx.DefaultPosition, size = wx.Size( 400,350 ), style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		self.login_mode_1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer6 = wx.BoxSizer( wx.VERTICAL )

		self.qrcode_login_btn = wx.StaticBitmap( self.login_mode_1, wx.ID_ANY, wx.Bitmap( u"banner.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.Size( 400,50 ), 0 )
		self.qrcode_login_btn.SetToolTip( u"二维码登录" )

		bSizer6.Add( self.qrcode_login_btn, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText1 = wx.StaticText( self.login_mode_1, wx.ID_ANY, u"账号：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )

		self.m_staticText1.SetFont( wx.Font( 14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		bSizer2.Add( self.m_staticText1, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.username = wx.TextCtrl( self.login_mode_1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 156,-1 ), 0 )
		self.username.SetFont( wx.Font( 12, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Times New Roman" ) )

		bSizer2.Add( self.username, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


		bSizer6.Add( bSizer2, 1, wx.ALIGN_CENTER, 5 )

		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText2 = wx.StaticText( self.login_mode_1, wx.ID_ANY, u"密码：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )

		self.m_staticText2.SetFont( wx.Font( 14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		bSizer3.Add( self.m_staticText2, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.password = wx.TextCtrl( self.login_mode_1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 156,-1 ), wx.TE_PASSWORD )
		self.password.SetFont( wx.Font( 12, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Times New Roman" ) )

		bSizer3.Add( self.password, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


		bSizer6.Add( bSizer3, 1, wx.ALIGN_CENTER, 5 )

		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )

		self.remember = wx.CheckBox( self.login_mode_1, wx.ID_ANY, u"记住登录信息", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.remember.SetValue(True)
		bSizer4.Add( self.remember, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.login_btn = wx.Button( self.login_mode_1, wx.ID_ANY, u"登录", wx.DefaultPosition, wx.Size( 120,40 ), 0 )
		self.login_btn.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		bSizer4.Add( self.login_btn, 0, wx.ALL, 5 )


		bSizer6.Add( bSizer4, 1, wx.ALIGN_CENTER, 5 )

		bSizer5 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText3 = wx.StaticText( self.login_mode_1, wx.ID_ANY, u"copyright @ 2025  XXX", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		bSizer5.Add( self.m_staticText3, 0, wx.ALL, 5 )


		bSizer6.Add( bSizer5, 1, wx.ALIGN_CENTER, 5 )


		self.login_mode_1.SetSizer( bSizer6 )
		self.login_mode_1.Layout()
		bSizer6.Fit( self.login_mode_1 )
		bSizer1.Add( self.login_mode_1, 1, wx.EXPAND |wx.ALL, 5 )

		self.login_mode_2 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.login_mode_2.Hide()

		bSizer8 = wx.BoxSizer( wx.VERTICAL )

		self.account_login_btn = wx.StaticBitmap( self.login_mode_2, wx.ID_ANY, wx.Bitmap( u"account2.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.account_login_btn.SetToolTip( u"账号登录" )

		bSizer8.Add( self.account_login_btn, 0, wx.ALL, 5 )

		self.m_qrcode = wx.StaticBitmap( self.login_mode_2, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 200,200 ), 0 )
		bSizer8.Add( self.m_qrcode, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.m_staticText6 = wx.StaticText( self.login_mode_2, wx.ID_ANY, u"copyright @ 2025  XXX", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )

		bSizer8.Add( self.m_staticText6, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		self.login_mode_2.SetSizer( bSizer8 )
		self.login_mode_2.Layout()
		bSizer8.Fit( self.login_mode_2 )
		bSizer1.Add( self.login_mode_2, 1, wx.ALL|wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()
		self.m_timer1 = wx.Timer()
		self.m_timer1.SetOwner( self, self.m_timer1.GetId() )

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.close )
		self.qrcode_login_btn.Bind( wx.EVT_LEFT_UP, self.qrcode_login )
		self.login_btn.Bind( wx.EVT_BUTTON, self.login )
		self.account_login_btn.Bind( wx.EVT_LEFT_UP, self.account_login )
		self.Bind( wx.EVT_TIMER, self.timer_func, id=self.m_timer1.GetId() )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def close( self, event ):
		event.Skip()

	def qrcode_login( self, event ):
		event.Skip()

	def login( self, event ):
		event.Skip()

	def account_login( self, event ):
		event.Skip()

	def timer_func( self, event ):
		event.Skip()


