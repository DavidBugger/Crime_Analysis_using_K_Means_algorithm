import os
from flask import Flask, render_template, request, flash,redirect, url_for,session
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import sqlite3
import os
import random
import string
from flask import jsonify

# def create_table():
#     with sqlite3.connect("crime_data.db") as con:
#         cur = con.cursor()
#         cur.execute(
#             "CREATE TABLE IF NOT EXISTS crime_data (id INTEGER PRIMARY KEY AUTOINCREMENT, filename TEXT)"
#         )
#         con.commit()
# def create_table():
#     with sqlite3.connect("crime_data.db") as con:
#         cur = con.cursor()
#         cur.execute(
#             "CREATE TABLE IF NOT EXISTS crime_data (id INTEGER PRIMARY KEY AUTOINCREMENT, filename TEXT)"
#         )
#         con.commit()

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/photos'

# Connect to the SQLite database
conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()

# Create the users table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
''')
               
cursor.execute(
            "CREATE TABLE IF NOT EXISTS crime_data (id INTEGER PRIMARY KEY AUTOINCREMENT, filename TEXT)"
        )

cursor.execute('''
    CREATE TABLE IF NOT EXISTS register_members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        firstname TEXT NOT NULL,
        lastname TEXT NOT NULL,
        address TEXT NOT NULL,
        photo TEXT NOT NULL,
        gender TEXT NOT NULL,
        criminal_offence TEXT NOT NULL,
        status TEXT NOT NULL,
        nationality TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')

# Insert an initial admin user
username = 'admin'
password = 'admin'
role = 'admin'




# @app.route("/", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]
#         # Perform admin login authentication, e.g., check if username and password match
#         # (add your own validation logic here)
#         if username == "admin" and password == "admin_password":
#             return redirect(url_for("/upload"))
#         else:
#             return render_template("login.html", error="Invalid credentials")
#     return render_template("login.html", error=None)


    
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user[2], password):
            session['username'] = user[1]
            session['role'] = user[3]
            flash('Login successful!', 'success')
            return redirect('/dashboard')

        flash('Invalid username or password', 'error')

    return render_template('login.html')



# @app.route("/upload", methods=["GET", "POST"])
# def upload():
#     if request.method == "POST":
#         file = request.files["file"]
#         if file:
#             filename = file.filename
#             file.save(os.path.join("uploads", filename))
#             with sqlite3.connect("crime_data.db") as con:
#                 cur = con.cursor()
#                 cur.execute("INSERT INTO crime_data (filename) VALUES (?)", (filename,))
#                 con.commit()

#             # Return a JSON response indicating that the analysis is in progress
#             return jsonify({"status": "processing"})

#     return render_template("upload.html")
    

# @app.route("/analyze", methods=["GET"])
# def analyze():
#     filename = request.args.get("filename")
#     if not filename:
#         return "Filename not provided in the URL parameters.", 400

#     with sqlite3.connect("crime_data.db") as con:
#         cur = con.cursor()
#         cur.execute("SELECT filename FROM crime_data WHERE filename=?", (filename,))
#         result = cur.fetchone()

#     if result:
#         filepath = os.path.join("uploads", filename)

#         # Perform data analysis (you may need to adjust this depending on your dataset format)
#         data = pd.read_csv(filepath)
#         # Perform the necessary analysis to get the highest crime rate cities
#         highest_crime_cities = data["Year"].value_counts().nlargest(10)

#         # Create a plot using Matplotlib
#         plt.bar(highest_crime_cities.index, highest_crime_cities.values)
#         plt.xlabel("Population")
#         plt.ylabel("Murder")
#         plt.title("Top 10 Cities with the Highest Crime Rate")
#         plt.xticks(rotation=45)
#         plt.tight_layout()
#         graph_filename = f"static/crime_plot.png"
#         plt.savefig(graph_filename)
#         plt.close()

