CustomStruct
============

Simple pure python module for packing and unpacking of structured data with no
ovearhead. It serves as base of a network protocol for a game I'm developing.

Nothing BIG. It's just a smart way I found to bend the native 'struct' module
to my needs. By using this module one avoid the boring and repetitive task of
manually defining it's own custom data pack and unpacking functions.

CustomStruct is (as far as pure python allow) optimized, using 'pre-compiled'
Structs and reducing function calls by flattening static structures when
possible.


* Why didn't you used Google's 'Protocol Buffers'

I developed this module instead of using 'Protocol Buffers' because I wanted a
pure python implementation, with no external definition files, simple and
intuitive syntax, direct and faster way to declare my protocol.

No compile, recompile definition file stuff. You define the protocol in code,
then you can throw dicts and objects in and out. Simple as that.

Also, I found it to be faster than 'Protocol Buffers'! But I didn't test too
much. So I preffer to say it is 'as fast as'. Maybe.

But this module is not a alternative to 'Protocol Buffers' if your aiming for
Google's cross-language support or formal protocol specification that a large
project require.


* Just show me how it works

#==============================================================================
# Defining protocol

import CustomStruct as cs

ContactStruct = cs.Structure(
    type= cs.Byte,
    data= cs.String,
)

PersonStruct = cs.Structure(
    name=     cs.String,
    birth=    cs.Short,
    contacts= cs.List(ContactStruct),
    parents=  cs.Tuple(cs.String, 2),
)

TYPE_EMAIL, TYPE_PHONE = 0, 1

#==============================================================================
# Test using dict

person = dict(
    name= 'John',
    birth= 1980,
    contacts= [
        dict(type= TYPE_EMAIL, data= 'john@email.com'),
        dict(type= TYPE_PHONE, data= '12345678'),
    ],
    parents= ('Smith', 'Lola')
)

packed = cs.pack(PersonStruct, person)
print packed, ' -> ', cs.unpack(packed)

#==============================================================================
# But I preffer packing objects

class Person:
    def __init__(self, name, birth, contacts, parents):
        self.name = name
        self.birth = birth
        self.contacts = contacts
        self.parents = parents

class Contact:
    def __init__(self, type, data):
        self.type = type
        self.data = data

person = Person('Eric', 1970, [ Contact(TYPE_EMAIL, 'luck@email.com') ], ('Mike', 'Sona'))

packed = cs.pack(PersonStruct, person) # it will use the __dict__ of the object
print packed, ' -> ', cs.unpack(packed)

#==============================================================================
# But I preffer unpacking objects

def aux_constructor(structure, data):
    if structure == PersonStruct:
        return Person(data['name'], data['birth'], data['contacts'], data['parents'])
    if structure == ContactStruct:
        return Contact(data['type'], data['data'])

cs.set_constructor(aux_constructor) # dicts will be supplied to the constructor
packed = cs.pack(PersonStruct, person)
print packed, ' -> ', cs.unpack(packed)

