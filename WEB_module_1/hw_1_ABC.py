from abc import ABC, ABCMeta, abstractmethod
import pickle
import json


class SerializationInterface(ABC):
    """
    Abstract class with two methods:
    serialize_data(self, data, path)
    deserialize_data(self, path)

    """

    @abstractmethod
    def serialize_data(self, data, path):
        pass

    @abstractmethod
    def deserialize_data(self, path):
        pass


class DictSerializeBIN(SerializationInterface):

    """
    Class for serialization and deserialization
    <dict> container in and out of bin files

    """

    def serialize_data(self, data, path):
        if isinstance(data, dict):
            with open(path, 'wb') as fh:
                pickle.dump(data, fh)
        else:
            raise ValueError(f'Type of data is {type(data)} not a <dict>')

    def deserialize_data(self, path):
        with open(path, 'rb') as fh:
            data = pickle.load(fh)
            if isinstance(data, dict):
                return data
            else:
                raise ValueError(f'Type of data is {type(data)} not a <dict>')


class DictSerializeJSON(SerializationInterface):

    """
    Class for serialization and deserialization
    <dict> container in and out of json files

    """

    def serialize_data(self, data, path):
        if isinstance(data, dict):
            with open(path, 'w') as fh:
                json.dump(data, fh)
        else:
            raise ValueError(f'Type of data is {type(data)} not a <dict>')

    def deserialize_data(self, path):
        with open(path, 'r') as fh:
            data = json.load(fh)
            if isinstance(data, dict):
                return data
            else:
                raise ValueError(f'Type of data is {type(data)} not a <dict>')


class ListSerializeBIN(SerializationInterface):

    """
    Class for serialization and deserialization
    <list> container in and out of bin files

    """

    def serialize_data(self, data, path):
        if isinstance(data, list):
            with open(path, 'wb') as fh:
                pickle.dump(data, fh)
        else:
            raise ValueError(f'Type of data is {type(data)} not a <list>')

    def deserialize_data(self, path):
        with open(path, 'rb') as fh:
            data = pickle.load(fh)
            if isinstance(data, list):
                return data
            else:
                raise ValueError(f'Type of data is {type(data)} not a <list>')


class ListSerializeJSON(SerializationInterface):

    """
    Class for serialization and deserialization
    <list> container in and out of json files

    """

    def serialize_data(self, data, path):
        if isinstance(data, list):
            with open(path, 'w') as fh:
                json.dump(data, fh)
        else:
            raise ValueError(f'Type of data is {type(data)} not a <list>')

    def deserialize_data(self, path):
        with open(path, 'r') as fh:
            data = json.load(fh)
            if isinstance(data, list):
                return data
            else:
                raise ValueError(f'Type of data is {type(data)} not a <list>')


class SetSerializeBIN(SerializationInterface):

    """
    Class for serialization and deserialization
    <set> container in and out of bin files

    """

    def serialize_data(self, data, path):
        if isinstance(data, set):
            with open(path, 'wb') as fh:
                pickle.dump(data, fh)
        else:
            raise ValueError(f'Type of data is {type(data)} not a <set>')

    def deserialize_data(self, path):
        with open(path, 'rb') as fh:
            data = pickle.load(fh)
            if isinstance(data, set):
                return data
            else:
                raise ValueError(f'Type of data is {type(data)} not a <set>')


class SetSerializeJSON(SerializationInterface):

    """
    Class for serialization and deserialization
    <set> container in and out of json files

    """

    def serialize_data(self, data, path):
        if isinstance(data, set):
            data = list(data)
            with open(path, 'w') as fh:
                json.dump(data, fh)
        else:
            raise ValueError(f'Type of data is {type(data)} not a <set>')

    def deserialize_data(self, path):
        with open(path, 'r') as fh:
            data = json.load(fh)
            if isinstance(data, list):
                data = set(data)
                return data
            else:
                raise ValueError(
                    f'Type of data is {type(data)} not a <list> for converting to <set> and deserialization')


