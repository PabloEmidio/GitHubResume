class _Item:
    pass


class _BaseResponse:
    def _set_response_object(self, response_obj: dict, set_path: str = ''):
        for key, value in response_obj.items():
            if isinstance(value, dict):
                self._set_response_object(
                    value, set_path=set_path + f'.{key}' if set_path else key
                )
            elif isinstance(value, list):
                if any(not isinstance(i, dict) for i in value):
                    raise ValueError(
                        'All response inside a list must have type "dict"'
                    )
                if (list_attr := getattr(self, key, None)) is None:
                    setattr(self, key, [])
                    list_attr = getattr(self, key)
                for each in value:
                    item = _Item()
                    for k, v in each.items():
                        setattr(item, k, v)
                    list_attr.append(item)
            else:
                set_path_list = set_path.split('.') if set_path else []
                set_obj = self
                while set_path_list:
                    attr = set_path_list.pop(0)
                    if not getattr(set_obj, attr, None):
                        setattr(set_obj, attr, _Item())
                    set_obj = getattr(set_obj, attr)
                setattr(set_obj, key, value)

    def set_response(self, data: dict):
        self._set_response_object(data)

    def __repr__(self):
        return f'Response <{type(self)}>'


class ServiceResponse(_BaseResponse):
    """Class to represet the response object"""
    pass
