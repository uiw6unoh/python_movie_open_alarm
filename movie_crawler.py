import requests
import telegram
from bs4 import BeautifulSoup
from apscheduler.schedulers.blocking import BlockingScheduler

bot = telegram.Bot(token = '5173563474:AAFj62H4OoH4sLyIOqXP-k7dLzpMaJUrCRY')
url = 'http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode=01&theatercode=0105&date=20220305'
html = requests.get(url)
soup = BeautifulSoup(html.text, 'html.parser')

# 함수로 묶어주기
def job_function():
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    imax = soup.select_one('span.imax')
    if (imax):
        imax = imax.find_parent('div', class_='col-times')
        title = imax.select_one('div.info-movie > a > strong').text.strip()
        bot.sendMessage(chat_id='1767897517', text=title + ' IMAX 예매가 열렸습니다.')
        sched.pause()

# 스케쥴러 새로 선언
sched = BlockingScheduler()
# 스케쥴러에 등록하기, interval로 일정간격 반복하겠다
sched.add_job(job_function, 'interval', seconds=30)
sched.start()