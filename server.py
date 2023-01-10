from flask import Flask
from controller import villagers_controller,home_controller, dressup_controller, wallpaper_controller, tools_controller, randomize_controller, accessory_controller,floor_controller
import mysql.connector
from database import Database


def createApp():
    app = Flask(__name__)
    app.add_url_rule("/", view_func=home_controller.home_index)

    app.add_url_rule("/villagers/index", view_func=villagers_controller.index, methods=["GET", "POST"])
    app.add_url_rule("/villagers/update", view_func=villagers_controller.update, methods=["POST"])
    app.add_url_rule("/villagers/delete", view_func=villagers_controller.delete, methods=["POST"])
    app.add_url_rule("/villagers/villagers_create", view_func=villagers_controller.villagers_create, methods=["POST"])

    # dress up url
    app.add_url_rule("/dressup/dressup_index", view_func=dressup_controller.dressup_index, methods=["GET", "POST"])
    app.add_url_rule("/dressup/dressup_update", view_func=dressup_controller.dressup_update, methods=["POST"])
    app.add_url_rule("/dressup/dressup_delete", view_func=dressup_controller.dressup_delete, methods=["POST"])
    app.add_url_rule("/dressup/dressup_create", view_func=dressup_controller.dressup_create, methods=["POST"])

    # accessories url
    app.add_url_rule("/accessory/accessory_index", view_func=accessory_controller.accessory_index, methods=["GET", "POST"])
    app.add_url_rule("/accessory/accessory_update", view_func=accessory_controller.accessory_update, methods=["POST"])
    app.add_url_rule("/accessory/accessory_delete", view_func=accessory_controller.accessory_delete, methods=["POST"])
    app.add_url_rule("/accessory/accessory_create", view_func=accessory_controller.accessory_create, methods=["POST"])

    app.add_url_rule("/wallpaper/wallpaper_index", view_func=wallpaper_controller.wallpaper_index, methods=["GET", "POST"])
    app.add_url_rule("/wallpaper/wallpaper_update", view_func=wallpaper_controller.wallpaper_update, methods=["POST"])
    app.add_url_rule("/wallpaper/wallpaper_delete", view_func=wallpaper_controller.wallpaper_delete, methods=["POST"])
    app.add_url_rule("/wallpaper/wallpaper_create", view_func=wallpaper_controller.wallpaper_create, methods=["POST"])

    app.add_url_rule("/tools/tools_index", view_func=tools_controller.tools_index, methods=["GET", "POST"])
    app.add_url_rule("/tools/tools_update", view_func=tools_controller.tools_update, methods=["POST"])
    app.add_url_rule("/tools/tools_delete", view_func=tools_controller.tools_delete, methods=["POST"])
    app.add_url_rule("/tools/tools_create", view_func=tools_controller.tools_create, methods=["POST"])

    # randomize url
    app.add_url_rule("/randomize/randomize_index", view_func=randomize_controller.randomize_index, methods=["GET", "POST"])
    app.add_url_rule("/randomize/randomize_image", view_func=randomize_controller.randomize_image, methods=["POST"])

    app.add_url_rule("/floor/floor_index", view_func=floor_controller.floor_index, methods=["GET", "POST"])
    app.add_url_rule("/floor/floor_update", view_func=floor_controller.floor_update, methods=["POST"])
    app.add_url_rule("/floor/floor_delete", view_func=floor_controller.floor_delete, methods=["POST"])
    app.add_url_rule("/floor/floor_create", view_func=floor_controller.floor_create, methods=["POST"])


    mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="enessefa55",
                port = "8687",
                database="ProjectDb"
                )

    db = Database(mydb)
    

    app.config["dbconfig"] = db.mydb  
    return app

if __name__ == "__main__":
    app = createApp()
    app.run(host="0.0.0.0", port=8080, debug=True)