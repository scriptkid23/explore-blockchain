import wikipedia
from googlesearch import search
from bs4 import BeautifulSoup
import urllib.request
wikipedia.set_lang('vi')
QUESTION = ["là gì", "ở đâu", "là ai"]
data = "Tuyên quang ở đâu"
for i in QUESTION:
    if data.find(i) != -1:
        _input = data.split(i)
        print(wikipedia.summary(_input[0],sentences=2))

result = search("Tuyên quang ở đâu", lang='vi', num_results=1)
for i in result:
    print(i)
# for i in result:
#     print(i)
