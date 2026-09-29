from flask import Flask, render_template, request, redirect, url_for, flash
import os, joblib, pandas as pd
from database.database import init_db, get_connection

BASE=os.path.dirname(os.path.abspath(__file__))
MODEL_PATH=os.path.join(BASE,"model","price_model.joblib")
DATA_PATH=os.path.join(BASE,"data","surat_real_estate.csv")

app=Flask(__name__)
app.secret_key="real-estate-demo-secret"
init_db()

def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Model not found. Run: python model/train_model.py")
    return joblib.load(MODEL_PATH)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict",methods=["POST"])
def predict():
    try:
        data={
            "location":request.form["location"],
            "property_type":request.form["property_type"],
            "area_sqft":float(request.form["area_sqft"]),
            "bhk":int(request.form["bhk"]),
            "bathrooms":int(request.form["bathrooms"]),
            "floor":int(request.form["floor"]),
            "property_age":int(request.form["property_age"]),
            "parking":request.form["parking"],
            "furnishing":request.form["furnishing"]
        }
        model=load_model()
        prediction=float(model.predict(pd.DataFrame([data]))[0])
        con=get_connection()
        con.execute("""INSERT INTO predictions
        (location,property_type,area_sqft,bhk,bathrooms,floor,property_age,parking,furnishing,predicted_price)
        VALUES (?,?,?,?,?,?,?,?,?,?)""",
        (*data.values(),prediction))
        con.commit(); con.close()
        return render_template("result.html",data=data,price=prediction)
    except Exception as e:
        flash(str(e))
        return redirect(url_for("home"))

@app.route("/history")
def history():
    con=get_connection()
    rows=con.execute("SELECT * FROM predictions ORDER BY id DESC").fetchall()
    con.close()
    return render_template("history.html",rows=rows)

@app.route("/analytics")
def analytics():
    df=pd.read_csv(DATA_PATH)
    location_data=df.groupby("location",as_index=False)["price"].mean()
    bhk_data=df.groupby("bhk",as_index=False)["price"].mean()
    return render_template("analytics.html",
        location_labels=location_data["location"].tolist(),
        location_values=[round(x) for x in location_data["price"].tolist()],
        bhk_labels=bhk_data["bhk"].tolist(),
        bhk_values=[round(x) for x in bhk_data["price"].tolist()])

if __name__=="__main__":
    app.run(debug=True)
