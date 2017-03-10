# encoding:utf-8

import xlrd
import re
import os

def duplicate_removal(new_uid_list):
    file_list = os.listdir(os.getcwd())
    old_uid_list = []
    for i in file_list:
        if i.isdigit():
            old_uid_list.append(i)
    if new_uid_list==old_uid_list:
        return []
    else:
        old_uid_list = set(old_uid_list)
        new_uid_list = set(new_uid_list)
        uid_list = old_uid_list ^ new_uid_list
        return uid_list




def get_excel_uid(file_name):
    new_uid_list = []
    data = xlrd.open_workbook(file_name)
    table = data.sheets()[0]
    uid_data = table.col_values(0)
    for i in uid_data:
        try:
            uid = re.search("u/\d*", i).group()
        except AttributeError:
            pass
        new_uid_list.append(str(re.search("\d+", uid).group()))
    uid_list = duplicate_removal(new_uid_list)
    print(len(uid_list))
    return uid_list



if __name__ == '__main__':
    # get_excel_uid("uid_file.xlsx")
    duplicate_removal()
