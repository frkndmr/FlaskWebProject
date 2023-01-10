from flask import current_app,render_template,request, redirect
from model.customize import Customize
import base64
from PIL import Image
from io import BytesIO
import random

initial = ['Jock', 'Gorgeous', 'Kimono', 'restaurant', 'Blue', 'bathroom']

def randomize_index():
    global initial
    print("INITIAL : ", initial)
    myDB = current_app.config["dbconfig"]
    cursor = myDB.cursor()
    name = []

    query = "SELECT Id FROM DressUp WHERE Shape=%s"
    val=(initial[2],)
    cursor.execute(query, val)

    shapes = [item[0] for item in cursor.fetchall()]
    rnum = random.randint(0, len(shapes)-1)
    random_dress_id = shapes[rnum]

    query = "SELECT Image FROM DressUp WHERE Id=%s"
    val=(random_dress_id,)
    cursor.execute(query,val)

    for image in cursor:
        #name.append(n[0])
        src =BytesIO(image[0])
        img_byte_d = base64.b64encode(src.getvalue())
        name.append(img_byte_d.decode("utf-8"))


    query = "SELECT Id FROM Accessories WHERE Stylish=%s"
    val=(initial[1],)
    cursor.execute(query, val)

    stylish_a = [item[0] for item in cursor.fetchall()]
    rnum = random.randint(0, len(stylish_a)-1)
    random_access_id = stylish_a[rnum]
    query = "SELECT Image FROM Accessories WHERE Id=%s"
    val=(random_access_id,)
    cursor.execute(query,val)

    for image in cursor:
        #name.append(n[0])
        src =BytesIO(image[0])
        img_byte_a = base64.b64encode(src.getvalue())
        name.append(img_byte_a.decode("utf-8"))


    # villagers 
    query = "SELECT Id FROM Villagers WHERE Personality=%s"
    val=(initial[0],)
    cursor.execute(query, val)

    person_v = [item[0] for item in cursor.fetchall()]
    rnum = random.randint(0, len(person_v)-1)
    random_villager_id = person_v[rnum]

    query = "SELECT Image FROM Villagers WHERE Id=%s"
    val=(random_villager_id,)
    cursor.execute(query,val)

    for image in cursor:
        #name.append(n[0])
        src =BytesIO(image[0])
        img_byte_v = base64.b64encode(src.getvalue())
        name.append(img_byte_v.decode("utf-8"))


    query = "SELECT Id FROM Tools WHERE Color=%s"
    val=(initial[4],)
    cursor.execute(query, val)

    color_tool = [item[0] for item in cursor.fetchall()]
    rnum = random.randint(0, len(color_tool)-1)
    random_tool_id = color_tool[rnum]

    query = "SELECT Image FROM Tools WHERE Id=%s"
    val=(random_tool_id,)
    cursor.execute(query,val)

    for image in cursor:
        #name.append(n[0])
        src =BytesIO(image[0])
        img_byte_t = base64.b64encode(src.getvalue())
        name.append(img_byte_t.decode("utf-8"))


    query = "SELECT Id FROM Wallpaper WHERE Concept=%s"
    val=(initial[3],)
    cursor.execute(query, val)

    wallpaper_concept = [item[0] for item in cursor.fetchall()]
    rnum = random.randint(0, len(wallpaper_concept)-1)
    random_tool_id = wallpaper_concept[rnum]
    query = "SELECT Image FROM Wallpaper WHERE Id=%s"
    val=(random_tool_id,)
    cursor.execute(query,val)

    for image in cursor:
        #name.append(n[0])
        src =BytesIO(image[0])
        img_byte_w = base64.b64encode(src.getvalue())
        name.append(img_byte_w.decode("utf-8"))


    query = "SELECT Id FROM Floor WHERE Concept=%s"
    val=(initial[5],)
    cursor.execute(query, val)

    floor_concept = [item[0] for item in cursor.fetchall()]
    rnum = random.randint(0, len(floor_concept)-1)
    random_floor_id = floor_concept[rnum]
    query = "SELECT Image FROM Floor WHERE Id=%s"
    val=(random_floor_id,)
    cursor.execute(query,val)

    for image in cursor:
        #name.append(n[0])
        src =BytesIO(image[0])
        img_byte_f = base64.b64encode(src.getvalue())
        name.append(img_byte_f.decode("utf-8"))
    
    

    print(len(name))

    customized = Customize(img_byte_v.decode('utf-8'), img_byte_a.decode('utf-8'), img_byte_d.decode('utf-8'),
                                             img_byte_w.decode('utf-8'), img_byte_t.decode('utf-8'), img_byte_f.decode('utf-8'))



    villager_colors = []
    query = "SELECT DISTINCT Personality FROM Villagers"
    cursor.execute(query)
    for color in cursor:
        villager_colors.append(color[0])

    accessory_style = []
    query = "SELECT DISTINCT Stylish FROM Accessories"
    cursor.execute(query)
    for a_style in cursor:
        accessory_style.append(a_style[0])

    dressup_shape = []
    query = "SELECT DISTINCT Shape FROM DressUp"
    cursor.execute(query)
    for shape in cursor:
        dressup_shape.append(shape[0])

    wallpaper_concept = []
    query = "SELECT DISTINCT Concept FROM Wallpaper"
    cursor.execute(query)
    for concept in cursor:
        wallpaper_concept.append(concept[0])

    tool_color = []
    query = "SELECT DISTINCT Color FROM Tools"
    cursor.execute(query)
    for color in cursor:
        tool_color.append(color[0])

    floor_concept = []
    query = "SELECT DISTINCT Concept FROM Floor"
    cursor.execute(query)
    for concept in cursor:
        floor_concept.append(concept[0])

    customs = []
    customs.append(customized)
    print("vicolors: ", villager_colors)
    print("dress ", dressup_shape)
    return render_template("/randomize/randomize_index.html", custom=customized, vicolors=villager_colors,
                            astyle=accessory_style, dshape=dressup_shape, wconcept=wallpaper_concept,
                            tcolor=tool_color, fconcept=floor_concept)

