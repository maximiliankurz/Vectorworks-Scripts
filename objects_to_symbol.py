import vs


# dialog funtion
def dialog_input_simple(vDialog_Titel = '', vDialog_Text = '', vDialog_Text_help = '', vDialog_Text_input = ''):

	cCancelButton = 2
	cOKButton = 1
	cSetupDialog = 12255


	def setup(vDialog_Titel, vDialog_Text, vDialog_Text_help, vDialog_Text_input):
	
		vDialog_ID = vs.CreateLayout(vDialog_Titel,1,'OK','Cancel')
		vs.CreateStaticText(vDialog_ID,100,vDialog_Text,-1)
		vs.CreateEditText(vDialog_ID,300,vDialog_Text_input,40)
		vs.CreateCheckBox(vDialog_ID, 400, 'Delete Input')

		vs.SetFirstLayoutItem(vDialog_ID, 100)
		vs.SetBelowItem (vDialog_ID,100,300,0,0)
		vs.SetBelowItem (vDialog_ID,300,400,0,0)

		vs.SetHelpText(vDialog_ID, 300,vDialog_Text_help)

		return (vDialog_ID)
		
		
	def control(vDialog_Item, vDialog_Data):
	
		# do not write any code here, as it is executed on every event cycle, even after the ok-event
		nonlocal vDialog_Text_input
		global vDialog_CheckBox_input

		if vDialog_Item == cSetupDialog:
			vDialog_Text_input = ''
		elif vDialog_Item == cCancelButton:
			pass # pass statement is a null operation
		elif vDialog_Item == cOKButton:
			vDialog_Text_input = vs.GetItemText(vDialog_ID, 300)
			vDialog_CheckBox_input = vs.GetBooleanItem(vDialog_ID, 400)
			
		return (vDialog_Item)
	
	vDialog_ID = setup(vDialog_Titel, vDialog_Text, vDialog_Text_help, vDialog_Text_input)
	vDialog_Result = vs.RunLayoutDialog(vDialog_ID, control)

	return (vDialog_Result, vDialog_Text_input)

# calculate box dimensions
def box_dimensions(box):
	return (box[1][0] - box[0][0], box[0][1] - box[1][1])
	
# calculate box center
def box_center(box):
	return (box[0][0] + ((box[1][0] - box[0][0]) / 2), box[1][1] + ((box[0][1] - box[1][1]) / 2))


# Main
#title of script
script_title = 'Objects to Symbols'

# returns handle to first selected object on active layer
group = vs.FSActLayer()
# count number of selected objects
num = vs.NumSelectedObjects()

# get a symbol name via dialog
symbol_name = dialog_input_simple(vDialog_Titel = script_title, vDialog_Text = 'Please name a symbol.', vDialog_Text_input = 'Symbol Name')[1]
# set active symbol by name
vs.SetActSymbol(symbol_name)
# handle to active symbol
symbol = vs.ActSymDef()

if symbol_name !=  vs.GetSDName(symbol):
	vs.AlertCritical(script_title, 'Invalid Symbol selected.')
else:
	# check if objects are selected
	if not num > 0:
		vs.AlertCritical(script_title, 'No Objects selected. Please select some something.')
	else:
		center_list = []
		dim_list = []

		# iterate over selected groups
		for x in range(num):
			# returns bounding box of active object
			box = vs.GetBBox(group)
			# calculated center of group
			center = box_center(box)
			# calculate size of group
			dim_group = box_dimensions(box)
	
			center_list.append(center)
			dim_list.append(dim_group)
	
			#handle to next group
			group = vs.NextSObj(group)
	
		# if delete group button is selected, delete groups:
		if vDialog_CheckBox_input:
			# delete selected groups
			vs.DeleteObjs()
		else:
			vs.DSelectAll()

		# calculate symbol dimensions
		# bounding box points of symbol
		box_symbol = vs.GetBBox(symbol)
		#calculate dimensions of symbol
		dim_symbol = box_dimensions(box_symbol)
	
		for p in center_list:
			# place symbol at center point with rotation 0
			vs.Symbol(symbol_name, p[0], p[1], 0)

		act_symbol = vs.FSActLayer()
	
		for d in dim_list:
			# set scale factor of inserted symbols to a fraction of its dimension and the symbols size
			vs.SetObjectVariableReal(act_symbol, 102, d[0]/dim_symbol[0])
			vs.SetObjectVariableReal(act_symbol, 103, d[1]/dim_symbol[1])

			act_symbol = vs.NextSObj(act_symbol)

		vs.AlertInform(script_title, str(len(dim_list)) + ' symbols placed. Please select scaling if desired.', False)