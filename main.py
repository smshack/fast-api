from typing import Optional
from googletrans import Translator
from fastapi import FastAPI
import re
import base64
from pydantic import BaseModel
from selenium.webdriver.common.keys import Keys
from fastapi.middleware.cors import CORSMiddleware
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import datetime
from PIL import Image
import cv2
import glob
import time
import pyperclip
from selenium.webdriver.common.action_chains import ActionChains

class Macro(BaseModel):
    nvid: str
    nvpass: str
    personcheck: bool
    title: str
    content: str
    images: str
    videoUrl: str
    

app = FastAPI()

origins = ["*"]
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.post("/macro")
def macro_function(macro:Macro):
    print(macro.title)
    title =macro.title
    content =macro.content
    images = macro.images
    tags =""
    nvid = macro.nvid
    # ===================================================================
    # 제목으로 키워드 처리 하는 부분
    # ===================================================================
    
    chrom_driver_path = "C:\\Users\\smart\\Desktop\\python\\chromedriver"
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(executable_path=chrom_driver_path,options=options)
    search_google = "https://google.com/search?q="+macro.title
    driver.get(f"{search_google}")
    driver.implicitly_wait(10)
    tag_list =[]
    soup = BeautifulSoup(driver.page_source, "html.parser")
    satshe_elements =  soup.find_all("div", attrs={"data-hveid": lambda x: x and x.startswith("C")})
    for satshe_element in satshe_elements:
        keywords= satshe_element.find_all("b")
        for keyword in keywords:
            tag_list.append(keyword.text)
    # Find the related search terms element
    # 연관 검색어 리스트에서 검색어와 같은 값 지우기
    if macro.title in tag_list:
        tag_list.remove(macro.title) 
    # 중복값 제거
    tag_list= list(set(tag_list))
    print(tag_list)
    driver.close()
    
    # ===================================================================
    # personcheck가 True일 시에 title에 프로필 단어를 붙여줌
    # ===================================================================
    
    if macro.personcheck:
        title = title +" 프로필"
    
    # # ===================================================================
    # # 본문 두번 거쳐서 한 - 일 - 한 으로 변경 하는 부분
    # ===================================================================
    # 초기 세팅시 [숫자 형식은 지우고 시작]
    content = re.sub(r"\[\d+\]", "", content) 
    
    translator = Translator()
    jacontent = translator.translate(content,src='ko', dest='ja').text
    content = translator.translate(jacontent,src='ja', dest='ko').text
    # ===================================================================
    # 이미지 데이터를 받아서 파일로 저장하는 부분
    # ===================================================================
    # 이미지 태그 안에 인코딩 된 값만 뽑아오는 부분
    # src_regex = r'src="(.*?)"'
    # # print(images)
    # imageslist = re.findall(src_regex, images)
    # nowdirpath = os.path.dirname(os.path.realpath(__file__))
    
    # #  저장한 파일을 실행 파일 위치에 아래에 년월일/타이틀/인덱스번호.png 로 저장
    # engtitle = translator.translate(title,src='ko', dest='en').text.replace(' ','_')
    # now = datetime.datetime.now()
    # nowstring = now.strftime("%Y%m%d")
    # makefirpath = f'{nowdirpath}\\{nowstring}\\{engtitle}'
    # os.makedirs(makefirpath, exist_ok=True)
    # #  가져온 base46 데이터를 디코딩해서 파일로 저장하는 부분
    # for index,imagestr in enumerate(imageslist):
    #     imagestr = imagestr.replace('data:image/png;base64,','')
    #     file_path = f'{makefirpath}\\{index}_.png'
    #     file__fliter_path = f'{makefirpath}\\{index}_fliter.png'
    #     with open(file_path, 'wb') as file:
    #         file.write(base64.b64decode(imagestr))
    #     # 이미지 파일을 좌우 반전 하는 부분 저장
    #     filter_image = Image.open(file_path)
    #     FlipImage = filter_image.transpose(Image.FLIP_LEFT_RIGHT)
    #     FlipImage.save(f'{file__fliter_path}')
    
    # ======================================================================
    # 원하는 페이지의 url을 받아서 영상으로 뽑는 부분
    # ======================================================================
    # 전체 페이지를 이미지 캡쳐해옴
