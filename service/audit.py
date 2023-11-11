import logging
from contextlib import contextmanager

from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from django.db.models import Model
from django.forms import model_to_dict

FIELDS_TO_HIDE = ["password"]
SECRETS_MASK = "*****"

logger = logging.getLogger("service.views")


def calc_diff(before_info, after_info):
    try:
        logger.info("Создание сообщения")
        log_before = {}
        log_after = {}
        ignored_fields = [
            "last_login",
            "date_joined",
        ]
        for key in before_info:
            if not (key is ignored_fields) and before_info[key] != after_info[key]:
                log_before[key] = before_info[key]
                log_after[key] = after_info[key]
        return {"change": {"fields": {"old": log_before, "new": log_after}}}
    except Exception as e:
        logger.error(f"Сообщение не созданно {e}")


def recur_encode_data(data, hide_msg=SECRETS_MASK):
    try:
        logger.info("Создание сообщения")
        def recur(_data):
            if isinstance(_data, dict):
                for k, v in _data.items():
                    if k in FIELDS_TO_HIDE:
                        _data[k] = hide_msg
                    recur(v)
            elif isinstance(_data, (set, list, tuple)):
                for el in _data:
                    recur(el)
            else:
                pass

        recur(data)
        return data
    except Exception as e:
        logger.error(f"Сообщение не созданно {e}")


@contextmanager
def change_log(user, obj: Model):
    try:
        logger.info("Создание аудита")
        before_info = model_to_dict(obj)
        yield
        obj.refresh_from_db()
        after_info = model_to_dict(obj)
        logger.info("Данные для сообщения собраны успешно")
        change_msg = calc_diff(before_info, after_info)
        logger.info("Сообщение составленно успешно")
        LogEntry.objects.create(
            user=user,
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.pk,
            object_repr=obj.pk,
            action_flag=CHANGE,
            change_message=recur_encode_data(change_msg),
        )
        logger.info("Создание аудита прошло успешно")
    except Exception as e:
        logger.error(f"Аудит не создан {e}")

def add_log(user, obj: Model):
    try:
        logger.info("Создание аудита")
        LogEntry.objects.create(
            user=user,
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.pk,
            object_repr=obj.pk,
            action_flag=ADDITION,
            change_message=recur_encode_data({"add": {"fields": model_to_dict(obj)}})
        )
        logger.info("Создание аудита прошло успешно")
    except Exception as e:
        logger.error(f"Аудит не создан {e}")


def delete_log(user, obj: Model):
    try:
        logger.info("Создание аудита")
        LogEntry.objects.create(
            user=user,
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.pk,
            object_repr=obj.pk,
            action_flag=DELETION,
            change_message=recur_encode_data({"delete": {"fields": model_to_dict(obj)}})
        )
        logger.info("Создание аудита прошло успешно")
    except Exception as e:
        logger.error(f"Аудит не создан {e}")