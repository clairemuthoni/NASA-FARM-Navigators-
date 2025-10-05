from flask import Flask
from flask_cors import CORS
import pandas as pd
import os

# Import the data
csv_path = os.path.join(os.path.dirname(__file__), "nasa_data.csv")
df = pd.read_csv(csv_path)

data = df.to_dict(orient="records")

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    return "Flask home route"

@app.route("/data")
def get_data():
    return data

# if __name__ == "__main__":
#     app.run()