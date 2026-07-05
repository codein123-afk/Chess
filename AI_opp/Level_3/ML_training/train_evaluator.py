import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import joblib

df = pd.read_csv("positions.csv")
df = df[df["target"].abs() < 10]
X=df.drop(columns=["target"])

Y=df["target"]
x_train,x_test,y_train,y_test=train_test_split(X,Y,test_size=0.2,random_state=42)
model=LinearRegression()
model.fit(x_train,y_train)
pred=model.predict(x_test)
print("RMSE:", mean_squared_error(y_test, pred) ** 0.5)
joblib.dump(model, "evaluation_model.pkl")

for name, coef in zip(X.columns, model.coef_):
    print(f"{name:25s} {coef:.4f}")
print("Intercept:", model.intercept_)
print(df.describe())