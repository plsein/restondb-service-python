# utils
import calendar
import json
import re
import time
import flask
from werkzeug.utils import secure_filename
from configs.config import CONFIG


class SingletonMetaClass(type):
    """
    Singleton Meta Class
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMetaClass, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class AppUtils:

    @classmethod
    def to_file(cls, path, data):
        with open(path, 'w') as f:
            f.write(data)

    @classmethod
    def make_response(cls, data: any, code: int = 200, msg: any = None, is_json=True):
        if is_json:
            if not msg:
                msg = {"status": "ok"}
            if int(code) < 200 or int(code) >= 300:
                if CONFIG['DEBUG']:
                    if isinstance(data, list) and len(data) > 0 and 'Exception' in data[0]:
                        data = data
                    else:
                        data = [{"Exception": data}]
                else:
                    data = []
            resp = flask.make_response(json.dumps({"code": code, "message": msg, "data": data}))
            resp.mimetype = 'application/json'
            return resp
        else:
            # return json.dumps({"code": code, "message": msg, "data": data})
            return data

    @classmethod
    def file_upload(cls, type_val, id_val, field, file):
        file.save(f"uploads/{type_val}/{id_val}/{field}/{secure_filename(file.filename)}")

    @classmethod
    def escape_string(cls, text):
        regex_slash = {"search": re.escape("\\"), "replace": re.escape("\\\\")}
        regex_hyphen = {"search": r"--", "replace": "&minus;&minus;"}
        regex_semicolon = {"search": r";", "replace": "&#59;"}
        regex_list = [regex_slash, regex_hyphen, regex_semicolon]
        if text.count("'") % 2 != 0:
            regex_quote = {"search": r"'", "replace": "''"}
            regex_list.append(regex_quote)
        for regex_q in regex_list:
            text = re.sub(regex_q["search"], regex_q["replace"], text)
        return text

    @classmethod
    def current_timestamp(cls):
        # Current UTC time in a tuple format
        current_utc_time = time.gmtime()
        # ts stores timestamp
        return calendar.timegm(current_utc_time)


metadic = {}


def _generatemetaclass(bases, metas, priority):
    trivial = lambda m: sum([issubclass(M, m) for M in metas], m is type)
    # hackish!! m is trivial if it is 'type' or, in the case explicit
    # metaclasses are given, if it is a superclass of at least one of them
    metabs = tuple([mb for mb in map(type, bases) if not trivial(mb)])
    metabases = (metabs + metas, metas + metabs)[priority]
    if metabases in metadic:  # already generated metaclass
        return metadic[metabases]
    elif not metabases:  # trivial metabase
        meta = type
    elif len(metabases) == 1:  # single metabase
        meta = metabases[0]
    else:  # multiple metabases
        metaname = "_" + ''.join([m.__name__ for m in metabases])
        meta = makecls()(metaname, metabases, {})
    return metadic.setdefault(metabases, meta)


def makecls(*metas, **options):
    """Class factory avoiding metatype conflicts. The invocation syntax is
    makecls(M1,M2,..,priority=1)(name,bases,dic). If the base classes have
    metaclasses conflicting within themselves or with the given metaclasses,
    it automatically generates a compatible metaclass and instantiate it.
    If priority is True, the given metaclasses have priority over the
    bases' metaclasses"""

    priority = options.get('priority', False)  # default, no priority
    return lambda n, b, d: _generatemetaclass(b, metas, priority)(n, b, d)