class TupleSerializeBIN(SerializationInterface):

    """
    Class for serialization and deserialization
    <tuple> container in and out of bin files

    """

    def serialize_data(self, data, path):
        if isinstance(data, tuple):
            with open(path, 'wb') as fh:
                pickle.dump(data, fh)
        else:
            raise ValueError(f'Type of data is {type(data)} not a <tuple>')

    def deserialize_data(self, path):
        with open(path, 'rb') as fh:
            data = pickle.load(fh)
            if isinstance(data, tuple):
                return data
            else:
                raise ValueError(f'Type of data is {type(data)} not a <tuple>')


class TupleSerializeJSON(SerializationInterface):

    """
    Class for serialization and deserialization
    <tuple> container in and out of json files

    """

    def serialize_data(self, data, path):
        if isinstance(data, tuple):
            with open(path, 'w') as fh:
                json.dump(data, fh)
        else:
            raise ValueError(f'Type of data is {type(data)} not a <tuple>')

    def deserialize_data(self, path):
        with open(path, 'r') as fh:
            data = json.load(fh)
            data = tuple(data)
            if isinstance(data, tuple):
                return data
            else:
                raise ValueError(f'Type of data is {type(data)} not a <tuple>')


if __name__ == '__main__':

    path_dict_bin = 'data_dict.bin'
    path_dict_json = 'data_dict.json'
    ex_dict = {'list': [1, 2, 3], 'dict': {
        '1': 'one', '2': 'two', '3': 'three'}}

    DictSerializeBIN().serialize_data(ex_dict, path_dict_bin)
    dict_data_bin = DictSerializeBIN().deserialize_data(path_dict_bin)

    DictSerializeJSON().serialize_data(ex_dict, path_dict_json)
    dict_data_json = DictSerializeJSON().deserialize_data(path_dict_json)

    print('___________________DICT______________________')
    print(f'base - {ex_dict}')
    print(f'bin - {dict_data_bin}')
    print(f'json - {dict_data_json}')
    print('___________________DICT______________________')

    assert ex_dict == dict_data_bin
    assert ex_dict == dict_data_json

    path_list_bin = 'data_list.bin'
    path_list_json = 'data_list.json'
    ex_list = [1, 2, 3, "4", {100: "100"}, (1, 2, 3)]

    ListSerializeBIN().serialize_data(ex_list, path_list_bin)
    list_data_bin = ListSerializeBIN().deserialize_data(path_list_bin)

    ListSerializeJSON().serialize_data(ex_list, path_list_json)
    list_data_json = ListSerializeJSON().deserialize_data(path_list_json)

    print('___________________LIST______________________')
    print(f'base - {ex_list}')
    print(f'bin - {list_data_bin}')
    print(f'json - {list_data_json}')
    print('___________________LIST______________________')

    assert ex_list == list_data_bin
    assert len(ex_list) == len(list_data_json)

    path_set_bin = 'data_set.bin'
    path_set_json = 'data_set.json'
    ex_set = {1, 's', 'm', '1', 7, 'a', 'j', 1, 'gjhg'}

    SetSerializeBIN().serialize_data(ex_set, path_set_bin)
    set_data_bin = SetSerializeBIN().deserialize_data(path_set_bin)

    SetSerializeJSON().serialize_data(ex_set, path_set_json)
    set_data_json = SetSerializeJSON().deserialize_data(path_set_json)

    print('___________________SET______________________')
    print(f'base - {ex_set}')
    print(f'bin - {set_data_bin}')
    print(f'json - {set_data_json}')
    print('___________________SET______________________')

    assert ex_set == set_data_bin
    assert ex_set == set_data_json

    path_tuple_bin = 'data_tuple.bin'
    path_tuple_json = 'data_tuple.json'
    ex_tuple = (1, 's', 'm', '1', 7, 'a', 'j', 1, 'gjhg')

    TupleSerializeBIN().serialize_data(ex_tuple, path_tuple_bin)
    tuple_data_bin = TupleSerializeBIN().deserialize_data(path_tuple_bin)

    TupleSerializeJSON().serialize_data(ex_tuple, path_tuple_json)
    tuple_data_json = TupleSerializeJSON().deserialize_data(path_tuple_json)

    print('___________________TUPLE______________________')
    print(f'base - {ex_tuple}')
    print(f'bin - {tuple_data_bin}')
    print(f'json - {tuple_data_json}')
    print('___________________TUPLE______________________')

    assert ex_tuple == tuple_data_bin
    assert ex_tuple == tuple_data_json
