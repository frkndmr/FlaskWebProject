from flask import current_app,render_template,request, redirect, url_for
from model.floor import Floor
from model.source import Source
import base64
from PIL import Image
from io import BytesIO




def floor_index():
    myDB = current_app.config["dbconfig"]
    cursor = myDB.cursor()
    floor = []
    sources = []
    query = "SELECT F.Id, F.Name, F.Image, F.Buy, F.Sell, F.Color, F.Concept, F.Tag, S.Name from Floor as F join Source as S on F.SourceId = S.Id"
    cursor.execute(query)
    for id,name,image,buy,sell,color,concept,tag,source in cursor:
        src =BytesIO(image)
        img_byte = base64.b64encode(src.getvalue())
        floor.append(Floor(id,name,img_byte.decode("utf-8"),source,buy,sell,color,concept,tag))

    query2 = "Select * from Source Where(Id in (select distinct SourceId FROM Floor));"
    cursor.execute(query2)
    for id,name in cursor:
        sources.append(Source(id,name))

    return render_template("/floor/index.html",floor = floor,sources = sources)
 
def floor_update():
    myDB = current_app.config["dbconfig"]
    cursor = myDB.cursor()
    name = request.form["name"]
    color = request.form["color"]
    concept = request.form["concept"]
    tag = request.form["tag"]
    buy = request.form["buy"]
    sell = request.form["sell"]
    source = request.form["source"]
    id = request.form["num"]
    sql = "UPDATE Floor SET Name=%s, Buy=%s, Sell=%s, Color=%s, Concept=%s, Tag=%s, SourceId=%s WHERE Id=%s "
    val = (name,buy,sell,color,concept,tag,source,id)
    cursor.execute(sql,val)
    myDB.commit()
    return redirect(url_for("floor_index"))


def floor_delete():
    myDB = current_app.config["dbconfig"]
    cursor = myDB.cursor()
    id = request.form["num"]
    sql = "DELETE FROM Floor WHERE Id=%s "
    val = (id,)
    cursor.execute(sql,val)
    myDB.commit()
    return redirect(url_for("floor_index"))

def floor_create():
    myDB = current_app.config["dbconfig"]
    cursor = myDB.cursor()

    name = request.form["name"]
    color = request.form["color"]
    concept = request.form["concept"]
    tag = request.form["tag"]
    buy = request.form["buy"]
    sell = request.form["sell"]
    source = request.form["source"]
    image = request.files["img"]
    image.save("myimage.png")

    with open("myimage.png", 'rb') as file:
        binaryData = file.read()

    
    sql = "INSERT INTO Floor (Name, Image, SourceId, Buy, Sell, Color, Concept, Tag) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = (name, binaryData, source, buy, sell, color, concept, tag)
    cursor.execute(sql, val)
    myDB.commit()
    
    return redirect(url_for("floor_index"))
