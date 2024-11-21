from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import csv
from globals import GO_YEAR, TIME_SLICE
from Parsing import *
import glob
from group_files import *

# ChromeDriver 경로 설정
chrome_driver_path = 'C:/Users/quant.QUANT/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe'

# 브라우저 옵션 설정
options = Options()
# options.add_argument('--headless')  # 브라우저 창을 띄우지 않음 (옵션)
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')


# 웹드라이버 초기화
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)

    
def open_url_ver1(driver, url):
    """Open the specified URL and switch to the second frame."""
    driver.get(url)
    driver.switch_to.frame(1)
    print("두 번째 프레임으로 전환 완료")

def open_url_ver2(driver, url):
    """Open the specified URL and switch to the second frame."""
    driver.get(url)

def click_match_center(driver):
    """Click the 'Match Center' element."""
    match_center_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'mcCenter'))
    )
    match_center_element.click()
    time.sleep(TIME_SLICE)

def click_data_center(driver):
    """Click the 'DATA Center' element using XPath."""
    # XPath로 'DATA Center' 요소 찾기 (이 예시는 예시로 사용된 XPath입니다. 실제 XPath는 페이지 구조에 맞게 변경해야 합니다.)
    data_center_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/div/div[1]/div[2]/ul/li[1]/a'))
    )
    data_center_element.click()
    time.sleep(TIME_SLICE)

def click_player_stats(driver):
    """Click on the 'PLAYER STATS' tab."""
    player_stats_tab = driver.find_element(By.XPATH, "//*[@id='contentsLayer']/div/div/ul/li[3]")
    player_stats_tab.click()
    time.sleep(TIME_SLICE)

def click_button_away(driver):
    """Click the 'Away' button."""
    away_button = driver.find_element(By.XPATH, '//*[@id="btnAwayTeam"]')
    away_button.click()
    time.sleep(TIME_SLICE)

def click_button_by_id(driver, button_id):
    """Click a button identified by its ID."""
    button = driver.find_element(By.XPATH, f"//*[@id='{button_id}']")
    button.click()
    time.sleep(TIME_SLICE)

def click_button_pass_matrix(driver):
    """Click a button identified by its XPath."""
    button = driver.find_element(By.XPATH, "//*[@id='contentsLayer']/div/div/ul/li[8]/a")
    button.click()
    time.sleep(TIME_SLICE)

def select_team_name(driver, team_button_id):
    """Select a team (home or away) and print its name."""
    team_button = driver.find_element(By.XPATH, f"//*[@id='{team_button_id}']")
    return team_button.text
    

def select_from_dropdown(driver, dropdown_id, value):
    """Select an option from a dropdown menu by value."""
    dropdown = Select(driver.find_element(By.ID, dropdown_id))
    dropdown.select_by_value(value)
    time.sleep(TIME_SLICE)

def select_round(driver):
    """Select the round from the dropdown."""
    box_round = Select(driver.find_element(By.ID, "selRoundId"))
    for option in box_round.options:
        value = option.get_attribute("value")
        box_round.select_by_value(value)  # Select by value
        time.sleep(TIME_SLICE)

def select_versus(driver):
    """Select each game in the versus dropdown."""
    box_versus = Select(driver.find_element(By.ID, "selGameId"))
    num = len(box_versus.options) - 1
    
    for i in range(1, num + 1):
        box_versus = Select(driver.find_element(By.ID, "selGameId"))
        box_versus.select_by_value(str(i))  # Select by value
        time.sleep(TIME_SLICE)

def save_home_공격data(driver, year, add_text):
    with open( str(year) + add_text +"공격_data.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//*[@id='homeAttList']/thead/tr/th"))
        )
        header_elements = driver.find_elements(By.XPATH, "//*[@id='homeAttList']/thead/tr/th")
        headers = [header.text for header in header_elements if header.text]
        headers.append("Ishome")
        writer.writerow(headers)

        rows = driver.find_elements(By.XPATH, "//*[@id='homeAttList']/tbody/tr")
        for row in rows:
            data = [cell.text for cell in row.find_elements(By.XPATH, ".//td")]
            data.append("1")
            writer.writerow(data)

def save_home_패스data(driver, year, add_text):
    with open(str(year) + add_text +"패스_data.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//*[@id='homePassList']/thead/tr/th"))
        )
        header_elements = driver.find_elements(By.XPATH, "//*[@id='homePassList']/thead/tr/th")
        headers = [header.text for header in header_elements if header.text]
        headers.append("Ishome")
        writer.writerow(headers)

        rows = driver.find_elements(By.XPATH, "//*[@id='homePassList']/tbody/tr")
        for row in rows:
            data = [cell.text for cell in row.find_elements(By.XPATH, ".//td")]
            data.append("1")
            writer.writerow(data)

