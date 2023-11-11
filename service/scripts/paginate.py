import requests

url = "http://127.0.0.1:8000/list_user"


class CustomIterator:
    def __init__(self, url):
        self.url = url

    def __iter__(self):
        return self

    def __next__(self):
        if self.url:
            data = requests.get(self.url).json()
            self.url = data["next"]
            return data["results"]
        raise StopIteration

result = ""
for page in CustomIterator(url):
    for user in page:
        result += user["username"]
print(result)
