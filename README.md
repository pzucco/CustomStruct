CustomStruct
============

Simple pure python module for serialization of structured data with no ovearhead. It serves as base of the network protocol for a game im developing.

Nothing BIG. It's just a smart way I found to bend the native 'struct' module to my needs. By using this module one avoid the boring and repetitive task of manually defining it's own custom data pack and unpacking functions.

CustomStruct is (as far as pure python allow) optimized, using 'pre-compiled' Structs and reducing function calls by flattening static structures when possible.

### Why didn't I use pickle

The game requires low length packets while pickle do leave considerable overhead to specify objects types.

### Why didn't I use Google's "Protocol Buffers"

I developed this module instead of using **Protocol Buffers** because I wanted a pure python implementation, with no external definition files, simple and intuitive syntax, direct and fast way to declare my protocol.

No compile, recompile definition file stuff. You define the protocol in code, then you can throw dicts and objects in and out. Simple as that. Plus, I found it to be faster than **Protocol Buffers**! And it has less overhead!

But this module is NOT a alternative to **Protocol Buffers**. **Protocol Buffers** has cross-language support, cross-protocol-version support and a much more formal specification that fits much better for larger projects.


## How it works

### Defining protocol

Direct and simple.

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

### Test using dict

The most simple way is to "serialize dicts".

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

### Packing objects

When packing object instances CustomStruct uses the object's (__dict__) to get the required fields.

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
    
    packed = cs.pack(PersonStruct, person)
    print packed, ' -> ', cs.unpack(packed)

### Unpacking objects

CustomStruct needs you to define an auxiliary constructor in order to build objects.

    def aux_constructor(structure, data):
        if structure == PersonStruct:
            return Person(data['name'], data['birth'], data['contacts'], data['parents'])
        elif structure == ContactStruct:
            return Contact(data['type'], data['data'])
        else:
            return data
    
    cs.set_constructor(aux_constructor) # dicts will be supplied to the constructor
    
    packed = cs.pack(PersonStruct, person)
    print packed, ' -> ', cs.unpack(packed)


## Built-in structures

Here is the list of all built-ins structures on can use.

    Byte     : unsigned, 1 byte
    Short    : unsigned, 2 bytes
    Int      : unsigned, 4 byte
    
    NegByte  : 1 byte
    NegShort : 2 byte
    NegInt   : 4 byte
    
    Float    : float, 4 bytes
    Double   : float, 8 bytes
    
    String   : 255 max-variable length string, 1 byte + string length

    List( structure* ) : 255 max-variable length list of structure*, 1 byte + content size
                       : list can be used as optional field

    Tuple( structure*, size* ) : size* fix length tuple of structure*, content size

    LongString : 4294967295 max-variable length string, 4 bytes + string length
             
### Packing arbritrary sub-structure

    SerializedStruct = cs.Structure(
        serial= cs.Int,
        data=   cs.LongString
    )
    
    serialized = { 'serial': 100, 'data': cs.pack(PersonStruct, person) }
    
    packed = cs.pack(SerializedStruct, serialized)
    unpacked = cs.unpack(packed)
    unpacked['data'] = cs.unpack(unpacked['data'])
    print packed, ' -> ', cs.unpack(packed)
