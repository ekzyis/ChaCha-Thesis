#!/usr/bin/env python

import csv
from dataclasses import dataclass
from typing import List
from pprint import pprint

@dataclass
class DataPoint:
  action: int
  samples: List[int]

  def average(self):
    return sum(self.samples)/len(self.samples)

@dataclass
class CacheDataPoint(DataPoint):
  cache: bool

@dataclass
class PlotData:
  name: str
  data: List[DataPoint]

def read_data(file: str) -> PlotData:
  with open(file) as csvfile:
    r = csv.reader(csvfile, delimiter='|')
    data = []
    for row in r:
      if len(row) == 3:
        data.append(CacheDataPoint(action=row[0], cache=row[1] == 'x', samples=row[2].split(',')))
      else:
        data.append(DataPoint(action=row[0], samples=row[1].split(',')))
    return PlotData(name=file.replace('benchmark/', '').replace('.benchmark.csv', ''), data=data)

data: List[PlotData] = []
data.append(read_data('benchmark/navsystem-cache-qr.benchmark.csv'))
data.append(read_data('benchmark/navsystem-cache-round.benchmark.csv'))
data.append(read_data('benchmark/navsystem-central.benchmark.csv'))
data.append(read_data('benchmark/navsystem-linear.benchmark.csv'))

pprint(data)