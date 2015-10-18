Also available from the archive at
http://EmpowermentZone.com/pyLbc.zip

Layout by Code for Python
Version 1.5
October 18, 2015
Copyright 2009 - 2015 by Jamal Mazrui
GNU Lesser General Public License (LGPL)

I have updated a Python module called Layout by Code (lbc), which simplifies design of dialogs with the WxWidgets GUI library.  It is another implementation of the Layout by Code approach that I originally developed for the AutoIt language, available at
http://EmpowermentZone.com/lbc.zip

I also developed a version for .NET languages, such as C# and Visual Basic, which is distributed as part of HomerApp, the Homer Application Framework, available at
http://EmpowermentZone.com/appsetup.exe

Although the Python version is not as flexible, it is still intended to support most dialogs one might need (based on years of experience with various applications and languages).  It should work with Python versions 2.4 through 2.7.  It depends on the following 3rd-party Python modules:

wxPython (2.8 or 2.9)
http://wxpython.org

py2exe
http://py2exe.org

Python for Windows extensions
http://sourceforge.net/projects/pywin32/

odict -- an ordered dictionary
http://www.voidspace.org.uk/python/odict.html

The py2exe module is only needed if one wants to create a Windows executable like lbc_fruit.exe.  The batch file run_setup_lbc_fruit.bat does this, using setup_lbc_fruit.py to specify how the executable is built.

After instantiating an lbc dialog object, any of the following controls may be added with a line of code:  Button, CheckBox, ListBox, RadioButton, RichEdit, StaticText, or TextCtrl.  The control is added to a horizontal band of controls, with layout automatically managed by wxSizer containers.  Adding a new band is analagous to pressing carriage return at the end of a line.  

The lbc Complete method adds a band of buttons at the bottom of the dialog before invoking it.  The method returns the ID of the button that ended the dialog.  At that point, the dialog object has an ordered dictionary attribute called Controls, containing the names of controls that were added to the dialog before it was invoked.  A control name is its class and label, if any, seperated by an underscore, e.g., Button_OK.  The dialog also has a dictionary attribute called Results, containing the control names and values when the dialog ended.

By default, a status bar is added as the last control of a dialog.  It may be used for help messages to the user.  For example, each control can trigger a help message when it receives focus.  These messages may be defined in a .ini file that accompanies the main script file (with the same name except for the extension).  The section name in the ini file corresponds to the title of the dialog.  The fruit basket sample script illustrates this feature in the file lbc_fruit.ini.  A screen reader user can press a hotkey to read the status bar.

The Complete method invokes the dialog after final preparations.  A band of buttons may optionally be added with a parameter.  The index of the default button may be specified with another parameter.  If not specified, the left-most button, at index 0, is chosen.  To indicate no default button, pass None or -1 as the index.

Another parameter of the Complete method specifies a custom event handler function for processing events after the default event handler.  A custom handler is passed three parameters each time it is called, corresponding to the dialog object, event object, and name of the control associated with the event.  Common events for the supported controls are automatically passed.  These include EVT_BUTTON, EVT_CHECKBOX, EVT_LISTBOX, EVT_RADIOBUTTON, and EVT_TEXT.  The dialog-level events EVT_INIT_DIALOG, EVT_IDLE, and EVT_CLOSE are also passed.  The lbc.GetEventName function returns the name of an event as a string, without the EVT_ prefix.  A custom handler can check event types by comparing against these upper case strings.  Alternatively, it can use functions like lbc.IsButtonEvent, which do the same comparisons internally.  See lbc_fruit.py for an example.

Over ten convenience dialogs have been defined using lbc, illustrated with the program test_lbc.py (which may be run with the batch file run_test_lbc.bat).  Also, a fruit basket program is in lbc_fruit.py (which may be run with the batch file run_lbc_fruit.bat or with the executable lbc_fruit.exe).

Below is a summary of lbc functions.  For convenient reference, the code in test_lbc.py and then lbc_fruit.py follows afterward.

Jamal


----------

lbc convenience dialogs

DialogBrowseForFolder(title='', value='') -- Select a folder

DialogChoose(title='Choose', message = '', names=[]) -- Choose a button

