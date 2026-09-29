import os, joblib, pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, r2_score

BASE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA=os.path.join(BASE,"data","surat_real_estate.csv")
OUT=os.path.join(BASE,"model","price_model.joblib")

df=pd.read_csv(DATA)
X=df.drop(columns=["price"])
y=df["price"]

cat=["location","property_type","parking","furnishing"]
num=["area_sqft","bhk","bathrooms","floor","property_age"]

preprocessor=ColumnTransformer([
    ("cat",OneHotEncoder(handle_unknown="ignore"),cat),
    ("num","passthrough",num)
])

model=RandomForestRegressor(n_estimators=300,max_depth=18,min_samples_leaf=2,
                            random_state=42,n_jobs=-1)
pipe=Pipeline([("preprocessor",preprocessor),("model",model)])

X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.20,random_state=42)
pipe.fit(X_train,y_train)
pred=pipe.predict(X_test)
print(f"MAE: ₹{mean_absolute_error(y_test,pred):,.0f}")
print(f"R2 : {r2_score(y_test,pred):.3f}")

joblib.dump(pipe,OUT)
print("Saved:",OUT)
