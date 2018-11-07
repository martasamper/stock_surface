import pytest
import sample_slopes as sample_slopes
import numpy as np
import pandas as pd


def test_get_columns_with_CLS():

    columns = ['hiCLS', 'hi', "yoooCLS", 'yoooo', 'hiCHG']

    CLS_columns, CHG_columns = sample_slopes.get_columns_with_CLS(columns)
    assert CLS_columns == ['hiCLS', 'yoooCLS']
    assert CHG_columns == ['hi', 'yoooo', 'hiCHG']


def test_sample_slopes():

    data = {'col1CHG': [3, 3, 4, 5, 7, 8, 7, 6, 5, 4],
            'col2CHG': [6, 5, 5, 6, 7, 6, 4, 3, 3, 8],
            'col3CHG': [7, 6, 4, 6, 4, 2, 4, 5, 6, 5],
            'col4CHG': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            'col5CHG': [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            'col6CHG': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            'col7CLS': [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            'col8CLS': [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            'col9CLS': [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            }

    stock_data = pd.DataFrame(data=data)
    print stock_data
    new_df_columns = sample_slopes.create_slope_sum(
        stock_data).columns

    counter = 0
    for column in new_df_columns:
        counter += 1

    # print new_df_columns
    assert counter == 13
    assert list(new_df_columns) == [u'col1CHG', u'col2CHG', u'col3CHG', u'col4CHG', u'col5CHG', u'col6CHG',
                                    u'col7CLS', u'col8CLS', u'col9CLS', u'col2slope_sum', u'col3slope_sum',
                                    u'col4slope_sum', u'col5slope_sum']


def test_get_columns_with_slope_sum():

    columns = ['hiCLS', 'hi', "yoooCLS",
               'yoooo', 'hiCHG', 'jasonrulesslope_sum', 'bahslope_sum']

    slope_sum_cols = sample_slopes.get_columns_with_slope_sum(columns)
    assert slope_sum_cols == ['jasonrulesslope_sum', 'bahslope_sum']


def test_target_values():
    data = {'col1CLS': [3, 3, 4, 5, 7, 8, 7, 6, 5, 4],
            'col2CLS': [6, 5, 5, 6, 7, 6, 4, 3, 3, 8],
            'col3CLS': [7, 6, 4, 6, 4, 2, 4, 5, 6, 5],
            'col4CLS': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            'col5CLS': [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            'col1CHG': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            'col2CHG': [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            'col3CHG': [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            'col4CHG': [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            'col5CHG': [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            'col2slope_sum': [13, 8, -3, 3, 3, 3, 3, 3, 3, 3],
            'col3slope_sum': [1, -3, 3, 5, 3, 3, 3, 3, 3, 3],
            'col4slope_sum': [9, 3, 9, 3, -3, 3, 3, 3, 3, 3],
            }
    stock_data = pd.DataFrame(data=data)
    assert sample_slopes.generate_target_values(
        stock_data, 3, "col2CLS", 2) == ([1, 1, -1, -1, -1, 1], 6)


def test_batcher():
    data = {'col1CLS': [3, 3, 4, 5, 7, 8, 7, 6, 5, 4],
            'col2CLS': [6, 5, 5, 6, 7, 6, 4, 3, 3, 8],
            'col3CLS': [7, 6, 4, 6, 4, 2, 4, 5, 6, 5],
            'col4CLS': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            'col5CLS': [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            'col1CHG': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            'col2CHG': [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            'col3CHG': [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            'col4CHG': [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            'col5CHG': [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            'col2slope_sum': [13, 8, -3, 3, 3, 3, 3, 3, 3, 3],
            'col3slope_sum': [1, -3, 3, 5, 3, 3, 3, 3, 3, 3],
            'col4slope_sum': [9, 3, 9, 3, -3, 3, 3, 3, 3, 3],
            }
    stock_data = pd.DataFrame(data=data)

    print sample_slopes.generate_target_values(
        stock_data, 3, "col2CLS", 2)

    assert len(sample_slopes.create_batch_of_slopes(
        stock_data, 'col4slope_sum', 2, 6)) == 6
    assert sample_slopes.create_batch_of_slopes(stock_data, 'col4slope_sum', 2, 6) == [
        [9, 3], [3, 9], [9, 3], [3, -3], [-3, 3], [3, 3], ]


def test_find_percent_change_calc():
    assert sample_slopes.find_percent_change(4, 2) == 1
    assert sample_slopes.find_percent_change(2, 4) == -0.5
    assert sample_slopes.find_percent_change(4, 4) == 0
    assert sample_slopes.find_percent_change(6, 1) == 5.0


def test_generate_target_values():
    data = {'col1CLS': [3, 3, 4, 5, 7, 8, 7, 6, 5, 4],
            'col2CLS': [6, 5, 5, 6, 7, 6, 4, 3, 3, 8],
            'col3CLS': [7, 6, 4, 6, 4, 2, 4, 5, 6, 5],
            'col4CLS': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            'col5CLS': [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            'col1CHG': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            'col2CHG': [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            'col3CHG': [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            'col4CHG': [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            'col5CHG': [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            'col2slope_sum': [13, 8, -3, 3, 3, 3, 3, 3, 3, 3],
            'col3slope_sum': [1, -3, 3, 5, 3, 3, 3, 3, 3, 3],
            'col4slope_sum': [9, 3, 9, 3, -3, 3, 3, 3, 3, 3],
            }
    stock_data = pd.DataFrame(data=data)

    assert sample_slopes.generate_target_values(
        stock_data, 3, 'col2CLS', 2) == ([1, 1, -1, -1, -1, 1], 6)
    assert sample_slopes.generate_target_values(
        stock_data, 3, 'col3CLS', 2) == ([1, -1, 1, 1, 1, 1], 6)


def test_generate_target_values_longer():
    """
    used to tests really long CLS lengths
    """
    data = {
        'col2CLS': [6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8, 6, 5, 5, 6, 7, 6, 4, 3, 3, 8],

    }
    stock_data = pd.DataFrame(data=data)

    sample_slopes.generate_target_values(
        stock_data, 18, 'col2CLS', 2)


def test_generate_target_values_and_sliding_window_lenth():

    data = {'col1CLS': [3, 3, 4, 5, 7, 8, 7, 6, 5, 4],
            'col2CLS': [6, 5, 5, 6, 7, 6, 4, 3, 3, 8],
            'col3CLS': [7, 6, 4, 6, 4, 2, 4, 5, 6, 5],
            'col4CLS': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            'col5CLS': [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            'col1CHG': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            'col2CHG': [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            'col3CHG': [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            'col4CHG': [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            'col5CHG': [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            'col2slope_sum': [13, 8, -3, 3, 3, 3, 3, 3, 3, 3],
            'col3slope_sum': [1, -3, 3, 5, 3, 3, 3, 3, 3, 3],
            'col4slope_sum': [9, 3, 9, 3, -3, 3, 3, 3, 3, 3],
            }
    stock_data = pd.DataFrame(data=data)

    # generate_target_values(df, batch_count, column_name, look_ahead)
    y_values = sample_slopes.generate_target_values(
        stock_data, 2, 'col4CLS', 2)

    # create_batch_of_slopes(df, batch_count, cut_length)
    x_vaules = sample_slopes.create_batch_of_slopes(
        stock_data, 'col4slope_sum', 2,   y_values[1])

    print (y_values[0]), 'len y ', len(y_values[0])
    print (x_vaules), 'len x ', len(x_vaules)

    assert len(y_values[0]) == len(x_vaules)

    y_values = sample_slopes.generate_target_values(
        stock_data, 3, 'col4CLS', 3)

    # create_batch_of_slopes(df, batch_count, cut_length)
    x_vaules = sample_slopes.create_batch_of_slopes(
        stock_data, 'col4slope_sum',  3,   y_values[1])

    print (y_values[0]), 'len y ', len(y_values[0])
    print (x_vaules), 'len x ', len(x_vaules)

    assert len(y_values[0]) == len(x_vaules)


def test_batcher_moving_average():
    data = {
            'col4slope_sum': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40],
            }
    stock_data = pd.DataFrame(data=data)

    for array in sample_slopes.create_batch_of_slopes(stock_data, 'col4slope_sum', 18, 4):
        print array

    print '----------------------------ima a line----------------------------'

    for array in sample_slopes.create_batch_of_slopes_moving_av(stock_data, 'col4slope_sum', 18, 4, 15):
        print array

    print sample_slopes.create_batch_of_slopes_moving_av(stock_data, 'col4slope_sum', 18, 4, 15) 
   
    # assert sample_slopes.create_batch_of_slopes_moving_av(stock_data, 'col4slope_sum', 5, 10) == [
    #     [9, 3], [3, 9], [9, 3], [3, -3], [-3, 3], [3, 3], ]


def test_sample_slopes_market():

    data = {'col1CHG': [3, 3, 4, 5, 7, 8, 7, 6, 5, 4],
            'col2CHG': [6, 5, 5, 6, 7, 6, 4, 3, 3, 8],
            'col3CHG': [7, 6, 4, 6, 4, 2, 4, 5, 6, 5],
            'col4CHG': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            'col5CHG': [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            'col6CHG': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            'col7CLS': [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            'col8CLS': [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            'col9CLS': [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            }

    stock_data = pd.DataFrame(data=data)
    print stock_data
    new_df_columns_dataframe = sample_slopes.create_slope_sum_market(
        stock_data)
    new_df_columns = new_df_columns_dataframe.columns
    print new_df_columns , ' new DF columns'

    counter = 0
    for column in new_df_columns:
        counter += 1

    # print new_df_columns
    assert counter == 13
    assert list(new_df_columns) == [u'col1CHG', u'col2CHG', u'col3CHG', u'col4CHG', u'col5CHG', u'col6CHG',
                                    u'col7CLS', u'col8CLS', u'col9CLS', u'col2slope_sum', u'col3slope_sum',
                                    u'col4slope_sum', u'col5slope_sum']

    print new_df_columns_dataframe['col2slope_sum'].tolist() == [15.0,11.0,12.0,14.0,19.0,15.0,4.0,-1.0,-1.0,26.0]