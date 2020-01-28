import logging

# PYTHON 2 - py2 - update to ABC direct use rather than __metaclass__ once we drop py2 support
from abc import ABCMeta

from great_expectations.core import DataContextKey, BatchKwargs
from great_expectations.exceptions import InvalidBatchKwargsError, InvalidBatchIdError

logger = logging.getLogger(__name__)


class BatchFingerprint(DataContextKey):
    def __init__(self, partition_id, fingerprint):
        self.partition_id = partition_id
        self.fingerprint = fingerprint

    def to_tuple(self):
        return self.partition_id, self.fingerprint
#
# class BatchFingerprint(OrderedDataContextKey):
#     _allowed_keys = OrderedDataContextKey._allowed_keys | {
#         "partition_id",
#         "fingerprint"
#     }
#     _required_keys = OrderedDataContextKey._required_keys | {
#         "partition_id",
#         "fingerprint"
#     }
#     _key_types = copy.copy(OrderedDataContextKey._key_types)
#     _key_types.update({
#         "partition_id": string_types,
#         "fingerprint": string_types
#     })
#     _key_order = copy.copy(OrderedDataContextKey._key_order)
#     _key_order.extend(["partition_id", "fingerprint"])

class BatchMarkers(BatchKwargs):
    """A BatchMarkers is a special type of BatchKwargs (so that it has a batch_fingerprint) but it generally does
    NOT require specific keys and instead captures information about the OUTPUT of a datasource's fetch
    process, such as the timestamp at which a query was executed."""
    def __init__(self, *args, **kwargs):
        super(BatchMarkers, self).__init__(*args, **kwargs)
        if "ge_load_time" not in self:
            raise InvalidBatchIdError("BatchMarkers requires a ge_load_time")

    @property
    def ge_load_time(self):
        return self.get("ge_load_time")


class PandasDatasourceBatchKwargs(BatchKwargs):
    __metaclass__ = ABCMeta
    """This is an abstract class and should not be instantiated. It's relevant for testing whether
    a subclass is allowed
    """
    pass


class SparkDFDatasourceBatchKwargs(BatchKwargs):
    __metaclass__ = ABCMeta
    """This is an abstract class and should not be instantiated. It's relevant for testing whether
    a subclass is allowed
    """
    pass


class SqlAlchemyDatasourceBatchKwargs(BatchKwargs):
    __metaclass__ = ABCMeta
    """This is an abstract class and should not be instantiated. It's relevant for testing whether
    a subclass is allowed
    """
    @property
    def schema(self):
        return self.get("schema")


class PathBatchKwargs(PandasDatasourceBatchKwargs, SparkDFDatasourceBatchKwargs):
    def __init__(self, *args, **kwargs):
        super(PathBatchKwargs, self).__init__(*args, **kwargs)
        if "path" not in self:
            raise InvalidBatchKwargsError("PathBatchKwargs requires a path element")

    @property
    def path(self):
        return self.get("path")

    @property
    def reader_method(self):
        return self.get("reader_method")


class S3BatchKwargs(PandasDatasourceBatchKwargs, SparkDFDatasourceBatchKwargs):
    def __init__(self, *args, **kwargs):
        super(S3BatchKwargs, self).__init__(*args, **kwargs)
        if "s3" not in self:
            raise InvalidBatchKwargsError("S3BatchKwargs requires a path element")

    @property
    def s3(self):
        return self.get("s3")

    @property
    def reader_method(self):
        return self.get("reader_method")

class InMemoryBatchKwargs(PandasDatasourceBatchKwargs, SparkDFDatasourceBatchKwargs):
    def __init__(self, *args, **kwargs):
        super(InMemoryBatchKwargs, self).__init__(*args, **kwargs)
        if "dataset" not in self:
            raise InvalidBatchKwargsError("InMemoryBatchKwargs requires a 'dataset' element")

    @property
    def dataset(self):
        return self.get("dataset")


class PandasDatasourceInMemoryBatchKwargs(InMemoryBatchKwargs):
    def __init__(self, *args, **kwargs):
        super(PandasDatasourceInMemoryBatchKwargs, self).__init__(*args, **kwargs)
        import pandas as pd
        if not isinstance(self["dataset"], pd.DataFrame):
            raise InvalidBatchKwargsError("PandasDatasourceInMemoryBatchKwargs 'dataset' must be a pandas DataFrame")


class SparkDFDatasourceInMemoryBatchKwargs(InMemoryBatchKwargs):
    def __init__(self, *args, **kwargs):
        super(SparkDFDatasourceInMemoryBatchKwargs, self).__init__(*args, **kwargs)
        try:
            import pyspark
        except ImportError:
            raise InvalidBatchKwargsError(
                "SparkDFDatasourceInMemoryBatchKwargs requires a valid pyspark installation, but pyspark import failed."
            )
        if not isinstance(self["dataset"], pyspark.sql.DataFrame):
            raise InvalidBatchKwargsError("SparkDFDatasourceInMemoryBatchKwargs 'dataset' must be a spark DataFrame")


class SqlAlchemyDatasourceTableBatchKwargs(SqlAlchemyDatasourceBatchKwargs):
    def __init__(self, *args, **kwargs):
        super(SqlAlchemyDatasourceTableBatchKwargs, self).__init__(*args, **kwargs)
        if "table" not in self:
            raise InvalidBatchKwargsError("SqlAlchemyDatasourceTableBatchKwargs requires a 'table' element")

    @property
    def table(self):
        return self.get("table")


class SqlAlchemyDatasourceQueryBatchKwargs(SqlAlchemyDatasourceBatchKwargs):
    def __init__(self, *args, **kwargs):
        super(SqlAlchemyDatasourceQueryBatchKwargs, self).__init__(*args, **kwargs)
        if "query" not in self:
            raise InvalidBatchKwargsError("SqlAlchemyDatasourceQueryBatchKwargs requires a 'query' element")

    @property
    def query(self):
        return self.get("query")


class SparkDFDatasourceQueryBatchKwargs(SparkDFDatasourceBatchKwargs):
    def __init__(self, *args, **kwargs):
        super(SparkDFDatasourceQueryBatchKwargs, self).__init__(*args, **kwargs)
        if "query" not in self:
            raise InvalidBatchKwargsError("SparkDFDatasourceQueryBatchKwargs requires a 'query' element")

    @property
    def query(self):
        return self.get("query")