import datetime
def prename_transform(farmer_selected):
    ### Transform Str to Int for Radiobutton Index ###
    if farmer_selected[1] == "นาย":
        farmer_selected[1] = 0
    elif farmer_selected[1] == "นาง":
        farmer_selected[1] = 1
    elif farmer_selected[1] == "นางสาว":
        farmer_selected[1] = 2
    return farmer_selected

def timestamp():
    timenow = datetime.datetime.now()
    return timenow