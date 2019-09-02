import json as jsons

from typing import Sequence, Union, Any, Dict, List, Set, Callable, Optional, Type
from kelmore_arrays import ArrayTools as Arrays
from kelmore_arrays.arrays import Matrix

Items = Union[None, Dict[str, Any]]
JSONList = List[Dict[Any, Any]]


class DictObject:
    json: Items

    def __init__(self, json_item: Items):
        self.json = json_item

    def __str__(self):
        return str(self.json)

    def __repr__(self):
        return str(self.json)


class JSONCheck:

    @staticmethod
    def equal(list_a: dict, list_b: dict) -> bool:
        """Checks if two json items are equivalent

        :param list_a: A json dictionary
        :param list_b: A json dictionary
        :return: True if the two items are equivalent, False otherwise
        """
        for key in list_a:
            if key in list_b:
                if list_a[key] != list_b[key]:
                    return False
            else:
                return False

        return True

    @staticmethod
    def has_children(json: dict, include_arrays: Optional[bool] = False) -> bool:
        if not isinstance(json, dict):
            return False

        for key in json:
            if isinstance(json[key], dict) or \
                    (include_arrays and isinstance(json[key], list)):
                return True

        return False


class JSONFiles:

    @staticmethod
    def open(full_path: str) -> dict:
        """ prec: file_name is a valid json file path
            postc: opens the json file and returns it as an object"""
        with open(full_path) as data_file:
            return jsons.load(data_file)

    @staticmethod
    def save(full_path: str, json: dict) -> None:
        """ prec: file_name is a valid file path, json_object is a json object
                postc: saves the json_object to file_name"""
        with open(full_path, 'w') as outfile:
            jsons.dump(json, outfile)


class JSONLists:

    @staticmethod
    def keys(json_list: List[Dict[str, any]]) -> List[str]:
        all_keys: Set[str] = set()
        for json_item in json_list:
            all_keys = all_keys | set(json_item.keys())

        return list(all_keys)

    @staticmethod
    def reduce(json_list: Sequence[dict], keys_to_keep: Sequence[str]) -> Sequence[dict]:
        """
        Removes all the keys except those in keys_to_keep from all the json items with json_list

        :param json_list: (Sequence[dict]) A list of dictionary objects
        :param keys_to_keep: (Sequence[str]) A list of keys to keep within each item in json_list
        :return: The json_list but reduced to only the specified keys from keys_to_keep
        """
        for item in json_list:
            JSONTransform.reduce(item, keys_to_keep)

        return json_list

    @staticmethod
    def remove_duplicates(json_list: List[dict]) -> List[dict]:
        """
        Removes all duplicate json dictionaries in a list of json dictionaries
        :param json_list: A list of json dictionaries
        :return: The json list
        """
        to_remove: List[int] = []

        for json_idx in range(len(json_list) - 1):
            json_item: dict = json_list[json_idx]

            for json_idx_2, json_item_2 in enumerate(json_list[json_idx + 1:]):
                if JSONCheck.equal(json_item, json_item_2):
                    to_remove.append(json_idx_2)

        return Arrays.transform.remove_indexes(json_list, to_remove)

    @staticmethod
    def replace_keys(json_list: List[dict],
                     keys_to_replace: Sequence[str],
                     replacement_keys: Sequence[str]) -> Sequence[dict]:
        if not Arrays.check.equal_length(keys_to_replace, replacement_keys):
            raise IndexError('Could not replace the json keys for the given list. '
                             'The length of the key arrays do not match.')

        for idx, json_dict in enumerate(json_list):
            json_list[idx] = JSONTransform.replace_keys(
                json_dict,
                keys_to_replace,
                replacement_keys
            )

        return json_list

    @staticmethod
    def replace_keys_custom(json_list: Sequence[dict],
                            replace_function: Callable[[str], str]) -> List[dict]:
        return [JSONTransform.replace_keys_custom(x, replace_function) for x in json_list]


