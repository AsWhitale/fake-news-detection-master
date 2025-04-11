import os
import urllib.error
import urllib.request
from urllib.parse import urlparse

output_dir = 'output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

error_log = []

urls = input("").split(',')

for url in urls:
    url = url.strip()
    if not url:
        continue

    try:
        response = urllib.request.urlopen(url)
        content = response.read()

        encoding = response.headers.get_content_charset() or 'utf-8'
        content = content.decode(encoding)

        parsed_url = urlparse(url)
        file_name = os.path.join(output_dir, f"{parsed_url.netloc}.txt")  # 域名命名文件

        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"成功爬取：{url}")

    except urllib.error.HTTPError as e:
        error_log.append(f"HTTPError: {e.code} - {url}")
        print(f"爬取失败（HTTPError）: {e.code} - {url}")
    except urllib.error.URLError as e:
        error_log.append(f"URLError: {e.reason} - {url}")
        print(f"爬取失败（URLError）: {e.reason} - {url}")
    except Exception as e:
        error_log.append(f"Error: {str(e)} - {url}")
        print(f"爬取失败（其他错误）: {str(e)} - {url}")

if error_log:
    error_file_path = os.path.join(output_dir, 'error_log.txt')
    with open(error_file_path, 'w', encoding='utf-8') as error_file:
        error_file.write(f"总共爬取次数: {len(urls)}\n")
        error_file.write(f"失败次数: {len(error_log)}\n\n")
        error_file.write("\n".join(error_log))

    print(f"错误信息已保存至 {error_file_path}")
else:
    print("没有错误发生。")
