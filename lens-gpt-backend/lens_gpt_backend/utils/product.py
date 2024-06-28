from typing import Union

T = Union[None, str, list['T'], dict[str, 'T']]


class Product:

    def __init__(self, data: T, data_type: str = 'unknown', data_description: str = 'unknown') -> None:
        self._data: T = data
        self._data_type: str = data_type
        self._data_description: str = data_description

    def get_data(self) -> T:
        return self._data

    def get_str(self) -> str:
        data = self._data
        if isinstance(data, str):
            return data
        raise ValueError(f"Expected str, got {type(data)}")

    def get_list(self) -> list['Product']:
        data = self._data
        if isinstance(data, list):
            return [Product(d) for d in data]
        raise ValueError(f"Expected list, got {type(data)}")

    def get_dict_str_str(self) -> dict[str, str | None]:
        data = self._data
        if isinstance(data, dict):
            return_data = {}
            for k, v in data.items():
                if isinstance(k, str) and (isinstance(v, str) or v is None):
                    return_data[k] = v
                else:
                    raise ValueError(f"Expected str, got {type(k)}")
            return return_data
        raise ValueError(f"Expected dict, got {type(data)}")
