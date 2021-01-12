"""
rename_classes.py
A simple script that renames multiple classes or parts of classes. This is useful as you can rename just one class at a time in VW. 
Besides the renaming functionality the script includes a simple user dialog from relume (https://forum.vectorworks.net/index.php?/topic/68801-python-dialog-box/)
Author: Maximilian Kurz
Date: 12/01/2021
License: MIT
"""

import vs

# dialog
def dialog_input_simple(vDialog_Titel = '', vDialog_Text = '', vDialog_Text_help = '', vDialog_Text_input_find = '', vDialog_Text_input_replace = ''):

	cCancelButton = 2
	cOKButton = 1
	cSetupDialog = 12255


	def setup(vDialog_Titel, vDialog_Text, vDialog_Text_help, vDialog_Text_input_find, vDialog_Text_input_replace):
	
		vDialog_ID = vs.CreateLayout(vDialog_Titel,1,'OK','Cancel')
		vs.CreateStaticText(vDialog_ID,100,vDialog_Text,-1)
		vs.CreateEditText(vDialog_ID,300,vDialog_Text_input_find,40)
		vs.CreateEditText(vDialog_ID,400,vDialog_Text_input_replace,40)

		vs.SetFirstLayoutItem(vDialog_ID, 100)
		vs.SetBelowItem (vDialog_ID,100,300,0,0)
		vs.SetBelowItem (vDialog_ID,300,400,0,0)

		vs.SetHelpText(vDialog_ID, 300,vDialog_Text_help)

		return (vDialog_ID)
		
		
	def control(vDialog_Item, vDialog_Data):
	
		# do not write any code here, as it is executed on every event cycle, even after the ok-event
		nonlocal vDialog_Text_input_find
		nonlocal vDialog_Text_input_replace

		if vDialog_Item == cSetupDialog:
			vDialog_Text_input_find = ''
			vDialog_Text_input_replace = ''
		elif vDialog_Item == cCancelButton:
			pass # pass statement is a null operation
		elif vDialog_Item == cOKButton:
			vDialog_Text_input_find = vs.GetItemText(vDialog_ID, 300)
			vDialog_Text_input_replace = vs.GetItemText(vDialog_ID, 400)
			
			
		return (vDialog_Item)
	
	vDialog_ID = setup(vDialog_Titel, vDialog_Text, vDialog_Text_help, vDialog_Text_input_find, vDialog_Text_input_replace)
	vDialog_Result = vs.RunLayoutDialog(vDialog_ID, control)

	return (vDialog_Result, vDialog_Text_input_find, vDialog_Text_input_replace)
	
# Main

# get text to find and to replace with dialog
input = dialog_input_simple(vDialog_Titel = 'Rename Classes', vDialog_Text = 'Find Class Names (or a part of it) and replace them', vDialog_Text_input_find = 'find...', vDialog_Text_input_replace = 'replace with...')

# get count of classes
classes_total = vs.ClassNum()
classNameList = []

# append class names to list
for x in range(classes_total):
	classNameList.append(vs.ClassList(x + 1))

rename_count = 0

# replace str in the class names
for a in classNameList:
	vs.RenameClass(a, a.replace(input[1], input[2],))
	if input[1] in a:
		rename_count += 1
		
# display number of renamed Classes
vs.AlertInform('Rename Classes', 'Renamed ' + str(rename_count) + ' Classes.', False)
	
