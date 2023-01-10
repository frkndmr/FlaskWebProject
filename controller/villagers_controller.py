from flask import current_app,render_template,request, redirect
from model.villagers import Villagers
from model.style import Style
from model.hobby import Hobby
import base64
from PIL import Image
from io import BytesIO




def index():
    myDB = current_app.config["dbconfig"]
    cursor = myDB.cursor()
    villagers = []
    styles = []
    hobbies = []
    query = "SELECT V.Id, V.Name, V.Image, V.Gender, V.FavoriteSong, V.Personality, S.Name, H.Name from Villagers as V join Style as S on V.Style_id = S.Id join Hobby H on V.Hobby_id = H.Id"
    cursor.execute(query)
    for id,name,image,gender,f_song,personality,style,hobby in cursor:
        src =BytesIO(image)
        img_byte = base64.b64encode(src.getvalue())
        villagers.append(Villagers(id,name,img_byte.decode("utf-8"),gender,f_song,personality,style,hobby))
    
    query2 = "SELECT Id, Name FROM Style"
    cursor.execute(query2)
    for id,name in cursor:
        styles.append(Style(id,name))

    query3 = "SELECT Id, Name FROM Hobby"
    cursor.execute(query3)
    for id,name in cursor:
        hobbies.append(Hobby(id,name))       
    return render_template("/villagers/index.html",villagers = villagers, styles = styles, hob = hobbies)
 
def update():
    myDB = current_app.config["dbconfig"]
    cursor = myDB.cursor()
    n = request.form["name"]
    g = request.form["gender"]
    f = request.form["fsong"]
    p = request.form["personality"]
    s = request.form["style"]
    h = request.form["hobby"]
    id = request.form["num"]
    sql = "UPDATE Villagers SET Name=%s, Gender=%s, FavoriteSong=%s, Personality=%s, Style_id=%s, Hobby_id=%s WHERE Id=%s "
    val = (n,g,f,p,s,h,id)
    cursor.execute(sql,val)
    myDB.commit()
    return redirect("/villagers/index")


def delete():
    myDB = current_app.config["dbconfig"]
    cursor = myDB.cursor()
    id = request.form["num"]
    sql = "DELETE FROM Villagers WHERE Id=%s "
    val = (id,)
    cursor.execute(sql,val)
    myDB.commit()
    return redirect("/villagers/index")


def villagers_create():
    myDB = current_app.config["dbconfig"]
    cursor = myDB.cursor()

    # attributes of the dressup
    name = request.form["name"]
    gender = request.form["gender"]
    fsong = request.form["fsong"]
    personality = request.form["personality"]
    style = request.form["style"]
    hobby = request.form["hobby"]
    image = request.files["img"]
    image.save("myimage.png")

    with open("myimage.png", 'rb') as file:
        binaryData = file.read()

    
    sql = "INSERT INTO Villagers (Name, Gender, FavoriteSong, Personality, Style_id, Hobby_id, Image) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (name, gender, fsong, personality, style, hobby, binaryData)
    cursor.execute(sql, val)
    myDB.commit()
    
    return redirect("/villagers/index")