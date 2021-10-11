class SomeObject:
    def __init__(self, integer_field=0, float_field=0.0, string_field=''):
        self.integer_field = integer_field
        self.float_field = float_field
        self.string_field = string_field


class EventGet():
    def __init__(self, _type):
        self._type = _type


class EventSet():
    def __init__(self, _value):
        self._value = _value


class NullHandler():
    def __init__(self, successor=None):
        self.successor = successor

    def handle(self, obj, event):
        if self.successor is not None:
            return self.successor.handle(obj, event)


class IntHandler(NullHandler):
    def handle(self, obj, event):
        if type(event) is EventGet and event._type is int:
            return obj.integer_field
        elif type(event) is EventSet and type(event._value) is int:
            obj.integer_field = event._value
        else:
            return super().handle(obj, event)


class FloatHandler(NullHandler):
    def handle(self, obj, event):
        if type(event) is EventGet and event._type is float:
            return obj.float_field
        elif type(event) is EventSet and type(event._value) is float:
            obj.float_field = event._value
        else:
            return super().handle(obj, event)


class StrHandler(NullHandler):
    def handle(self, obj, event):
        if type(event) is EventGet and event._type is str:
            return obj.string_field
        elif type(event) is EventSet and type(event._value) is str:
            obj.string_field = event._value
        else:
            return super().handle(obj, event)


def main():
    """
    Run only if file xecured directly.
    Not running id imported
    """
    obj = SomeObject()
    obj.integer_field = 42
    obj.float_field = 3.14
    obj.string_field = "some text"
    chain = IntHandler(FloatHandler(StrHandler(NullHandler)))
    print(chain.handle(obj, EventGet(int)))
    #  42
    print(type(chain.handle(obj, EventGet(float))))
    #  3.14
    print(chain.handle(obj, EventGet(str)))
    #  'some text'
    chain.handle(obj, EventSet(100))
    print(chain.handle(obj, EventGet(int)))
    #  100
    chain.handle(obj, EventSet(0.5))
    print(chain.handle(obj, EventGet(float)))
    #  0.5
    chain.handle(obj, EventSet('new text'))
    print(chain.handle(obj, EventGet(str)))
    #  'new text'
    obj = SomeObject(integer_field=-16, float_field=-14.4411,
                     string_field="JagEFq")
    print(type(chain.handle(obj, EventGet(int))))


if __name__ == '__main__':
    main()
