from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
import time

# task ：http://nb.ncha.gov.cn  把所有博物馆年报信息爬取下来  id="listDiv"

# 使用Chrome浏览器驱动
driver = webdriver.Chrome()

# 指定要爬取的博物馆信息网站URL格式
base_url = 'http://nb.ncha.gov.cn/?page={}&nianfen={}'

# 用于存储所有博物馆信息的列表
museums_data = []

# 循环爬取数据和年份
start_year = 2018  # 起始年份
end_year = 2021  # 结束年份

for year in range(start_year, end_year + 1):
    current_page = 1

    while True:  # 无限循环，直到没有下一页链接为止
        # 构建完整的网页URL
        url = base_url.format(current_page, year)

        # 打开网页
        driver.get(url)

        # 等待页面加载完成（根据需要进行调整）
        driver.implicitly_wait(10)  # 最多等待10秒

        # 使用Beautiful Soup解析网页内容
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # 查找所有<div>元素，每个<div>元素代表一个博物馆信息
        div_elements = soup.find_all('div', class_='listitem')  # 请替换成实际的class属性值

        # 遍历每个<div>元素，提取信息并存储到列表中
        for div_element in div_elements:
            # 提取<div>元素下的<p>标签信息
            paragraphs = div_element.find_all('p')  # 查找所有<p>标签
            museum_info = [p.get_text() for p in paragraphs]  # 提取<p>标签中的文本

            # 检查是否有“免费”列，如果没有则添加空字符串
            free_column = div_element.find('div', class_='isfree')  # 请替换成实际的class属性值
            museum_info.append(free_column.get_text() if free_column else '')

            # 在每行数据开头加入年份和页数
            museum_info.insert(0, str(year))  # 将年份添加到开头
            museum_info.insert(1, str(current_page))  # 将页数添加到开头

            museums_data.append(museum_info)

        # 查找下一页链接，如果不存在则退出循环
        try:
            nav_element = driver.find_element_by_css_selector('nav.turnpage ul.pagination.pagination-lg')
            next_page_button = nav_element.find_element_by_xpath('.//li/a[@aria-label="Next"]')
            next_page_button.click()
            current_page += 1
        except Exception:
            break

        # 等待一段时间，避免频繁请求
        time.sleep(2)

# 打印爬取的博物馆信息
for museum_info in museums_data:
    print(museum_info)

# 关闭浏览器
driver.quit()
