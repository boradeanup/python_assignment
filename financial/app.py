from .models import FinancialData
from . import app
from .services import (validate_query_params, get_financial_data, InvalidQueryParameter,
                       is_company_symbol, calculate_statistics, get_stats_financial_data,
                       validate_stats_input)
from flask import jsonify, request, Blueprint
import datetime

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/')
def hello():
    return {"hello": "world"}


# Custom error handler for invalid query parameters
@api_bp.errorhandler(InvalidQueryParameter)
def handle_invalid_query_parameter(error):
    response = jsonify({"data": [], "pagination": {}, 'info': {'error':str(error)}})
    response.status_code = 400
    return response


@api_bp.route('/financial_data')
def get():
    # Get the query parameters from the request with default values
    symbol = request.args.get('symbol', '')
    start_date = request.args.get('start_date', '2022-01-01')
    end_date = request.args.get('end_date', '2024-01-01')
    limit = request.args.get('limit', 5)
    page = request.args.get('page', 1)
    
    # Validate query parameters
    validate_query_params(symbol, start_date, end_date, limit, page)
    
    # Retrieve financial data based on query parameters
    response_data = get_financial_data(symbol, start_date, end_date, limit, page)
    
    # Return response as JSON
    return jsonify(response_data)


@api_bp.route('/statistics')
def get_statistics():
    # Retrieve query parameters from request
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    symbol = request.args.get('symbol')

    # Validate query parameters
    error, status_code = validate_stats_input(start_date_str, end_date_str, symbol)
    if error:
        # Return error response if validation fails
        return jsonify({'data': {}, 'info': {'error': error}}), status_code

    # Convert date strings to datetime objects
    start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d')
    
    # Retrieve financial data based on query parameters
    financial_data = get_stats_financial_data(symbol, start_date, end_date)

    # Return error response if no financial data is found for the given symbol and period
    if not financial_data:
        return jsonify({'data': {}, 'info': {'error': 'No financial data found for the given symbol and period.'}})

    # Calculate statistics based on financial data
    response_data = calculate_statistics(financial_data)
    
    # Add additional fields to response data
    response_data.update({
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'symbol': symbol
    })

    # Return response as JSON
    return jsonify({'data': response_data, 'info': {'error': ''}})

# Register the blueprint
app.register_blueprint(api_bp)

if __name__ == '__main__':
    app.run(debug=True)
