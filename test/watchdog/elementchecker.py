import requests
from bs4 import BeautifulSoup
from watchdog.urlchecker import generate_base_url as get_base_url


def main(env, split, test_data):
    base_url = get_base_url(env, split)
    test_data_genration(base_url, test_data)

def test_data_genration(base_url, test_data):
    for data in test_data['urls']:
        elements = []
        if data.get("url") == "/":
            check_url = base_url
            for elementid in data.get("elements"):
                elements.append(elementid.get("element_id", []))
        else:
            check_url = base_url + data.get("url")
            for elementid in data.get("elements"):
                elements.append(elementid.get("element_id", []))
        check_page(check_url, elements)

def check_page(url, ids):
    
    results = {
        "url_present": False,
        "blank_screen": False,
        "all_ids_found": False,
        "missing_ids": [],
    }

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for non-2xx status codes
        results["url_present"] = True
        
        soup = BeautifulSoup(response.content, "html.parser")
        text = soup.get_text(strip=True)  # Get text content without whitespace

        if not text:
            results["blank_screen"] = True
        else:
            found_ids = []
            for id_ in ids:
                if soup.find(id=id_):
                    found_ids.append(id_)
                else:
                    if soup.find_all("div", {"class": id_}):
                        found_ids.append(id_)
        
        results["all_ids_found"] = len(found_ids) == len(ids)
        results["missing_ids"] = [id_ for id_ in ids if id_ not in found_ids]

    except requests.exceptions.RequestException as e:
        print(f"Error: Could not reach URL: {url} ({e})")

    print(results)
    return results

if __name__ == "__main__":

    main(env, split, test_data)