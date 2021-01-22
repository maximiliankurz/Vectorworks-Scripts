"""
divide_line_by_length.py
Sometimes you don't want to divide a line by the number of parts, but by length. 
This is what this script does, you can choose wheter you'd like to divide evenly with the rounded number or precise with a rest. 
Includes a simple user dialog from relume (https://forum.vectorworks.net/index.php?/topic/68801-python-dialog-box/)
Author: Maximilian Kurz
Date: 12/01/2021
License: MIT
"""

import vs

script_title = "Divide Line By Length"
div_length = 2.2
even_divide = True

# dialog funtion
def dialog_input_simple(vDialog_Titel = '', vDialog_Text = '', vDialog_Text_help = '', vDialog_Text_input = ''):

	cCancelButton = 2
	cOKButton = 1
	cSetupDialog = 12255


	def setup(vDialog_Titel, vDialog_Text, vDialog_Text_help, vDialog_Text_input):
	
		vDialog_ID = vs.CreateLayout(vDialog_Titel,1,'OK','Cancel')
		vs.CreateStaticText(vDialog_ID,100,vDialog_Text,-1)
		vs.CreateEditText(vDialog_ID,300,vDialog_Text_input,40)
		vs.CreateCheckBox(vDialog_ID, 400, 'Even Divide')

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

def normalized_vector(vector, length):
	return (vector[0]/length, vector[1]/length)
	
def move_point(point, vector):
	return (point[0]+vector[0], point[1]+vector[1])
		
def vector_from_line(line):
	b_box = vs.GetBBox(line)
	start = vs.Get2DPt(line, 1)
	end = vs.Get2DPt(line, 2)
	return (end[0]-start[0], end[1]-start[1])
	

# Main
# handle to first selcted object
line = vs.FSActLayer()

# nothing selected
if not line:
	vs.AlertInform(script_title, "Please select a line.", False)
	
else:
	# get division length and if divide should be even
	input = dialog_input_simple(vDialog_Titel = script_title, vDialog_Text = "Length to divide curve with", vDialog_Text_input = "eg 3.2")
	try:	
		div_length = float(input[1])
	except:
		vs.AlertInform(script_title, "Please insert a valid number", False)
	
	# set if divide should be even
	even_divide = vDialog_CheckBox_input
	
	# length of line
	line_length = vs.HLength(line)

	#divisions = round(line_length/div_length)
	
	#vs.AlertInform("Line Start Point", str(vs.Get2DPt(line, 1)), False)
	#vs.AlertInform("Line End Point", str(vs.Get2DPt(line, 2)), False)
	
	# end points
	start_point = vs.Get2DPt(line, 1)
	#point_on_line(line, 0)
	end_point = vs.Get2DPt(line, 2)
	#point_on_line(line, 1)
	line_vector = vector_from_line(line)

	div_point = start_point

	if even_divide:
		divisions = round(line_length/div_length)
		div_vector = (line_vector[0]/divisions, line_vector[1]/divisions)
	
		for i in range(divisions+1):
			# place locus at calculated point
			vs.Locus(div_point)
			# calculate next point
			div_point = move_point(div_point, div_vector)
		
	else:
		divisions = int(line_length/div_length)
		n_vec = normalized_vector(line_vector, line_length)
		div_vector = (n_vec[0]*div_length, n_vec[1]*div_length)
	
		for i in range(divisions+1):
			# place locus at calculated point
			vs.Locus(div_point)
			# calculate next point
			div_point = move_point(div_point, div_vector)
