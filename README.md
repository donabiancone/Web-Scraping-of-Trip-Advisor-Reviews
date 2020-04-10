# Web Scraping of Trip Advisor Reviews 
 Web Scraper written in Python, using Selenium and BeautifulSoup
 
This web scraper has been created in order to collect Trip Advisor reviews for one of the neighborhood of Rome (Prenestino-Centocelle)

Data was collected according two different strategies:

- **Strategy 1:** Collect last 5 comments posted for each restaurant located in the neighborhood.
- **Strategy 2:** Collect last 50 comments posted for the 20 top-reviewed restaurants located in the neighborhood.

For each comment, we collect the following meta-information:

1. rating
2. review's date
3. reviewer's nickname

`Selenium` has been used for dynamic navigation of web page and `BeautifulSoup` for collecting data, instead. 

I used the collected data in order to create two corpora and perform a text mining analysis. The analysis' results are published on [RPubs](https://rpubs.com/donabiancone/trip-advisor-textmining) (in italian).


