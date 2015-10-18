"""
Layout by Code for Python
Version 1.5
October 18, 2015
Copyright 2009 - 2015 by Jamal Mazrui
GNU Lesser General Public License (LGPL)
"""

import ctypes, os, sys
import win32api
import wx
from odict import OrderedDict

DEFAULT_PARENT = -1
DEFAULT_STYLE = 0
BorderPad = 2
CharHeight = 16
LabelWidth = -1
ButtonWidth = 100
ButtonHeight = 16
CheckBoxWidth = -1
RadioBoxWidth = -1
RadioBoxHeight = -1
RadioButtonWidth = -1
InputWidth = 200
EditWidth = 200
EditHeight = 200
ListWidth = 200
ListHeight = 100
HORIZONTAL_LABEL_PAD = 6
HORIZONTAL_RELATED_PAD = 8
HORIZONTAL_DIVIDER_PAD = 14
VERTICAL_RELATED_PAD = 8
VERTICAL_DIVIDER_PAD = 14

def ActivateWindow(hWindow):
	KERNEL32 = ctypes.windll.KERNEL32
	GetCurrentThreadId = KERNEL32.GetCurrentThreadId
	
	USER32 = ctypes.windll.USER32
	AttachThreadInput = USER32.AttachThreadInput
	BringWindowToTop = USER32.BringWindowToTop
	GetForegroundWindow = USER32.GetForegroundWindow
	GetWindowThreadProcessId = USER32.GetWindowThreadProcessId
	ShowWindow=USER32.ShowWindow
	
	iForegroundThread = GetWindowThreadProcessId(GetForegroundWindow(), 0)
	#print 'foreground thread', iForegroundThread
	iAppThread = GetCurrentThreadId()
	#print 'app thread', iAppThread
	if iForegroundThread == iAppThread:
		BringWindowToTop(hWindow)
		ShowWindow(hWindow,5)
	else:
		iResult = AttachThreadInput(iForegroundThread, iAppThread, 1)
		#print 'result', iResult
		iResult = BringWindowToTop(hWindow)
		iResult = ShowWindow(hWindow,5)
		iResult = AttachThreadInput(iForegroundThread, iAppThread, 0)
		#print 'result', iResult

def Activator(event):
	dlg = event.GetEventObject()
	h = dlg.GetHandle()
	ActivateWindow(h)

def DialogBrowseForFolder(parent=DEFAULT_PARENT, message='', value='', style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON):
	sResult = ''
	app = None
	if not wx.GetApp(): app = App()
	if parent == DEFAULT_PARENT: parent = GetDefaultParent()
	dlg = wx.DirDialog(parent=parent, message=message, defaultPath=value, style=style)
	dlg.Bind(wx.EVT_INIT_DIALOG, Activator)
	if dlg.ShowModal() == wx.ID_OK: sResult = dlg.GetPath()
	#dlg.Destroy() 
	if app: app.ExitMainLoop()
	return sResult
	# end def

def DialogChoose(parent=DEFAULT_PARENT, title='Choose', message = '', names=[], index=0):
	sResult = ''
	app = None
	if not wx.GetApp(): app = App()
	if parent == DEFAULT_PARENT: parent = GetDefaultParent()
	dlg = Dialog(parent=parent, title=title)
	if message:
		dlg.AddStaticText(label=message)
		dlg.AddBand()
	lNames = names[:]
	lNames.append('Cancel')
	# print 'lNames', lNames
	for i in range(len(lNames)):
		if i > 0: dlg.AddBand()
		btn = dlg.AddButton(label=lNames[i])
		# dlg.Bind(wx.EVT_BUTTON, dlg.DefaultHandler, id=btn.GetId())
		if i == index: btn.SetFocus()
	# end for
	iID = dlg.Complete(buttons=[])
	btn = dlg.FindWindowById(iID)
	sResult = FixName(btn.GetLabel())
	sResult = sResult.replace('_', '')
	if app: app.ExitMainLoop()
	return sResult
# end def

