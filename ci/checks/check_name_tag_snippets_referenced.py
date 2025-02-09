"""
Purpose: To ensure that all named snippets are referenced in the docs.

Python code snippets refers to the Python module, containing the test, as follows:

```python name="tests/integration/docusaurus/general_directory/specific_directory/how_to_do_my_operation.py get_context"
```

whereby "tests/integration/docusaurus/general_directory/specific_directory/how_to_do_my_operation.py get_context", which
is the Python module, containing the integration test in the present example, would contain the following tagged code:

# Python
# <snippet name="tests/integration/docusaurus/general_directory/specific_directory/how_to_do_my_operation.py get_context">
import great_expectations as gx

context = gx.get_context()
# </snippet>

Find all named snippets and ensure that they are referenced in the docs using the above syntax.
"""  # noqa: E501

import pathlib
import shutil
import subprocess
import sys
from typing import List

# TODO: address ignored snippets by deleting snippet or test file, or adding documentation that references them  # noqa: E501
IGNORED_VIOLATIONS = [
    "tests/integration/docusaurus/connecting_to_your_data/cloud/azure/pandas/inferred_and_runtime_python_example.py add datasource",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/cloud/azure/pandas/inferred_and_runtime_python_example.py datasource config",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/cloud/azure/pandas/inferred_and_runtime_python_example.py test datasource",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/cloud/azure/pandas/inferred_and_runtime_yaml_example.py add_datasource",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/cloud/azure/pandas/inferred_and_runtime_yaml_example.py batch_request",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/cloud/azure/pandas/inferred_and_runtime_yaml_example.py datasource_yaml",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/cloud/azure/pandas/inferred_and_runtime_yaml_example.py get_context",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/cloud/azure/pandas/inferred_and_runtime_yaml_example.py imports",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/cloud/azure/pandas/inferred_and_runtime_yaml_example.py test_yaml_config",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/cloud/azure/pandas/inferred_and_runtime_yaml_example.py validator_creation",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/cloud/azure/spark/inferred_and_runtime_python_example.py add datasource",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/cloud/azure/spark/inferred_and_runtime_python_example.py datasource config",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/cloud/azure/spark/inferred_and_runtime_python_example.py test datasource",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/cloud/azure/spark/inferred_and_runtime_yaml_example.py add datasource",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/cloud/azure/spark/inferred_and_runtime_yaml_example.py batch request",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/cloud/azure/spark/inferred_and_runtime_yaml_example.py datasource config",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/cloud/azure/spark/inferred_and_runtime_yaml_example.py get validator",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/cloud/azure/spark/inferred_and_runtime_yaml_example.py imports",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/cloud/azure/spark/inferred_and_runtime_yaml_example.py test datasource",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/cloud/gcs/pandas/inferred_and_runtime_python_example.py add_datasource",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/cloud/gcs/pandas/inferred_and_runtime_python_example.py datasource_config",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/cloud/gcs/pandas/inferred_and_runtime_python_example.py test_yaml_config",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/cloud/gcs/pandas/inferred_and_runtime_yaml_example.py add_datasource",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/cloud/gcs/pandas/inferred_and_runtime_yaml_example.py batch_request",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/cloud/gcs/pandas/inferred_and_runtime_yaml_example.py datasource_yaml",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/cloud/gcs/pandas/inferred_and_runtime_yaml_example.py get_context",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/cloud/gcs/pandas/inferred_and_runtime_yaml_example.py imports",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/cloud/gcs/pandas/inferred_and_runtime_yaml_example.py rumtime_batch_request",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/cloud/gcs/pandas/inferred_and_runtime_yaml_example.py validator_creation",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/cloud/gcs/spark/inferred_and_runtime_python_example.py add datasource config",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/cloud/gcs/spark/inferred_and_runtime_python_example.py datasource config",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/cloud/gcs/spark/inferred_and_runtime_python_example.py test datasource config",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/cloud/gcs/spark/inferred_and_runtime_yaml_example.py add_datasource",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/cloud/gcs/spark/inferred_and_runtime_yaml_example.py batch_request",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/cloud/gcs/spark/inferred_and_runtime_yaml_example.py datasource_yaml",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/cloud/gcs/spark/inferred_and_runtime_yaml_example.py imports",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/cloud/gcs/spark/inferred_and_runtime_yaml_example.py runtime_batch_request",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/cloud/gcs/spark/inferred_and_runtime_yaml_example.py test_yaml_config",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/cloud/gcs/spark/inferred_and_runtime_yaml_example.py validator_creation",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/cloud/gcs/spark/inferred_and_runtime_yaml_example.py validator_creation_2",  # noqa: E501
    "docs/docusaurus/docs/oss/guides/connecting_to_your_data/cloud/s3/components_spark/inferred_and_runtime_python_example.py datasource config",  # noqa: E501
    "docs/docusaurus/docs/oss/guides/connecting_to_your_data/cloud/s3/components_spark/inferred_and_runtime_python_example.py test datasource config",  # noqa: E501
    "docs/docusaurus/docs/snippets/inferred_and_runtime_yaml_example_spark_s3.py datasource config",
    "docs/docusaurus/docs/snippets/inferred_and_runtime_yaml_example_spark_s3.py test datasource config",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/database/bigquery_python_example.py add_datasource",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/database/bigquery_python_example.py batch_request",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/database/bigquery_python_example.py datasource_config",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/database/bigquery_python_example.py test_yaml_config",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/database/mysql_python_example.py add datasource config",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/database/mysql_python_example.py datasource config",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/database/mysql_python_example.py test datasource config",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/database/postgres_python_example.py add_datasource",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/database/postgres_python_example.py datasource_config",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/database/postgres_python_example.py test_yaml_config",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/database/postgres_yaml_example.py add_datasource",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/database/postgres_yaml_example.py batch_request with query",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/database/postgres_yaml_example.py batch_request with table",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/database/postgres_yaml_example.py datasource_yaml",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/database/postgres_yaml_example.py get_context",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/database/postgres_yaml_example.py imports",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/database/postgres_yaml_example.py test_yaml_config",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/database/snowflake_python_example.py add_datasource",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/database/snowflake_python_example.py datasource_config",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/database/snowflake_python_example.py python batch_request name table",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/database/snowflake_python_example.py test_yaml_config",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/database/sqlite_python_example.py add_datasource",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/database/sqlite_python_example.py batch request table name",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/database/sqlite_python_example.py datasource_config",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/database/sqlite_python_example.py test_yaml_config",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/database/trino_python_example.py add_datasource",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/database/trino_python_example.py datasource_config",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/database/trino_python_example.py get_context",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/database/trino_python_example.py test_yaml_config",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/filesystem/pandas_python_example.py add_datasource",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/filesystem/pandas_python_example.py test_yaml_config",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/filesystem/pandas_python_example.py yaml",
    "tests/integration/docusaurus/connecting_to_your_data/filesystem/spark_python_example.py add_datasource",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/filesystem/spark_python_example.py batch_request directory validator",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/filesystem/spark_python_example.py batch_request directory",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/filesystem/spark_python_example.py batch_request validator",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/filesystem/spark_python_example.py batch_request",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/filesystem/spark_python_example.py python",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/filesystem/spark_python_example.py runtime_batch_request validator",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/filesystem/spark_python_example.py runtime_batch_request",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/filesystem/spark_python_example.py test_yaml_config",  # noqa: E501
    "docs/docusaurus/docs/snippets/get_existing_data_asset_from_existing_datasource_pandas_filesystem_example.py my_datasource",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_choose_which_dataconnector_to_use.py datasource_config",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_choose_which_dataconnector_to_use.py datasource_config_2",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_choose_which_dataconnector_to_use.py datasource_yaml",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_choose_which_dataconnector_to_use.py datasource_yaml_2",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_configure_a_runtimedataconnector.py add_datasource",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_configure_a_runtimedataconnector.py batch_request 1",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_configure_a_runtimedataconnector.py batch_request example 2",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_configure_a_runtimedataconnector.py datasource_config yaml",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_configure_a_runtimedataconnector.py get_validator 1",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_configure_a_runtimedataconnector.py get_validator example 2",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_configure_a_runtimedataconnector.py import pandas",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_configure_a_runtimedataconnector.py path",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_configure_a_runtimedataconnector.py python datasource_config",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_configure_a_runtimedataconnector.py python imports",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_configure_a_runtimedataconnector.py yaml imports",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_configure_an_inferredassetdataconnector.py batch_request 2019-02",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_configure_an_inferredassetdataconnector.py datasource_config add an InferredAssetDataConnector to a Datasource configuration",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_configure_an_inferredassetdataconnector.py datasource_config basic configuration with more than one Data Asset",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_configure_an_inferredassetdataconnector.py datasource_config each file own data asset",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_configure_an_inferredassetdataconnector.py datasource_config nested directory structure with the data_asset_name on the inside",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_configure_an_inferredassetdataconnector.py datasource_config nested directory structure with the data_asset_name on the outside",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_configure_an_inferredassetdataconnector.py datasource_yaml add an InferredAssetDataConnector to a Datasource configuration",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_configure_an_inferredassetdataconnector.py datasource_yaml basic configuration with more than one Data Asset",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_configure_an_inferredassetdataconnector.py datasource_yaml each file own data asset",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_configure_an_inferredassetdataconnector.py datasource_yaml nested directory structure with the data_asset_name on the inside",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_configure_an_inferredassetdataconnector.py datasource_yaml nested directory structure with the data_asset_name on the outside",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_configure_an_inferredassetdataconnector.py datasource_yaml redundant information in the naming convention",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_configure_an_inferredassetdataconnector.py get_validator",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_configure_an_inferredassetdataconnector.py imports python",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_configure_an_inferredassetdataconnector.py imports yaml",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_configure_an_inferredassetdataconnector.py python datasource_config redundant information in the naming convention",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_create_a_batch_of_data_from_an_in_memory_pandas_dataframe.py add_datasource",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_create_a_batch_of_data_from_an_in_memory_pandas_dataframe.py create_expectation_suite",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_create_a_batch_of_data_from_an_in_memory_pandas_dataframe.py datasource_yaml",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_create_a_batch_of_data_from_an_in_memory_pandas_dataframe.py get_context",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_create_a_batch_of_data_from_an_in_memory_pandas_dataframe.py get_expectation_suite",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_create_a_batch_of_data_from_an_in_memory_pandas_dataframe.py get_validator_args",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_create_a_batch_of_data_from_an_in_memory_pandas_dataframe.py get_validator_runtime_batch_request",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_create_a_batch_of_data_from_an_in_memory_pandas_dataframe.py imports",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_create_a_batch_of_data_from_an_in_memory_pandas_dataframe.py path_to_file",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_create_a_batch_of_data_from_an_in_memory_pandas_dataframe.py read_csv",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_create_a_batch_of_data_from_an_in_memory_pandas_dataframe.py runtime_batch_request",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_create_a_batch_of_data_from_an_in_memory_pandas_dataframe.py runtime_batch_request_with_path",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_create_a_batch_of_data_from_an_in_memory_pandas_dataframe.py validator head",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_create_a_batch_of_data_from_an_in_memory_spark_dataframe.py add_datasource",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_create_a_batch_of_data_from_an_in_memory_spark_dataframe.py create_expectation_suite",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_create_a_batch_of_data_from_an_in_memory_spark_dataframe.py datasource_yaml",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_create_a_batch_of_data_from_an_in_memory_spark_dataframe.py get_context",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_create_a_batch_of_data_from_an_in_memory_spark_dataframe.py get_expectation_suite",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_create_a_batch_of_data_from_an_in_memory_spark_dataframe.py get_validator",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_create_a_batch_of_data_from_an_in_memory_spark_dataframe.py get_validator_2",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_create_a_batch_of_data_from_an_in_memory_spark_dataframe.py imports",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_create_a_batch_of_data_from_an_in_memory_spark_dataframe.py path_to_file",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_create_a_batch_of_data_from_an_in_memory_spark_dataframe.py pyspark_df",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_create_a_batch_of_data_from_an_in_memory_spark_dataframe.py runtime_batch_request",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_create_a_batch_of_data_from_an_in_memory_spark_dataframe.py runtime_batch_request_2",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_create_a_batch_of_data_from_an_in_memory_spark_dataframe.py validator_head",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_get_one_or_more_batches_of_data_from_a_configured_datasource.py all batches",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_get_one_or_more_batches_of_data_from_a_configured_datasource.py data_connector_query",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_get_one_or_more_batches_of_data_from_a_configured_datasource.py first 5 batches from 2020",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_get_one_or_more_batches_of_data_from_a_configured_datasource.py get_batch_list",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_get_one_or_more_batches_of_data_from_a_configured_datasource.py get_validator",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_get_one_or_more_batches_of_data_from_a_configured_datasource.py index data_connector_query",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_get_one_or_more_batches_of_data_from_a_configured_datasource.py print(validator.batches)",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_get_one_or_more_batches_of_data_from_a_configured_datasource.py print(validator.head())",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_get_one_or_more_batches_of_data_from_a_configured_datasource.py twelve batches from 2020",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/files/yaml_example_complete.py add_datasource",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/files/yaml_example_complete.py batch_filter_parameters",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/files/yaml_example_complete.py batch_request",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/files/yaml_example_complete.py datasource_yaml",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/files/yaml_example_complete.py get_context",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/files/yaml_example_complete.py imports",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/files/yaml_example_complete.py sample_using_random 10 pct",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/files/yaml_example_complete.py sampling batch size",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/files/yaml_example_complete.py split_on_column_value passenger_count",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/files/yaml_example_complete.py test_yaml_config",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/files/yaml_example_gradual.py add configureed asset data connector to datasource",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/files/yaml_example_gradual.py add_datasource",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/files/yaml_example_gradual.py another_buggy_data_connector_yaml",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/files/yaml_example_gradual.py buggy_data_connector_yaml",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/files/yaml_example_gradual.py configured_data_connector_yaml add granular group_names",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/files/yaml_example_gradual.py configured_data_connector_yaml only by filename and type",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/files/yaml_example_gradual.py datasource_yaml",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/files/yaml_example_gradual.py get_available_data_asset_names",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/files/yaml_example_gradual.py get_context",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/files/yaml_example_gradual.py imports",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/files/yaml_example_gradual.py test_yaml_config",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/sql_database/yaml_example_complete.py add_datasource",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/sql_database/yaml_example_complete.py assertions",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/sql_database/yaml_example_complete.py batch_request",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/sql_database/yaml_example_complete.py datasource_yaml",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/sql_database/yaml_example_complete.py get_context",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/sql_database/yaml_example_complete.py imports",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/sql_database/yaml_example_complete.py test_yaml_config",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/sql_database/yaml_example_gradual.py add_datasource",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/sql_database/yaml_example_gradual.py add_datasource_2",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/sql_database/yaml_example_gradual.py buggy_datasource_yaml",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/sql_database/yaml_example_gradual.py datasource_yaml",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/sql_database/yaml_example_gradual.py datasource_yaml_introspection",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/sql_database/yaml_example_gradual.py datasource_yaml_tables",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/sql_database/yaml_example_gradual.py datasource_yaml_tables_partitioners",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/sql_database/yaml_example_gradual.py get_available_data_asset_names",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/sql_database/yaml_example_gradual.py get_context",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/sql_database/yaml_example_gradual.py imports",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/sql_database/yaml_example_gradual.py test_yaml_config",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/sql_database/yaml_example_gradual.py test_yaml_config_2",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/sql_database/yaml_example_gradual.py test_yaml_config_3",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/sql_database/yaml_example_gradual.py test_yaml_config_4",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/in_memory/pandas_python_example.py add_datasource",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/in_memory/pandas_python_example.py datasource_config",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/in_memory/pandas_python_example.py test_yaml_config",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/in_memory/spark_python_example.py add datasource",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/in_memory/spark_python_example.py batch request",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/in_memory/spark_python_example.py config",
    "tests/integration/docusaurus/connecting_to_your_data/in_memory/spark_python_example.py test yaml_config",  # noqa: E501
    "tests/integration/docusaurus/connecting_to_your_data/in_memory/spark_python_example.py validator",  # noqa: E501
    "docs/docusaurus/docs/snippets/aws_cloud_storage_pandas.py get_batch_list",
    "docs/docusaurus/docs/snippets/aws_cloud_storage_pandas.py get_batch_request",
    "docs/docusaurus/docs/snippets/aws_cloud_storage_spark.py add_data_docs_store",
    "docs/docusaurus/docs/snippets/aws_cloud_storage_spark.py add_expectations",
    "docs/docusaurus/docs/snippets/aws_cloud_storage_spark.py build_docs",
    "docs/docusaurus/docs/snippets/aws_cloud_storage_spark.py create_checkpoint",
    "docs/docusaurus/docs/snippets/aws_cloud_storage_spark.py existing_expectations_store",
    "docs/docusaurus/docs/snippets/aws_cloud_storage_spark.py existing_validations_store",
    "docs/docusaurus/docs/snippets/aws_cloud_storage_spark.py get_batch_list",
    "docs/docusaurus/docs/snippets/aws_cloud_storage_spark.py get_batch_request",
    "docs/docusaurus/docs/snippets/aws_cloud_storage_spark.py get_validator",
    "docs/docusaurus/docs/snippets/aws_cloud_storage_spark.py imports",
    "docs/docusaurus/docs/snippets/aws_cloud_storage_spark.py new_expectations_store",
    "docs/docusaurus/docs/snippets/aws_cloud_storage_spark.py new_validations_store",
    "docs/docusaurus/docs/snippets/aws_cloud_storage_spark.py run checkpoint",
    "docs/docusaurus/docs/snippets/aws_cloud_storage_spark.py save_expectations",
    "docs/docusaurus/docs/snippets/aws_cloud_storage_spark.py set_new_validations_store",
    "docs/docusaurus/docs/snippets/aws_redshift_deployment_patterns.py add_data_docs_store",
    "docs/docusaurus/docs/snippets/aws_redshift_deployment_patterns.py create_checkpoint",
    "docs/docusaurus/docs/snippets/aws_redshift_deployment_patterns.py existing_expectations_store",
    "docs/docusaurus/docs/snippets/aws_redshift_deployment_patterns.py existing_validations_store",
    "docs/docusaurus/docs/snippets/aws_redshift_deployment_patterns.py imports",
    "docs/docusaurus/docs/snippets/aws_redshift_deployment_patterns.py new_expectations_store",
    "docs/docusaurus/docs/snippets/aws_redshift_deployment_patterns.py new_validations_store",
    "docs/docusaurus/docs/snippets/aws_redshift_deployment_patterns.py run checkpoint",
    "docs/docusaurus/docs/snippets/aws_redshift_deployment_patterns.py save_expectations",
    "docs/docusaurus/docs/snippets/aws_redshift_deployment_patterns.py set_new_validations_store",
    "docs/docusaurus/docs/snippets/aws_redshift_deployment_patterns.py validator_calls",
    "docs/docusaurus/docs/snippets/databricks_deployment_patterns_dataframe_python_configs.py choose context_root_dir",  # noqa: E501
    "docs/docusaurus/docs/snippets/databricks_deployment_patterns_dataframe_python_configs.py imports",  # noqa: E501
    "docs/docusaurus/docs/snippets/databricks_deployment_patterns_dataframe_python_configs.py run checkpoint",  # noqa: E501
    "docs/docusaurus/docs/snippets/databricks_deployment_patterns_dataframe_python_configs.py set up context",  # noqa: E501
    "docs/docusaurus/docs/snippets/databricks_deployment_patterns_dataframe_yaml_configs.py add datasource config",  # noqa: E501
    "docs/docusaurus/docs/snippets/databricks_deployment_patterns_dataframe_yaml_configs.py add expectations",  # noqa: E501
    "docs/docusaurus/docs/snippets/databricks_deployment_patterns_dataframe_yaml_configs.py create batch request",  # noqa: E501
    "docs/docusaurus/docs/snippets/databricks_deployment_patterns_dataframe_yaml_configs.py datasource config",  # noqa: E501
    "docs/docusaurus/docs/snippets/databricks_deployment_patterns_dataframe_yaml_configs.py get validator",  # noqa: E501
    "docs/docusaurus/docs/snippets/databricks_deployment_patterns_dataframe_yaml_configs.py imports",  # noqa: E501
    "docs/docusaurus/docs/snippets/databricks_deployment_patterns_dataframe_yaml_configs.py root directory",  # noqa: E501
    "docs/docusaurus/docs/snippets/databricks_deployment_patterns_dataframe_yaml_configs.py run checkpoint",  # noqa: E501
    "docs/docusaurus/docs/snippets/databricks_deployment_patterns_dataframe_yaml_configs.py save suite",  # noqa: E501
    "docs/docusaurus/docs/snippets/databricks_deployment_patterns_dataframe_yaml_configs.py set up context",  # noqa: E501
    "docs/docusaurus/docs/snippets/databricks_deployment_patterns_dataframe_yaml_configs.py test datasource config",  # noqa: E501
    "docs/docusaurus/docs/snippets/databricks_deployment_patterns_file_python_configs.py add expectations",  # noqa: E501
    "docs/docusaurus/docs/snippets/databricks_deployment_patterns_file_python_configs.py get validator",  # noqa: E501
    "docs/docusaurus/docs/snippets/databricks_deployment_patterns_file_python_configs.py save suite",  # noqa: E501
    "docs/docusaurus/docs/oss/guides/connecting_to_your_data/fluent/database/gcp_deployment_patterns_file_bigquery.py existing_expectations_store",  # noqa: E501
    "docs/docusaurus/docs/oss/guides/connecting_to_your_data/fluent/database/gcp_deployment_patterns_file_bigquery.py get_context",  # noqa: E501
    "docs/docusaurus/docs/oss/guides/connecting_to_your_data/fluent/database/gcp_deployment_patterns_file_gcs.py batch_request",  # noqa: E501
    "docs/docusaurus/docs/snippets/postgres_deployment_patterns.py pg_batch_request",
    "tests/integration/docusaurus/expectations/how_to_create_and_edit_expectations_with_a_profiler build_suite",  # noqa: E501
    "tests/integration/docusaurus/expectations/how_to_create_and_edit_expectations_with_a_profiler create_asset",  # noqa: E501
    "tests/integration/docusaurus/expectations/how_to_create_and_edit_expectations_with_a_profiler create_profiler",  # noqa: E501
    "tests/integration/docusaurus/expectations/how_to_create_and_edit_expectations_with_a_profiler create_validator",  # noqa: E501
    "tests/integration/docusaurus/expectations/how_to_create_and_edit_expectations_with_a_profiler e2e",  # noqa: E501
    "tests/integration/docusaurus/expectations/how_to_create_and_edit_expectations_with_a_profiler get_asset",  # noqa: E501
    "tests/integration/docusaurus/expectations/how_to_create_and_edit_expectations_with_a_profiler name_suite",  # noqa: E501
    "tests/integration/docusaurus/expectations/how_to_create_and_edit_expectations_with_a_profiler optional_params",  # noqa: E501
    "tests/integration/docusaurus/expectations/how_to_create_and_edit_expectations_with_a_profiler semantic",  # noqa: E501
    "docs/docusaurus/docs/snippets/checkpoints_and_actions.py assert_suite",
    "docs/docusaurus/docs/snippets/checkpoints_and_actions.py checkpoint_example",
    "docs/docusaurus/docs/snippets/checkpoints_and_actions.py keys_passed_at_runtime",
    "docs/docusaurus/docs/snippets/checkpoints_and_actions.py nesting_with_defaults",
    "docs/docusaurus/docs/snippets/checkpoints_and_actions.py no_nesting",
    "docs/docusaurus/docs/snippets/checkpoints_and_actions.py run_checkpoint_5",
    "docs/docusaurus/docs/snippets/checkpoints_and_actions.py using_simple_checkpoint",
    "docs/docusaurus/docs/snippets/checkpoints_and_actions.py using_template",
    "docs/docusaurus/docs/snippets/checkpoints.py create_and_run",
    "docs/docusaurus/docs/snippets/checkpoints.py save",
    "docs/docusaurus/docs/snippets/checkpoints.py setup",
    "docs/docusaurus/docs/oss/guides/setup/configuring_data_docs/data_docs.py data_docs",
    "docs/docusaurus/docs/oss/guides/setup/configuring_data_docs/data_docs.py data_docs_site",
    "docs/docusaurus/docs/oss/guides/setup/configuring_data_contexts/how_to_configure_credentials.py add_credential_from_yml",  # noqa: E501
    "docs/docusaurus/docs/oss/guides/setup/configuring_data_contexts/how_to_configure_credentials.py add_credentials_as_connection_string",  # noqa: E501
    "docs/docusaurus/docs/oss/guides/setup/configuring_data_contexts/how_to_configure_credentials.py export_env_vars",  # noqa: E501
    "docs/docusaurus/docs/oss/guides/setup/configuring_data_docs/how_to_host_and_share_data_docs_on_gcs.py build data docs command",  # noqa: E501
    "docs/docusaurus/docs/oss/guides/setup/configuring_data_docs/how_to_host_and_share_data_docs_on_gcs.py build data docs output",  # noqa: E501
    "docs/docusaurus/docs/oss/guides/setup/configuring_data_docs/how_to_host_and_share_data_docs_on_gcs.py create bucket command",  # noqa: E501
    "docs/docusaurus/docs/oss/guides/setup/configuring_data_docs/how_to_host_and_share_data_docs_on_gcs.py create bucket output",  # noqa: E501
    "docs/docusaurus/docs/oss/guides/setup/configuring_data_docs/how_to_host_and_share_data_docs_on_gcs.py gcloud app deploy",  # noqa: E501
    "docs/docusaurus/docs/oss/guides/setup/configuring_data_docs/how_to_host_and_share_data_docs_on_gcs.py gcloud login and set project",  # noqa: E501
    "docs/docusaurus/docs/oss/guides/setup/configuring_metadata_stores/how_to_configure_a_validation_result_store_in_gcs.py copy_validation_command",  # noqa: E501
    "docs/docusaurus/docs/oss/guides/setup/configuring_metadata_stores/how_to_configure_a_validation_result_store_in_gcs.py copy_validation_output",  # noqa: E501
    "docs/docusaurus/docs/oss/guides/setup/configuring_metadata_stores/how_to_configure_a_validation_result_store_in_gcs.py list_validation_stores_command",  # noqa: E501
    "docs/docusaurus/docs/oss/guides/setup/configuring_metadata_stores/how_to_configure_a_validation_result_store_in_gcs.py list_validation_stores_output",  # noqa: E501
    "docs/docusaurus/docs/oss/guides/setup/configuring_metadata_stores/how_to_configure_an_expectation_store_in_gcs.py copy_expectation_command",  # noqa: E501
    "docs/docusaurus/docs/oss/guides/setup/configuring_metadata_stores/how_to_configure_an_expectation_store_in_gcs.py copy_expectation_output",  # noqa: E501
    "docs/docusaurus/docs/oss/guides/setup/configuring_metadata_stores/how_to_configure_an_expectation_store_in_gcs.py list_expectation_stores_command",  # noqa: E501
    "docs/docusaurus/docs/oss/guides/setup/configuring_metadata_stores/how_to_configure_an_expectation_store_in_gcs.py list_expectation_stores_output",  # noqa: E501
    "docs/docusaurus/docs/oss/guides/setup/configuring_metadata_stores/how_to_configure_an_expectation_store_in_gcs.py list_expectation_suites_command",  # noqa: E501
    "tests/integration/docusaurus/setup/setup_overview.py setup",
    "docs/docusaurus/docs/oss/templates/script_example.py full",
    "tests/integration/docusaurus/tutorials/getting-started/getting_started.py checkpoint_yaml_config",  # noqa: E501
    "tests/integration/docusaurus/tutorials/getting-started/getting_started.py datasource_yaml",
    "tests/integration/docusaurus/tutorials/quickstart/v1_pandas_quickstart.py connect_to_data",
    "tests/integration/docusaurus/tutorials/quickstart/v1_pandas_quickstart.py create_expectation",
    "tests/integration/docusaurus/tutorials/quickstart/v1_pandas_quickstart.py get_context",
    "tests/integration/docusaurus/tutorials/quickstart/v1_pandas_quickstart.py import_gx",
    "tests/integration/docusaurus/tutorials/quickstart/v1_pandas_quickstart.py update_expectation",
    "tests/integration/docusaurus/tutorials/quickstart/v1_sql_quickstart.py connect_to_data",
    "tests/integration/docusaurus/tutorials/quickstart/v1_sql_quickstart.py create_expectation",
    "tests/integration/docusaurus/tutorials/quickstart/v1_sql_quickstart.py get_context",
    "tests/integration/docusaurus/tutorials/quickstart/v1_sql_quickstart.py import_gx",
    "tests/integration/docusaurus/tutorials/quickstart/v1_sql_quickstart.py update_expectation",
    "tests/integration/docusaurus/validation/validator/how_to_create_and_edit_expectations_with_instant_feedback_block_config.py build_batch_request",  # noqa: E501
    "tests/integration/docusaurus/validation/validator/how_to_create_and_edit_expectations_with_instant_feedback_block_config.py get_context",  # noqa: E501
    "tests/integration/docusaurus/validation/validator/how_to_create_and_edit_expectations_with_instant_feedback_block_config.py get_validator_and_inspect_data",  # noqa: E501
    "tests/integration/docusaurus/validation/validator/how_to_create_and_edit_expectations_with_instant_feedback_block_config.py imports",  # noqa: E501
    "tests/integration/docusaurus/validation/validator/how_to_create_and_edit_expectations_with_instant_feedback_block_config.py inspect_data_no_jupyter",  # noqa: E501
    "tests/integration/docusaurus/validation/validator/how_to_create_and_edit_expectations_with_instant_feedback_block_config.py interactive_validation",  # noqa: E501
    "tests/integration/docusaurus/validation/validator/how_to_create_and_edit_expectations_with_instant_feedback_block_config.py interactive_validation_no_jupyter",  # noqa: E501
    "tests/integration/docusaurus/validation/validator/how_to_create_and_edit_expectations_with_instant_feedback_block_config.py save_expectation_suite",  # noqa: E501
    "tests/integration/fixtures/gcp_deployment/great_expectations/great_expectations.yml expectations_GCS_store",  # noqa: E501
    "tests/integration/fixtures/gcp_deployment/great_expectations/great_expectations.yml expectations_store_name",  # noqa: E501
    "tests/integration/fixtures/gcp_deployment/great_expectations/great_expectations.yml gs_site",
    "tests/integration/fixtures/gcp_deployment/great_expectations/great_expectations.yml validations_GCS_store",  # noqa: E501
    "tests/integration/fixtures/gcp_deployment/great_expectations/great_expectations.yml validations_store_name",  # noqa: E501
]


