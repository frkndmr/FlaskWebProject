from flask import current_app,render_template,request, redirect
from model.dressup import Dressup
from model.source import Source
import base64
from PIL import Image
from io import BytesIO
from werkzeug.utils import secure_filename

def dressup_index():
    myDB = current_app.config["dbconfig"]
    cursor = myDB.cursor()
    
    # query for dressup
    dressup = []
    query = "SELECT dress.Id, dress.Name, dress.Image, dress.Buy, dress.Sell, dress.Color, dress.Stylish, dress.Shape, source.Name from DressUp as dress join Source as source on dress.SourceId = source.Id"
    cursor.execute(query)
    for id,name,image,buy,sell,color,stylish,shape,source in cursor:
        src =BytesIO(image)
        img_byte = base64.b64encode(src.getvalue())
        dressup.append(Dressup(id,source,name,img_byte.decode("utf-8"),buy,sell,color,stylish,shape))
        if (id == 5):
            print("IMAGEEEEEEEE: ", type(image))

    # sources related to dressup to make dropdown
    sources = []
    query = "SELECT Id, Name FROM Source WHERE Id IN (SELECT DISTINCT SourceId FROM DressUp)"
    cursor.execute(query)
    for id, name in cursor:
        sources.append(Source(id, name))

    return render_template("/dressup/dressup_index.html", dressup = dressup, sources = sources)
 
def dressup_update():
    myDB = current_app.config["dbconfig"]
    cursor = myDB.cursor()

    # attributes of the dressup
    name = request.form["name"]
    buy = request.form["buy"]
    sell = request.form["sell"]
    color = request.form["color"]
    stylish = request.form["stylish"]
    shape = request.form["shape"]
    source = request.form["source"]
    id = request.form["num"]

    #Name, Image, Buy, Sell, Color, Stylish, Shape
    sql = "UPDATE DressUp SET Name=%s, Buy=%s, Sell=%s, Color=%s, Stylish=%s, Shape=%s, SourceId=%s WHERE Id=%s "
    val = (name, buy, sell, color, stylish, shape, source, id)
    cursor.execute(sql,val)
    myDB.commit()
    return redirect("/dressup/dressup_index")

def dressup_delete():
    myDB = current_app.config["dbconfig"]
    cursor = myDB.cursor()
    id = request.form["num"]
    
    sql = "DELETE FROM DressUp WHERE Id=%s "
    val = (id,)
    cursor.execute(sql, val)
    myDB.commit()
    return redirect("/dressup/dressup_index")

def dressup_create():
    myDB = current_app.config["dbconfig"]
    cursor = myDB.cursor()

    # attributes of the dressup
    name = request.form["name"]
    buy = request.form["buy"]
    sell = request.form["sell"]
    color = request.form["color"]
    stylish = request.form["stylish"]
    shape = request.form["shape"]
    source = request.form["source"]
    image = request.files["img"]
    image.save("myimage.png")

    with open("myimage.png", 'rb') as file:
        binaryData = file.read()

    
    sql = "INSERT INTO DressUp (Name, Buy, Sell, Color, Stylish, Shape, SourceId, Image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = (name, buy, sell, color, stylish, shape, source, binaryData)
    cursor.execute(sql, val)
    myDB.commit()
    
    return redirect("/dressup/dressup_index")