#         # Return a JSON response indicating that the analysis is done and provide the graph filename
#         return jsonify({"status": "done", "graph_filename": graph_filename})

#     # If the file does not exist in the database, show an error message or redirect to the upload page.
#     return "File not found in the database. Please upload the file first.", 404



@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            filename = file.filename
            file.save(os.path.join("uploads", filename))
            with sqlite3.connect("crime_data.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO crime_data (filename) VALUES (?)", (filename,))
                con.commit()

            # Return a JSON response indicating that the analysis is in progress
            return jsonify({"status": "processing"})

    return render_template("upload.html")
    

# @app.route("/analyze", methods=["GET"])
# def analyze():
#     filename = request.args.get("filename")
#     if not filename:
#         return "Filename not provided in the URL parameters.", 400

#     with sqlite3.connect("crime_data.db") as con:
#         cur = con.cursor()
#         cur.execute("SELECT filename FROM crime_data WHERE filename=?", (filename,))
#         result = cur.fetchone()

#     if result:
#         filepath = os.path.join("uploads", filename)

#         # Perform data analysis (you may need to adjust this depending on your dataset format)
#         data = pd.read_csv(filepath)
#         # Perform the necessary analysis to get the highest crime rate cities
#         highest_crime_cities = data["Year"].value_counts().nlargest(10)

#         # Create a scatter plot using Matplotlib
#         plt.scatter(highest_crime_cities.index, highest_crime_cities.values)
#         plt.xlabel("Year")
#         plt.ylabel("Crime Count")
#         plt.title("Top 10 Cities ")
#         plt.xticks(rotation=45)
#         plt.tight_layout()
#         graph_filename = f"static/crime_scatter_plot.png"
#         plt.savefig(graph_filename)
#         plt.close()

#         # Return a JSON response indicating that the analysis is done and provide the graph filename
#         return jsonify({"status": "done", "graph_filename": graph_filename})

#     # If the file does not exist in the database, show an error message or redirect to the upload page.
#     return "File not found in the database. Please upload the file first.", 404


@app.route("/analyze", methods=["GET"])
def analyze():
    filename = request.args.get("filename")
    if not filename:
        return "Filename not provided in the URL parameters.", 400

    with sqlite3.connect("crime_data.db") as con:
        cur = con.cursor()
        cur.execute("SELECT filename FROM crime_data WHERE filename=?", (filename,))
        result = cur.fetchone()

    if result:
        filepath = os.path.join("uploads", filename)

        # Perform data analysis (you may need to adjust this depending on your dataset format)
        data = pd.read_csv(filepath)

        # Extract relevant columns
        crime_data = data[["Year", "Population", "Murder", "Rape", "Robbery"]]

        # Calculate crime rates per 100,000 people
        crime_data["Murder Rate"] = crime_data["Murder"] / crime_data["Population"] * 100000
        crime_data["Rape Rate"] = crime_data["Rape"] / crime_data["Population"] * 100000
        crime_data["Robbery Rate"] = crime_data["Robbery"] / crime_data["Population"] * 100000

        # Identify trends in crime rates
        crime_trends = {}
        for col in ["Murder Rate", "Rape Rate", "Robbery Rate"]:
            trend = "Stable"
            if crime_data[col].diff().mean() > 0:
                trend = "Increasing"
            elif crime_data[col].diff().mean() < 0:
                trend = "Decreasing"
            crime_trends[col] = trend

        # Create a scatter plot using Matplotlib
        plt.scatter(crime_data["Year"], crime_data["Murder Rate"], label="Murder Rate")
        plt.scatter(crime_data["Year"], crime_data["Rape Rate"], label="Rape Rate")
        plt.scatter(crime_data["Year"], crime_data["Robbery Rate"], label="Robbery Rate")
        plt.xlabel("Year")
        plt.ylabel("Crime Rate per 100,000 People")
        plt.title("Crime Rates Trend")
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        graph_filename = f"static/crime_scatter_plot.png"
        plt.savefig(graph_filename)
        plt.close()

        # Return a JSON response indicating that the analysis is done and provide the graph filename
        return jsonify({"status": "done", "graph_filename": graph_filename, "crime_trends": crime_trends})

    # If the file does not exist in the database, show an error message or redirect to the upload page.
    return "File not found in the database. Please upload the file first.", 404