def DialogConfirm(parent=DEFAULT_PARENT, title='Confirm', message='', value='Y'):
	iStyle = wx.YES_NO | wx.CANCEL | wx.ICON_QUESTION
	if value == 'Y':
		iStyle |= wx.YES_DEFAULT
	# end if
	else:
		iStyle |= wx.NO_DEFAULT
	# end else
	app = None
	if not wx.GetApp(): app = App()
	if parent == DEFAULT_PARENT: parent = GetDefaultParent()
	#btn = wx.MessageBox(parent=parent, caption=title, message=message, style=iStyle)
	btn = wx.MessageBox(message, title, iStyle)
	if btn == wx.YES:
		# oST.Say('Yes')
		sResult = 'Y'
	# end if
	elif btn == wx.NO:
		# oST.Say('No')
		sResult = 'N'
	# end elif
	else:
		# oST.Say('Cancel')
		sResult = ''
	# end else
	#dlg.Destroy()
	if app: app.ExitMainLoop()
	return sResult
# end def

def DialogInput(parent=DEFAULT_PARENT, title='Input', label='', value='', ):
	result = None
	app = None
	if not wx.GetApp(): app = App()
	if parent == DEFAULT_PARENT: parent = GetDefaultParent()
	#dlg = wx.TextEntryDialog(parent=parent, caption=title, label=label, value=value)
	dlg = wx.TextEntryDialog(parent, label, title, value)
	dlg.Bind(wx.EVT_INIT_DIALOG, Activator)
	if dlg.ShowModal() == wx.ID_OK: result = dlg.GetValue()
	dlg.Destroy()
	if app: app.ExitMainLoop()
	return result
# end def

def DialogMemo(parent=DEFAULT_PARENT, title='Memo', label='', value='', style= wx.TE_MULTILINE | wx.TE_PROCESS_ENTER, readonly=False):
	sResult = ''
	app = None
	if not wx.GetApp(): app = App()
	if parent == DEFAULT_PARENT: parent = GetDefaultParent()
	dlg = Dialog(parent=parent, title=title)
	iStyle = style
	if readonly: iStyle |= wx.TE_READONLY
	dlg.AddRichEdit(label=label, value=value, pos=wx.DefaultPosition, size=wx.DefaultSize, style=iStyle)
	if readonly: iID = dlg.Complete(['Close'])
	else: iID = dlg.Complete()
	if iID == wx.ID_OK: sResult = dlg.Results['RichEdit_' + FixName(label)] 
		#dlg.Destroy()
	if app: app.ExitMainLoop()
	return sResult
# end def

def DialogMultiInput(parent=DEFAULT_PARENT, title='MultiInput', labels=[], values=[], options=[], statusbar=False, ini=''):
	sResults = ''
	app = None
	if not wx.GetApp(): app = App()
	if parent == DEFAULT_PARENT: parent = GetDefaultParent()
	dlg = Dialog(parent=parent, title=title)
	#print 'labels', len(labels), labels
	#print 'values', len(values), values
	for i in range(len(labels)):
		if i > 0: dlg.AddBand()
		sLabel, sValue = labels[i], values[i]
		dlg.AddTextCtrl(label=sLabel, value=sValue)
	# end for
	iID = dlg.Complete(statusbar=statusbar, ini=ini)
	lResults = []
	if iID == wx.ID_OK:
		for control in dlg.Controls.keys():
			if control.startswith('TextCtrl_'): lResults.append(dlg.Results[control])
		# end for
		#dlg.Destroy()
		if app: app.ExitMainLoop()
	return lResults
# end def

def DialogMultiPick(parent=DEFAULT_PARENT, title='Multi Pick', message='', names=[], values=[], sort=False, index=0):
	lResults = []
	if len(values) == 0: values = names
	if sort: names, values = SortNamesAndValues(names, values) 	 	
	app = None
	if not wx.GetApp(): app = App()
	if parent == DEFAULT_PARENT: parent = GetDefaultParent()
	dlg = Dialog(parent=parent, title=title)
	lst = dlg.AddListBox(label=message, names=names, style=DEFAULT_STYLE | wx.LB_MULTIPLE)
	dlg.Bind(wx.EVT_INIT_DIALOG, Activator)
	iID = dlg.Complete()
	if iID == wx.ID_OK: lResults = [values[i] for i in lst.GetSelections()]
	#dlg.Destroy()
	if app: app.ExitMainLoop()
	return lResults
# end def

