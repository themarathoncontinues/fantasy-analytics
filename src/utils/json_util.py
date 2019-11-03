"""Get value form complex key"""

def get_nested(payload, jpath):
    """
    Utility function to get nested json values
    :param payload:
    :param jpath:
    :return:
    """
    path_list = jpath.split('.')
    # logger.info(f' Path List: {path_list}')

    control = None
    for jpath in path_list:
        control = payload.get(str(jpath))
        payload = control


    return control