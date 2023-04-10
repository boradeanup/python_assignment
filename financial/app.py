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
    response = jsonify({"data": [], "pagination": {}, 'info': {'error':str(error)}})
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
    if symbol and len(symbol)>0 and not is_company_symbol(symbol):
        raise InvalidQueryParameter('symbol should be one of AAPL(Apple Inc.), IBM')
    if start_date and is_date_error(start_date):
        raise InvalidQueryParameter('date must be a of format YY-mm-dd')
    if end_date and is_date_error(end_date):
        raise InvalidQueryParameter('date must be a of format YY-mm-dd')
    if limit and not str(limit).isnumeric():
        raise InvalidQueryParameter('limit must be an integer greater than zero')
    if page and not str(page).isnumeric():
        raise InvalidQueryParameter('page must be an integer greater than zero')



    query = FinancialData.query
    if(start_date > end_date):
        raise InvalidQueryParameter("Please specify start date earlier than end date.")
    else:
        query = query.filter(FinancialData.date >= start_date, FinancialData.date <= end_date)
        query = query.order_by(FinancialData.date.asc())
# if symbol is legit, use to filter otherwise don't
    if(is_company_symbol(symbol)):
        query = query.filter_by(symbol=symbol)

# Calculate pagination properties
    count = query.count()
    pages = int(int(count)/int(limit)) + 1  


    error=''

    if(int(page) > pages):
        error = 'Page number exceeds total number of pages'


    query = query.paginate(page = int(page), per_page = int(limit), error_out=False)
    results = query.items

    # Construct response JSON object
    data = []
    for result in results:
        data.append({
            'symbol': result.symbol,
            'date': result.date.isoformat(),
            'open_price': float(result.open_price),
            'close_price': float(result.close_price),
            'volume': int(result.volume)
        })

    pagination = {
        'count': count,
        'page': page,
        'limit': limit,
        'pages': pages
    }

    response = {
        'data': data,
        'pagination': pagination,
        'info': {'error': error}
    }


    return jsonify(response)

# error hanlder class somewhere
# helper methods somewhere
# function 1: create json response
# function 2: input query param check
# function 3: get data for this. . . 
# functino 4: generate paginatio data.


@app.route('/statistics')
def get_statistics():
    # Get input parameters
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    symbol = request.args.get('symbol')

    # Validate input parameters
    if not start_date_str or not end_date_str or not symbol:
        return jsonify({'data': {},'info': {'error': 'Missing required parameters'}}), 400
    
    try:
        start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d')
    except ValueError:
        return jsonify({'data': {},'info': {'error': 'Invalid date format'}}), 400

    if start_date > end_date:
        return jsonify({'data': {},'info': {'error': 'Invalid date range'}}), 400

    if not is_company_symbol(symbol):
        return jsonify({'data': {},'info': {'error': 'symbol should be one of AAPL(Apple Inc.), IBM'}}), 400

    financial_data = FinancialData.query.filter_by(symbol=symbol).\
                    filter(FinancialData.date >= start_date.date()).\
                    filter(FinancialData.date <= end_date.date()).all()

    if not financial_data:
        return jsonify({'data': {}, 'info': {'error': 'No financial data found for the given symbol and period.'}})

    # Calculate statistics
    total_open_price = sum([float(fd.open_price) for fd in financial_data])
    total_close_price = sum([float(fd.close_price) for fd in financial_data])
    total_volume = sum([int(fd.volume) for fd in financial_data])
    num_days = len(financial_data)
    average_daily_open_price = total_open_price / num_days
    average_daily_close_price = total_close_price / num_days
    average_daily_volume = total_volume / num_days

    # Create response
    response_data = {
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'symbol': symbol,
        'average_daily_open_price': average_daily_open_price,
        'average_daily_close_price': average_daily_close_price,
        'average_daily_volume': average_daily_volume
    }

    return jsonify({'data': response_data, 'info': {'error': ''}})



if __name__ == '__main__':
    app.run(debug=True)