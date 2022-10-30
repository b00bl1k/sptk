# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-88b0f50)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MainWindow
###########################################################################

class MainWindow ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"sptk", pos = wx.DefaultPosition, size = wx.Size( 745,412 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		self.menubar = wx.MenuBar( 0 )
		self.mnu_file = wx.Menu()
		self.mnu_send = wx.MenuItem( self.mnu_file, wx.ID_ANY, u"Send", wx.EmptyString, wx.ITEM_NORMAL )
		self.mnu_file.Append( self.mnu_send )

		self.mnu_file.AppendSeparator()

		self.mnu_exit = wx.MenuItem( self.mnu_file, wx.ID_ANY, u"Exit", wx.EmptyString, wx.ITEM_NORMAL )
		self.mnu_file.Append( self.mnu_exit )

		self.menubar.Append( self.mnu_file, u"File" )

		self.mnu_settings = wx.Menu()
		self.mnu_ser_port = wx.MenuItem( self.mnu_settings, wx.ID_ANY, u"Serial port", wx.EmptyString, wx.ITEM_NORMAL )
		self.mnu_settings.Append( self.mnu_ser_port )

		self.menubar.Append( self.mnu_settings, u"Settings" )

		self.mnu_help = wx.Menu()
		self.mnu_about = wx.MenuItem( self.mnu_help, wx.ID_ANY, u"About", wx.EmptyString, wx.ITEM_NORMAL )
		self.mnu_help.Append( self.mnu_about )

		self.menubar.Append( self.mnu_help, u"About" )

		self.SetMenuBar( self.menubar )

		self.toolbar = self.CreateToolBar( wx.TB_HORIZONTAL, wx.ID_ANY )
		self.tool_open_port = self.toolbar.AddTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_FILE_OPEN,  ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None )

		self.tool_close_port = self.toolbar.AddTool( wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap( wx.ART_CLOSE,  ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None )

		self.toolbar.AddSeparator()

		self.tool_exit = self.toolbar.AddTool( wx.ID_ANY, u"Exit", wx.ArtProvider.GetBitmap( wx.ART_QUIT,  ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None )

		self.toolbar.Realize()

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		self.splitter = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.splitter.Bind( wx.EVT_IDLE, self.splitterOnIdle )

		self.left_panel = wx.Panel( self.splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer3 = wx.BoxSizer( wx.VERTICAL )

		self.tx_list = wx.ListCtrl( self.left_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		self.tx_list.SetFont( wx.Font( 10, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		bSizer3.Add( self.tx_list, 1, wx.ALL|wx.EXPAND, 5 )

		self.btn_tx_clear = wx.Button( self.left_panel, wx.ID_ANY, u"Clear", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.btn_tx_clear, 0, wx.ALL, 5 )


		self.left_panel.SetSizer( bSizer3 )
		self.left_panel.Layout()
		bSizer3.Fit( self.left_panel )
		self.right_panel = wx.Panel( self.splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer4 = wx.BoxSizer( wx.VERTICAL )

		self.rx_list = wx.ListCtrl( self.right_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		self.rx_list.SetFont( wx.Font( 10, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		bSizer4.Add( self.rx_list, 1, wx.ALL|wx.EXPAND, 5 )

		self.btn_rx_clear = wx.Button( self.right_panel, wx.ID_ANY, u"Clear", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.btn_rx_clear, 0, wx.ALL, 5 )


		self.right_panel.SetSizer( bSizer4 )
		self.right_panel.Layout()
		bSizer4.Fit( self.right_panel )
		self.splitter.SplitVertically( self.left_panel, self.right_panel, 0 )
		bSizer1.Add( self.splitter, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()
		self.statusbar = self.CreateStatusBar( 5, wx.STB_SIZEGRIP, wx.ID_ANY )

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.on_close )
		self.Bind( wx.EVT_MENU, self.mnu_send_click, id = self.mnu_send.GetId() )
		self.Bind( wx.EVT_MENU, self.mnu_exit_click, id = self.mnu_exit.GetId() )
		self.Bind( wx.EVT_MENU, self.mnu_ser_port_click, id = self.mnu_ser_port.GetId() )
		self.Bind( wx.EVT_MENU, self.mnu_about_click, id = self.mnu_about.GetId() )
		self.Bind( wx.EVT_TOOL, self.tool_open_port_click, id = self.tool_open_port.GetId() )
		self.Bind( wx.EVT_TOOL, self.tool_close_port_click, id = self.tool_close_port.GetId() )
		self.Bind( wx.EVT_TOOL, self.tool_exit_click, id = self.tool_exit.GetId() )
		self.btn_tx_clear.Bind( wx.EVT_BUTTON, self.btn_tx_clear_click )
		self.btn_rx_clear.Bind( wx.EVT_BUTTON, self.btn_rx_clear_click )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def on_close( self, event ):
		event.Skip()

	def mnu_send_click( self, event ):
		event.Skip()

	def mnu_exit_click( self, event ):
		event.Skip()

	def mnu_ser_port_click( self, event ):
		event.Skip()

	def mnu_about_click( self, event ):
		event.Skip()

	def tool_open_port_click( self, event ):
		event.Skip()

	def tool_close_port_click( self, event ):
		event.Skip()

	def tool_exit_click( self, event ):
		event.Skip()

	def btn_tx_clear_click( self, event ):
		event.Skip()

	def btn_rx_clear_click( self, event ):
		event.Skip()

	def splitterOnIdle( self, event ):
		self.splitter.SetSashPosition( 0 )
		self.splitter.Unbind( wx.EVT_IDLE )


###########################################################################
## Class SerialPortDialog
###########################################################################

class SerialPortDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Serial Port", pos = wx.DefaultPosition, size = wx.Size( 312,306 ), style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer5 = wx.BoxSizer( wx.VERTICAL )

		gSizer2 = wx.GridSizer( 0, 2, 0, 0 )

		self.lbl_port = wx.StaticText( self, wx.ID_ANY, u"Port:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl_port.Wrap( -1 )

		gSizer2.Add( self.lbl_port, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 5 )

		list_portChoices = []
		self.list_port = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, list_portChoices, 0 )
		self.list_port.SetSelection( 0 )
		gSizer2.Add( self.list_port, 1, wx.ALL|wx.EXPAND, 5 )

		self.lbl_baud = wx.StaticText( self, wx.ID_ANY, u"Baudrate:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl_baud.Wrap( -1 )

		gSizer2.Add( self.lbl_baud, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 5 )

		list_baudChoices = []
		self.list_baud = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, list_baudChoices, 0 )
		self.list_baud.SetSelection( 0 )
		gSizer2.Add( self.list_baud, 1, wx.ALL|wx.EXPAND, 5 )

		self.lbl_data = wx.StaticText( self, wx.ID_ANY, u"Data:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl_data.Wrap( -1 )

		gSizer2.Add( self.lbl_data, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 5 )

		list_dataChoices = []
		self.list_data = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, list_dataChoices, 0 )
		self.list_data.SetSelection( 0 )
		gSizer2.Add( self.list_data, 1, wx.ALL|wx.EXPAND, 5 )

		self.lbl_parity = wx.StaticText( self, wx.ID_ANY, u"Parity:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl_parity.Wrap( -1 )

		gSizer2.Add( self.lbl_parity, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 5 )

		list_parityChoices = []
		self.list_parity = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, list_parityChoices, 0 )
		self.list_parity.SetSelection( 0 )
		gSizer2.Add( self.list_parity, 1, wx.ALL|wx.EXPAND, 5 )

		self.lbl_stop = wx.StaticText( self, wx.ID_ANY, u"Stop bits:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl_stop.Wrap( -1 )

		gSizer2.Add( self.lbl_stop, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 5 )

		list_stopChoices = []
		self.list_stop = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, list_stopChoices, 0 )
		self.list_stop.SetSelection( 0 )
		gSizer2.Add( self.list_stop, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer5.Add( gSizer2, 0, wx.EXPAND, 5 )


		bSizer5.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		bSizer6 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer6.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )

		self.btn_ok = wx.Button( self, wx.ID_ANY, u"Ok", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.btn_ok, 0, wx.ALL, 5 )

		self.btn_cancel = wx.Button( self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.btn_cancel, 0, wx.ALL, 5 )


		bSizer6.Add( bSizer7, 0, wx.ALIGN_RIGHT, 5 )


		bSizer5.Add( bSizer6, 0, wx.EXPAND, 5 )


		self.SetSizer( bSizer5 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.btn_ok.Bind( wx.EVT_BUTTON, self.btn_ok_click )
		self.btn_cancel.Bind( wx.EVT_BUTTON, self.btn_cancel_click )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def btn_ok_click( self, event ):
		event.Skip()

	def btn_cancel_click( self, event ):
		event.Skip()


###########################################################################
## Class SendDialog
###########################################################################

class SendDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Send", pos = wx.DefaultPosition, size = wx.Size( 567,226 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.Size( 300,200 ), wx.DefaultSize )

		bSizer7 = wx.BoxSizer( wx.VERTICAL )

		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )

		combo_sendChoices = []
		self.combo_send = wx.ComboBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, combo_sendChoices, 0 )
		bSizer9.Add( self.combo_send, 1, wx.ALL, 5 )

		self.btn_send = wx.Button( self, wx.ID_ANY, u"Send", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer9.Add( self.btn_send, 0, wx.ALL, 5 )


		bSizer7.Add( bSizer9, 0, wx.EXPAND, 5 )

		bSizer12 = wx.BoxSizer( wx.VERTICAL )

		self.check_hex = wx.CheckBox( self, wx.ID_ANY, u"Hex data", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.check_hex.SetValue(True)
		bSizer12.Add( self.check_hex, 0, wx.ALL, 5 )


		bSizer7.Add( bSizer12, 1, wx.EXPAND, 5 )


		bSizer7.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		bSizer6 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer6.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer71 = wx.BoxSizer( wx.HORIZONTAL )

		self.btn_close = wx.Button( self, wx.ID_ANY, u"Close", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer71.Add( self.btn_close, 0, wx.ALL, 5 )


		bSizer6.Add( bSizer71, 0, wx.ALIGN_RIGHT, 5 )


		bSizer7.Add( bSizer6, 0, wx.EXPAND, 5 )


		self.SetSizer( bSizer7 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.btn_send.Bind( wx.EVT_BUTTON, self.btn_send_click )
		self.check_hex.Bind( wx.EVT_CHECKBOX, self.check_hex_click )
		self.btn_close.Bind( wx.EVT_BUTTON, self.btn_close_click )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def btn_send_click( self, event ):
		event.Skip()

	def check_hex_click( self, event ):
		event.Skip()

	def btn_close_click( self, event ):
		event.Skip()


