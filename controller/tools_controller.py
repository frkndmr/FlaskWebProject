from flask import current_app,render_template,request, redirect
from model.tools import Tools
from model.source import Source
import base64
from PIL import Image
from io import BytesIO




def tools_index():
    myDB = current_app.config["dbconfig"]
    cursor = myDB.cursor()
    tools = []
    sources = []
    query = "SELECT T.Id, T.Name, T.Image, T.Buy, T.Sell, T.Color, S.Name FROM Tools T join Source S on T.SourceId = S.Id"
    cursor.execute(query)
    for id,name,image,buy,sell,color,sour in cursor:
        src =BytesIO(image)
        img_byte = base64.b64encode(src.getvalue())
        tools.append(Tools(id,sour,name,img_byte.decode("utf-8"),buy,sell,color))
    
    query2 = "SELECT Id, Name FROM Source"
    cursor.execute(query2)
    for id,name in cursor:
        sources.append(Source(id,name))

      
    return render_template("/tools/index.html",tools = tools, sources=sources)
 
def tools_update():
    myDB = current_app.config["dbconfig"]
    cursor = myDB.cursor()
    n = request.form["name"]
    g = request.form["buy"]
    f = request.form["sell"]
    p = request.form["source"]
    s = request.form["color"]
    id = request.form["num"]
    print(n,g,f,p,s,id)
    sql = "UPDATE Tools SET Name=%s, Buy=%s, Sell=%s, SourceId=%s, Color=%s WHERE Id=%s "
    val = (n,g,f,p,s,id)
    cursor.execute(sql,val)
    myDB.commit()
    return redirect("/tools/tools_index")


def tools_delete():
    myDB = current_app.config["dbconfig"]
    cursor = myDB.cursor()
    id = request.form["num"]
    sql = "DELETE FROM Tools WHERE Id=%s "
    val = (id,)
    cursor.execute(sql,val)
    myDB.commit()
    return redirect("/tools/tools_index")


def tools_create():
    myDB = current_app.config["dbconfig"]
    cursor = myDB.cursor()

    name = request.form["name"]
    buy = request.form["buy"]
    sell = request.form["sell"]
    color = request.form["color"]
    source = request.form["source"]
    image = request.files["img"]
    image.save("myimage.png")

    with open("myimage.png", 'rb') as file:
        binaryData = file.read()

    
    sql = "INSERT INTO Tools (Name, Buy, Sell, Color, SourceId, Image) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (name, buy, sell, color, source, binaryData)
    cursor.execute(sql, val)
    myDB.commit()


    
    return redirect("/tools/tools_index")