# @app.route("/upload", methods=["GET", "POST"])
# def upload():
#     if request.method == "POST":
#         file = request.files["file"]
#         if file:
#             filename = file.filename
#             file.save(os.path.join("uploads", filename))
#             with sqlite3.connect("crime_data.db") as con:
#                 cur = con.cursor()
#                 cur.execute("INSERT INTO crime_data (filename) VALUES (?)", (filename,))
#                 con.commit()
#             return redirect(url_for("analyze"))
#     return render_template("upload.html")




# @app.route("/upload", methods=["GET", "POST"])
# def upload():
#     if request.method == "POST":
#         file = request.files["file"]
#         if file:
#             filename = file.filename
#             file.save(os.path.join("uploads", filename))
#             with sqlite3.connect("crime_data.db") as con:
#                 cur = con.cursor()
#                 cur.execute("INSERT INTO crime_data (filename) VALUES (?)", (filename,))
#                 con.commit()

#             # Analyze the crime data and generate the scatter graph
#             data = pd.read_csv(os.path.join("uploads", filename))
#             plt.scatter(data["Population"], data["Murder"])  # Replace "x_column" and "y_column" with the actual column names in your dataset
#             plt.xlabel("X Label")  # Replace with the appropriate X-axis label
#             plt.ylabel("Y Label")  # Replace with the appropriate Y-axis label
#             plt.title("Crime Data Scatter Plot")  # Replace with the appropriate plot title
#             graph_filename = f"uploads/{filename.split('.')[0]}.png"
#             plt.savefig(graph_filename)
#             plt.close()

#             return redirect(url_for("analyze", graph_filename=graph_filename))

#     return render_template("upload.html")



# @app.route("/analyze", methods=["GET"])
# def analyze():
#      filename = request.args.get("filename")
#     if not filename:
#         return "Filename not provided in the URL parameters.", 400
#     with sqlite3.connect("crime_data.db") as con:
#         cur = con.cursor()
#         cur.execute("SELECT filename FROM crime_data WHERE filename=?", (filename,))
#         result = cur.fetchone()

#     if result:
#         filepath = os.path.join("uploads", filename)

#         # Perform data analysis (you may need to adjust this depending on your dataset format)
#         data = pd.read_csv(filepath)
#         # Perform the necessary analysis to get the highest crime rate cities
#         highest_crime_cities = data["Year"].value_counts().nlargest(10)

#         # Create a plot using Matplotlib
#         plt.bar(highest_crime_cities.index, highest_crime_cities.values)
#         plt.xlabel("Population")
#         plt.ylabel("Murder")
#         plt.title("Top 10 Cities with the Highest Crime Rate")
#         plt.xticks(rotation=45)
#         plt.tight_layout()
#         plt.savefig("static/crime_plot.png")
#         plt.close()

#         return render_template("analysis.html", filename=filename)

#     # If the file does not exist in the database, show an error message or redirect to the upload page.
#     return "File not found in the database. Please upload the file first."


# @app.route("/", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]
#         # Perform admin login authentication, e.g., check if username and password match
#         # (add your own validation logic here)
#         if username == "admin" and password == "admin_password":
#             return redirect(url_for("upload"))
#         else:
#             return render_template("login.html", error="Invalid credentials")
#     return render_template("login.html", error=None)


# @app.route("/upload", methods=["GET", "POST"])
# def upload():
#     if request.method == "POST":
#         file = request.files["file"]
#         if file:
#             filename = file.filename
#             file.save(os.path.join("uploads", filename))
#             with sqlite3.connect("crime_data.db") as con:
#                 cur = con.cursor()
#                 cur.execute("INSERT INTO crime_data (filename) VALUES (?)", (filename,))
#                 con.commit()
#             return redirect(url_for("analyze"))
#     return render_template("upload.html")