#     driver = webdriver.Chrome(executable_path=chrom_driver_path,options=options)
#     driver.get(f"{macro.videoUrl}")
#     driver.implicitly_wait(10)
#     width = driver.execute_script("return Math.max( document.body.scrollWidth, document.body.offsetWidth, document.documentElement.clientWidth, document.documentElement.scrollWidth, document.documentElement.offsetWidth );")
#     height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")

# # # Set the window size to the size of the entire page
#     driver.set_window_size(width, height)

# # # Take a screenshot of the page
#     screenshot = driver.get_screenshot_as_png()
#     with open(f'{makefirpath}\\screenshot.png', 'wb') as f:
#         f.write(screenshot)
        
#     driver.close()
    
    # fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    # print(f'{makefirpath}\\screenshot.mp4')
    # # Write the images to the video file
    # files = glob.glob(f'{makefirpath}\\*.png')
    # result = []
    # for idx , path in enumerate(files) :
    #     img = cv2.imread(path)
    #     img = cv2.resize(img , (1049, 685) , interpolation = cv2.INTER_AREA)
    #     result.append(img)
    #     name = path.split(".png")[0]
    #     cv2.imwrite(f'{makefirpath}\\{name}.png' , img)   
    # frames = []
    # for file in files:
    #     new_frame = Image.open(file)
    #     frames.append(new_frame)
    # frames[0].save(f'{makefirpath}\\video.gif',format='gif',
    #                append_images=frames[1:],
    #                save_all=True,
    #                duration=2,
    #                loop=0
    #                )
    # ff = ffmpy.FFmpeg(
    #  inputs={f'{makefirpath}\\video.gif': None},
    #  outputs={f'{makefirpath}\\video.mp4': None}
    # )
    # ff.run()
    
    # =========================================================
    # 네이버 블로그 제목 쓰기
    #=========================================================
    driver = webdriver.Chrome(executable_path=chrom_driver_path,options=options)
    driver.get('http://naver.com')
    time.sleep(3)
    elem = driver.find_element(By.CLASS_NAME,'link_login')
    elem.click()
    time.sleep(3)
    # 3. id 복사 붙여넣기
    elem_id = driver.find_element(By.ID,'id')
    elem_id.click()
    time.sleep(1)
    pyperclip.copy(macro.nvid)
    elem_id.send_keys(Keys.CONTROL, 'v')
    time.sleep(3)

    # 4. pw 복사 붙여넣기
    elem_pw = driver.find_element(By.ID,'pw')
    elem_pw.click()
    time.sleep(1)
    pyperclip.copy(macro.nvpass)
    elem_pw.send_keys(Keys.CONTROL, 'v')
    time.sleep(3)

    # 5. 로그인 버튼 클릭
    driver.find_element(By.ID,'log.login').click()
    time.sleep(1)
    driver.get(f'https://blog.naver.com/{macro.nvid}/postwrite')
    time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    iframe_element = soup.find('iframe')

# Get the id attribute of the iframe
    iframe_id = iframe_element['id']
    action = ActionChains(driver)
    # print(iframe_id)
    
    # switchdriver = driver.switch_to.frame(iframe_id)
    time.sleep(2)
    driver.find_element(By.XPATH,'//span[contains(text(),"제목")]').click()
    action.send_keys(title).perform()
    driver.find_element(By.XPATH,'//span[contains(text(),"본문에 #을 이용하여 태그를 사용해보세요! (최대 30개)")]').click()
    action.send_keys(content).perform()
    action.send_keys(Keys.ENTER).perform()
    
    
    time.sleep(100)