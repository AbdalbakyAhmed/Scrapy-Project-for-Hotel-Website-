## Scrapy Project for Hotel Website

*a Python scrapy spider to scrape from `Trivago.com`. The spider should scrape the following details:*

The spider should take as `input parameters`:
- city/ destination
- Check in date
- Check out date 
- Number of adults
- Number of children  
- Max price per night 
- Currency selector 

For example, the `filters` data structure might look like this:
```
filters = {
        "city": "Miami",
        "check_in": "2021-04-05",
        "check_out": "2021-04-09",
        "adults": 2,
        "children": 0,
        "max_price": 200,
        "currency": "USD"
}
```
The spider then should search Trivago with the `parameters` supplied above. From there, it needs to extract the following details:
- Hotel name
- Hotel detail link (the link you get if you click on the hotel name)
- Image link
- Rating number (7.4)
- Number of ratings
- Number of stars for hotel (3/4/5 star hotel etc)
- Hotel address
- Price per night
- Total Price
- Amount of taxes and fees
- Total Price with taxes and fees
- Major box price and name of seller
- Minor box price and name of seller
- Cheapest price and name of seller
  - The total price with taxes and fees should be based on this
  - The average nightly price should also be based on this as well
- Link to the primary box, link to the secondary box, and link to the cheapest price
