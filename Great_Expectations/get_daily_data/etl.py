from polygon import RESTClient
import pandas as pd
import datetime
import time
from sqlalchemy import create_engine
import great_expectations as gx
from great_expectations.data_context import FileDataContext
from great_expectations.core.expectation_configuration import (
    ExpectationConfiguration,
)

# Replace with your actual API key
api_key = "aTfYB3ReEal95GJHxM5mExGCeg6l63gq"  
client = RESTClient(api_key)

#Inicialization
start_date = datetime.date(2024, 1, 2)
end_date = datetime.date(2024, 1, 28)
today = start_date
engine = create_engine('postgresql://catedra:S3cret@postgres:5432/catedra')

#Great expectations measurements
context = FileDataContext.create(project_root_dir='.')
datasource = context.sources.add_or_update_pandas(name="Pandas datasource")
data_asset = datasource.add_dataframe_asset(name="pandas NYSE DataFrame")

#Create expectations
suite = context.add_or_update_expectation_suite("expectations_data_frame")

# 1- Check that the generated table has 3 columns
exp = ExpectationConfiguration(
    expectation_type="expect_table_column_count_to_equal",
    kwargs={
        "value": 3,
    },
    meta={
        "notes": {
            "format": "markdown",
            "content": "No NULLs should be found on the ticker",
        }
    },
)
suite.add_expectation_configurations(
    expectation_configurations=[exp]
)
context.save_expectation_suite(expectation_suite=suite)


#Dialy loop
while today <= end_date:

    #If it's a bank day
    if today.weekday() < 5:

        try:
            #Call API to get daily data
            data = pd.DataFrame(client.get_grouped_daily_aggs(date=str(today)))

            #Process daily data (project columns, rename 'close' column, add 'date' column)
            data = data[['ticker', 'close']]
            data = data.rename(columns={'close': 'close_value'})

            data['date'] = str(today)
        
            #Write daily data into PostgreSQL
            data.to_sql('nyse', engine, if_exists='append', index=False)

        except Exception as e:
            print(f"An error occurred while writing data to PostgreSQL on date {today}: {str(e)}")

        #Great expectations
        batch_request = data_asset.build_batch_request(dataframe=data)

        checkpoint = context.add_or_update_checkpoint(
            name="data_frame_checkpoint",
            validations=[
                {
                    "batch_request": batch_request,
                    "expectation_suite_name": "expectations_data_frame",
                }
            ]
        )
    
        checkpoint_result = checkpoint.run()
        context.build_data_docs()
    
    #Next day. We simulate one day every 20 seconds. Remember that the Polygon API free tier has a cap of 5 calls/minute.
    time.sleep(20)
    today += datetime.timedelta(days=1)

