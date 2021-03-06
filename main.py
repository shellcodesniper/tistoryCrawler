import requests
from bs4 import BeautifulSoup
import requests
from openpyxl import Workbook

def prepare_session():
	user_agent = 'Mozilla/5.0 & (Windows & NT & 6.3& WOW64) & AppleWebKit/537.36&(KHTML, & like & Gecko) & Chrome/30.0.1599.101 & Safari/537.36'
	session = requests.session()
	session.headers.update({'referer': None, 'User-agent': user_agent})
	return session

def findSubject(soup):
	predictedTarget = []

	# for item in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5']):
	predictedSoupList = []
	

	# if(len(soup.select('strong[class*="title"]')) != 0):
	# 	predictedSoupList.append(soup.select('strong[class*="title"]'))
	# if(len(soup.select('h1[class*="title"]')) != 0):
	# 	predictedSoupList.append(soup.select('h1[class*="title"]'))
	
	selector = '[class*="txt_sub_tit"]'
	if(len(soup.select(selector)) != 0):
		predictedSoupList.append(soup.select(selector))
	
	selector = '[class*="title_view"]'
	if(len(soup.select(selector)) != 0):
		predictedSoupList.append(soup.select(selector))
	
	selector = '[class*="tit_post"]'
	if(len(soup.select(selector)) != 0):
		predictedSoupList.append(soup.select(selector))

	selector = '[class*="hd-heading"]'
	if(len(soup.select(selector)) != 0):
		predictedSoupList.append(soup.select(selector))

	selector = '[class*="gh-text"]'
	if(len(soup.select(selector)) != 0):
		predictedSoupList.append(soup.select(selector))

	selector = '[class*="headline"]'
	if(len(soup.select(selector)) != 0):
		predictedSoupList.append(soup.select(selector))

	selector = '[class*="jb-content-title"]'
	if(len(soup.select(selector)) != 0):
		predictedSoupList.append(soup.select(selector))

	selector = '[class*="titleWrap"]'
	if(len(soup.select(selector)) != 0):
		predictedSoupList.append(soup.select(selector))

	selector = '[class*="post-title"]'
	if(len(soup.select(selector)) != 0):
		predictedSoupList.append(soup.select(selector))

	selector = '[class*="title"]'
	if(len(soup.select(selector)) != 0):
		predictedSoupList.append(soup.select(selector))

	selector = '[class*="article-header"]'
	if(len(soup.select(selector)) != 0):
		predictedSoupList.append(soup.select(selector))

	# selector = '[class*="tit_post"]'
	# if(len(soup.select(selector)) != 0):
	# 	predictedSoupList.append(soup.select(selector))

	# selector = '[class*="tit_post"]'
	# if(len(soup.select(selector)) != 0):
	# 	predictedSoupList.append(soup.select(selector))
	# if(len(soup.select('h3[class*="title"]')) != 0):
	# 	predictedSoupList.append(soup.select('h3[class*="title"]'))
	# if(len(soup.select('h3[class*="title"]')) != 0):
	# 	predictedSoupList.append(soup.select('h3[class*="title"]'))
	# if(len(soup.select('h3[class*="title"]')) != 0):
	# 	predictedSoupList.append(soup.select('h3[class*="title"]'))
	# if(len(soup.select('h3[class*="title"]')) != 0):
	# 	predictedSoupList.append(soup.select('h3[class*="title"]'))

	# if(len(soup.select('div[class*="title"]')) != 0):
	# 	predictedSoupList.append(soup.select('div[class*="title"]'))
	
	if(len(soup.find_all(['h1', 'h2', 'h3', 'h4'])) != 0):
		predictedSoupList.append(soup.find_all(['h1', 'h2', 'h3', 'h4']))

	for psl in predictedSoupList:
		for item in psl:
			# print(item)
			if(item.find('a')):
				if(item.find('a').get('href').strip() == '/'):
					continue

			predictedTarget.append(item.get_text().strip())

	return predictedTarget

