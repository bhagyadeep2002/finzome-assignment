import pandas as pd
import statistics
import math
from flask import Flask,request,jsonify

''' make sure uploaded file is in xlsx format (Excel) '''
def is_valid(filename):
    extension = filename.split('.')
    if extension[-1] != 'xlsx':
        return False
    else:
        return True

def calculate(file):
    daily_returns = []
    df = pd.read_excel(file)
    ''' remove whitespaces from the names of the columns '''
    df.columns = df.columns.str.strip()

    for close in range(1,len(df['Close'])):
        ''' Daily Returns = (current close / previous close) - 1 (given in assignment) '''
        daily_return = (df['Close'][close]/df['Close'][close-1]) - 1
        daily_returns.append(daily_return)

    daily_returns = pd.Series(daily_returns)

    ''' Daily Volatility = Standard Deviation (Daily Returns) (given in assignment) '''
    daily_volatility = statistics.stdev(daily_returns)
    data_len = len(df['Close'])

    ''' Annualized Volatility = Daily Volatility * Square Root (length of data) (given in assignment) '''
    annual_volatility = daily_volatility * math.sqrt(data_len)

    return daily_volatility, annual_volatility

app = Flask(__name__)

@app.route('/', methods=['POST'])
def get_file():

    ''' the parameter name when uploading the file should be "file" '''
    file = request.files['file']
    if is_valid(file.filename) == False:
        response = {
            "error": "invalid format"
        }
    else:
        results = calculate(file)
        response = {
            "daily volatility": results[0],
            "annual volatility": results[1]
        }
    return jsonify(response)


