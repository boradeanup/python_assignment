
README-

** A brief project description

This repository fetches some simple stock price data for 2 companies using the free API from AlphaVantage  locally and makes it accessible via a RESTful web API interface.

*** Financial data API- 
Inputs:
* Optional parameters: start_date (YYYY-MM-DD), end_date (YYYY-MM-DD), and symbol (string) which represents the company name.
* Optional pagination parameters: limit (integer) and page (integer)
Outputs:
* A JSON response containing the following three properties:
    * data: an array of financial data records that match the provided filters
    * pagination: an object containing pagination information, including the total count of records, current page index, limit, and total number of pages
    * info: an object containing any error information if applicable
Note: If no filters are provided, all financial data records will be returned. The default limit for one page is 5 records.


*** Statistics API- 

Inputs:
* Required parameters: start_date (YYYY-MM-DD), end_date (YYYY-MM-DD), and symbol (string) which represents the company name. Outputs:
* A JSON response containing the following two properties:
    * data: an object containing the calculated statistic results for the given period, including the average daily open price, average daily closing price, and average daily volume
    * info: an object containing any error information if applicable
Note: All parameters are required, and the endpoint performs calculations on the data within the specified period of time.
