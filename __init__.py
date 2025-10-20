from __future__ import absolute_import, print_function, unicode_literals
from .NektarPacer import NektarPacer

def create_instance(c_instance):
    return NektarPacer(c_instance)