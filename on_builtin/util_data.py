# -*- coding=utf-8 -*-
"""
주요 기능: python 기본 유틸(자료형 변환/파일/)
    - 문자열 검색/치환/정규식
    - 데이터(dict/list/dicts/lists/dataframe/...) 변환
    - 각종 파일(json/csv/xlsx/yml/...) 읽기/쓰기
    - 디버그/기타

사용례: 
    - 
"""

##@@@ Package/Module
##============================================================

##@@ Built-In Package/Module
##------------------------------------------------------------
import os, sys
from pathlib import Path
import re, json
from glob import glob
from itertools import product

##@@ External Package/Module
##------------------------------------------------------------
import yaml
import pandas as pd

##@@ User Package/Module
##------------------------------------------------------------

##@@@ Constant/Varible
##============================================================

##@@ path, var
##------------------------------------------------------------

##@@@ Private Function
##============================================================

##@@ str(문자열 검색/치환/정규식)
##------------------------------------------------------------
def _replace_regex(maps={}, string=""):
    """_replace_regex: 정규식(regex)을 사용한 문자열 치환
    Desc:
        - 문자열 치환(정규식) 반복

    Args:
        - maps(dict, {}): 치환 패턴 목록  예) {r'\s*\n+\s*': ';', r';{2,}': ';'}
        - string(str, ""): 치환 대상 문자열

    Returns:
        - str: 치환후 문자열

    Usages:
        - _replace_regex(maps={r'\s*\n+\s*': ';', r';{2,}': ';'}, string=" \n\n abc;;;def")
    """    
    for key, val in maps.items():
        string = re.sub(key, val, string)
    return string


def _replace_str(repls, _str):
    """문자열 치환
    _str: 대상 문자열
    _rep: 치환 규칙 dictionary {'A': 'a', 'r_(\d+)', '\1-'} / list [('A', 'a'), ('r_(\d+)', '\1-'), ...]
    """
    def _replace(p, r, _str):
        (p, p_re) = (p[2:] if p[:2] == "r_" else p, p[:2] == "r_")
        _str = re.sub(p, r, _str) if p_re else _str.replace(p, r)

    if type(repls) == dict:
        for p, r in repls.items():
            _str = _replace(p, r, _str)
    else:
        for (p, r) in repls:
            _str = _replace(p, r, _str)
    
    return _str


def _insert_join(patterns=[], replacements=[], content=""):
    """
    content(문자열)에 포함된 patterns들을 replacements로 대체(replace(X) insert and join)
    NOTE: 속도(성능) 차이 분석
    content = "abcdefghijklmnopqrstuvwxyz"*10000
    patterns=['d', 'j', 'm', 'x']
    replacements=['D', 'J', 'M', 'X']
        insert_join time : 0.0003902912139892578
        replace time : 0.0005877017974853516
    """
    if len(patterns) == len(replacements):
        splits = []
        for pattern in patterns:
            (piece, content) = content.split(pattern, 1)
            splits.append(piece)
        splits.append(content)
    else:
        return None

    result = splits[0]
    for i, repl in enumerate(replacements):
        result = repl.join([result, splits[i+1]])

    return result


def _to_digit(string=""):
    """_to_digit: 숫자 추출
    Desc:
        - 숫자, '.', '-'를 제외한 문자 모두 제거

    Args:
        - string(str, ''): 추출 대상 문자열  예) "100,500.5원"

    Returns:
        - int|float: 100500.5
    """    
    string = re.sub('[^\d.\-]', '', string)
    string = '0' if string == '' else string
    return float(string) if '.' in string else int(string)


##@@ 반복/loop
##------------------------------------------------------------
def _multi_iter(data):
    """
    data = {"i": [1, 2, 3], "j": [4, 5, 6], "k": [9, 10]}
    return [{'i': 1, 'j': 4, 'k': 9}, {'i': 1, 'j': 4, 'k': 10}, ..., {'i': 3, 'j': 6, 'k': 10}]
    """
    return list(dict(zip(data.keys(), values)) for values in product(*data.values()))


