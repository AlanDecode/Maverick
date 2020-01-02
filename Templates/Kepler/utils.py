# -*- coding: utf-8 -*-
"""utils

utils for Kepler
"""

import os
import json
from Maverick.Config import g_conf
from Maverick.Utils import unify_joinpath, safe_read

g_translation = None


def tr(str, locale="english"):
    """translation support

    translate str according to translation file
    """
    global g_translation
    if g_translation is None:
        path = unify_joinpath(os.path.dirname(
            __file__) + '/locale', g_conf.language+".json")
        g_translation = json.loads(safe_read(path) or '{}')

    return g_translation.get(str, str)

