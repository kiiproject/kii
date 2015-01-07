import re
from django.utils.encoding import force_unicode
from django.utils.html import strip_spaces_between_tags as short

_RE_NO_SPACELESS_BDELIM = re.compile(u"<!-- BEGIN NO SPACELESS -->")
_RE_NO_SPACELESS_EDELIM = re.compile(u"<!-- END NO SPACELESS -->")

# from http://www.kd7eek.com/resources/software/python-django/middleware/
def awesome_strip_spaces_between_tags(value, _bre = _RE_NO_SPACELESS_BDELIM, _ere = _RE_NO_SPACELESS_EDELIM):
    """Returns the given HTML with spaces between tags removed.
       Enhanced With Pre tag Awesomeness """
    _val = force_unicode(value)

    index = 0
    rejoin = []

    while index < len(_val):
        _begin_match = _bre.search(_val, index)
        if _begin_match is None:
            break
        begin_index = _begin_match.start()
        begin_length = _begin_match.end() - begin_index

        _end_match = _ere.search(_val, begin_index+begin_length)
        if _end_match is None:
            break
        end_index = _end_match.start()
        end_length = _end_match.end() - end_index

    if begin_index > index:
        rejoin.append(short(_val[index:begin_index]))
        rejoin.append(_val[begin_index + begin_length:end_index])
        index = end_index + end_length

    if index < len(_val):
        rejoin.append(short(_val[index:]))

    return u''.join(rejoin)