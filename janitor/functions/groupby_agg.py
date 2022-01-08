from typing import Callable, List, Union
import pandas_flavor as pf
import pandas as pd

from janitor.utils import deprecated_alias


@pf.register_dataframe_method
@deprecated_alias(new_column="new_column_name", agg_column="agg_column_name")
def groupby_agg(
    df: pd.DataFrame,
    by: Union[List, Callable, str],
    new_column_name: str,
    agg_column_name: str,
    agg: Union[Callable, str],
    dropna: bool = True,
) -> pd.DataFrame:
    """Shortcut for assigning a groupby-transform to a new column.

    This method does not mutate the original DataFrame.

    Intended to be the method-chaining equivalent of:

    ```python
    df = df.assign(...=df.groupby(...)[...].transform(...))
    ```

    Example: Basic usage.

        >>> import pandas as pd
        >>> import janitor
        >>> df = pd.DataFrame({
        ...     "item": ["shoe", "shoe", "bag", "shoe", "bag"],
        ...     "quantity": [100, 120, 75, 200, 25],
        ... })
        >>> df.groupby_agg(
        ...     by="item",
        ...     agg="mean",
        ...     agg_column_name="quantity",
        ...     new_column_name="avg_quantity",
        ... )
           item  quantity  avg_quantity
        0  shoe       100         140.0
        1  shoe       120         140.0
        2   bag        75          50.0
        3  shoe       200         140.0
        4   bag        25          50.0

    Example: Set `dropna=False` to compute the aggregation, treating the null
    values in the `by` column as an isolated "group".

        >>> import pandas as pd
        >>> import janitor
        >>> df = pd.DataFrame({
        ...     "x": ["a", "a", None, "b"], "y": [9, 9, 9, 9],
        ... })
        >>> df.groupby_agg(
        ...     by="x",
        ...     agg="count",
        ...     agg_column_name="y",
        ...     new_column_name="y_count",
        ...     dropna=False,
        ... )
              x  y  y_count
        0     a  9        2
        1     a  9        2
        2  None  9        1
        3     b  9        1

    :param df: A pandas DataFrame.
    :param by: Column(s) to groupby on, will be passed into `DataFrame.groupby`.
    :param new_column_name: Name of the aggregation output column.
    :param agg_column_name: Name of the column to aggregate over.
    :param agg: How to aggregate.
    :param dropna: Whether or not to include null values, if present in the
        `by` column(s). Default is True (null values in `by` are assigned NaN in
        the new column).
    :returns: A pandas DataFrame.
    """  # noqa: E501

    return df.assign(
        **{
            new_column_name: df.groupby(by, dropna=dropna)[
                agg_column_name
            ].transform(agg),
        }
    )