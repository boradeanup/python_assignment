from .models import FinancialData
from . import app
from flask import jsonify, request
import datetime




@app.route('/')
def hello():
    return {"hello": "world"}


# Custom exception for invalid query parameters
class InvalidQueryParameter(Exception):
    pass

# Custom error handler for invalid query parameters
@app.errorhandler(InvalidQueryParameter)
def handle_invalid_query_parameter(error):
    response = jsonify({"data": [], "pagination": {}, 'info': str(error)})
    response.status_code = 400
    return response

def is_date_error(date_string): 
    try:
        datetime.datetime.strptime(date_string, "%Y-%m-%d").date()
        return False
    except ValueError:
        return True
        
def is_company_symbol(symbol):
    return symbol in ["AAPL", "IBM"]



@app.route('/financial_data')
def get():
    
    # Get the query parameters from the request with default values
    symbol = request.args.get('symbol', '')
    start_date = request.args.get('start_date', '2022-01-01')
    end_date = request.args.get('end_date', '2024-01-01')
    limit = request.args.get('limit', 5)
    page = request.args.get('page', 1)

    # Check data types of query parameters if they are not None
    if symbol and not is_company_symbol(symbol):
        raise InvalidQueryParameter('symbol should be one of AAPL, IBM')
    if start_date and is_date_error(start_date):
        raise InvalidQueryParameter('date must be a of format YY-mm-dd')
    if end_date and is_date_error(end_date):
        raise InvalidQueryParameter('date must be a of format YY-mm-dd')
    if limit and not str(limit).isnumeric():
        raise InvalidQueryParameter('limit must be an integer greater than zero')
    if page and not str(page).isnumeric():
        raise InvalidQueryParameter('page must be an integer greater than zero')



    financial_data_list = FinancialData.query.all()
    json_list = [{"symbol": row.symbol,
                        "date": row.date.strftime("%Y-%m-%d"),
                        "open_price": float(row.open_price),
                        "close_price": float(row.close_price),
                        "volume": int(row.volume)}
                for row in financial_data_list]
    return {"data": json_list, pagination: {}, "info": {}}




if __name__ == '__main__':
    app.run(debug=True)