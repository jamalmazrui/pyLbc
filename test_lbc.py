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