def check_dependencies(*deps: str) -> None:
    for dep in deps:
        if not shutil.which(dep):
            raise Exception(f"Must have `{dep}` installed in PATH to run {__file__}")  # noqa: TRY002, TRY003


def get_snippet_definitions(target_dir: pathlib.Path) -> List[str]:
    try:
        res_snippets = subprocess.run(  # noqa: PLW1510
            [
                "grep",
                "--recursive",
                "--binary-files=without-match",
                "--no-filename",
                "--ignore-case",
                "--word-regexp",
                "--regexp",
                r"^# <snippet .*name=.*>",
                str(target_dir),
            ],
            text=True,
            capture_output=True,
        )
        res_snippet_names = subprocess.run(  # noqa: PLW1510
            ["sed", 's/.*name="//; s/">//; s/version-[0-9\\.]* //'],
            text=True,
            input=res_snippets.stdout,
            capture_output=True,
        )
        return res_snippet_names.stdout.splitlines()
    except subprocess.CalledProcessError as e:
        raise RuntimeError(  # noqa: TRY003
            f"Command {e.cmd} returned with error (code {e.returncode}): {e.output}"
        ) from e


def get_snippets_used(target_dir: pathlib.Path) -> List[str]:
    try:
        res_snippet_usages = subprocess.run(  # noqa: PLW1510
            [
                "grep",
                "--recursive",
                "--binary-files=without-match",
                "--no-filename",
                "--exclude-dir=versioned_code",
                "--exclude-dir=versioned_docs",
                "--ignore-case",
                "-E",
                "--regexp",
                r"```(python|yaml).*name=",
                str(target_dir),
            ],
            text=True,
            capture_output=True,
        )
        res_snippet_used_names = subprocess.run(  # noqa: PLW1510
            ["sed", 's/.*="//; s/".*//; s/version-[0-9\\.]* //'],
            text=True,
            input=res_snippet_usages.stdout,
            capture_output=True,
        )
        return res_snippet_used_names.stdout.splitlines()
    except subprocess.CalledProcessError as e:
        raise RuntimeError(  # noqa: TRY003
            f"Command {e.cmd} returned with error (code {e.returncode}): {e.output}"
        ) from e


def main() -> None:
    check_dependencies("grep", "sed")
    project_root = pathlib.Path(__file__).parent.parent.parent
    docs_dir = project_root / "docs"
    assert docs_dir.exists()
    tests_dir = project_root / "tests"
    assert tests_dir.exists()
    new_violations = sorted(
        set(get_snippet_definitions(tests_dir))
        .difference(set(get_snippets_used(docs_dir)))
        .difference(set(IGNORED_VIOLATIONS))
    )
    if new_violations:
        print(f"[ERROR] Found {len(new_violations)} snippets which are not used within a doc file.")
        for line in new_violations:
            print(line)
        sys.exit(1)


if __name__ == "__main__":
    main()