@app.route("/upload", methods=["GET", "POST"])
def upload_data():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            filename = file.filename
            file.save(os.path.join("uploads", filename))
            with sqlite3.connect("crime_data.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO crime_data (filename) VALUES (?)", (filename,))
                con.commit()
            return redirect(url_for("analyze", filename=filename))
    return render_template("upload.html")


# @app.route("/analyze")
# def analyze():
#     with sqlite3.connect("crime_data.db") as con:
#         cur = con.cursor()
#         cur.execute("SELECT filename FROM crime_data ORDER BY id DESC LIMIT 1")
#         filename = cur.fetchone()[0]
#         filepath = os.path.join("uploads", filename)

#     # Perform data analysis (you may need to adjust this depending on your dataset format)
#     data = pd.read_csv(filepath)
#     # Perform the necessary analysis to get the highest crime rate cities
#     highest_crime_cities = data["city"].value_counts().nlargest(10)

#     # Create a plot using Matplotlib
#     plt.bar(highest_crime_cities.index, highest_crime_cities.values)
#     plt.xlabel("Cities")
#     plt.ylabel("Crime Rate")
#     plt.title("Top 10 Cities with the Highest Crime Rate")
#     plt.xticks(rotation=45)
#     plt.tight_layout()
#     plt.savefig("static/crime_plot.png")
#     plt.close()

#     return render_template("analysis.html", filename=filename)




# @app.route('/dashboard', methods=['GET', 'POST'])
# def dashboard():
#     if 'username' not in session or session['role'] != 'admin':
#         flash('Unauthorized access!', 'error')
#         return redirect('/')
#         # username = session['username']
#     if request.method == 'POST':
#         member_username = request.form['member_username']

#         cursor.execute("SELECT * FROM users WHERE username = ?", (member_username,))
#         member = cursor.fetchone()

#         if member:
#             return render_template('modal.html', member=member)
#         else:
#             flash('Member not found!', 'error')
    
#     return render_template('dashboard.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    # if 'username' not in session or session['role'] != 'admin':
    #     flash('Unauthorized access!', 'error')
    #     return redirect(url_for('login'))
    
    # if request.method == 'POST':
    #     member_username = request.form['member_username']

    #     cursor.execute("SELECT * FROM users WHERE username = ?", (member_username,))
    #     member = cursor.fetchone()

    #     if member:
    #         return render_template('modal.html', member=member)
    #     else:
    #         flash('Member not found!', 'error')
    
    return render_template('dashboard.html')

# @app.route("/dashboard")
# def dashboard():
#     with sqlite3.connect("crime_data.db") as con:
#         cur = con.cursor()
#         cur.execute("SELECT filename FROM users ORDER BY id DESC LIMIT 1")
#         filename = cur.fetchone()[0]
#         filepath = os.path.join("uploads", filename)

#     # Perform data analysis (you may need to adjust this depending on your dataset format)
#     data = pd.read_csv(filepath)
#     # Perform the necessary analysis to get the highest crime rate cities
#     highest_crime_cities = data["City"].value_counts().nlargest(10)

#     # Create a plot using Matplotlib
#     plt.bar(highest_crime_cities.index, highest_crime_cities.values)
#     plt.xlabel("Cities")
#     plt.ylabel("Crime Rate")
#     plt.title("Top 10 Cities with the Highest Crime Rate")
#     plt.xticks(rotation=45)
#     plt.tight_layout()
#     plt.savefig("static/crime_plot.png")
#     plt.close()

#     return render_template("dashboard.html", filename=filename)




# Replace this with your desired secret key for session management
app.secret_key = "hello"
if __name__ == "__main__":
    app.run(debug=True)
