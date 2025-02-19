# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.2.1-0-g80c4cb6)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.grid

###########################################################################
## Class FrameUI
###########################################################################

class FrameUI ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"桂花抓取工具", pos = wx.DefaultPosition, size = wx.Size( 900,600 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.Size( -1,-1 ), wx.Size( -1,-1 ) )
		self.SetFont( wx.Font( 9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "微软雅黑" ) )
		self.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		self.set_panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText5 = wx.StaticText( self.set_panel, wx.ID_ANY, u"抓取的网址\n（一行一个\n最多10个）", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )

		bSizer7.Add( self.m_staticText5, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.urls = wx.TextCtrl( self.set_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 720,180 ), wx.HSCROLL|wx.TE_MULTILINE )
		bSizer7.Add( self.urls, 0, wx.ALL, 5 )


		bSizer2.Add( bSizer7, 1, wx.EXPAND, 5 )

		bSizer8 = wx.BoxSizer( wx.VERTICAL )

		self.submit_btn = wx.Button( self.set_panel, wx.ID_ANY, u"提交", wx.DefaultPosition, wx.Size( -1,36 ), 0 )
		bSizer8.Add( self.submit_btn, 0, wx.ALL, 5 )


		bSizer2.Add( bSizer8, 1, wx.ALIGN_CENTER|wx.ALIGN_LEFT, 5 )


		self.set_panel.SetSizer( bSizer2 )
		self.set_panel.Layout()
		bSizer2.Fit( self.set_panel )
		bSizer1.Add( self.set_panel, 1, wx.EXPAND |wx.ALL, 5 )

		self.plat_panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )

		self.res_info = wx.grid.Grid( self.plat_panel, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), 0 )

		# Grid
		self.res_info.CreateGrid( 10, 5 )
		self.res_info.EnableEditing( False )
		self.res_info.EnableGridLines( True )
		self.res_info.EnableDragGridSize( False )
		self.res_info.SetMargins( 0, 0 )

		# Columns
		self.res_info.SetColSize( 0, 50 )
		self.res_info.SetColSize( 1, 300 )
		self.res_info.SetColSize( 2, 300 )
		self.res_info.SetColSize( 3, 130 )
		self.res_info.SetColSize( 4, 90 )
		self.res_info.EnableDragColMove( False )
		self.res_info.EnableDragColSize( False )
		self.res_info.SetColLabelValue( 0, u"编号" )
		self.res_info.SetColLabelValue( 1, u"网址" )
		self.res_info.SetColLabelValue( 2, u"标题" )
		self.res_info.SetColLabelValue( 3, u"来源" )
		self.res_info.SetColLabelValue( 4, u"状态" )
		self.res_info.SetColLabelSize( 30 )
		self.res_info.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.res_info.SetRowSize( 0, 25 )
		self.res_info.SetRowSize( 1, 25 )
		self.res_info.SetRowSize( 2, 25 )
		self.res_info.SetRowSize( 3, 25 )
		self.res_info.SetRowSize( 4, 25 )
		self.res_info.SetRowSize( 5, 25 )
		self.res_info.SetRowSize( 6, 25 )
		self.res_info.SetRowSize( 7, 25 )
		self.res_info.SetRowSize( 8, 25 )
		self.res_info.SetRowSize( 9, 25 )
		self.res_info.EnableDragRowSize( False )
		self.res_info.SetRowLabelSize( 1 )
		self.res_info.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.res_info.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_CENTER )
		bSizer3.Add( self.res_info, 0, wx.ALL|wx.EXPAND, 0 )


		self.plat_panel.SetSizer( bSizer3 )
		self.plat_panel.Layout()
		bSizer3.Fit( self.plat_panel )
		bSizer1.Add( self.plat_panel, 1, wx.EXPAND |wx.ALL, 5 )

		self.btn_panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )

		self.start_btn = wx.Button( self.btn_panel, wx.ID_ANY, u"开始采集", wx.DefaultPosition, wx.Size( 100,36 ), 0 )
		self.start_btn.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )
		self.start_btn.Enable( False )

		bSizer4.Add( self.start_btn, 0, wx.ALL, 5 )

		self.reset_btn = wx.Button( self.btn_panel, wx.ID_ANY, u"清除重来", wx.DefaultPosition, wx.Size( 100,36 ), 0 )
		self.reset_btn.Enable( False )

		bSizer4.Add( self.reset_btn, 0, wx.ALL, 5 )

		bSizer71 = wx.BoxSizer( wx.HORIZONTAL )

		self.push_db_btn = wx.Button( self.btn_panel, wx.ID_ANY, u"加入稿库", wx.DefaultPosition, wx.Size( 95,36 ), 0 )
		self.push_db_btn.Enable( False )

		bSizer71.Add( self.push_db_btn, 0, wx.ALL, 5 )


		bSizer4.Add( bSizer71, 1, wx.EXPAND, 5 )


		self.btn_panel.SetSizer( bSizer4 )
		self.btn_panel.Layout()
		bSizer4.Fit( self.btn_panel )
		bSizer1.Add( self.btn_panel, 1, wx.ALIGN_CENTER, 0 )


		self.SetSizer( bSizer1 )
		self.Layout()
		self.m_statusBar1 = self.CreateStatusBar( 3, 0, wx.ID_ANY )
		self.m_timer1 = wx.Timer()
		self.m_timer1.SetOwner( self, self.m_timer1.GetId() )

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.quit )
		self.submit_btn.Bind( wx.EVT_BUTTON, self.submit )
		self.start_btn.Bind( wx.EVT_BUTTON, self.start )
		self.reset_btn.Bind( wx.EVT_BUTTON, self.reset )
		self.push_db_btn.Bind( wx.EVT_BUTTON, self.push_db )
		self.Bind( wx.EVT_TIMER, self.timer_func, id=self.m_timer1.GetId() )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def quit( self, event ):
		event.Skip()

	def submit( self, event ):
		event.Skip()

	def start( self, event ):
		event.Skip()

	def reset( self, event ):
		event.Skip()

	def push_db( self, event ):
		event.Skip()

	def timer_func( self, event ):
		event.Skip()


