import traceback
from io import StringIO

import common


class ObjectConvertor:
    @staticmethod
    def _to_basic(o: object):
        if isinstance(o, int) or isinstance(o, float):
            r = str(o)
        elif isinstance(o, bool):
            r = str(o).lower()
        else:
            r = '"%s"' % str(o).replace('\n', '\\n').replace('"', '\\"')
        return r

    @staticmethod
    def _to_list(l: list):
        r = ''
        for i in l:
            if r != '':
                r += ', '
            r += ObjectConvertor.to_object(i)
        return '{%s}' % r

    @staticmethod
    def _to_dict(d: dict):
        r = ''
        for k, v in d.items():
            if r != '':
                r += ', '
            r += '%s: %s' % (k, ObjectConvertor.to_object(v))
        return '{%s}' % r

    @staticmethod
    def to_object(o: object):
        if isinstance(o, list):
            r = ObjectConvertor._to_list(o)
        elif isinstance(o, dict):
            r = ObjectConvertor._to_dict(o)
        else:
            r = ObjectConvertor._to_basic(o)

        return r


class AppleScript:
    @staticmethod
    def exec(code: str):
        stat = -1
        out = ''

        try:
            p = common.popen('/usr/bin/osascript')
            p.stdin.write(code)
            p.stdin.close()
            out = p.stdout.read()
            err = p.stderr.read()
            stat = p.wait()
        except:
            with StringIO() as io:
                traceback.print_exc(file=io)
                io.seek(0)
                err = io.read()

        if stat != 0:
            print('code exec error:\nstatus: %d\nmsg: %s\ncode: %s' % (stat, err, code))

        return stat, out, err