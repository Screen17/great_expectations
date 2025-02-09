from typing import List

import pandas as pd
import sqlalchemy as sa

import great_expectations as gx
from great_expectations.core.batch import BatchRequest, LegacyBatchDefinition
from great_expectations.core.batch_spec import SqlAlchemyDatasourceBatchSpec
from great_expectations.datasource import BaseDatasource
from great_expectations.datasource.data_connector import ConfiguredAssetSqlDataConnector
from great_expectations.execution_engine.sqlalchemy_batch_data import (
    SqlAlchemyBatchData,
)
from tests.integration.db.taxi_data_utils import (
    loaded_table,
)
from tests.integration.fixtures.partition_and_sample_data.sampler_test_cases_and_fixtures import (
    SamplerTaxiTestData,
    TaxiSamplingTestCase,
    TaxiSamplingTestCases,
)
from tests.test_utils import (
    get_connection_string_and_dialect,
)

if __name__ == "test_script_module":
    dialect, connection_string = get_connection_string_and_dialect(
        athena_db_name_env_var="ATHENA_TEN_TRIPS_DB_NAME"
    )
    print(f"Testing dialect: {dialect}")

    with loaded_table(dialect, connection_string) as table:
        test_df: pd.DataFrame = table.inserted_dataframe
        table_name: str = table.table_name

        taxi_test_data: SamplerTaxiTestData = SamplerTaxiTestData(
            test_df, test_column_name="pickup_datetime"
        )
        test_cases: TaxiSamplingTestCases = TaxiSamplingTestCases(taxi_test_data)

        test_cases: List[TaxiSamplingTestCase] = test_cases.test_cases()

        for test_case in test_cases:
            print("Testing sampler method:", test_case.sampling_method_name)

            # 1. Setup

            context = gx.get_context()

            datasource_name: str = "test_datasource"
            data_connector_name: str = "test_data_connector"
            data_asset_name: str = table_name  # Read from generated table name

            # 2. Set sampler in DataConnector config
            data_connector_config: dict = {
                "class_name": "ConfiguredAssetSqlDataConnector",
                "assets": {
                    data_asset_name: {
                        "sampling_method": test_case.sampling_method_name,
                        "sampling_kwargs": test_case.sampling_kwargs,
                    }
                },
            }

            context.add_datasource(
                name=datasource_name,
                class_name="Datasource",
                execution_engine={
                    "class_name": "SqlAlchemyExecutionEngine",
                    "connection_string": connection_string,
                },
                data_connectors={data_connector_name: data_connector_config},
            )

            datasource: BaseDatasource = context.get_datasource(datasource_name=datasource_name)

            data_connector: ConfiguredAssetSqlDataConnector = datasource.data_connectors[
                data_connector_name
            ]

            # 3. Check if resulting batches are as expected
            # using data_connector.get_batch_definition_list_from_batch_request()
            batch_request: BatchRequest = BatchRequest(
                datasource_name=datasource_name,
                data_connector_name=data_connector_name,
                data_asset_name=data_asset_name,
            )
            batch_definition_list: List[LegacyBatchDefinition] = (
                data_connector.get_batch_definition_list_from_batch_request(batch_request)
            )

            assert len(batch_definition_list) == test_case.num_expected_batch_definitions

            # 4. Check that loaded data is as expected

            batch_spec: SqlAlchemyDatasourceBatchSpec = data_connector.build_batch_spec(
                batch_definition_list[0]
            )

            batch_data: SqlAlchemyBatchData = context.datasources[
                datasource_name
            ].execution_engine.get_batch_data(batch_spec=batch_spec)

            num_rows: int = batch_data.execution_engine.execute_query(
                sa.select(sa.func.count()).select_from(batch_data.selectable)
            ).scalar()
            assert num_rows == test_case.num_expected_rows_in_first_batch_definition

            # TODO: AJB 20220502 Test the actual rows that are returned e.g. for random sampling.
