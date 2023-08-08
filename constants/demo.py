# -*- coding: utf-8 -*-

from git import *
import os


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
repo = Repo(os.path.join(CURRENT_DIR, ''))

print(repo.remotes)