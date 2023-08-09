from functions import *
from datetime import timedelta
import os



LogoSvg = read_file("./static/assets/main.svg")
likesvg = read_file("./static/assets/like.svg")
moon = read_file("./static/assets/moon.html")


app = Flask(__name__)
app.secret_key = 'very secure key'

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=1440)
def add_cache_headers(response):
    # Set cache control headers to prevent caching
    response.headers[
        "Cache-Control"
    ] = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "-1"
    return response


socketio = SocketIO(app)
# app.config["MYSQL_HOST"] = "localhost"
# app.config["MYSQL_USER"] = "root"
# app.config["MYSQL_PASSWORD"] = ""
# app.config["MYSQL_DB"] = "chatrtc"
# app.config["MYSQL_PORT"] = 3306


IST = pytz.timezone("Asia/Kolkata")
socketio = SocketIO(app)


# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('Hub.html'), 404



@app.route("/")
def index():
    return render_template("Home.html", svg_data=LogoSvg)


# Register the after_request function for all routes


@app.route("/Public")
def Public():
    return render_template("public.html", svg_data=LogoSvg, svg=likesvg)


@app.route("/Hub")
def Hub():
    return render_template("hub.html")


@app.route("/Hub/Login", methods=["POST", "GET"])
def LogIn():
    message = request.args.get("message")
    username1 = request.args.get("username")
    if message == None:
        message = ""
    else:
        message = request.args.get("message")

    if username1 == None:
        username1 = ""
    else:
        username1 = request.args.get("username")

    if request.method == "POST":
        username = request.form["UsernameAtLogin"]
        password = request.form["PasswordAtLogin"]
        op = isPasswordOkay(username, password)
        if op != False:
            
           

           
            session['authenticated'] = op[1]
            
            session['shit'] = "real"
            
            return redirect('/Home')


            headers = {
                'Authorization': f'Bearer {op}'
            }




            # response = requests.get('/Home', headers=headers)

            # decoded_payload = jwt.decode(op, "kousic", algorithms=["HS256"])
            # print(decoded_payload)

            # return render_template(
            #     "LogIn.html", moon=moon, error=op, username=username1
            # )
        else:
            return render_template(
                "LogIn.html",
                moon=moon,
                error="Incorrect Password or Username", 
                username=username1,
            )

    return render_template("LogIn.html", moon=moon, error=message, username=username1)


@app.route("/Hub/SignUp", methods=["POST", "GET"])
def SignUp():
    if request.method == "POST":
        username = request.form["Username"]
        password = request.form["Password"]
        passwordre = request.form["ConfrimPassword"]
        InpData = InputValidation(username, password, passwordre)
        if isinstance(InpData, list):
            if send_sign_up_data_to_db(InpData[0], InpData[1]) == 200:
                return redirect(
                    url_for(
                        "LogIn",
                        message="Now Please Login to your Account",
                        username=username,
                    )
                )
                # return render_template('SignUp.html', moon=moon, error="Success", Username=username, name="SignUp")
            else:
                return render_template(
                    "SignUp.html",
                    moon=moon,
                    error="Some error occured",
                    Username=username,
                    name="SignUp",
                )

        else:
            return render_template(
                "SignUp.html",
                moon=moon,
                error=InpData,
                Username=username,
                name="SignUp",
            )

    return render_template("SignUp.html", moon=moon)


@app.route("/test")
def test():
    return render_template("moon.html")


# ==============================From Here On The Real Magic Starts====================#Complicated shit#











@app.route("/Home", methods=[ "GET"])
@require_token
def Home():
        return render_template("AfterLoginHome.html")






    







































@app.route("/get/interests")
def get_interests():
    # Specify the path to your local JSON file
    json_file_path = "./json/interests.json"

    if os.path.exists(json_file_path):
        with open(json_file_path, "r") as json_file:
            interests_data = json.load(json_file)
    else:
        # Handle error when the file does not exist or cannot be read
        interests_data = {"interests": []}

    return jsonify(interests_data)


@app.route("/get/intropara")
def intropara():
    # Specify the path to your local JSON file
    json_file_path = "./json/intro.json"

    if os.path.exists(json_file_path):
        with open(json_file_path, "r") as json_file:
            intro_data = json.load(json_file)
    else:
        # Handle error when the file does not exist or cannot be read
        intro_data = {"description": []}

    return jsonify(intro_data)


@socketio.on("message")
def message(data):
    message_text = data["data"]

    datetime_now = datetime.now(IST)

    # Format the datetime as desired: date:monthname:year and 12-hr time format
    formatted_date = datetime_now.strftime("%d %B %Y")
    formatted_time = datetime_now.strftime("%I:%M %p")
    final_time = formatted_date + " - " + formatted_time
    content = {
        "message": message_text,
        "datetime": formatted_date + " - " + formatted_time,
    }
    print(content)
    socketio.emit("message", content)

    # with mysql.cursor() as cursor:
    #     cursor.execute("INSERT INTO messages (message, datetime) VALUES (%s, %s)", (message_text, final_time))
    #     mysql.commit()


# @app.route("/history")
# def get_chat_history():
#     with mysql.cursor() as cursor:
#         cursor.execute("SELECT message, datetime FROM messages ORDER BY id DESC LIMIT 100")
#         rows = cursor.fetchall()
#         print(jsonify({"messages": [{"message": row[0], "datetime": row[1]} for row in rows]}))
#     return jsonify({"messages": [{"message": row[0], "datetime": row[1]} for row in rows]})


app.after_request(add_cache_headers)
if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0")
