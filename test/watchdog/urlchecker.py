import requests
from . import common_utility_function

def main(env, split, test_data):
    urls = generate_test_urls(env, split, test_data)
    check_urls(urls)

def generate_test_urls(env, split, test_data):
    urls_list = []
    base_url = generate_base_url(env, split)
    for data in test_data['urls']:
        if data.get("url") == "/":
             urls_list.append(base_url)
        else:
            urls_list.append(base_url + data.get("url"))
    return urls_list


def generate_base_url(env, split):
    if split == "static":
        base_url = env['base_url']
    elif split == "blog":
        base_url = env['blog_url']
    elif split == "life":
        base_url = env['life_url']
    else :
        base_url = env['app_url']
    return base_url

def check_urls(urls):

    for url in urls:
        try:
            response = requests.get(url)
            status_code = response.status_code
            # TODO
            # need to print it into output file 
            print(f"URL: {url} - Response Code: {status_code}")
        except requests.exceptions.RequestException as e:
            print(f"URL: {url} - Error: {e}")
            # TODO
            # need to print it into output file

if __name__ == "__main__":

    main(env, split, test_data)