def save_home_수비data(driver, year, add_text):
    with open(str(year) + add_text +"수비_data.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # homeAttList의 헤더 추출 및 작성
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//*[@id='homeDefList']/thead/tr/th"))
        )
        header_elements = driver.find_elements(By.XPATH, "//*[@id='homeDefList']/thead/tr/th")
        headers = [header.text for header in header_elements if header.text]
        headers.append("Ishome")
        writer.writerow(headers)

        # homeAttList의 데이터 추출 및 작성
        rows = driver.find_elements(By.XPATH, "//*[@id='homeDefList']/tbody/tr")
        for row in rows:
            data = [cell.text for cell in row.find_elements(By.XPATH, ".//td")]
            data.append("1")
            writer.writerow(data)

def save_home_골키퍼data(driver, year, add_text):
    with open(str(year) + add_text +"골키퍼_data.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # homeAttList의 헤더 추출 및 작성
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//*[@id='homeGkList']/thead/tr/th"))
        )
        header_elements = driver.find_elements(By.XPATH, "//*[@id='homeGkList']/thead/tr/th")
        headers = [header.text for header in header_elements if header.text]
        headers.append("Ishome")
        writer.writerow(headers)

        # homeAttList의 데이터 추출 및 작성
        rows = driver.find_elements(By.XPATH, "//*[@id='homeGkList']/tbody/tr")
        for row in rows:
            data = [cell.text for cell in row.find_elements(By.XPATH, ".//td")]
            data.append("1")
            writer.writerow(data)

def save_home_passMatrix(driver, year, add_text):
    with open(str(year) + add_text +"passMatrix.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # 헤더 추출 및 CSV 파일에 작성
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//*[@id='homeList']/thead/tr/th"))
        )
        header_elements = driver.find_elements(By.XPATH, "//*[@id='homeList']/thead/tr/th")
        headers = [header.text for header in header_elements if header.text]  # 빈 헤더 제외
        headers.append("Ishome")
        writer.writerow(headers)

        # 각 행 데이터 추출 및 CSV 파일에 작성
        rows = driver.find_elements(By.XPATH, "//*[@id='homeList']/tbody/tr")
        for row in rows:
            data = [cell.text for cell in row.find_elements(By.XPATH, ".//td")]
            data.append("1")
            writer.writerow(data)

def save_away_공격data(driver, year, add_text):
    with open(str(year) + add_text +"공격_data.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//*[@id='awayAttList']/thead/tr"))
        )

        rows = driver.find_elements(By.XPATH, "//*[@id='awayAttList']/tbody/tr")
        for row in rows:
            data = [cell.text for cell in row.find_elements(By.XPATH, ".//td")]
            data.append("0")
            writer.writerow(data)


def save_away_패스data(driver, year, add_text):
    with open(str(year) + add_text +"패스_data.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//*[@id='awayPassList']/thead/tr"))
        )

        rows = driver.find_elements(By.XPATH, "//*[@id='awayPassList']/tbody/tr")
        for row in rows:
            data = [cell.text for cell in row.find_elements(By.XPATH, ".//td")]
            data.append("0")
            writer.writerow(data)


def save_away_수비data(driver, year, add_text):
    with open(str(year) + add_text +"수비_data.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # homeAttList의 헤더 추출 및 작성
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//*[@id='awayDefList']/thead/tr"))
        )

        # homeAttList의 데이터 추출 및 작성
        rows = driver.find_elements(By.XPATH, "//*[@id='awayDefList']/tbody/tr")
        for row in rows:
            data = [cell.text for cell in row.find_elements(By.XPATH, ".//td")]
            data.append("0")
            writer.writerow(data)


def save_away_골키퍼data(driver, year, add_text):
    with open(str(year) + add_text +"골키퍼_data.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # homeAttList의 헤더 추출 및 작성
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//*[@id='awayGkList']/thead/tr"))
        )

        # homeAttList의 데이터 추출 및 작성
        rows = driver.find_elements(By.XPATH, "//*[@id='awayGkList']/tbody/tr")
        for row in rows:
            data = [cell.text for cell in row.find_elements(By.XPATH, ".//td")]
            data.append("0")
            writer.writerow(data)


def save_away_passMatrix(driver, year, add_text):
    with open(str(year) + add_text +"passMatrix.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # 헤더 추출 및 CSV 파일에 작성
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//*[@id='awayList']/thead/tr/th"))
        )
        header_elements = driver.find_elements(By.XPATH, "//*[@id='awayList']/thead/tr/th")
        headers = [header.text for header in header_elements if header.text]  # 빈 헤더 제외
        headers.append("Ishome")
        writer.writerow(headers)

        # 각 행 데이터 추출 및 CSV 파일에 작성
        rows = driver.find_elements(By.XPATH, "//*[@id='awayList']/tbody/tr")
        for row in rows:
            data = [cell.text for cell in row.find_elements(By.XPATH, ".//td")]
            data.append("0")
            writer.writerow(data)


