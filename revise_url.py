import pandas as pd
import re

data = pd.read_csv('mp3_urls.csv')
data = data.replace(r'http://www\.namoamitabha\.net','/proxy', regex=True)
data.to_csv('mp3_urls_2.csv', index=False)
print(data[:3])
