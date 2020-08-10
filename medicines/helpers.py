'''
Helper functions for the `medicines` Django app
'''


def process_pricing_data(raw_data):
    '''
    Method processes input `raw_data` consisting of e.g.
      {"items":32961,"quantity":1114647,"actual_cost":956153.35,"date":"2014-11-01"}

    returning `price_per_unit` data consisting of e.g.
      {"price_per_unit":0.8578082119271841,"date":"2014-11-01"}
    '''

    # Return an empty list by default
    pricing_data = []

    # Process the data to calculate price_per_unit. price_per_unit = actual_cost / quantity
    if raw_data:
        for row in raw_data:
            # Check that the input data is non-zero before doing calculations
            if row['quantity'] > 0:
                # If data is valid, process and append to output list
                pricing_data.append(
                    {'date': row['date'], 'price_per_unit': (row['actual_cost']/row['quantity'])}
                )

    return pricing_data