def OptiMizer(arr):
	darr = []
	deleteArray = ['티스토리툴바', '툴바', 'toolbar', 'related', 'articles','태그','최근글','댓글','공지사항','관련글','더보기','포스트']
	for row in arr:
		deleteSwitch = False
		for deleteTarget in deleteArray:
			if(row.count(deleteTarget) != 0):
				deleteSwitch = True
				continue
			try:
				if(row.lower().count(deleteTarget) != 0):
					deleteSwitch = True
					continue
			except:
				pass
		if(deleteSwitch == False):
			darr.append(row)
	return darr
		

def main():
	urlList = []
	EM = EXCEL_MAKER()

	open('lists.txt', 'a').close()
	with open ('lists.txt', 'rt') as F:
		for link in F.readlines():
			if(link.strip() != ''):
				url = link
				if(url.count('http') == 0):
					url = "https://{}".format(url)
				if(url[-1] == '/'):
					url = url[:-1]
				url = url.strip()
				urlList.append(url)

	for url in urlList:
		EM.NewSite(url)
		
		session = prepare_session()
		
		r = session.get(url)

		soup = BeautifulSoup(r.text, 'html.parser')

		topindex = 0
		last_crawled = 0

		open('history.txt', 'a').close()

		with open('history.txt', 'r') as F:
			for row in F.readlines():
				try:
					tUrl = row.split('||')[0].strip()
					tLast = int(row.split('||')[1].strip())

					if(tUrl.count(url) != 0):
						# print(tUrl,tLast)
						last_crawled = tLast
						break
				except:
					pass
			



		for link in soup.find_all('a'):
			link = link.get('href')
			if(link == None):
				continue
			
			replacedText = link.split('?', 1)[0].replace('/', '').strip()
			if(replacedText.isdecimal()):
				if(topindex < int(replacedText)):
					topindex = int(replacedText)

		# print(topindex,last_crawled)
		if(topindex == 0):
			print ("이 사이트는 /10 같은 url 형식이 아닌, 제목을 이용한 형식으로 크롤링이 불가능합니다.")
		
		for index in range(topindex, last_crawled, -1):
			print ("\t# 진행상황 : {} 부터 {} 까지 {}%.".format(1,topindex, int((1 - index/topindex)*100)))
			currentUrl = "{}/{}".format(url, index)

			r = session.get(currentUrl)
			soup = BeautifulSoup(r.text, 'html.parser')

			predictedTarget = findSubject(soup)
			predictedTarget = OptiMizer(predictedTarget)

			if(len(predictedTarget) > 0):
				print("{} : {}".format(topindex-index, predictedTarget[0]))
				EM.Append(currentUrl, predictedTarget[0])

		EM.Finish(url, topindex, last_crawled)
		print("##    완료 혹은 새로운 게시물이 없습니다.    ##")
	
	EM.Save()
		

class EXCEL_MAKER(object):
	
	def __init__(self):
		self.wb = Workbook()
		self.sheet = self.wb.active
		self.sheet.title = u'분석결과'

		self.sheet.column_dimensions['A'].width = 25
		self.sheet.column_dimensions['B'].width = 50
		self.sheet.column_dimensions['C'].width = 50
		self.sheet.column_dimensions['E'].width = 20
		self.sheet.column_dimensions['F'].width = 20
		self.index = 0

	def NewSite(self, siteName):
		self.sheet.append(['인덱스', '주소', '제목', '', '사이트기준주소', siteName])

	def Append(self, url, subject):
		self.index += 1
		self.sheet.append([self.index, '=HYPERLINK("{}", "{}")'.format(url,url), subject])

	def Finish(self, url, topIndex, last_crawled):
		writeList = []
		processed = False

		self.sheet.append([])
		self.sheet.append([])
		with open('history.txt', 'rt') as F:
			for row in F.readlines():
				try:
					tUrl = row.split('||')[0].strip()
					if(tUrl.count(url) != 0):
						writeList.append("{} || {}".format(url,topIndex))
						processed = True
					else:
						writeList.append(row)
				except:
					pass
			if(processed == False):
				writeList.append("{} || {}".format(url, topIndex))

		with open('history.txt', 'wt') as F:
			for row in writeList:
				if(row.strip() == ''):
					continue
				F.writelines(row.strip()+'\n')

	def Save(self):
		self.wb.save('사이트분석파일.xlsx')

if __name__ == "__main__":
	main()
