from flask import current_app,render_template,request, redirect, url_for
from model.wallpaper import Wallpaper
from model.source import Source
from model.type import Type
import base64
from PIL import Image
from io import BytesIO




def wallpaper_index():
    myDB = current_app.config["dbconfig"]
    cursor = myDB.cursor()
    wallpaper = []
    sources = []
    types = []

    query = "SELECT W.Id, W.Name, W.Image, W.Buy, W.Sell, W.Color, W.Concept, W.Type, W.Tag, S.Name from Wallpaper as W join Source as S on W.SourceId = S.Id"
    cursor.execute(query)
    for id,name,image,buy,sell,color,concept,type,tag,source in cursor:
        src =BytesIO(image)
        img_byte = base64.b64encode(src.getvalue())
        wallpaper.append(Wallpaper(id,name,img_byte.decode("utf-8"),source,buy,sell,color,concept,type,tag))

    query2 = "Select * from Source Where(Id in (select distinct SourceId FROM Wallpaper));"
    cursor.execute(query2)
    for id,name in cursor:
        sources.append(Source(id,name))

    query3 = "SELECT distinct type FROM Wallpaper"
    cursor.execute(query3)
    for type in cursor:
        print(type[0])
        types.append(Type(type[0]))

    return render_template("/wallpaper/index.html",wallpaper = wallpaper,sources = sources,types=types)
 
def wallpaper_update():
    myDB = current_app.config["dbconfig"]
    cursor = myDB.cursor()
    name = request.form["name"]
    color = request.form["color"]
    concept = request.form["concept"]
    type = request.form["type"]
    tag = request.form["tag"]
    buy = request.form["buy"]
    sell = request.form["sell"]
    source = request.form["source"]
    id = request.form["num"]
    sql = "UPDATE Wallpaper SET Name=%s, Buy=%s, Sell=%s, Color=%s, Concept=%s, Type=%s, Tag=%s, SourceId=%s WHERE Id=%s "
    val = (name,buy,sell,color,concept,type,tag,source,id)
    cursor.execute(sql,val)
    myDB.commit()
    return redirect(url_for("wallpaper_index"))


def wallpaper_delete():
    myDB = current_app.config["dbconfig"]
    cursor = myDB.cursor()
    id = request.form["num"]
    sql = "DELETE FROM Wallpaper WHERE Id=%s "
    val = (id,)
    cursor.execute(sql,val)
    myDB.commit()
    return redirect(url_for("wallpaper_index"))

def wallpaper_create():
    myDB = current_app.config["dbconfig"]
    cursor = myDB.cursor()

    name = request.form["name"]
    color = request.form["color"]
    concept = request.form["concept"]
    type = request.form["type"]
    tag = request.form["tag"]
    buy = request.form["buy"]
    sell = request.form["sell"]
    source = request.form["source"]
    image = request.files["img"]
    image.save("myimage.png")

    with open("myimage.png", 'rb') as file:
        binaryData = file.read()

    
    sql = "INSERT INTO Wallpaper (Name, Image, SourceId, Buy, Sell, Color, Concept, Type, Tag) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (name, binaryData, source, buy, sell, color, concept, type, tag)
    cursor.execute(sql, val)
    myDB.commit()
    
    return redirect(url_for("wallpaper_index"))
