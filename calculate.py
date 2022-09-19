import datetime
from io import BytesIO
from PIL import Image

def prename_transform(farmer_selected):
    ### Transform Str to Int for Radiobutton Index ###
    if farmer_selected == "นาย":
        prename_index = 0
    elif farmer_selected == "นาง":
        prename_index = 1
    elif farmer_selected == "นางสาว":
        prename_index = 2
    return prename_index

def timestamp():
    timenow = datetime.datetime.now()
    return timenow

def load_image(image_file):
    img = Image.open(image_file)
    fp = BytesIO()
    img.save(fp, "PNG")
    bytes_data = fp.getvalue()
    return bytes_data
