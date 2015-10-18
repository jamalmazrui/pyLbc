"""
Fruit basket program in Python with lbc
Public domain by Jamal Mazrui
June 20, 2011
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

