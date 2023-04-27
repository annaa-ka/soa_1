import timeit
from dicttoxml import dicttoxml
import ast
import xmltodict
import json
from dicttoxml import dicttoxml
import data_pb2
from io import BytesIO
import fastavro
from fastavro import writer
import avro
from avro.datafile import DataFileWriter, DataFileReader
from avro.io import DatumWriter, DatumReader
import yaml
import msgpack
import sys

data = {"string": "string",
        "array" : [1, 2, 3],
        "dict": {'jack': 4098, 'sape': 4139},
        "number": 100,
        "point_number": 1.009}


def native_format():
    mycode = '''
str(data)
'''
    ser_data_size = sys.getsizeof(str(data))
    serialization_time = timeit.timeit(stmt = mycode, number = 10000, globals=globals())

    setup_code = '''
ser_data = str(data)
'''
    mycode = '''
ast.literal_eval(ser_data)
'''
    deserialization_time = timeit.timeit(setup=setup_code, stmt = mycode, number = 10000, globals=globals())
    return (serialization_time, deserialization_time, ser_data_size)

def xml_format():
    mycode = '''
dicttoxml(data)
'''
    serialization_time = timeit.timeit(stmt = mycode, number = 500, globals=globals())

    ser_data_size = sys.getsizeof(dicttoxml(data))

    setup_code = '''
ser_data = dicttoxml(data)
'''
    mycode = '''
xmltodict.parse(ser_data)
'''
    deserialization_time = timeit.timeit(setup=setup_code, stmt = mycode, number = 500, globals=globals())
    return (serialization_time, deserialization_time, ser_data_size)

def json_format():
    mycode = '''
json.dumps(data)
'''
    serialization_time = timeit.timeit(stmt = mycode, number = 10000, globals=globals())

    ser_data_size = sys.getsizeof(json.dumps(data))

    setup_code = '''
ser_data = json.dumps(data)
'''
    mycode = '''
json.loads(ser_data)
'''
    deserialization_time = timeit.timeit(setup=setup_code, stmt = mycode, number = 10000, globals=globals())
    return (serialization_time, deserialization_time, ser_data_size)

def create_proto_msg():
    msg = data_pb2.Data()
    msg.string = data["string"]
    msg.number = data["number"]
    for value in data["array"]:
        msg.array.append(value)
    for key, value in data["dict"].items():
        msg.dict[key] = value
    return msg

def protobuf_format():
    setup_code = '''
from __main__ import create_proto_msg
data_proto = create_proto_msg()
'''
    mycode = '''
data_proto.SerializeToString()
'''
    serialization_time = timeit.timeit(setup=setup_code, stmt = mycode, number = 10000, globals=globals())

    data_proto = create_proto_msg()
    ser_data_size = sys.getsizeof(data_proto.SerializeToString())

    setup_code = '''
from __main__ import create_proto_msg
data_proto = create_proto_msg()
ser_data = data_proto.SerializeToString()
msg = data_pb2.Data()
'''
    mycode = '''
msg.ParseFromString(ser_data)
'''
    deserialization_time = timeit.timeit(setup=setup_code, stmt = mycode, number = 10000, globals=globals())
    return (serialization_time, deserialization_time, ser_data_size)

def serialize(schema, data):
    bytes_writer = BytesIO()
    fastavro.schemaless_writer(bytes_writer, schema, data)
    return bytes_writer.getvalue()

def deserialize(schema, binary):
    bytes_writer = BytesIO()
    bytes_writer.write(binary)
    bytes_writer.seek(0)

    data = fastavro.schemaless_reader(bytes_writer, schema)
    return data

schema = {
    "name": "avro.example",
    "type": 'record',
    "fields": [
        {
            "name": "string",
            "type": "string"
        },
        {
            "name": "array",
            "type": {"type": "array", "items": "int"}
        },
        {
            "name": "dict",
            "type": {"type": "map", "values": "int"}
        },
        {
            "name": "number",
            "type": "int"
        },
        {
            "name": "point_number",
            "type": "float"
        },
    ]
}

def apache_avro():
    setup_code = '''
from __main__ import serialize, deserialize
    '''
    mycode = '''
binary = serialize(schema, data)
    '''
    serialization_time = timeit.timeit(setup=setup_code, stmt = mycode, number = 10000, globals=globals())
    ser_data_size = sys.getsizeof(serialize(schema, data))

    setup_code = '''
from __main__ import serialize, deserialize
binary = serialize(schema, data)
'''
    mycode = '''
data2 = deserialize(schema, binary)
'''
    deserialization_time = timeit.timeit(setup=setup_code, stmt = mycode, number = 10000, globals=globals())
    return (serialization_time, deserialization_time, ser_data_size)

def yaml_test():
    mycode = '''
yaml.dump(data)
    '''
    serialization_time = timeit.timeit(stmt = mycode, number = 100, globals=globals())
    ser_data_size = sys.getsizeof(yaml.dump(data))

    setup_code = '''
ser_data = yaml.dump(data)
'''
    mycode = '''
data2 = yaml.load(ser_data, Loader=yaml.FullLoader)
'''
    deserialization_time = timeit.timeit(setup=setup_code, stmt = mycode, number = 100, globals=globals())
    return (serialization_time, deserialization_time, ser_data_size)

def msg_pack_test():
    mycode = '''
msgpack.packb(data, use_bin_type=True)
    '''
    serialization_time = timeit.timeit(stmt = mycode, number = 10000, globals=globals())
    ser_data_size = sys.getsizeof(msgpack.packb(data, use_bin_type=True))

    setup_code = '''
ser_data = msgpack.packb(data, use_bin_type=True)
'''
    mycode = '''
msgpack.unpackb(ser_data, raw=False)
'''
    deserialization_time = timeit.timeit(setup=setup_code, stmt = mycode, number = 10000, globals=globals())
    return (serialization_time, deserialization_time, ser_data_size)
