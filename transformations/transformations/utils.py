from pyspark.sql import DataFrame


def are_dfs_equal(df1: DataFrame, df2: DataFrame):
    return set(df1.columns) == set(df2.columns) \
        and df1.subtract(df2).collect() == []
