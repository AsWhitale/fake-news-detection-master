import urllib.request
from urllib.request import Request

from bs4 import BeautifulSoup


def get_web_text(url):
    try:

        header = {
            'User-Agent': 'Mozilla / 5.0(WindowsNT10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 134.0.0.0Safari / 537.36Edg / 134.0.0.0'}
        ret = Request(url, headers=header)
        # 发送 HTTP 请求并获取响应
        response = urllib.request.urlopen(ret)
        # 获取响应的内容类型
        content_type = response.headers.get_content_type()

        # 读取响应的 HTML 内容
        html_content = response.read()

        # 使用 BeautifulSoup 解析 HTML 内容
        soup = BeautifulSoup(html_content, 'html.parser')

        # 提取文本内容
        text_content = soup.get_text(separator='\n', strip=True)

        return text_content

    except urllib.error.HTTPError as e:
        print(f"HTTPError: {e.code} for URL: {url}")
        return None
    except urllib.error.URLError as e:
        print(f"URLError: {e.reason} for URL: {url}")
        return None
    except Exception as e:
        print(f"Error: {str(e)} for URL: {url}")
        return None


# 示例调用
if __name__ == '__main__':
    url = "https://book.douban.com/subject/1728816/"  # 替换为你要爬取的实际 URL
    text = get_web_text(url)
    if text:
        print(text)
