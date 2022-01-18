from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import requests
import time
password = ""
login = ""
serv = Service("chromedriver.exe")
browser = webdriver.Chrome(service=serv)

class InstagramBot:

    def __init__(self, login, password):
        self.browser = browser
        self.login = login
        self.password = password
        # try:
        #     browser.get("https://www.instagram.com/")
        #     time.sleep(5)
        #     log_info = browser.find_element(By.CLASS_NAME, "-MzZI").find_element(By.NAME, "username")
        #     log_info.clear()
        #     log_info.send_keys(self.login)
        #     time.sleep(5)
        #
        #     paswd = browser.find_element(By.XPATH,
        #                                  "/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input")
        #     paswd.clear()
        #     paswd.send_keys(self.password)
        #     time.sleep(5)
        #     paswd.send_keys(Keys.ENTER)
        #     time.sleep(10)
        # except Exception as ex:
        #     print(ex)
        # self.browser_close()


    def browser_close(self):
        browser.close()
        browser.quit()


    def xpath_exists(self, url):
        browser = self.browser
        try:
            browser.find_element(By.XPATH, url)
            exist = True
        except NoSuchElementException as ex:
            print(ex)
            exist = False
        return exist


    def get_all_posts_urls(self, userpage):
        self.browser = browser
        browser.get(userpage)
        time.sleep(5)

        wrong_userpage = "https://www.instagram.com/aratakillzz/"
        if self.xpath_exists(wrong_userpage):
            print("Вы ввели неправильный URL")
            self.browser_close()
        else:
            print("Страница пользователя найдена")


            post_urls = []
            hrefs = browser.find_elements(By.TAG_NAME, "a")
            hrefs = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]

            for href in hrefs:
                post_urls.append(href)

            filename = userpage.split("/")[-2]
            print(filename)
            print(post_urls)

            with open(f"{filename}.txt", "a") as file:
                for post_url in post_urls:
                    file.write(post_url + "\n")

            set_posts_urls = set(post_urls)
            set_posts_urls = list(set_posts_urls)

            with open(f"{filename}_set.txt", "a") as file:
                for post_url in set_posts_urls:
                    file.write(post_url + '\n')





    def userpage_download_content(self,userpage):
        browser = self.browser
        self.get_all_posts_urls(userpage)
        filename = userpage.split("/")[-2]
        time.sleep(5)
        browser.get(userpage)
        time.sleep(5)
        img_and_video_src_urls = []
        with open(f"{filename}_set.txt") as file:
            urls_list = file.readlines()
            for post_url in urls_list:
                try:
                    browser.get(post_url)
                    time.sleep(5)
                    post_id = post_url.split("/")[-2]
                    image_src = "/html/body/div[1]/section/main/div/div[3]/article/div/div/div[1]/div[1]/a/div/div[1]/img"
                    video_src = "/html/body/div[6]/div[2]/div/article/div/div[1]/div/div/div/div/div/video"

                    img_src_url = browser.find_element(By.XPATH, image_src).get_attribute('src')
                    img_and_video_src_urls.append(img_src_url)
                    video_src_url = browser.find_element(By.XPATH, video_src).get_attribute('src')
                    img_and_video_src_urls.append(video_src)
                    # download
                    get_img = requests.get(img_src_url)
                    with open(f"{post_id}_img.jpg", "wb") as img_file:
                        img_file.write(get_img.content)
                except Exception as ex:
                    print(ex)
        with open(f"img_and_video_src.txt", "a") as file:
            for i in img_and_video_src_urls:
                file.write(i + "\n")









Inst = InstagramBot(login, password)
Inst.get_all_posts_urls("https://www.instagram.com/aratakill/")