def get_csv_real_home(year, add_text):
    click_button_by_id(driver, 'btnAttFlag')  # 공격
    # csv
    save_home_공격data(driver, year, add_text)
    click_button_by_id(driver, 'btnPassFlag')  # 패스
    # csv 
    save_home_패스data(driver, year, add_text)
    click_button_by_id(driver, 'btnDefFlag')   # 수비
    # csv
    save_home_수비data(driver, year, add_text)
    click_button_by_id(driver, 'btnGkFlag')    # 골키퍼
    # csv
    save_home_골키퍼data(driver, year, add_text)

def get_csv_real_away(year, add_text):
    click_button_by_id(driver, 'btnAttFlag')  # 공격
    # csv
    save_away_공격data(driver, year, add_text)
    click_button_by_id(driver, 'btnPassFlag')  # 패스
    # csv 
    save_away_패스data(driver, year, add_text)
    click_button_by_id(driver, 'btnDefFlag')   # 수비
    # csv
    save_away_수비data(driver, year, add_text)  
    click_button_by_id(driver, 'btnGkFlag')    # 골키퍼
    # csv
    save_away_골키퍼data(driver, year, add_text)

def gogo():
    select_from_dropdown(driver, "selMeetYear", str(GO_YEAR))       # year
    select_from_dropdown(driver, "selMeetSeq", "1")          # competition
    year = GO_YEAR
    num = 0
    for i in range(1, 39):
        box_round = Select(driver.find_element(By.ID, "selRoundId"))

        box_round.select_by_value(str(i))  # Select by value
        time.sleep(TIME_SLICE)
        box_versus = Select(driver.find_element(By.ID, "selGameId"))
        
        
        num += len(box_versus.options) - 1 # 6 12 18
        start = num - len(box_versus.options) + 2 

        if(i == 2):
            break

        for j in range(start, num + 1):
            if(j == 2):
                break

            print(j)
            box_versus = Select(driver.find_element(By.ID, "selGameId"))
            box_versus.select_by_value(str(j))  # Select by value

            # 현재 선택된 옵션의 텍스트 가져오기
            box_versus = Select(driver.find_element(By.ID, "selGameId"))
            full_text = box_versus.first_selected_option.text

            full_text = full_text.replace('/', '_')
            
            print(f"선택된 전체 텍스트: {full_text}")

            time.sleep(TIME_SLICE)
            click_player_stats(driver) # player stats
            get_csv_real_home(year, full_text)
            click_button_away(driver)
            get_csv_real_away(year, full_text)
            
            click_button_pass_matrix(driver)  # pass home matrix
            #csv
            save_home_passMatrix(driver, year, full_text)
            
            click_button_away(driver) # pass away home matrix
            #csv
            save_away_passMatrix(driver, year, full_text)

            print(select_team_name(driver, 'btnHomeTeam'))          # home
            print(select_team_name(driver, 'btnAwayTeam'))          # away

# Main execution flow
try:
    url = 'https://data.kleague.com/'
    open_url_ver1(driver, url)
    click_data_center(driver)
    gogo()

except Exception as e:
    print(f"에러 발생: {e}")

finally:
    driver.quit()


# 파일 이름이 '*골키퍼_data.csv' 패턴에 맞는 모든 CSV 파일을 처리
csv_files = glob.glob("*골키퍼_data.csv")  # 파일 이름이 '골키퍼_data.csv'로 끝나는 모든 파일을 찾습니다.
for file_path in csv_files:
    rename_columns_for_goalkeeping_data(file_path)

# 모든 CSV 파일을 처리
csv_files = glob.glob("*공격_data.csv")  # 현재 디렉토리 내의 모든 CSV 파일을 찾습니다.
for file_path in csv_files:
    rename_columns_for_attack_data(file_path)

# 파일 이름이 '*패스_data.csv' 패턴에 맞는 모든 CSV 파일을 처리
csv_files = glob.glob("*패스_data.csv")  # 예를 들어 '패스_data.csv'로 끝나는 모든 파일을 찾습니다.
for file_path in csv_files:
    rename_columns_for_passing_data(file_path)

# 파일 이름이 '*수비_data.csv' 패턴에 맞는 모든 CSV 파일을 처리
csv_files = glob.glob("*수비_data.csv")  # 파일 이름이 '수비_data.csv'로 끝나는 모든 파일을 찾습니다.
for file_path in csv_files:
    rename_columns_for_defensive_data(file_path)

######################################################  group_files.py

data_directory = './'  # 데이터 디렉토리 경로
file_pattern = str(GO_YEAR) + '*'  # 파일 검색 패턴

# 파일 그룹화
file_groups = group_files_by_prefix(data_directory, file_pattern)

# 데이터 병합 및 저장
merge_and_save_data(data_directory, file_groups)


######################################################## passmatrix랑 골키퍼 파일만 다른 폴더에 복사

copy_pass_matrix_files()  # matrix 파일을 다른 폴더로 복사

source_dir = './'  # 검색할 폴더 경로
destination_dir = './'+ str(GO_YEAR) +'_골키퍼'  # 파일을 복사할 대상 폴더 경로
pattern = '골키퍼_'  # 파일명에 포함된 패턴

copy_files_with_pattern(source_dir, destination_dir, pattern)