##@@ 데이터(dict/list/dicts/lists/dataframe/...) 처리/변환
##------------------------------------------------------------
def _to_slices(data, size):
    """data리스트를 size개씩 묶음
    Args:
        data (list): 리스트 예) ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k']
        size (int): 묶음 수 예) 3

    Returns:
        [list of list]: [['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h', 'i'], ['j', 'k']]
    
    Refs:
        https://hleecaster.com/python-how-to-split-a-list-into-chunks/
    """
    return [data[i*size:(i+1)*size] for i in range((len(data)+size-1)//size)]


def _duplicates(xs):
    """
    리스트에서 중복인 원소들
    """
    once = set()
    seenOnce = once.add
    return list(set(x for x in xs if x in once or seenOnce(x)))


def _flatten_list(xs):
    """리스트 내의 리스트 제거 -> 1차원 배열
    xs = [['1', '2', ['3', '4', ['5', 6]]], ['7', 'a', ['b', 'c']]]
    flatten_list(xs): ['1', '2', '3', '4', '5', 6, '7', 'a', 'b', 'c']

    Args:
        xs ([type]): [description]

    Returns:
        [type]: [description]

    Refs:
        https://towardsdatascience.com/30-helpful-python-snippets-that-you-can-learn-in-30-seconds-or-less-69bb49204172
    """
    flat_list = []
    [flat_list.extend(_flatten_list(x)) for x in xs] if isinstance(xs, list) else flat_list.append(xs)
    return flat_list


def _difference_list(a, b):
    """리스트 차집합(A - B)
    a = ['1', '2', '3', '4']
    b = ['2', '3', '5']
    difference_list(a, b) : ['4', '1']

    Args:
        a ([list]): [description]
        b ([list]): [description]

    Returns:
        [type]: [description]
    """
    return list(set(a).difference(set(b)))


def _filter_dicts(dicts, filter):
    """dicts에서 filter 조건에 맞는 dict만 추출

    Args:
        dicts (list of dictionary): 
        filter ([type]): [description]

    Returns:
        [list of dictionary]: [description]
    
    Usages:
        dicts = [
            {'a': 1, 'b': 2, 'c': 3},
            {'a': 1, 'b': 3, 'c': 4},
            {'a': 1, 'b': 2, 'c': 8},
        ]
        filter = {'a': 1, 'b': 2}
        _filter_dicts(dicts, filter)

        return: [{'a': 1, 'b': 2, 'c': 3}, {'a': 1, 'b': 2, 'c': 8}]
    """
    remove_indices = []
    for k, v in filter.items():
        for i, d in enumerate(dicts):
            if d[k] != v:
                remove_indices.append(i)

    dicts = [i for j, i in enumerate(dicts) if j not in remove_indices]
    return dicts


def _find_in_dicts(dicts=[], filter={}, pops=[], one=True):
    """dicts에서 filter에 해당하는 dicts/dict 반환

    Args:
        dicts (list, optional): [description]. Defaults to [].
        filter (dict, optional): [description]. Defaults to {}.
        pops (list, optional): [description]. Defaults to [].

    Returns:
        [type]: [description]
    """
    dicts = _filter_dicts(dicts, filter)
    if one:
        d = dicts[0]
        for p in pops:
            d.pop(p)
        return d
    else:
        for d in dicts:
            for p in pops:
                d.pop(p)
        return dicts


def _inserts(ins=[], target=[]):
    """다중 삽입multiple insert
    ins: [(idx1, val1), ...] idx 오름차순으로 정렬되어 있어야 함!! TODO: 자동 정렬...
    target: insert 대상 list
    """
    for i, (pos, val) in enumerate(ins):
        target.insert(pos+i, val)
    return target

##@@ nested
##------------------------------------------------------------
def _get_value_nested(path, nested):
    """path (key0, key1, key2, ...) -> nested[key1][key2][key3]
    """
    for i, key in enumerate(path):
        if i == len(path) -1: return nested[key]
        else: return _get_value_nested(path[i+1:], nested[key])


def _set_value_nested(value, path, nested):
    for i, key in enumerate(path):
        if i == len(path) -1:
            nested[key] = value
            return nested[key]
        else: 
            return _set_value_nested(value, path[i+1:], nested[key])


def _get_items_nested(nested):
    """
    전체 아이템 (key, val)
    for key, value in _get_items_nested(nested):
        print(key, value)
    """
    for key, value in nested.items():
        if type(value) is dict:
            yield (key, value)
            yield from _get_items_nested(value)
        else:
            yield (key, value)


def _get_path_nested(value, nested, prepath=()):
    """
    val값을 가지는 path
    """
    iters = nested.items() if isinstance(nested, dict) else enumerate(nested)  # dict/list 
    for k, v in iters:
        path = prepath + (k,)
        if v == value: # found value
            return path
        elif isinstance(v, dict) or isinstance(v, (dict, list)):
        # elif isinstance(v, dict) or isinstance(v, list):
            p = _get_path_nested(value, v, path) # recursive call
            if p is not None:
                return p


def _get_path_nested_by_key(key, nested, prepath=()):
    """
    하위 key값을 가지는 path
    """
    iters = nested.items() if isinstance(nested, dict) else enumerate(nested)  # dict/list 
    for k, v in iters:
        path = prepath + (k,)
        if k == key: # found key
            return path
        # elif hasattr(v, 'items'): # v is a dict
        elif isinstance(v, dict) or isinstance(v, (dict, list)):
        # elif isinstance(v, dict) or isinstance(v, list):
            p = _get_path_nested_by_key(key, v, path) # recursive call
            if p is not None:
                return p


def _sort_nesteds(path, nesteds):
    """
    path 기준으로 정렬
    """
    return sorted(nesteds, key = lambda x: _get_value_nested(path, x))


##@@ dict / dicts / lists / df
##------------------------------------------------------------
def _dicts_to_dict(dicts=[], key=''):
    """dicts -> dict (key: )

    Args:
        dicts (list, optional): dict 리스트 ex) [{'a': 'k1', 'b': 2}, {'a': 'k2', 'b': 3}]. Defaults to [].
        key (str, optional): 키값으로 사용할 key ex) 'a'. Defaults to ''.

    Returns:
        [dict]: ex) {'k1': {'b': 2}, 'k2': {'b': 3}}
    """
    return {d.pop(key): d for d in dicts}


def _dicts_to_lists(dicts):
    """_dicts_to_lists: 딕션너리 배열 -> 2차원 배열
    Desc:
        - dicts: 딕션너리 배열 
        - lists: 2차원 배열 [['a', 'b'], [1, 2], [3, 4]]

    Args:
        - dicts(list): 딕션너리 배열 [{'a': 1, 'b': 2}, {'a': 3, 'b': 4}]

    Returns:
        - [list]: 2차원 배열 [['a', 'b'], [1, 2], [3, 4]]

    Usages:
        - _dicts_to_lists([{'a': 1, 'b': 2}, {'a': 3, 'b': 4}])
    """    
    return [list(dicts[0].keys())] + pd.DataFrame(dicts).values.tolist()


def _to_lists(data, header=True):
    """_to_lists: data를 2차원 배열로 변환
    Desc:
        - dicts, dataframe -> lists

    Args:
        - data(list|dataframe): [description]
        - header(bool, True): True: header 포함 / False: header 제외

    Returns:
        - list: 2차원 배열  [['a', 'b'], [1, 2], [3, 4]]

    Usages:
        - _to_lists([{'a': 1, 'b': 2}, {'a': 3, 'b': 4}])
    """    
    if 'frame' in str(type(data)):  ## dataframe
        data = [list(data.columns)] + data.values.tolist()  ## TODO: 확인 필요
    elif type(data[0]) == dict:   ## [{'h1': 'v1', ...}, {'h1': 'v2', ...}]
        data = _dicts_to_lists(data)

    if not header:  ## NOTE: 첫번째 행(header) 제외
        data = data[1:]

    return data


def _to_str(data, bgn="", end=""):
    _data = bgn
    if type(data) == str:
        _data += data
    elif type(data) == dict or type(data) == list:
        _data += json.dumps(data, ensure_ascii=False, indent="\t")
    elif 'frame' in str(type(data)):  ## dataframe
        _data += json.dumps(_to_dicts(data), ensure_ascii=False, indent="\t")
    else:
        _data += str(data)
    
    return _data + end


def _to_dicts(data, header=0):
    """_to_dicts: 2차원 배열|dataframe -> 딕션너리 배열
    Desc:
        - data: 2차원 배열|dataframe
        - dicts: 딕션너리 배열 
    Args:
        - data(list|dataframe): 
        - header(int, 0): 해더 위치(행번호)
    
    Returns:
        - [list]: 딕션너리 배열 [{'a': 1, 'b': 2}, {'a': 3, 'b': 4}]

    Usages:
        - _to_dicts([['a', 'b'], [1, 2], [3, 4]])
    """ 
    _data = []
    if 'frame' in str(type(data)):  ## dataframe
        _data = _to_dicts([list(data.columns)] + data.values.tolist(), header=header)
    elif type(data) == dict and (type(list(data.values())[0]) == list or tuple):  ## {'key1': [1, 2, 3], 'key2': [4, 5, 6], ...} NOTE: tuple 추가
        _data = _to_dicts(pd.DataFrame(data), header=0)
        # values = list(data.values())
        # _data = [{} for _ in range(len(values[0]))]
        # for key, vals in zip(list(data.keys()), values):
        #     for i, val in enumerate(vals):
        #         _data[i][key] = val
    elif (type(data[header]) == list or tuple):  ## [['h1', 'h2', ..], ['v1', 'v2', ...]] NOTE: tuple 추가
        for row in data[header+1:]:
            _data.append({key: val  for key, val in zip(data[header], row)})

    return _data


def _to_df(data, header=0):
    """_to_df: data(lists|dicts) -> dataframe
    Desc:
        - [extended_summary]

    Args:
        - data(lists|dicts): 
        - header(int, 0): 

    Returns:
        - datafrane: 

    Usages:
        - _to_df(data, header=0)
    """
    if not data:
        return pd.DataFrame()

    if 'frame' in str(type(data)):  # dataframe이면
        return data
    if type(data[header]) == dict:  ## [{'h1': 'v1', ...}, {'h1': 'v2', ...}]
        return pd.DataFrame(data)
    elif (type(data[header]) == list or tuple):  ## [['h1', 'h2', ..], ['v1', 'v2', ...]] NOTE: tuple 추가
        return pd.DataFrame(_to_dicts(data, header=header))


def _upsert_df(keys, *dfs):
    """dataframe upsert(combine)
    keys: upsert 기준 컬럼
    """
    df0 = dfs[0].set_index(keys)
    for df in dfs[1:]:
       df0 = df.set_index(keys).combine_first(df0)
    
    return df0.reset_index().fillna("")


##@@ folder, path
##------------------------------------------------------------
def _file_list_one(path, find="*/", recursive=True):
    find = "**/" + find if recursive else find
    path = path if path[-1] == "/" else f"{path}/"
    return [f.replace("\\", "/") for f in glob(path + find, recursive=recursive)]


def _folder_list(path, ignores=[], recursive=True):
    """폴더 목록
    ignores: ["ignore1", ...] 폴더 경로에 포함되어 있으면 목록에서 제외
    """
    folders = _file_list_one(path, find="*/", recursive=recursive)
    return [folder for folder in folders if all([not f"{ignore}" in folder for ignore in ignores])]


def _file_list(path, finds=["*"], recursive=True):
    files = set()
    finds = ["*"] if not finds else finds
    for find in finds:
        files = files | set(_file_list_one(path, find=find, recursive=True))
    return list(files)


def _abs_path(path, join=False):
    """ './', '../'
    """
    return os.path.abspath(path).replace("\\", "/")
    # path = path.replace("\\", "/")
    # if path[0] == "." or not "/" in path or join:
    #     path = os.getcwd().replace("\\", "/") + '/' + path

    # # 중간에 있는 ../ ./ 처리
    # if "../" in path:  # TODO: "../"가 2개 이상있는 경우
    #     (path1, path2) = path.split("../")
    #     path = path1[:-1].rsplit("/", 1)[0] + "/" + path2
    # elif "./" in path:  # TODO: "../"가 2개 이상있는 경우
    #     path = path.replace("./", "")
    
    # return path


def _split_path(path, sep="/", abs=False, join=False):
    path = _abs_path(path, join) if abs else path.replace("\\", sep)
    if sep in path:
        (folder, base) = path.rsplit(sep, 1)
    else:
        (folder, base) = ("", path)

    (name, ext) = base.rsplit(".", 1)
    return (folder, name, ext)


def _create_folder(path):
    """_create_folder: 폴더가 있는지 확인하고, 없으면 생성
    Args:
        - path(str): 파일 경로
    """    
    os.makedirs(os.path.dirname(path), exist_ok=True)


##@@ 각종 파일(json/csv/xlsx/yml/...) 읽기/쓰기
##------------------------------------------------------------
def _read_file(path, out_type="str", encoding="utf-8", errors='ignore'):
    """_read_file: 파일 읽기(파일 경로 -> 데이터)
    Desc:
        - out_type에 따라
        - 문자열(str) / 줄단위(line) / json / dataframe 형식으로 출력

    Args:
        - path(str): 파일 경로(파일명 포함)
        - encoding(str, "utf-8"): 인코딩: utf-8|cp949|euc-kr
        - out_type(str, "str"): 출력 형식: str(string)|list(line)|dict(json)|df(dataframe)

    Returns:
        - str|list|dict|json|dataframe: 파일 내용

    Usages:
        - _read_file("./folder/fname1.ext", out_type="line")
    """    
    ext = Path(path).suffix
    with open(path, "r", encoding=encoding, errors=errors) as f:
        if ext in ['.yml', '.yaml']:
            data = yaml.load(open(path, "r", encoding="UTF-8"), Loader=yaml.FullLoader)
        elif ext in ['.json']:
            data = json.load(f)
        elif out_type == "str":
            data = f.read()
        elif out_type == "list" or out_type == "line":
            data = f.readlines()
        elif out_type == "dict" or out_type == "json":
            data = json.load(f)
        elif out_type == "df" or out_type == "frame":
            data = _to_df(json.load(f))
        else:
            data = f.read()

    return data


def _write_file(data, path, mode="w", encoding="utf-8", start="", end=""):
    """_write_file: data를 파일로 저장
    Desc:
        - 파일 확장자(json/csv/xlsx/...)별 자동 저장

    Args:
        - data(str|dict|list|dataframe): 저장할 data
        - path(str): 저장할 파일 경로(파일명 포함)
        - encoding(str, "utf-8"): 인코딩: utf-8|cp949|euc-kr

    Usages:
        - _write_file([{'a': 'b'}, 5], "./folder1/fname2.ext", encoding="utf-8")
    """
    ext = Path(path).suffix
    if "@" in path:  # NOTE!!: path = "<sheet_name>@<file_path>"
        (sheet_name, path) = path.split("@", 1)

    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)

    if ext == '.json':
        json.dump(data, open(path, mode, encoding=encoding), ensure_ascii=False, indent="\t")
    elif ext in ['.yml', '.yaml']:
        with open(path, 'w', encoding="utf-8") as file:
            yaml.dump(data, file)
    elif ext == '.csv':
        df = _to_df(data)
        if not os.path.exists(path):
            df.to_csv(path, index=False, mode='w', header=True)
        else:
            df.to_csv(path, index=False, mode='a', header=False)
    elif ext in ['.xls', '.xlsx']:
        if not os.path.exists(path):
            with pd.ExcelWriter(path, mode='w', engine='openpyxl') as writer:
                _to_df(data).to_excel(writer, sheet_name=sheet_name, index=False)
        else:
            with pd.ExcelWriter(path, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
                _to_df(data).to_excel(writer, sheet_name=sheet_name, index=False)
    else:
        if mode == "wb":
            with open(path, mode) as f:
                f.write(data)
        else:
            if type(data) == dict or type(data) == list:
                data = json.dumps(data, ensure_ascii=False, indent="\t")
            with open(path, mode, encoding="utf-8") as f:
                data = start + data + end
                f.write(data)


def _update_file(data, path, encoding="utf-8"):
    """update file by date
    .json / .yaml / .py
    """
    ext = Path(path).suffix
    with open(path, 'r') as f:
        if ext == '.json':
            json.dump(data, open(path, encoding=encoding), ensure_ascii=False, indent="\t")
        elif ext in ['.yml', '.yaml']:
            _data = yaml.load(f, Loader=yaml.FullLoader)
            if isinstance(_data, dict):
                _data = dict(_data, **data)
            elif isinstance(_data, list) and isinstance(data, list):
                _data += data
            elif isinstance(_data, list) and isinstance(data, dict):
                _data += [data]

            with open("./yaml_test.yml", 'w') as f:
                yaml.dump(_data, f)
        elif ext == '.csv':
            df = _to_df(data)
            if not os.path.exists(path):
                df.to_csv(path, index=False, mode='w', header=True)
            else:
                df.to_csv(path, index=False, mode='a', header=False)


# def _write_file(data, path, mode="w", encoding="utf-8", start="", end="", ext=True):
#     """_write_file: data를 파일로 저장
#     Desc:
#         - 파일 확장자(json/csv/xlsx/...)별 자동 저장

#     Args:
#         - data(str|dict|list|dataframe): 저장할 data
#         - path(str): 저장할 파일 경로(파일명 포함)
#         - encoding(str, "utf-8"): 인코딩: utf-8|cp949|euc-kr

#     Usages:
#         - _write_file([{'a': 'b'}, 5], "./folder1/fname2.ext", encoding="utf-8")
#     """
#     if "@" in path:  # NOTE!!: path = "<sheet_name>@<file_path>"
#         (sheet_name, path) = path.split("@", 1)

#     os.makedirs(os.path.dirname(path), exist_ok=True)

#     _ext_ = {'json': '.json', 'excel': '.xls', 'csv': '.csv'}  # 지정된 파일타입
#     _ext = None
#     for k, v in _ext_.items():
#         if v in path[-6:]:
#             _ext = k

#     if ext and _ext:
#         if _ext == 'json':
#             json.dump(data, open(path, mode, encoding=encoding), ensure_ascii=False, indent="\t")
#         elif _ext == 'csv':
#             df = _to_df(data)
#             if not os.path.exists(path):
#                 # print("csv, write")
#                 df.to_csv(path, index=False, mode='w', header=True)
#             else:
#                 # print("csv, append")
#                 df.to_csv(path, index=False, mode='a', header=False)
#         elif _ext == 'excel':
#             if not os.path.exists(path):
#                 with pd.ExcelWriter(path, mode='w', engine='openpyxl') as writer:
#                     _to_df(data).to_excel(writer, sheet_name=sheet_name, index=False)
#             else:
#                 with pd.ExcelWriter(path, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
#                     _to_df(data).to_excel(writer, sheet_name=sheet_name, index=False)
#     else:
#         if mode == "wb":
#             with open(path, mode) as f:
#                 f.write(data)
#         else:
#             if type(data) == dict or type(data) == list:
#                 data = json.dumps(data, ensure_ascii=False, indent="\t")
#             with open(path, mode, encoding="utf-8") as f:
#                 data = start + data + end
#                 f.write(data)


def _strip_file(path, save=True):
    """_strip_file: 텍스트 파일 줄 끝 공백 제거
    Args:
        - path(str): 파일 경로
        - save(bool): 저장 여부

    Returns:
        - str: 공백 제거후 문자열
    """
    with open(path, "r", encoding="utf-8") as f:
        data = ""
        for line in f.readlines():
            data += line.strip() + '\n'
    if save:
        with open(path, "w", encoding="utf-8") as f:
            f.write(data)

    return data


##@@ 디버그 / 기타
##------------------------------------------------------------
def _fn(level=0):
    """_fn: 함수 이름 출력
    Desc:
        - [extended_summary]

    Args:
        - level(int, 0): 함수 위치(레벨)  예) 0: 현재 함수, 1: 호출한 함수, 2: 1을 호출한 함수

    Returns:
        - str: 함수 이름

    Usages:
        - print(f"{_fn(1)}") : 함수 내부에 삽입
    """    
    return sys._getframe(level).f_code.co_name


def _act(name, *args, **kwargs):
    """모듈 함수 실행(by 문자열)
    _act("momentum.rsi", df.Close, period)
    """
    (module, func) = name.split(".", 1)
    return getattr(globals()[module], func)(*args, **kwargs)


def _exec(script, sep=';', rep={}, con=" _if "):
    """
    sep: separator  '_r'로 끝나면 정규표현식
    rep: replacement '_r'로 끝나면 정규표현식
    con: 조건식 구분자  _script _if condition 
    """
    if con in script:
        (script, condition) = script.split(con)
        if eval(condition):
            _exec(script, sep=sep, rep=rep)
            return True
    # else:
    #     return False
    
    (sep_str, sep_re) = (sep[2:] if sep[:2] == "r_" else sep, sep[:2] == "r_")
    # print(sep_str, sep_re)
    
    if sep_str:
        for _script in re.split(sep_str, script) if sep_re else script.split(sep_str):
            # print(f"inits script {_replace_str(rep, _script)}")
            if _script == "base=int(price*(1+upper)) if base==0 else base":
                # print(f"BUG script: {_script}")
                # print(f"{price=}, {base=}, {upper=}")
                exec(_script, globals())
            else:
                exec(_replace_str(rep, _script), globals())
            ## TODO: BUG TypeError: can't multiply sequence by non-int of type 'float'


# def _exec(script, sep=';', rep={}, con=" _if "):
#     """
#     sep: separator  '_r'로 끝나면 정규표현식
#     rep: replacement '_r'로 끝나면 정규표현식
#     con: 조건식 구분자  _script _if condition 
#     """
#     if con in script:
#         (script, condition) = script.split(con)
#         if eval(condition):
#             _exec(script, sep=sep, rep=rep)
#             return True
#     # else:
#     #     return False
    
#     (sep_str, sep_re) = (sep[2:] if sep[:2] == "r_" else sep, sep[:2] == "r_")
#     # print(sep_str, sep_re)
    
#     if sep_str:
#         for _script in re.split(sep_str, script) if sep_re else script.split(sep_str):
#             exec(_replace_str(rep, _script), globals())


if __name__ == "__main__":
    pass
    # data = dict(
    #     a = 1,
    #     b = [1, 2, '3']
    # )
    path = "./yaml_test.yml"
    data = {'d': 'F'}
    # _write_file(data, path, mode="w", encoding="utf-8", start="", end="")
    _update_file(data, path, encoding="utf-8")

