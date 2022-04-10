from scraper import *
from graphics import *
import pickle

data = get_data('kalkulator413', 'monthly')

with open('data', 'wb') as f: 
    pickle.dump(data, f)

with open('data', 'rb') as f: 
    data  = pickle.load(f)

graphics(data)