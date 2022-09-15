import datetime
from io import BytesIO
from PIL import Image

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

def load_image(image_file):
    img = Image.open(image_file)
    fp = BytesIO()
    img.save(fp, "PNG")
    bytes_data = fp.getvalue()
    return bytes_data