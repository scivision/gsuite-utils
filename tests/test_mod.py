#!/usr/bin/env python
import pytest
import gsuite as G
from pathlib import Path

R = Path(__file__).parent


def test_useradd():
    fn = R / 'newusers.xlsx'

    df = G.xls2df(fn)

# NOTE: these are obviously not good security settings, it's just for test.
    G.df2csv(df, 'test.com', 'MD5', 4, R/'newusers.csv')


if __name__ == '__main__':
    pytest.main(['-x', __file__])
