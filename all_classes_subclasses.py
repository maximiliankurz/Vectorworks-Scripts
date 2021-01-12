"""
all_classes_subclasses.py
A subclass in VW is realised with a "-". This script ask for a prefix and uses it as a parent class for all classes in a VW file.
Besides the subclass functionality the script includes a simple user dialog from relume (https://forum.vectorworks.net/index.php?/topic/68801-python-dialog-box/)
Author: Maximilian Kurz
Date: 12/01/2021
License: MIT
"""


import vs

# dialog
def dialog_input_simple(vDialog_Titel = '', vDialog_Text = '', vDialog_Text_help = '', vDialog_Text_input = ''):

	cCancelButton = 2
	cOKButton = 1
	cSetupDialog = 12255


	def setup(vDialog_Titel, vDialog_Text, vDialog_Text_help, vDialog_Text_input):
	
		vDialog_ID = vs.CreateLayout(vDialog_Titel,1,'OK','Cancel')
		vs.CreateStaticText(vDialog_ID,100,vDialog_Text,-1)
		vs.CreateEditText(vDialog_ID,300,vDialog_Text_input,40)

		vs.SetFirstLayoutItem(vDialog_ID, 100)
		vs.SetBelowItem (vDialog_ID,100,300,0,0)

		vs.SetHelpText(vDialog_ID, 300,vDialog_Text_help)

		return (vDialog_ID)
		
		
	def control(vDialog_Item, vDialog_Data):
	
		# do not write any code here, as it is executed on every event cycle, even after the ok-event
		nonlocal vDialog_Text_input

		if vDialog_Item == cSetupDialog:
			vDialog_Text_input = ''
		elif vDialog_Item == cCancelButton:
			pass # pass statement is a null operation
		elif vDialog_Item == cOKButton:
			vDialog_Text_input = vs.GetItemText(vDialog_ID, 300)
			# vestB.messageA(vObject_ID)
			
		return (vDialog_Item)
	
	vDialog_ID = setup(vDialog_Titel, vDialog_Text, vDialog_Text_help, vDialog_Text_input)
	vDialog_Result = vs.RunLayoutDialog(vDialog_ID, control)

	return (vDialog_Result, vDialog_Text_input)
	
# Main	
# count classes	
classes_total = vs.ClassNum()

#append class names to list
classNameList = []
for x in range(classes_total):
	classNameList.append(vs.ClassList(x + 1))

# get new prefix with dialog
input = dialog_input_simple(vDialog_Titel = 'Add new Prefix to all class names', vDialog_Text = 'Do not use "-"', vDialog_Text_input = 'New Prefix')

# add '-' and change class names
if int(input[0]) == 1:
	prefix = input[1] + '-'
	for a in classNameList:
		vs.RenameClass(a,prefix + a)
