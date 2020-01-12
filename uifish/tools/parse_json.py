def base_keys_tree(base_value: dict, n=100, full_list=False):
    base_tree_list = [[key] for key in base_value.keys()]

    for num in range(n):
        enab = False
        for key in base_tree_list:

            val = base_value
            for ke in key:
                val = val[ke]
            if type(val) == dict:
                for ke in val.keys():
                    new_ke = key + [ke]
                    base_tree_list.append(new_ke)
                    enab = True
            elif type(val) == list:
                if len(val) > 0:
                    if full_list:
                        for idx in range(len(val)):
                            new_ke = key + [idx]
                            base_tree_list.append(new_ke)
                    else:
                        new_ke = key + [0]
                        base_tree_list.append(new_ke)
                    enab = True
                else:
                    enab = True
            else:
                enab = True

        if enab:
            break
    base_tree_list.sort(key=lambda ele: ele)
    return base_tree_list


def to_value(data: dict, keys):
    val = data
    if isinstance(keys, list):
        for key in keys:
            if val:
                if isinstance(key, int):
                    val = val[key]
                elif isinstance(key, str):
                    if key.startswith('$'):
                        new_key = key[1:]
                        if val.get(new_key) is not None:
                            val = val.get(new_key)
                        else:
                            val = val.get(key)
                    else:
                        val = val.get(key)
                if val == data:
                    break
            else:
                break
    if isinstance(keys, str) and '.' in keys:
        keys = keys.split('.')
        for key in keys:
            try:
                key = int(key)
            except:
                pass
            if val:
                if isinstance(key, int):
                    val = val[key]
                elif isinstance(key, str):
                    if key.startswith('$'):
                        new_key = key[1:]
                        if val.get(new_key) is not None:
                            val = val.get(new_key)
                        else:
                            val = val.get(key)
                    else:
                        if val.get(key) is not None:
                            val = val.get(key)
                        else:
                            val = val.get('${}'.format(key))
                if val == data:
                    break
            else:
                break
    elif isinstance(keys, str):
        val = val.get(keys)

    return val