DialogConfirm(title='Confirm', message='', value='Y') -- Choose from a Yes/No/Cancel message box

DialogInput(title='Input', label='', value='', ) -- Input with a single-line edit box

DialogMemo(title='Memo', label='', value='', readonly=False) -- Input or read text with a multiple-line edit box 

DialogMultiInput(title='MultiInput', labels=[], values=[], options=[]) -- Input with multiple edit boxes

DialogMultiPick(title='Multi Pick', message='', names=[], values=[], sort=False, index=0) -- Pick from a multiple-selection listbox

DialogOpenFile(title='Open', value='', wildcard='All files (*.*)|*.*') -- Specify a file to open

DialogPick(title='Pick', message='', names=[], values=[], sort=False, index=0) -- Pick from a single-selection listbox

DialogSaveFile(title='Save', value='', wildcard='All files (*.*)|*.*') -- Specify a file to save

DialogShow(title='Show', message='') -- Show a message

----------

Content of test_lbc.py

import lbc

labels = 'Label1 Label2 Label3'.split()
names = 'Name1 Name2 Name3'.split()
values = 'Value1 Value2 Value3'.split()

lbc.DialogShow(title='Introduction', message='This is a demo of several canned dialogs, invoked with single function calls.  Each prompts for input, then the result is shown.')

result = lbc.DialogChoose(title='Choose a Button', message='My message', names=['Button1', 'Button2', 'Button3'])
lbc.DialogShow(title='result', message=result)

result = lbc.DialogConfirm(title='Confirm an Action', message='my question', value='Y')
lbc.DialogShow(title='result', message=result)

result=lbc.DialogInput(title='Input a Value', label='My Label', value='My Value')
lbc.DialogShow(title='result', message=result)

result = lbc.DialogMemo(title='Input Multiple Lines', label='', value='line1\nline2\nline3')
lbc.DialogShow(title='result', message=result)

result = lbc.DialogMultiInput(title='Input Multiple Values', labels=labels, values=values)
lbc.DialogShow(title='result', message=result)

result = lbc.DialogPick(title='Pick an Item', names=names, values=values, sort=True)
lbc.DialogShow(title='result', message=result)

result=lbc.DialogMultiPick(title='Pick Multiple Items', names=names, values=values)
lbc.DialogShow(title='result', message=result)

result = lbc.DialogOpenFile(value=r'c:\temp\test.txt')
lbc.DialogShow(title='result', message=result)

result = lbc.DialogSaveFile(value=r'c:\temp\test.txt')
lbc.DialogShow(title='result', message=result)

result = lbc.DialogBrowseForFolder(value=r'c:\temp')
lbc.DialogShow(title='result', message=result)

lbc.DialogShow(title='Demo is done!')
----------

Content of lbc_fruit.py

"""
Fruit basket program in Python with lbc
Public domain by Jamal Mazrui
"""

import wx, lbc

# Custom event handler
def OnEvent(dlg, event, name):
	if lbc.IsCloseEvent(event):
		if lbc.DialogConfirm(title='Confirm', message='Exit program?', value='Y') == 'Y': return event.Skip() 
		else: return event.Veto()

	txt = dlg.Controls['TextCtrl_Fruit']
	lst = dlg.Controls['ListBox_Basket']
	if not lbc.IsButtonEvent(event): pass
	elif name == 'Button_Add':
		fruit = txt.GetValue()
		if len(fruit) == 0: return lbc.DialogShow(title='Alert', message='No fruit to add!')
		lst.Append(fruit)
		index = lst.GetCount() - 1
		lst.SetSelection(index)
		txt.Clear()
	elif name == 'Button_Delete':
		index = lst.GetSelection()
		if index == -1: return lbc.DialogShow(title='Alert', message='No fruit to delete!')
		lst.Delete(index)
		if index == lst.GetCount(): index -= 1
		if index >= 0: lst.SetSelection(index)

# Main program
app = lbc.App()
dlg = lbc.Dialog(title='Fruit Basket')
dlg.AddTextCtrl(label='Fruit')
dlg.AddListBox(label='Basket')
dlg.Complete(buttons=['Add', 'Delete'], handler=OnEvent)
app.Exit()