def DialogOpenFile(parent=DEFAULT_PARENT, title='Open', value='', wildcard='All files (*.*)|*.*'):
	sResult = ''
	path = value
	sDir, sFile = os.path.split(path)
	if os.path.isfile(path): sDir, sFile = os.path.split(path)
	elif os.path.isdir(path): sDir, sFile = (path, '')
	elif not os.path.isdir(sDir): sDir, sFile = ('', '')
	app = None
	if not wx.GetApp(): app = App()
	if parent == DEFAULT_PARENT: parent = GetDefaultParent()
	dlg = wx.FileDialog(parent, message=title, defaultDir=sDir, defaultFile=sFile, wildcard=wildcard, style=wx.OPEN)
	dlg.Bind(wx.EVT_INIT_DIALOG, Activator)
	if dlg.ShowModal() == wx.ID_OK: sResult = dlg.GetPath()
	#dlg.Destroy()
	if app: app.ExitMainLoop()
	return sResult
	# end def

def DialogPick(parent=DEFAULT_PARENT, title='Pick', message='', names=[], values=[], sort=False, index=0):
	vResult = ''
	if len(values) == 0: values = names
	if sort: names, values = SortNamesAndValues(names, values) 	
	app = None
	if not wx.GetApp(): app = App()
	if parent == DEFAULT_PARENT: parent = GetDefaultParent()
	#dlg = wx.SingleChoiceDialog(parent=parent, id=wx.ID_ANY, message=message, title=title, choices=names, style=wx.OK | wx.CANCEL)
	dlg = wx.SingleChoiceDialog(parent, message, title, names, style=wx.OK | wx.CANCEL)
	dlg.SetSelection(index)
	dlg.Bind(wx.EVT_INIT_DIALOG, Activator)
	if dlg.ShowModal() == wx.ID_OK:
		i = dlg.GetSelection()
		vResult = values[i]
	# end if
	else:
		# oST.Say('Cancel')
		pass
	# end else
#	iIndex = wx.GetSingleChoiceIndex(message, title, names, parent)    
#	vResult = values[iIndex]
	#dlg.Destroy()
	if app: app.ExitMainLoop()
	return vResult
# end def

def DialogSaveFile(parent=DEFAULT_PARENT, title='Save', value='', wildcard='All files (*.*)|*.*'):
	sResult = ''
	path = value
	sDir, sFile = os.path.split(path)
	if os.path.isfile(path): sDir, sFile = os.path.split(path)
	elif os.path.isdir(path): sDir, sFile = (path, '')
	elif not os.path.isdir(sDir): sDir, sFile = ('', '')
	app = None
	if not wx.GetApp(): app = App()
	if parent == DEFAULT_PARENT: parent = GetDefaultParent()
	dlg = wx.FileDialog(parent, message=title, defaultDir=sDir, defaultFile=sFile, wildcard=wildcard, style=wx.SAVE | wx.OVERWRITE_PROMPT)
	dlg.Bind(wx.EVT_INIT_DIALOG, Activator)
	if dlg.ShowModal() == wx.ID_OK: sResult = dlg.GetPath()
	#dlg.Destroy()
	if app: app.ExitMainLoop()
	return sResult
	# end def

def DialogShow(parent=DEFAULT_PARENT, title='Show', message=''):
	app = None
	if not wx.GetApp(): app = App()
	if parent == DEFAULT_PARENT: parent = GetDefaultParent()
	# wx.MessageBox(parent=parent, caption=str(title), message=str(message), style=wx.OK)
	wx.MessageBox(parent=parent, caption=unicode(title), message=unicode(message), style=wx.OK)
	if app: app.ExitMainLoop()
# end def

def GetDefaultParent():
	app = None
	if not wx.GetApp(): app = App()
	parent = wx.GetActiveWindow()
	if not parent: parent = wx.FindWindowByName('desktop') # ctypes.windll.USER32.GetDesktopWindow()
	if app: app.Destroy()
	return parent

def GetEventDict():
	dEvents = {}
	for s in dir(wx):
		if not s.startswith('EVT_'): continue
		e = wx.__dict__[s]
		if not getattr(e, 'evtType', None): continue
		sName = s[4:]
		for iType in e.evtType: dEvents[iType] = sName

	return dEvents

def GetEventName(event):
	iType = event.GetEventType()
	sName = EVENT_DICT[iType]
	return sName

def GetScript():
	sScript = sys.executable
	if sScript.endswith('python.exe'): sScript = sys.argv[0]
	return sScript

def GetIni():
	sIni = GetScript()
	i = sIni.find('.')
	sIni = sIni[0:i] + '.ini'
	return sIni

