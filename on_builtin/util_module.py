# TODO
# - var Block 지정(시작 문자열, 끝 문자열): var 외의 다른 코드들과 섞여있는 경우 대비

import re
import json
from pprint import pprint


content="""
##@ PACKAGE AREA
#==============================================


##@ VAR AREA
#==============================================

var0 = "1234"

var1 = "12345678910111213123456789101112131234567891011121312345678910111213123456789101112131234567891011121312345678910111213123456789101112131234567891011121312345678910111213123456789101112131234567891011121312345678910111213"

var2 = 1234

var3 = [
    1,
    2,
    3,
    4
]

var5 = [
    1,
    2,
    3,
    4
]

var6 = {
    "a": 1,
    "b": 2,
    "c": 3
}

##@ FUNCTION AREA
#==============================================



## MAIN AREA
#==============================================
"""

VAR_AREA_BGN = """##@ VAR AREA
#==============================================
"""

VAR_AREA_END = """
##@ """


datas = dict(
    var0 = '1234',
    var1 = "12345678910111213123456789101112131234567891011121312345678910111213123456789101112131234567891011121312345678910111213123456789101112131234567891011121312345678910111213123456789101112131234567891011121312345678910111213",
    var2 = 1234,
    var3 = [1, 2, 3, 4],
    var5 = [
        1,
        2,
        3,
        4
    ],
    var6 = {
        'a': 1,
        'b': 2,
        'c': 3,
    },
)


def _var_area(content, bgn=VAR_AREA_BGN, end=VAR_AREA_END):
    """var area
    """
    return re.findall(f"{bgn}.+{end}", content, flags=re.DOTALL)


def _replace_var_area(content, repl, bgn=VAR_AREA_BGN, end=VAR_AREA_END):
    """content에서 var 영역을 repl로 치환
    """
    pattern = _var_area(content, bgn=bgn, end=end)
    if pattern:
        print(f"{pattern=}")
        content = content.replace(pattern[0], f"{bgn}\n{repl}\n{end}")
    else:
        content = f"{bgn}\n{repl}\n{end}"
    return content


