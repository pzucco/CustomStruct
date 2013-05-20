__author__ = 'pzucco'

import CustomStruct as cs

ContactStruct = cs.Structure(
    type= cs.Byte,
    data= cs.String,
)

PersonStruct = cs.Structure(
    name=     cs.String,
    birth=    cs.Short,
    contacts= cs.List(ContactStruct),
)

TYPE_EMAIL, TYPE_PHONE = 0, 1


person = dict(
    name= 'John',
    birth= 1980,
    contacts= [
        dict(type= TYPE_EMAIL, data= 'john@email.com'),
        dict(type= TYPE_PHONE, data= '12345678'),
    ],
)

serialized = cs.serialize(PersonStruct, person)
structure, data = cs.deserialize(serialized)
print data
print 'received data is a PersonStruct?', structure == PersonStruct


class Person:
    def __init__(self, name, birth, contacts):
        self.name = name
        self.birth = birth
        self.contacts = contacts

class Contact:
    def __init__(self, type, data):
        self.type = type
        self.data = data

person = Person('John', 1980, [Contact(TYPE_EMAIL, 'john@email.com'), Contact(TYPE_PHONE, '12345678')])
serialized = cs.serialize(PersonStruct, person)
print cs.deserialize(serialized)[1]


def aux_constructor(structure, data):
    if structure == PersonStruct:
        return Person(data['name'], data['birth'], data['contacts'])
    elif structure == ContactStruct:
        return Contact(data['type'], data['data'])
    else:
        return data

cs.set_constructor(aux_constructor)

print cs.deserialize(serialized)[1]


ArchiveStruct = cs.Structure(
    date=    cs.Tuple(cs.Byte, 3),
    content= cs.RawData
)

archive = {
    'date'   : (17, 05, 13),
    'content': cs.serialize(PersonStruct, person)
}

def aux_constructor(structure, data):
    if structure == ArchiveStruct:
        data['content'] = cs.deserialize(data['content'])
    return data

cs.set_constructor(aux_constructor)

serialized = cs.serialize(ArchiveStruct, archive)
print 'deserialized: %s' % cs.deserialize(serialized)[1]