class JSONTransform:

    @staticmethod
    def create(fields: Sequence[str], values: Sequence[object]) -> dict:
        if not Arrays.check.equal_length(fields, values):
            raise IndexError('Could not create the dictionary. '
                             'The length of fields and values did not match.')

        output = {}
        for idx, field in enumerate(fields):
            output[field] = values[idx]

        return output

    @staticmethod
    def flatten(json_item: dict,
                recursive: bool = False):
        if recursive:
            return JSONTransform._recursive_flatten_helper(json_item)

        keys: List[str] = list(json_item.keys())
        for key in keys:
            child: Any = json_item[key]
            if isinstance(child, dict):
                child: dict = json_item.pop(key)
                json_item = JSONTransform.merge(json_item, child)

        return json_item

    @staticmethod
    def intersection(json_list_1: dict,
                     json_list_2: dict,
                     fields: List[str] = None) -> dict:
        """
        Takes two json dictionaries, finds the overlapping elements (aka elements that are in
        both json_list_1 and json_list_2), and then adds the overlapped element to a new
        json dictionary
        :param json_list_1: json dictionary
        :param json_list_2: json dictionary
        :param fields: list of fields
        :return: The intersection between json_list_1 and json_list_2
        """
        intersection: dict = {}
        for key in json_list_1:
            if key in json_list_2:
                json_value_1: Any = json_list_1[key]
                json_value_2: Any = json_list_2[key]

                if json_value_2:
                    intersection[key] = json_value_2
                else:
                    intersection[key] = json_value_1

        if fields:
            all_keys: List[str] = list(intersection.keys())
            keys_to_remove: List[str] = [x for x in all_keys if x not in fields]

            for key in keys_to_remove:
                del intersection[key]

        return intersection

    @staticmethod
    def matrix(matrix: Matrix,
               headers: List[str] = None) -> List[dict]:
        if not headers:
            headers = matrix[0]
            del matrix[0]

        output: List[dict] = []
        for row in matrix:
            while len(row) < len(headers):
                row.append(None)

            while len(row) > len(headers):
                row.pop()

            output.append(JSONTransform.create(headers, row))

        return output

    @staticmethod
    def merge(json_a: dict, json_b: dict):
        return {**json_a, **json_b}

    @staticmethod
    def replace_keys(json: dict,
                     keys_to_replace: Sequence[str],
                     replacement_keys: Sequence[str]) -> dict:
        if not Arrays.check.equal_length(keys_to_replace, replacement_keys):
            raise IndexError('Could not replace the json keys for the given list. '
                             'The length of the key arrays do not match.')

        for key_idx, key in enumerate(keys_to_replace):
            if key in json:
                replacement: str = replacement_keys[key_idx]
                datum: Any = json.get(key)
                del json[key]

                json[replacement] = datum

        return json

    @staticmethod
    def replace_keys_custom(json: dict,
                            replace_function: Callable[[str], str]) -> dict:
        keys: List[str] = list(json.keys())
        for key in keys:
            new_key: str = replace_function(key)
            datum: Any = json[key]
            del json[key]

            json[new_key] = datum
        return json

    @staticmethod
    def reduce(json: dict,
               keys_to_keep: Sequence[str]) -> dict:
        keys = [x for x in json.keys() if x not in keys_to_keep]
        for key in keys:
            if key in json:
                del json[key]

        return json

    @staticmethod
    def remove_null_values(json_item: dict) -> dict:
        keys: List[str] = list(json_item.keys())
        for key in keys:
            if json_item.get(key) is None:
                del json_item[key]

        return json_item

    @staticmethod
    def _recursive_flatten_helper(json_item: dict):
        has_children: bool = JSONCheck.has_children(json_item)
        while has_children is True:
            json_item = JSONTransform.flatten(json_item)
            has_children = JSONCheck.has_children(json_item)

        return json_item


class JSONTools:
    check: Type[JSONCheck] = JSONCheck
    files: Type[JSONFiles] = JSONFiles
    lists: Type[JSONLists] = JSONLists
    transform: Type[JSONTransform] = JSONTransform
