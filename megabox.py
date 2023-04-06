import time
import asyncio
import telegram
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# 텔레그램 봇 토큰과 채팅방 ID
bot_token = '토큰'
chat_id = '아이디'

# 페이지에서 가져올 영화 제목과 예매일
target_title = "스뮤페"
target_date = "2023.04.11"

# 이전에 확인한 예매 오픈 정보
prev_booking_info = None


def init_webdriver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    ua = UserAgent()
    user_agent = ua.random
    chrome_options.add_argument(f'user-agent={user_agent}')

    chromedriver_path = 'D:/Project/megabox/chromedriver.exe'
    driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
    return driver


def click_booking_date_button(driver, booking_date_button):
    # 클릭하기
    booking_date_button.click()

    # 페이지 로드 대기
    wait = WebDriverWait(driver, 5)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.time-schedule')))

    # 일정한 대기 시간 추가
    time.sleep(3)


async def check_booking_info():
    global prev_booking_info

    url = "https://www.megabox.co.kr/theater/time?brchNo=0019"
    driver = init_webdriver()

    try:
        driver.get(url)
    except Exception as e:
        print(f"Error occurred: {e}")
        driver.quit()
        return

    soup = BeautifulSoup(driver.page_source, "html.parser")
    movie_list = soup.select(".reserve.theater-list-box > .theater-list")
    if not movie_list:
        print("No movie found on the page.")
        driver.quit()
        return

    # 페이지에서 예매 날짜 버튼 클릭
    booking_date_button = driver.find_element_by_css_selector(f".date-area button[date-data='{target_date}']")
    click_booking_date_button(driver, booking_date_button)

    # 예매 가능한 영화 검색
    is_movie_found = False
    soup = BeautifulSoup(driver.page_source, "html.parser")
    movie_list = soup.select(".reserve.theater-list-box > .theater-list")
    # for movie in movie_list:
    #     movie_title = movie.select_one(".theater-tit a").text.strip()
    #     if target_title in movie_title:
    #         booking_info = f"[{movie_title}] 예매 오픈!"
    #         if prev_booking_info != booking_info:
    #             bot = telegram.Bot(token=bot_token)
    #             await bot.send_message(chat_id=chat_id, text=booking_info)
    #             prev_booking_info = booking_info
    #             print(f"{booking_info}\n텔레그램으로 전송했습니다!")
    #         is_movie_found = True

    for movie in movie_list:
        movie_title = movie.select_one(".theater-tit a").text.strip()
        if target_title in movie_title:
            booking_info = f"[{movie_title}] 예매 오픈!"
            bot = telegram.Bot(token=bot_token)
            await bot.send_message(chat_id=chat_id, text=booking_info)
            print(f"{booking_info}\n텔레그램으로 전송했습니다!")
            is_movie_found = True

    if not is_movie_found:
        print(f"No movie with the title '{target_title}' found on the page.")

    driver.quit()


async def main():
    while True:
        await check_booking_info()
        await asyncio.sleep(10)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
