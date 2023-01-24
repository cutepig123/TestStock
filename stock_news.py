import os, sys

def get_stock_news(stock_id:int):
	url = 'http://www.aastocks.com/tc/stocks/analysis/stock-aafn/%.5d/0/all/1'%stock_id
	command = f'curl -s {url} | pandoc -f html -t plain >1.txt'
	print(command)
	os.system(command)
	data = open('1.txt' ,'r', encoding='utf-8').read()
	p1 = data.find('AAAASTOCKS新聞')
	if p1<0: return ''
	p2 = data.find('最HIT熱話', p1)
	if p2<0: 
		news_data = data[p1:]
	else:
		news_data = data[p1:p2]
	news_datas = news_data.split('AAAASTOCKS新聞')
	news_datas = [x.replace('\n', ' ').strip() for x in news_datas]
	news_datas.append(url)
	return '\n\n' + '\n* '.join(news_datas) + '\n\n'
	
#print(get_stock_news(522))
