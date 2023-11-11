import json
import random
import string
import datetime


class GenerateJsonData:
    def generate_users(self, n):
        return [
            {
                "model": "service.User",
                "pk": i + 1,
                "fields": {"username": f"user{i + 1}",
                           "email": f"user{i + 1}@gmail.com",
                           "password": "".join(random.choices(string.ascii_letters, k=20))}
            } for i in range(n)
        ]

    def generate_dialogs(self, n):
        dt = datetime.datetime.now()
        return [
            {
                "model": "service.Dialog",
                "pk": i + 1,
                "fields": {"name": f"dialog{i + 1}",
                           "time_create": dt.strftime("%Y-%m-%d %H:%M:%S"),
                           "users": [i + 1, i + 2]}
            } for i in range(n-1)
        ]


    def generate_messages(self, n):
        dt = datetime.datetime.now()
        return [
            {
                "model": "service.Message",
                "pk": i + 1,
                "fields": {"text": f"message{i + 1}",
                           "time_creation": dt.strftime("%Y-%m-%d %H:%M:%S"),
                           "time_update": dt.strftime("%Y-%m-%d %H:%M:%S"),
                           "text_changed": False,
                           "user": i + 1,
                           "dialog": i + 1}
            } for i in range(n - 1)
        ]


    def generate_alboms(self, n):
        dt = datetime.datetime.now()
        return [
            {
                "model": "service.Album",
                "pk": i + 1,
                "fields": {"name": f"album{i + 1}",
                           "time_creation": dt.strftime("%Y-%m-%d %H:%M:%S"),
                           "user": i + 1}
            } for i in range(n)
        ]


    def generate_photos(self, n):
        dt = datetime.datetime.now()
        return [
            {
                "model": "service.Photo",
                "pk": i + 1,
                "fields": {"description": f"description{i + 1}",
                           "path": f"photo{i + 1}",
                           "time_creation": dt.strftime("%Y-%m-%d %H:%M:%S"),
                           "album": i + 1}
            } for i in range(n)
        ]


    def generate(self, n):
        return (
                self.generate_users(n) +
                self.generate_dialogs(n) +
                self.generate_messages(n) +
                self.generate_alboms(n) +
                self.generate_photos(n)
        )


if __name__ == "__main__":
    with open("dump.json", "w") as f:
        json.dump(GenerateJsonData().generate(10), indent=2, fp=f)