def randomize_image():
    global initial
    myDB = current_app.config["dbconfig"]
    cursor = myDB.cursor()

    if ("villager-color" in request.form):
        print("EVET")

    villager_color = request.form["villager-color"]
    accessory_style = request.form["accessory-style"]
    dressup_shape = request.form["dress-shape"]
    wallpaper_concept = request.form["wallpaper-concept"]
    tool_color = request.form["tool-color"]
    floor_concept = request.form["floor-concept"]
    print("SBFSHDJ")

    print(villager_color)
    print(accessory_style)
    print(dressup_shape)
    print(wallpaper_concept)
    print(tool_color)
    print(floor_concept)

    print("SBFJHGDFJ")
    initial = [villager_color, accessory_style, dressup_shape, wallpaper_concept, tool_color, floor_concept]

    myDB = current_app.config["dbconfig"]
    cursor = myDB.cursor()
    name = []

    query = "SELECT Id FROM DressUp WHERE Shape=%s"
    val=(initial[2],)
    cursor.execute(query, val)

    shapes = [item[0] for item in cursor.fetchall()]
    rnum = random.randint(0, len(shapes)-1)
    random_dress_id = shapes[rnum]

    query = "SELECT Image FROM DressUp WHERE Id=%s"
    val=(random_dress_id,)
    cursor.execute(query,val)

    for image in cursor:
        #name.append(n[0])
        src =BytesIO(image[0])
        img_byte_d = base64.b64encode(src.getvalue())
        name.append(img_byte_d.decode("utf-8"))


    query = "SELECT Id FROM Accessories WHERE Stylish=%s"
    val=(initial[1],)
    cursor.execute(query, val)

    stylish_a = [item[0] for item in cursor.fetchall()]
    rnum = random.randint(0, len(stylish_a)-1)
    random_access_id = stylish_a[rnum]
    query = "SELECT Image FROM Accessories WHERE Id=%s"
    val=(random_access_id,)
    cursor.execute(query,val)

    for image in cursor:
        #name.append(n[0])
        src =BytesIO(image[0])
        img_byte_a = base64.b64encode(src.getvalue())
        name.append(img_byte_a.decode("utf-8"))


    # villagers 
    query = "SELECT Id FROM Villagers WHERE Personality=%s"
    val=(initial[0],)
    cursor.execute(query, val)

    person_v = [item[0] for item in cursor.fetchall()]
    rnum = random.randint(0, len(person_v)-1)
    random_villager_id = person_v[rnum]

    query = "SELECT Image FROM Villagers WHERE Id=%s"
    val=(random_villager_id,)
    cursor.execute(query,val)

    for image in cursor:
        #name.append(n[0])
        src =BytesIO(image[0])
        img_byte_v = base64.b64encode(src.getvalue())
        name.append(img_byte_v.decode("utf-8"))


    query = "SELECT Id FROM Tools WHERE Color=%s"
    val=(initial[4],)
    cursor.execute(query, val)

    color_tool = [item[0] for item in cursor.fetchall()]
    rnum = random.randint(0, len(color_tool)-1)
    random_tool_id = color_tool[rnum]

    query = "SELECT Image FROM Tools WHERE Id=%s"
    val=(random_tool_id,)
    cursor.execute(query,val)

    for image in cursor:
        #name.append(n[0])
        src =BytesIO(image[0])
        img_byte_t = base64.b64encode(src.getvalue())
        name.append(img_byte_t.decode("utf-8"))


    query = "SELECT Id FROM Wallpaper WHERE Concept=%s"
    val=(initial[3],)
    cursor.execute(query, val)

    wallpaper_concept = [item[0] for item in cursor.fetchall()]
    rnum = random.randint(0, len(wallpaper_concept)-1)
    random_tool_id = wallpaper_concept[rnum]
    query = "SELECT Image FROM Wallpaper WHERE Id=%s"
    val=(random_tool_id,)
    cursor.execute(query,val)

    for image in cursor:
        #name.append(n[0])
        src =BytesIO(image[0])
        img_byte_w = base64.b64encode(src.getvalue())
        name.append(img_byte_w.decode("utf-8"))


    query = "SELECT Id FROM Floor WHERE Concept=%s"
    val=(initial[5],)
    cursor.execute(query, val)

    floor_concept = [item[0] for item in cursor.fetchall()]
    rnum = random.randint(0, len(floor_concept)-1)
    random_floor_id = floor_concept[rnum]
    query = "SELECT Image FROM Floor WHERE Id=%s"
    val=(random_floor_id,)
    cursor.execute(query,val)

    for image in cursor:
        #name.append(n[0])
        src =BytesIO(image[0])
        img_byte_f = base64.b64encode(src.getvalue())
        name.append(img_byte_f.decode("utf-8"))
    
    

    print(len(name))

    customized = Customize(img_byte_v.decode('utf-8'), img_byte_a.decode('utf-8'), img_byte_d.decode('utf-8'),
                                            img_byte_w.decode('utf-8'), img_byte_t.decode('utf-8'), img_byte_f.decode('utf-8'))



    
    return render_template("/randomize/random_3d.html", custom=customized)