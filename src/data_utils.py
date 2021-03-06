'''
Utilities for reading and writing data.
'''
import re
import functools
import datetime

import pandas as pd

from sample import Sample

# dictionaries
def get_cdr3_counter_from_file(id_, filepath):
  '''
  Given a `filepath` for a .ann file, load the data and return a {cdr3_sequence:frequency} dictionary.
  '''
  fp = f'data/ann/{filepath}'
  df = pd.read_csv(fp,
    encoding='utf_8',
    delimiter=',',
    names=['cdr3-sequence', 'frequency'],
    index_col='cdr3-sequence',
  )
  dict_ = df.to_dict()['frequency']
  counter = Sample(id_, dict_)
  return counter

def get_cdr3_counter_from_files(id_, filepaths):
  '''
  Given some filepaths, get a counter which contains the data from all the files combined.
  '''
  counters = [get_cdr3_counter_from_file(id_, fp) for fp in filepaths]
  counter = functools.reduce(Sample.__add__, counters)
  # recristen with single ID
  counter.id = id_
  return counter

# Pandas Series
def get_cdr3_series_from_file(filepath):
  '''
  Given a `filepath` for a .ann file, load the data and return a {cdr3_sequence:frequency} Series.
  '''
  fp = f'data/ann/{filepath}'
  df = pd.read_csv(fp,
    encoding='utf_8',
    delimiter=',',
    names=['cdr3-sequence', 'frequency'],
    index_col='cdr3-sequence',
  )
  return df['frequency']

def get_date_from_file_name(filename):
  # cdr3.a.A_2000_2001_d_00_47407.ann
  # cdr3.a.A_2000_2001_m_04_47407.ann
  year = int(filename[14:14+4])
  day_month_indicator = filename[19]
  days_or_months = int(filename[21:23])
  if day_month_indicator == 'd':
    days = days_or_months
    dt = datetime.datetime(year, 1, 1) + datetime.timedelta(days=days)
  elif day_month_indicator == 'm':
    months = days_or_months
    dt = datetime.datetime(year, 1, 1) + datetime.timedelta(days=365/12*months)
  else:
    raise ValueError('day month indicator was not "d" nor "m"')
  return dt

def to_beta(filepaths):
  ''' Convert alpha file names or file paths to their corresponding beta file names. '''
  new_filepaths = [re.sub(r'\.a\.', '.b.', f) for f in filepaths]
  return new_filepaths

def make_series_compatible(series_iterable):
    ''' If you have multiple series (representing samples), then we need to make them share the same CDR3 sequences, and in the same order (alphabetical), before we can do vector operations between them. '''
    # use a kluge to fill in 0 values where missing
    # create a big 0 vector with all the CDR3s
    zero_series = pd.Series(dtype=object)
    for s in series_iterable:
        zero_series.add(s, fill_value=0).subtract(s, fill_value=0)
    print('zero ser:')
    print(zero_series)
    print(list(zero_series.keys()))
    print(zero_series.values)
    # add all the CDR3s to all the series, and sort the indices alphabetically
    for s in series_iterable:
        s.add(zero_series, fill_value=0).subtract(zero_series, fill_value=0).sort_index()
        print('s:')
        print(s)
    # return the resulting series
    return series_iterable
