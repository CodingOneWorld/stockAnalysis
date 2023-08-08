# -*- coding: utf-8 -*-

from git import *
import os


# 返回当前仓库名
def get_cur_repo():
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    repo = Repo(os.path.join(CURRENT_DIR, ''))
    cur_repo=repo.head.reference

    return str(cur_repo)


if __name__ == '__main__':
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    repo = Repo(os.path.join(CURRENT_DIR, ''))

    # print(repo.remotes)
    # print(repo.heads)
    # print(repo.head.reference)
    #
    # branches = repo.branches
    # for branch in branches:
    #     print(branch.name)

    cur_repo=get_cur_repo()
    print(cur_repo)
    print(type(str(cur_repo)))
