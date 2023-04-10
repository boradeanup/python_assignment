import datetime
from .models import FinancialData

# Custom exception for invalid query parameters
class InvalidQueryParameter(Exception):
    pass

def is_date_error(date_string): 
    try:
        datetime.datetime.strptime(date_string, "%Y-%m-%d").date()
        return False
    except ValueError:
        return True
        
def is_company_symbol(symbol):
    return symbol in ["AAPL", "IBM"]

def validate_query_params(symbol, start_date, end_date, limit, page):

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


# Function to retrieve financial data based on query parameters
def get_financial_data(symbol, start_date, end_date, limit, page):
    query = FinancialData.query
    
    # Check that start date is earlier than end date
    if start_date > end_date:
        raise InvalidQueryParameter("Please specify start date earlier than end date.")
    else:
        query = query.filter(FinancialData.date >= start_date, FinancialData.date <= end_date)
        query = query.order_by(FinancialData.date.asc())
    
    # Filter by symbol if it's a valid company symbol
    if is_company_symbol(symbol):
        query = query.filter_by(symbol=symbol)
    
    # Paginate results
    count = query.count()
    pages = int(int(count)/int(limit)) + 1  
    error=''
    if(int(page) > pages):
        error = 'Page number exceeds total number of pages'
    query = query.paginate(page=int(page), per_page=int(limit), error_out=False)
    results = query.items
    
    # Convert results to a list of dictionaries
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
    
    return {'data': data, 'pagination': pagination, 'info': {'error': error}}


def validate_stats_input(start_date_str, end_date_str, symbol):
    if not start_date_str or not end_date_str or not symbol:
        return {'error': 'Missing required parameters'}, 400
    
    try:
        start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d')
    except ValueError:
        return {'error': 'Invalid date format'}, 400

    if start_date > end_date:
        return {'error': 'Invalid date range'}, 400

    if not is_company_symbol(symbol):
        return {'error': 'symbol should be one of AAPL(Apple Inc.), IBM'}, 400

    return None, None

def calculate_statistics(financial_data):
    total_open_price = sum([float(fd.open_price) for fd in financial_data])
    total_close_price = sum([float(fd.close_price) for fd in financial_data])
    total_volume = sum([int(fd.volume) for fd in financial_data])
    num_days = len(financial_data)
    average_daily_open_price = total_open_price / num_days
    average_daily_close_price = total_close_price / num_days
    average_daily_volume = total_volume / num_days

    response_data = {
        'average_daily_open_price': average_daily_open_price,
        'average_daily_close_price': average_daily_close_price,
        'average_daily_volume': average_daily_volume
    }

    return response_data

def get_stats_financial_data(symbol, start_date, end_date):
    return FinancialData.query.filter_by(symbol=symbol).\
                    filter(FinancialData.date >= start_date.date()).\
                    filter(FinancialData.date <= end_date.date()).all()
