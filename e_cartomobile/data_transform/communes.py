
def dep_str_to_int(dep_str):

    if dep_str in ['2A','2B']:
        dep_int = 20
    else:
        dep_int = int(dep_str)

    return dep_int