def FixName(name=''):
	sName = name
	sName = sName.replace('&', '')
	sName = sName.replace(':', '')
	sName = sName.replace(' ', '_')
	return sName

def FixLabel(label = ''):
	sLabel = label
	if len(sLabel) == 0: return sLabel
	sLabel = sLabel.replace('_', '')
	if sLabel.find('&') == -1: sLabel = '&' + sLabel
	if not sLabel.endswith(':'): sLabel += ':'
	return sLabel
# end def

def IsButtonEvent(event):
	return GetEventName(event) in ['BUTTON']

def IsCheckBoxEvent(event):
	return GetEventName(event) in ['CHECKBOX']

def IsCloseEvent(event):
	return GetEventName(event) in ['CLOSE', 'WINDOW_MODAL_DIALOG_CLOSED']

def IsFocusEvent(event):
	return GetEventName(event) in ['CHILD_FOCUS']

def IsIdleEvent(event):
	return GetEventName(event) in ['IDLE']

def IsInitDialogEvent(event):
	return GetEventName(event) in ['INIT_DIALOG']

def IsLeftClickEvent(event):
	return GetEventName(event) in ['COMMAND_LEFT_CLICK']

def IsRadioButtonEvent(event):
	return GetEventName(event) in ['RADIOBUTTON']

def IsRightClickEvent(event):
	return GetEventName(event) in ['COMMAND_RIGHT_CLICK']

def IsTextEvent(event):
	return GetEventName(event) in ['TEXT']

def SortNamesAndValues(names, values):
	l = [(names[i].lower(), i, names[i], values[i]) for i in range(len(names))]
	l.sort()
	names = [name for name_lower, i, name, value in l]
	values = [value for name_lower, i, name, value in l]
	return names, values
	# end def

class App(wx.App):

	def __init__(self, redirect=False, filename=None, useBestVisual=False, clearSigInt=True):
		wx.App.__init__(self, redirect, filename, useBestVisual, clearSigInt)

	def OnInit(self): return True

class Dialog(wx.Dialog):
	
	# def __init__(self, parent=None, title='Dialog', pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE):
	# def __init__(self, parent=None, title='Dialog', pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE):
	def __init__(self, parent=None, title='Dialog', pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE):
		style = wx.RESIZE_BORDER
		wx.Dialog.__init__(self, parent=parent, title=title, pos=pos, size=size, style=style)
		# self.Bind(wx.EVT_INIT_DIALOG, self.DefaultHandler)
		self.SetName('Dialog_' + title)
		self.CustomHandler = None
		self.Results = {}
		self.Tips = {}
		self.Sizers = []
		self.Controls = OrderedDict()
		self.Sizers.append(wx.BoxSizer(wx.VERTICAL))
		self.band = 0
		self.Sizers[0].Add(wx.Size(1, VERTICAL_DIVIDER_PAD))
		self.AddBand()
