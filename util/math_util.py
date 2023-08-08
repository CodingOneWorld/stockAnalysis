# -*- coding: utf-8 -*-

# 一些数学工具


# 列表工具
class List_util():
    # 判断是否是正序
    @staticmethod
    def isAZ(nums):
        l = []
        for num in nums:
            l.append(num)
        l.sort()
        for i in range(len(l)):
            if l[i] == nums[i]:
                continue
            else:
                return False
        return True

    # 判断是否是倒序
    @staticmethod
    def isZA(nums):
        l = []
        for num in nums:
            l.append(num)
        l.sort(reverse=True)
        for i in range(len(l)):
            if l[i] == nums[i]:
                continue
            else:
                return False
        return True


if __name__ == '__main__':
    l = [1, 2, 3]

    print(List_util.isAZ(l))
