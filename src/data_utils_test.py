import datetime

from sample import Sample
from data_utils import *
from data_utils import get_cdr3_series_from_file as get_series

def test_get_cdr3_counter_from_file():
  assert get_cdr3_counter_from_file('A', 'cdr3.test.ann') == Sample('A', {
    'cAVRDRVGGGNKLTf': 23230,
    'cAMSTADKLIf': 8493,
  })

def test_get_cdr3_counter_from_files():
  assert get_cdr3_counter_from_files('G', ['cdr3.test.ann', 'cdr3.test2.ann']) == Sample('G', {
    'cAVRDRVGGGNKLTf': 23230,
    'cAVRDRVGGGNKLTg': 23230,
    'cAMSTADKLIf': 8493*2,
  })

def test_get_date_from_file_name():
  # we are using 365/12 days per month
  # it's a bit weird and we should change it if we need to do anything fancy
  assert get_date_from_file_name('cdr3.a.A_2000_2001_d_00_47407.ann') == datetime.datetime(2001, 1, 1)
  assert get_date_from_file_name('cdr3.a.A_2017_2018_d_00_53535.ann') == datetime.datetime(2018, 1, 1)
  assert get_date_from_file_name('cdr3.a.A_2017_2018_d_07_11143.ann') == datetime.datetime(2018, 1, 8)
  assert get_date_from_file_name('cdr3.a.A_2017_2018_d_28_44887.ann') == datetime.datetime(2018, 1, 29)
  assert get_date_from_file_name('cdr3.a.A_2017_2018_m_04_73516.ann') == datetime.datetime(2018, 5, 2, 16)

def test_to_beta():
  assert to_beta(['cdr3.a.A_2017_2018_m_04_73516.ann']) == ['cdr3.b.A_2017_2018_m_04_73516.ann']

def test_make_series_compatible():
  a = get_series('cdr3.test4.ann')
  b = get_series('cdr3.test5.ann')
  a,b = make_series_compatible([a, b])

if __name__ == '__main__':
  test_make_series_compatible()
