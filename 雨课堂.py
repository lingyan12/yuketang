#encoding:utf-8



import os
import time

import selenium
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait as wait_wd
from selenium.webdriver.support import ui
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains as ac

from selenium.webdriver.support import expected_conditions  as ec
from selenium.common.exceptions import TimeoutException
from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures.process import ProcessPoolExecutor
from concurrent.futures import wait
from concurrent.futures import ALL_COMPLETED

class WangKe:

    cookies = [{'domain': '#需要填写',
      'name': 'sessionid',
      'path': '/',
      'value': '#需要填写'},
     {'domain': 'zzugs.yuketang.cn',
      'name': '#需要填写',
      'path': '/',
      'value': '#需要填写'},
     {'domain': '#需要填写',
      'name': '',
      'path': '/',
      'value': '#需要填写'},
     {'domain': '#需要填写',
      'name': '#需要填写',
      'path': '/',
      'value': '#需要填写'},
     {'domain': '#需要填写',
      'name': '#需要填写',
      'path': '/',
      'value': '#需要填写'},
     {'domain': '#需要填写',
      'name': '#需要填写',
      'path': '/',
      'value': '#需要填写'},
     {'domain': '#需要填写',
      'name': '#需要填写',
      'path': '/',
      'value': '#需要填写'},
     {'domain': '#需要填写',
      'name': '#需要填写',
      'path': '/',
      'value': '#需要填写'}]


    def get_list(self,url,location):
        wd = webdriver.Chrome()
        wd.get("https://www.baidu.com")
        wd.delete_all_cookies()
        time.sleep(2)
        for i in WangKe.cookies:
            wd.add_cookie(i)
        with open(location,'w+') as fp:
            wd.get(url)
            time.sleep(2)
            try:
                while 1:
                    # next_button = self.wd.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[3]/div/div/div[1]/div/div[3]/button[2]')
                    next_button = wait_wd(wd,10,poll_frequency=1).until(ec.element_to_be_clickable((By.XPATH,"//button[@class='el-tooltip btn-next item']")))
                    if next_button:
                        next_button.click()
                        current_url = (wd.current_url+'\r')
                        print(wd.current_url)
                        fp.writelines(current_url)
                        fp.flush()
                        time.sleep(2)
                    else:
                        print('已无新课程')
                        break
            except TimeoutException :
                print('已无新课程')
                wd.close()


    def watching_letter(self, url ):
        print(url)
        wd = webdriver.Chrome()
        wd.set_page_load_timeout(10)
        wd.get("https://www.baidu.com")
        wd.delete_all_cookies()

        for i in WangKe.cookies:
            wd.add_cookie(i)
        try:
            print(1)
            wd.get(url)
            print(2)
        except :
            print(3)
            wd.execute_script("window.stop()")
        finally:
            print(4)
            time.sleep(5)
            homework_title = wd.find_element_by_xpath("//span[@class='text text-ellipsis']")
            homework_text =homework_title.text
            try:
                time_persent = wd.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[3]/div/div[2]/div[1]/section[1]/div[2]/div/div/span').text
            except:
                time_persent = None
            finally:
                print('==============================================================================================')
                print(time_persent, homework_text,wd.current_url )

                print('==============================================================================================')

                if (not '随堂作业' in homework_text) and ( not '100%' in time_persent):
                    try:
                        # button = wait_wd(wd,10,poll_frequency=2).until(ec.element_to_be_clickable((By.XPATH , "//xt-playbutton[@class='xt_video_player_play_btn fl']")))
                        button = wait_wd(wd,10,poll_frequency=2).until(ec.element_to_be_clickable((By.XPATH , '//*[@id="video-box"]/div/xt-wrap/xt-controls/xt-inner/xt-playbutton')))
                        button_text = wd.find_element_by_xpath('//*[@id="video-box"]/div/xt-wrap/xt-controls/xt-inner/xt-playbutton/xt-tip').text
                        print(button_text)

                        # print('button cunzai')
                        if button:
                            time.sleep(5)
                            speed_button = wait_wd(wd,10,poll_frequency=1).until(ec.presence_of_element_located((By.XPATH , '//*[@id="video-box"]/div/xt-wrap/xt-controls/xt-inner/xt-speedbutton/xt-speedvalue')))
                            speed_2 = wd.find_element_by_xpath('//*[@id="video-box"]/div/xt-wrap/xt-controls/xt-inner/xt-speedbutton/xt-speedlist/ul/li[1]')
                            ac(wd).move_to_element(speed_button).perform()
                            time.sleep(1)
                            speed_2.click()
                            button.click()
                            time_ = wd.find_element_by_xpath('//*[@id="video-box"]/div/xt-wrap/xt-controls/xt-inner/xt-time/span[2]').text.split(':')
                            time_long = ((int(time_[1]) * 60 + int(time_[2])) + 30) / 2
                            print(time_long)
                            time.sleep(time_long)
                            # print('watching ',url)
                            print('----', url, '成功')
                            wd.close()
                        else:
                            # print('button 不存在')
                            wd.close()
                    except TimeoutException:
                        print('未找到 button')
                        print('-------------', url, '失败')
                        wd.close()

                else:
                    # print("100% or 作业")
                    print('close----',url)
                    wd.close()

                return 1



def read_url_list(location):
    url_list = []
    with open(location, 'r') as fp:
        url_content = fp.readlines()
        for url in url_content:
            url = url[:-1]
            url_list.append(url)
    return url_list




def Get_Start_List(url,location):
    wangke = WangKe()
    wangke.get_list(url,location)




def main(location, num):
    url_list = read_url_list(location)
    url_list_str = []
    for i in url_list:
        # url_list_str.append(i.decode('utf-8'))   #读取二进制
        url_list_str.append(i)

    print(url_list_str)
    future = []
    with ProcessPoolExecutor(max_workers=num) as exe:
        f= exe.map(WangKe().watching_letter, url_list_str)
        list(f)
        wait(future, return_when=ALL_COMPLETED)

        print('all finished')






if __name__ == '__main__':                     # 置顶部位有cookies 请自己填写
    num = 5                                     #并发进程数量
    url = 'https://zzugs.yuketang.cn/pro/lms/2544n8RaSEH3/2642786/video/1769660'
    location = r'url_list.txt'                 #url  保存为txt文件
    # Get_Start_List(url,location)            #先运行这个  这个是 获取网课全部url
    main(location ,num)                        #多进程看网课
