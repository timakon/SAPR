import numpy as np

import json
from io import StringIO


SEQ_LEN = 10


def make_row(visited: set, cur: int) -> np.array:
    row = []
    for i in range(SEQ_LEN):
        row.append(1 if i+1 in visited else 0)
    return np.array(row)

def make_matrix(data: list) -> np.array:
    visited = set()
    matrix = list()

    for elem in data:
        if type(elem) == str:
            visited.add(int(elem))
            row = make_row(visited=visited, cur=int(elem))
            matrix.append({'num': int(elem), 'row': row})
        else:
            for subelem in elem:
                visited.add(int(subelem))
            for subelem in elem:
                row = make_row(visited=visited, cur=int(subelem))
                matrix.append({'num': int(subelem), 'row': row})

    matrix.sort(key=(lambda x: x['num']))
    raw = [elem['row'] for elem in matrix]

    return np.array(raw)


def get_json_data(json_path1, json_path2):
    data1 = json.loads(open(json_path1).read())
    data2 = json.loads(open(json_path2).read())
    return find_controversies(make_matrix(data1), make_matrix(data2))


def find_controversies(data1, data2):
    matrix12 = data1 * data2
    matrix12T = data1.T * data2.T

    criterion = np.logical_or(matrix12, matrix12T)

    answer = []
    for i in range(criterion.shape[0]):
        for j in range(i):
            if not criterion[i][j]:
                answer.append((['{}'.format(j+1), '{}'.format(i+1)]))

    return answer


get_json_data("example.json", "example2.json")