#		super(self, '__init__')
#		wx.Dialog.__init__(self, parent=parent, id=id, title=title, pos=pos, size=size, style=style)
	# end def
	
	def AddBand(self):
		if self.band > 0: 
			self.Sizers[self.band].Add(wx.Size(HORIZONTAL_LABEL_PAD, 1))
			iFlags = wx.GROW
			self.Sizers[0].Add(self.Sizers[self.band], 1, iFlags)

		self.Sizers[0].Add(wx.Size(1, VERTICAL_RELATED_PAD))
		self.Sizers.append(wx.BoxSizer(wx.HORIZONTAL))
		self.band += 1
		self.Sizers[self.band].Add(wx.Size(HORIZONTAL_DIVIDER_PAD, 1))
	# end def

	def AddButtonBand(self, buttons=[], index=0, handler=None):
		self.CustomHandler = handler
		self.AddBand()
		for i in range(len(buttons)):
			sButton = buttons[i]
			btn = self.AddButton(label=sButton)
			if index != None and index != -1 and i == index: btn.SetDefault()
			#print 'handler', handler
			# # self.Bind(wx.EVT_BUTTON, self.DefaultHandler, id=btn.GetId())
		# end for
	# end def
	
	def AddButton(self, id=wx.ID_ANY, label='', pos=wx.DefaultPosition, size=wx.DefaultSize, style=DEFAULT_STYLE, name=''):
		sLabel = label
		if sLabel == 'OK':
			iID = wx.ID_OK
		# end if
		elif label == 'Cancel':
			iID = wx.ID_CANCEL
		# end elif
		elif label == 'Close':
			iID = wx.ID_CANCEL
			# iID = wx.ID_CLOSE
			# iID = 2
		# end elif
		else:
			iID = wx.ID_ANY
			if sLabel.find('&') == -1: sLabel = '&' + sLabel
		# end else
		sName = name
		if len(sName) == 0: sName = 'Button_' + FixName(label)
		btn = wx.Button(parent=self, id=iID, label=sLabel, pos=pos, size=size, style=style, name=sName)
		self.Sizers[self.band].Add(btn, 0, wx.ALIGN_LEFT | wx.ALIGN_TOP)
		self.Sizers[self.band].Add(wx.Size(HORIZONTAL_RELATED_PAD, 1))
		self.Bind(wx.EVT_BUTTON, self.DefaultHandler, id=btn.GetId())
		self.Controls[sName] = btn
		# print sName, iID
		return btn
	# end def
	
	def AddCheckBox(self, id=wx.ID_ANY, label='', value=False, pos=wx.DefaultPosition, size=wx.DefaultSize, style=DEFAULT_STYLE, name=''):
		sLabel = label
		if sLabel.find('&') == -1: sLabel = '&' + sLabel
		sName = name
		if len(sName) == 0: sName = 'CheckBox_' + FixName(label)
		chk = wx.CheckBox(parent=self, id=id, label=sLabel, pos=pos, size=size, style=style, name=sName)
		chk.SetValue(value)
		self.Sizers[self.band].Add(chk, 0, wx.ALIGN_LEFT | wx.ALIGN_TOP)
		self.Sizers[self.band].Add(wx.Size(HORIZONTAL_RELATED_PAD, 1))
		self.Bind(wx.EVT_CHECKBOX, self.DefaultHandler, id=chk.GetId())
		self.Controls[sName] = chk
		return chk
	# end def
	
	def AddListBox(self, id=wx.ID_ANY, label='', names=[], values=[], sort=False, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.LB_HSCROLL, name=''):
		if len(label) > 0: self.AddStaticText(label=label)
		sName = name
		if len(sName) == 0: sName = 'ListBox_' + FixName(label)
		iStyle = style
		if sort: iStyle |= wx.LB_SORT
		lst = wx.ListBox(parent=self, id=id, pos=pos, size=size, style=iStyle, name=sName)
		for i in range(len(names)):
			lst.Append(item=names[i], clientData=i)
		# end for
		
		if lst.GetCount(): lst.SetSelection(0)
		self.Sizers[self.band].Add(lst, 1, wx.ALIGN_LEFT | wx.ALIGN_TOP | wx.GROW)
		self.Sizers[self.band].Add(wx.Size(HORIZONTAL_RELATED_PAD, 1))
		self.Bind(wx.EVT_LISTBOX, self.DefaultHandler, id=lst.GetId())
		self.Controls[sName] = lst
		return lst
	# end def
	
	def AddMemo(self, id=wx.ID_ANY, label='', value='', readonly=False, pos=wx.DefaultPosition, size=wx.DefaultSize, style= wx.TE_MULTILINE | wx.TE_PROCESS_ENTER, name=''):
		if len(label) > 0: self.AddStaticText(label=label)
		sName = name
		if len(sName) == 0: sName = 'Memo_' + FixName(label)
		iStyle = style
		if readonly: iStyle |= wx.TE_READONLY
		txt = wx.TextCtrl(parent=self, id=id, pos=pos, size=size, style=iStyle, name=sName)
		txt.SetValue(value)
		self.Sizers[self.band].Add(txt, 1, wx.ALIGN_LEFT | wx.ALIGN_TOP | wx.GROW)
		self.Sizers[self.band].Add(wx.Size(HORIZONTAL_RELATED_PAD, 1))
		self.Controls[sName] = txt
		# self.Bind(wx.EVT_SET_FOCUS, self.DefaultHandler, id=txt.GetId())
		# self.Bind(wx.EVT_KEY_DOWN, self.DefaultHandler, id=txt.GetId())
		return txt
	# end def

	def AddRadioButton(self, id=wx.ID_ANY, label='', value=False, pos=wx.DefaultPosition, size=wx.DefaultSize, style=DEFAULT_STYLE, name=''):
		sLabel = label
		if sLabel.find('&') == -1: sLabel = '&' + sLabel
		iStyle = style
		if len(self.Controls) > 0 and not self.Controls[-1].startswith('RadioButton_'): iStyle = wx.RB_GROUP
		sName = name
		if len(sName) == 0: sName = 'RadioButton_' + FixName(label)
		rdn = wx.RadioButton(parent=self, id=id, label=sLabel, pos=pos, size=size, style=style, name=sName)
		rdn.SetValue(value)
		self.Sizers[self.band].Add(rdn, 0, wx.ALIGN_LEFT | wx.ALIGN_TOP)
		self.Sizers[self.band].Add(wx.Size(HORIZONTAL_RELATED_PAD, 1))
		self.Bind(wx.EVT_RADIOBUTTON, self.DefaultHandler, id=rbn.GetId())
		self.Controls[sName] = rdn
		return rdn
	# end def
	
	def AddRichEdit(self, id=wx.ID_ANY, label='', value='', readonly=False, pos=wx.DefaultPosition, size=wx.DefaultSize, style= wx.TE_MULTILINE | wx.TE_PROCESS_ENTER | wx.TE_RICH2, name=''):
		if len(label) > 0: self.AddStaticText(label=label)
		sName = name
		if len(sName) == 0: sName = 'RichEdit_' + FixName(label)
		iStyle = style
		if readonly: iStyle |= wxTE_READONLY
		aSize = size
		if aSize == wx.DefaultSize: aSize = (300, 300)
		rtb = wx.TextCtrl(parent=self, id=id, pos=pos, size=aSize, style=iStyle, name=sName)
		rtb.SetMaxLength(0)
		rtb.SetValue(value)
		self.Sizers[self.band].Add(rtb, 1, wx.ALIGN_LEFT | wx.ALIGN_TOP | wx.GROW)
		self.Sizers[self.band].Add(wx.Size(HORIZONTAL_RELATED_PAD, 1))
		self.Bind(wx.EVT_RADIOBUTTON, self.DefaultHandler, id=rtb.GetId())
		self.Controls[sName] = rtb
		return rtb
	# end def

	def AddStaticText(self, id=wx.ID_ANY, label='', pos=wx.DefaultPosition, size=wx.DefaultSize, style=DEFAULT_STYLE, name=''):
		sName = name
		if len(sName) == 0: sName = 'StaticText_' + FixName(label)
		sLabel = FixLabel(label)
		lbl = wx.StaticText(self, id=id, label=sLabel, pos=pos, size=size, style=style, name=sName)
		self.Sizers[self.band].Add(lbl, 0, wx.ALIGN_LEFT | wx.ALIGN_TOP)
		self.Sizers[self.band].Add(wx.Size(HORIZONTAL_LABEL_PAD, 1))
		self.Controls[sName] = lbl
		return lbl
	# end def
	
	def AddTextCtrl(self, id=wx.ID_ANY, label='', value='', pos=wx.DefaultPosition, size=wx.DefaultSize, style=DEFAULT_STYLE, name=''):
		if len(label) > 0: self.AddStaticText(label=label)
		sName = name
		if len(sName) == 0: sName = 'TextCtrl_' + FixName(label)
		iStyle = style
		if sName == 'TextCtrl_Password': iStyle |= wx.TE_PASSWORD
		aSize = size
		if aSize == wx.DefaultSize: aSize = (300, 21)
		txt = wx.TextCtrl(parent=self, id=id, pos=pos, size=aSize, style=iStyle, name=sName)
		txt.SetMaxLength(0)
		txt.SetValue(value)
		# sValue = unicode(value)
		# txt.SetValue(sValue)
		#txt.SetSize((2 * (txt.GetSize()[0]), txt.GetSize()[1]))
		# print txt.GetSize()
		self.Sizers[self.band].Add(txt, 1, wx.ALIGN_LEFT | wx.ALIGN_TOP)
		self.Sizers[self.band].Add(wx.Size(HORIZONTAL_RELATED_PAD, 1))
		self.Bind(wx.EVT_TEXT, self.DefaultHandler, id=txt.GetId())
		self.Bind(wx.EVT_TEXT_MAXLEN, self.DefaultHandler, id=txt.GetId())
		# self.Bind(wx.EVT_KEY_DOWN, self.DefaultHandler, id=txt.GetId())
		self.Controls[sName] = txt
		return txt
	# end def
	
	def DefaultHandler(self, event):
		# print 'event', str(event), 'id', event.GetId(), 'type', event.GetEventType()
		iEventID = event.GetId()
		iEventType = event.GetEventType()
		oWindow = event.GetEventObject()
		iID = oWindow.GetId()
		#print 'event', event, 'eventID', iEventID, 'eventType', iEventType, 'windowID', iID
		oParent = oWindow.GetParent()
		# for control in self.Controls.keys(): 
			# window = self.FindWindowByName(control)
		for control, window in self.Controls.items(): 
			try: result = window.GetValue()
			except:
				try: result = window.GetSelection()
				except: 
					try: result = window.GetLabel()
					except: 
						try: result = window.GetSelections()
						except: result = None
			self.Results[control] = result
		sName = event.GetEventObject().GetName()
		if self.ini and IsFocusEvent(event):
			sSection = self.GetTitle()
			sIni = self.ini
			sValue = win32api.GetProfileVal(sSection, sName, '', sIni)
			i = sValue.find(',')
			# if i >= 0: sValue = sValue[i + 1:].strip()
			# print sIni, sSection, sName, sValue
			self.SetStatus(sValue)

		if self.CustomHandler: return self.CustomHandler(self, event, sName)
		# self.Close()
		# if self.IsModal() and IsCloseEvent(event): self.EndModal(iID)
		if self.IsModal() and not IsFocusEvent(event) and sName.startswith('Button_'): self.EndModal(iID)
	# end def
	
	def Complete(self, buttons = ['OK', 'Cancel'], index=0, handler=None, statusbar=True, ini=GetIni(), idle=False):
		if len(buttons) > 0: self.AddButtonBand(buttons=buttons, index=index, handler=handler)
		else: self.CustomHandler = handler

		# self.Bind(wx.EVT_INIT_DIALOG, Activator)
		self.Bind(wx.EVT_INIT_DIALOG, self.DefaultHandler)
		self.Bind(wx.EVT_SHOW, self.DefaultHandler)
		self.Bind(wx.EVT_MENU, self.DefaultHandler)
		self.Bind(wx.EVT_CONTEXT_MENU, self.DefaultHandler)
		self.Bind(wx.EVT_CLOSE, self.DefaultHandler)
		# self.Bind(wx.EVT_CHAR, self.DefaultHandler)
		# self.Bind(wx.EVT_KEY_DOWN, self.DefaultHandler)
		# self.Bind(wx.EVT_SET_FOCUS, self.DefaultHandler)

		# at = wx.AcceleratorTable([(0, wx.WXK_ESCAPE, wx.ID_CANCEL)])
		# self.SetAcceleratorTable(at)
		# self.SetEscapeId(wx.ID_CANCEL)

		# self.Bind(wx.EVT_COMMAND_SET_FOCUS, self.DefaultHandler)
		self.Bind(wx.EVT_CHILD_FOCUS, self.DefaultHandler)
		if idle: self.Bind(wx.EVT_IDLE, self.DefaultHandler)
		# self.Bind(wx.EVT_CHAR, self.DefaultHandler)
		# self.Bind(wx.EVT_KEY_DOWN, self.DefaultHandler)

		self.ini = ini
		if statusbar:
			self.AddBand()
			self.AddStaticText(label='', name='StaticText_Status')

		self.Sizers[self.band].Add(wx.Size(HORIZONTAL_LABEL_PAD, 1))
		iFlags = wx.GROW | wx.ALIGN_CENTER
		iFlags = wx.ALIGN_RIGHT
		iFlags = wx.ALIGN_CENTER
		self.Sizers[0].Add(self.Sizers[self.band], 1, iFlags)
		self.Sizers[0].Add(wx.Size(1, VERTICAL_DIVIDER_PAD))
		self.SetSizerAndFit(self.Sizers[0])
		self.Center()
		iID = self.ShowModal()
		# iID = self.Show()
		# wx.GetApp().MainLoop()
		# self.Close()
		return iID
	# end def

	def SetStatus(self, text=''):
		sb = self.Controls['StaticText_Status']
		sb.SetLabel(text)
	def GetStatus(self):
		sb = self.Controls['StaticText_Status']
		return sb.GetLabel()

EVENT_DICT = GetEventDict()

