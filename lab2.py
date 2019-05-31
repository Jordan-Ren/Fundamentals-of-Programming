# NO IMPORTS ALLOWED!

import json

def did_x_and_y_act_together(data, actor_id_1, actor_id_2):
    for set in data:
        if actor_id_1 in set and actor_id_2 in set:
            return True
    return False

def create_graph(data):
    graph = {}
    for vals in data:
        if vals[0] not in graph:
            graph[vals[0]] = set([vals[1]])
        else:
            graph[vals[0]].add(vals[1])
        if vals[1] not in graph:
            graph[vals[1]] = set([vals[0]])
        else:
            graph[vals[1]].add(vals[0])
    return graph

def get_actors_with_bacon_number(data, n):
    if n == 0:
        return {4724}
    graph = create_graph(data)
    q = [4724]
    visited = set()
    visited.add(4724)
    for i in range(n-1):
        temp_q = []
        while len(q) > 0:
            original = q.pop(0)
            for actor in graph[original]:
                if actor not in visited:
                    visited.add(actor)
                    temp_q.append(actor)
        q = temp_q
        if len(q) == 0:
            return set()
    result = set()
    for actor in q:
        for co_actor in graph[actor]:
            if co_actor not in visited:
                result.add(co_actor)
    return result


def get_bacon_path(data, actor_id):
    return get_path(data, 4724, actor_id)

def get_path(data, actor_id_1, actor_id_2):
    if actor_id_2 == actor_id_1:
        return {actor_id_1, actor_id_2}
    graph = create_graph(data)
    if actor_id_1 not in graph or actor_id_2 not in graph:
        return
    q = [[actor_id_1]]
    visited = {actor_id_1}
    n = 0
    while q:
        path = q[n]
        original = path[-1]
        for actor in set(graph[original]) - visited:
            path_copy = path.copy()
            path_copy.append(actor)
            q.append(path_copy)
            if actor == actor_id_2:
                return path_copy
            visited.add(actor)
        n += 1
        if n == len(q):
            break
    return

def get_movies_path(data, actor_id_1, actor_id_2):
    path = get_path(data, actor_id_1, actor_id_2)
    result = []
    for i in range(len(path)-1):
        for L in data:
            if path[i] == L[0] and path[i+1] == L[1]:
                result.append(L[2])
            if path[i] == L[1] and path[i+1] == L[0]:
                result.append(L[2])
    with open('resources/movies.json') as f:
        movies_db = json.load(f)
    final = []
    for movie in result:
        for ID in movies_db:
            if movies_db[ID] == movie:
                final.append(ID)
    return final

if __name__ == '__main__':
    # with open('resources/small.json') as f:
    #     smalldb = json.load(f)
    # with open('resources/names.json') as f:
    #     namesdb = json.load(f)
    # for i in namesdb:
    #     if i == "Katherine LaNasa":
    #         frank = namesdb["Katherine LaNasa"]
    # for i in namesdb:
    #     if i == "Sven Batinic":
    #         bruce = namesdb["Sven Batinic"]
    # with open('resources/large.json') as f:
    #     tinydb = json.load(f)
    # print(get_movies_path(tinydb, frank, bruce))
    # helo = get_path(tinydb, frank, bruce)
    # final = []
    # for actor in helo:
    #     for name in namesdb:
    #         if namesdb[name] == actor:
    #             final.append(name)
    # with open('resources/large.json') as f:
    #     largedb = json.load(f)
    # print(get_path(largedb, 43011, 1379833))
    # print(final)
    # with open('resources/movies.json') as f:
    #     movies = json.load(f)
    # print(movies)
    # print(get_actors_with_bacon_number(tinydb, 1))
    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.
    pass
