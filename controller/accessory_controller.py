from flask import current_app,render_template,request, redirect
from model.accessories import Accessory
from model.theme import Theme
from model.source import Source
import base64
from PIL import Image
from io import BytesIO

def accessory_index():
    myDB = current_app.config["dbconfig"]
    cursor = myDB.cursor()

    themes_all = []
    query = "SELECT Id, Name FROM Themes"
    cursor.execute(query)
    for id, name in cursor:
        themes_all.append(Theme(id, name))
    
    # sources related to dressup to make dropdown
    sources = []
    query = "SELECT Id, Name FROM Source WHERE Id IN (SELECT DISTINCT SourceId FROM Accessories)"
    cursor.execute(query)
    for id, name in cursor:
        sources.append(Source(id, name))

    query = """SELECT accessory.Id, accessory.Name, accessory.Image, accessory.Buy, accessory.Sell, accessory.Color, accessory.Stylish, source.Name 
                from ProjectDb.Accessories as accessory, ProjectDb.Source as source where (accessory.SourceId = source.Id)"""
    cursor.execute(query)
    accessories = cursor.fetchall()

    
    query = """SELECT AccessoriesId, ThemeId FROM ProjectDb.AccessoriesThemes"""
    cursor.execute(query)
    accessories_themes = cursor.fetchall()

    accessories2 = []
    for i in range(1, len(accessories)+1):
        my_accessory = accessories[i-1]

        id = my_accessory[0]
        name = my_accessory[1]
        image = my_accessory[2]
        src =BytesIO(image)
        img_byte = base64.b64encode(src.getvalue())
        buy = my_accessory[3]
        sell = my_accessory[4]
        color = my_accessory[5]
        stylish = my_accessory[6]
        source = my_accessory[7]
        
        themes_for_acc = [themes_all[x[1]-1].name for x in accessories_themes if x[0] == id]
        
        accessories2.append(Accessory(id,source,name,img_byte.decode("utf-8"),buy,sell,color,stylish, themes_for_acc))

    return render_template("/accessory/accessory_index.html", accessories = accessories2, sources=sources, themes1 = themes_all)

def accessory_delete():
    myDB = current_app.config["dbconfig"]
    cursor = myDB.cursor()
    id = request.form["num"]

    # remove relation rows from common table
    sql = "DELETE FROM AccessoriesThemes WHERE AccessoriesId=%s "
    val = (id,)
    cursor.execute(sql,val)
    
    sql = "DELETE FROM Accessories WHERE Id=%s "
    val = (id,)
    cursor.execute(sql,val)

    myDB.commit()
    return redirect("/accessory/accessory_index")

def accessory_create():
    myDB = current_app.config["dbconfig"]
    cursor = myDB.cursor()

    # attributes of the dressup
    name = request.form["name"]
    buy = request.form["buy"]
    sell = request.form["sell"]
    color = request.form["color"]
    stylish = request.form["stylish"]
    source = request.form["source"]
    image = request.files["img"]
    themes_box = request.form.getlist("themes-box")
    print("THEMES BOX : " , themes_box)
    image.save("myimage.png")

    with open("myimage.png", 'rb') as file:
        binaryData = file.read()

   
    sql = "INSERT INTO Accessories (Name, Buy, Sell, Color, Stylish, SourceId, Image) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (name, buy, sell, color, stylish, source, binaryData)
    cursor.execute(sql, val)
    myDB.commit()

    # get accessory id 
    sql = "SELECT Id, Name FROM Accessories WHERE (Name = %s AND Image = %s)"
    val = (name, binaryData)
    cursor.execute(sql, val)

    for id, name in cursor.fetchall():
        accid = id
    
    for i in range(len(themes_box)):
        themeid = themes_box[i]
        sql = "INSERT INTO AccessoriesThemes (AccessoriesId, ThemeId) VALUES (%s, %s)"
        val = (accid, themeid)
        cursor.execute(sql, val)
        myDB.commit()
    
    return redirect("/accessory/accessory_index")

def accessory_update():
    myDB = current_app.config["dbconfig"]
    cursor = myDB.cursor()

    # attributes of the dressup
    name = request.form["name"]
    buy = request.form["buy"]
    sell = request.form["sell"]
    color = request.form["color"]
    stylish = request.form["stylish"]
    source = request.form["source"]
    id = request.form["num"]
    themes_box = request.form.getlist("themes-box")

    #Name, Image, Buy, Sell, Color, Stylish, Shape
    sql = "UPDATE Accessories SET Name=%s, Buy=%s, Sell=%s, Color=%s, Stylish=%s, SourceId=%s WHERE Id=%s "
    val = (name, buy, sell, color, stylish, source, id)
    cursor.execute(sql,val)
    myDB.commit()


    themes_all = []
    query = "SELECT Id, Name FROM Themes"
    cursor.execute(query)

    for id2, name in cursor:
        themes_all.append(Theme(id2, name))

    sql = "SELECT * FROM AccessoriesThemes where AccessoriesId=%s"
    val = (id,)
    cursor.execute(sql, val)

    sonuc = cursor.fetchall()
    themes_already_exist = [themes_all[int(row[2])-1].id for row in sonuc]

    for theme in themes_already_exist:
        if (str(theme) in themes_box): # eger eski olan yeni olanda da varsa o rowla isimiz yok devam
            themes_box.remove(str(theme))
            continue
        else: # eski olan yenide yoksa bu iliski kalkacak
            sql = "DELETE FROM AccessoriesThemes WHERE ((AccessoriesId = %s) and (ThemeId = %s)) "
            val = (id, theme)
            cursor.execute(sql,val)
            myDB.commit()
    
    # kalan yeniler de eklenecek
    for new_theme in themes_box:
        sql = "INSERT INTO AccessoriesThemes (AccessoriesId, ThemeId) VALUES (%s, %s)"
        val = (id, new_theme)
        cursor.execute(sql,val)
        myDB.commit()

    return redirect("/accessory/accessory_index")