def _to_json(data, path=None, save=True):
    """data를 json 형식으로 변경
    """
    if save:
        path = 'test.json' if not path else path
        with open(path, "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    else:
        json.dumps(data, ensure_ascii=False, indent=4)


def _to_py_one(name, data, path=None):
    data = f"{name} = {json.dumps(data, ensure_ascii=False, indent=4)}"
    path = 'test.py' if not path else path
    with open(path, "w") as f:
        f.write(data)


def _to_py_new(datas, path=None, sep="\n\n"):
    """datas {'name1': data1, 'name2': data2, ...} 를 변수로 하는 .py 생성 또는 덮어씀
    """
    content = ''
    path = 'test.py' if not path else path
    for name, data in zip(datas.keys(), datas.values()):
        content += f"{name} = {json.dumps(data, ensure_ascii=False, indent=4)}{sep}"

    with open(path, "w+") as f:
        f.write(content)


def _update_py_var(datas, path=None, sep="\n\n"):
    """datas {'name1': data1, 'name2': data2, ...} upsert(insert + update)
    """
    pass


# def _data_block(name, type=None, path=None):
#     """datas {'name1': data1, 'name2': data2, ...} upsert(insert + update)
#     """
#     with open(path, "r") as f:
#         content = f.read()
#     print(content)


def _regex_block(name, type):
    """name, type을 가지는 data 블럭의 정규표현식
    """
    return name + " *= *\[.+?\n\]\n" if type == list else name + " *= *\{.+?\n\}\n" if type == dict else name + " *= *.+?\n"


def _data_block(content, **datas):
    """content 내에 있는 data 블럭
    """
    print('='*100)
    for name, data in zip(datas.keys(), datas.values()):
        s = re.findall(_regex_block(name, type(data)), content, flags=re.DOTALL)
        # s = re.findall(_regex_block(name, type(data)), content, flags=re.DOTALL | re.MULTILINE)
        if s:
            print(f"_data_block name: {name} var: {s[0]}")
        print('-'*80)



# def _regex_block(name, data):
#     if type(data) == list:
#         regex = name + " *= *\[.+?\n\]"
#     elif type(data) == dict:
#         regex = name + " *= *\{.+?\n\}"
#     else:  # str, int, float
#         regex = name + " *= *.+"


def _data_to_py_one(name, data, path):
    # print(f"{name=} {data=} {path=}")
    if type(data) == str:
        pass
    elif type(data) == int or type(data) == float:
        pass

    regex = name + " *= *\{[\S\n ]*?\n\}\n"  ## NOTE: python에 삽입된 block 내용


def _data_to_py(path, **datas):
# def _data_to_py(data, name, path=None):
    """data를 python 파일에 삽입(생성,추가,수정)
    """
    for name, data in zip(datas.keys(), datas.values()):
        _data_to_py_one(name, data, path)


if __name__ == "__main__":
    data = dict(
        a = [1,2,3,4],
        b = dict(
            A = '2',
            B = '4'
        ),
        c = [(1, 2), ('3', '4')]
    )
    path = "D:/moon/dev/projects/_test/test1.json"
    _to_json(data, path=path, save=True)





# # -*- coding=utf-8 -*-
# """
# 주요 기능: 
#     - 패키지/모듈 관리
#     - 패키지 내 모듈
#     - 모듈 내 imports / constants / classes / functions 목록

# 사용 방법: 
#     - 


# """

# ##@@@ Package/Module
# ##============================================================

# ##@@ Built-In Package/Module
# ##------------------------------------------------------------
# import os, sys
# from datetime import datetime, timedelta

# ##@@ External Package/Module
# ##------------------------------------------------------------

# ##@@ User Package/Module
# ##------------------------------------------------------------
# sys.path.append(os.path.join(os.path.dirname(__file__), "."))
# from util_basic import (_file_list, _folder_list, _split_path, _write_file, _to_lists)
# from google_sheets import GoogleSheets

# sys.path.append(os.path.join(os.path.dirname(__file__), "../../mp_stock/mp_stock"))
# from configs._googles import bot_nick, _CONFIGS, sheets


# ##@@@ Constant/Varible
# ##============================================================

# ##@@ path, var
# ##------------------------------------------------------------
# ROOT = "C:/Dev/"
# # TODAY = datetime.now().strftime("%Y%m%d")
# # MS = Mysql(name='mysql_HMS_local', db='sats')


# ##@@@ Private Function
# ##============================================================
# # def _to_googlesheets():
# #     logs = MS.find(f"log_req_{TODAY}")  # NOTE: API 요청
# #     logs = [dict(log, time=str(log['time'])) for log in logs]
# #     gs = GoogleSheets(bot_nick=bot_nick, id=sheets['logs_daily']['id'])
# #     gs.write_sheet(sheet_name=TODAY, sheet_range=None, values=_to_lists(logs))

# def _packages(root=ROOT):
#     paths = _folder_list(root, ignores=["temp", "test"], recursive=False)
#     names = [path.replace(root, "").replace("/", "") for path in paths]
#     return [dict(name=name, path=path) for (name, path) in zip(names, paths)]
#     # path, ignores=[], recursive=True


# def _moldules(folder="C:/Dev/mp_util/mp_util/"):
#     files = _file_list(folder, finds=["*.py"], recursive=True)
#     print(files)


# def _extract_imports():
#     pass


# def _extract_globals():
#     pass


# def _extract_functions():
#     pass


# def _extract_classes():
#     pass


#     # time     | acnt_no | req_code | result_code | user | agency | cnt_10m | module    | function | message


# ##@@ util function 
# ##------------------------------------------------------------

# ##@@ sub function
# ##------------------------------------------------------------


# ##@@@ Public Class/function
# ##============================================================

# ##@@ 
# ##------------------------------------------------------------


# ##@@@ Main Function(테스트용)
# ##============================================================
# if __name__ == "__main__":
#     pass
#     ## NOTE: packages
#     # r = _packages()
#     r = _moldules(folder="C:/Dev/mp_util/mp_util/")
#     print(r)





    # my_dir = "C:\data\projects"
    # print(to_raw(my_dir))
    # name = "var1"
    # path = "D:/moon/dev/projects/_test/test1.py"
    # _data_block(name, type=None, path=path)

    # _data_block(content, **datas)

    # # content = _var_area(content, bgn="~~"+VAR_AREA_BGN, end=VAR_AREA_END)
    # repl = "_var1 = '1234'\n\n"
    # content = _replace_var_area(content, repl, bgn=VAR_AREA_BGN, end=VAR_AREA_END)

    # print(content)

    # datas = dict(
    #     var0 = '1234',
    #     var1 = "12345678910111213123456789101112131234567891011121312345678910111213123456789101112131234567891011121312345678910111213123456789101112131234567891011121312345678910111213123456789101112131234567891011121312345678910111213",
    #     var2 = 1234,
    #     var3 = [1, 2, 3, 4],
    #     var5 = [
    #         1,
    #         2,
    #         3,
    #         4
    #     ],
    #     var6 = {
    #         'a': 1,
    #         'b': 2,
    #         'c': 3,
    #     },
    # )


    # # _to_json(data, path=None, save=True)
    # # _to_py_one(name, data, path=None)
    # _to_py_new(datas, path=None)


    # print(name(d=d))

# def _data_to_py(data, name, path):
#     """data를 python 파일에 삽입(생성,추가,수정)
#     """
#     pass


# def _packed_json_from_spec_dict_old(src=""):
#     """res spec dict(python 변수용) <- packed json
#     Args:
#         src (str, ""): [description]. Defaults to None.
#     Returns:
#         dict(json): [description]
#     """
#     regex = BLOCK_VAR + " *= *\{[\S\n ]*?\n\}\n"  ## NOTE: python에 삽입된 block 내용
#     data = re.findall(regex, src)[0].split("=", 1)[1].strip()
#     data = re.sub(r' # *"', ' "#', data)  # 제외 필드
#     data = re.sub(r'" *: *\{ *#+ *(.+)', r'##\1": {', data)  # 블럭 desc
#     data = re.sub(r'" *: *"*(.*?)"*(,*) *#+ *(.+)', r'": "\1##\3"\2', data)  # 필드 remark 
#     data = re.sub(r'\},\n+( *)\}', r'}\n\1}', data)  # 불필요한 ',' 제거

#     return json.loads(data)



# def _spec_dict_from_packed_json(src=""):
#     """res spec dict(python 변수용) <- packed json
#     Args:
#         src (str, ""): [description]. Defaults to None.
#     Returns:
#         str: [description]
#     """
#     # src = src.replace('"0`', '# "').replace('"1`', '"')  # field key (사용여부에 따라) 코멘트 처리
#     src = src.replace('"#`', '# "')  # field key 코멘트 처리
#     src = re.sub(r'"(.+)`(.*)" *: *\{', r'"\1": { #@ \2', src)  # block field key
#     src = re.sub(r': *"(.+)`(.*)"(,*) *', r': "\1"\3 #@ \2', src)  # block field val

#     return f"{BLOCK_VAR} = {src}" # block 시작 문자열 추가


# _spec_dict_from_packed_json(src=json.dumps(src, ensure_ascii=False, indent=4))