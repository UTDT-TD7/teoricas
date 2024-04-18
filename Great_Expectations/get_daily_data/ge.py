import great_expectations as gx
from great_expectations.data_context import FileDataContext
import psycopg2
import time
from great_expectations.core.expectation_configuration import (
    ExpectationConfiguration,
)

#Create data context and connect to data source
context = FileDataContext.create(project_root_dir='.')

connection_string = "postgresql+psycopg2://catedra:S3cret@postgres/catedra"
datasource = context.sources.add_or_update_sql(
    name="PostgreSQL database", connection_string=connection_string
)
table_asset = datasource.add_table_asset(name="NYSE Table", table_name="nyse")

#Create expectations
suite = context.add_or_update_expectation_suite("expectations_table")

# 1- Check that there are no NULL values in the 'nyse' table
exp = ExpectationConfiguration(
    expectation_type="expect_column_values_to_not_be_null",
    kwargs={
        "column": "close_value",
    },
    meta={
        "notes": {
            "format": "markdown",
            "content": "No NULLs should be found on the close_value",
        }
    },
)
suite.add_expectation_configurations(
    expectation_configurations=[exp]
)
context.save_expectation_suite(expectation_suite=suite)


while (1):
    
    #Validate

    batch_request = table_asset.build_batch_request()

    checkpoint = context.add_or_update_checkpoint(
        name="postgresql_checkpoint",
        validations=[
            {
                "batch_request": batch_request,
                "expectation_suite_name": "expectations_table",
            }
        ]
    )

    checkpoint_result = checkpoint.run()
    context.build_data_docs()

    time.sleep(20)    
