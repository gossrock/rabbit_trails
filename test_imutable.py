from typing import Any, Dict, Type, Callable
import sys
'''
In the attempt to figure out how to make a class immutable after object instatiation
I came across a couple of different methods here they are along with my thoughts and
variations on them.

My goal in making a "Immutable" is not to create something that people who *really*
want to change something from changing it but to create something that can't be
changed 'accedentally' similar to the modivation of this poster on Stackoverflow:
https://stackoverflow.com/questions/4996815/ways-to-make-a-class-immutable-in-python#4999158

I will not try to block any direct calls to dunder methods.
I will try to minimize boiler plate.
I want to be able to set attributes like normal inside the __init__ method and to
beable to create other methods.

'''

'''
Here's the first for direct creation of an immutable from 'Mouse vs Python'
(I have made minor modifications for python3 only with type anotations):
https://www.blog.pythonlibrary.org/2014/01/17/how-to-create-immutable-classes-in-python/

'''
class Immutable1:
    '''
        This uses __slots__ as a way to keep from creating additional attributes and
        __setattr__ to keep from modifying the attributes. To bypass the modification
        block the __init__ method uses the object's super's __setattr__ instead. I
        don't like this one because the super setting is more verbose than the standard
        attribute = value syntax.
    '''
    __slots__ = ("one", "two", "three")
    one: int
    two: int
    three: int

    def __init__(self, one: int, two: int, three: int) -> None:
        super(Immutable1, self).__setattr__("one", one)
        super(Immutable1, self).__setattr__("two", two)
        super(Immutable1, self).__setattr__("three", three)

    def __setattr__(self, name: str, value: Any) -> None:
        """"""
        msg = "'%s' has no attribute %s" % (self.__class__, name)
        raise AttributeError(msg)

    def other_method(self):
        print('other')


'''

    I made my own version of this. Turns out the use of __slots__ isn't really
    nessisary. __slots__ keeps attributes from being able to be created but doesn't
    keep you from setting them. If you override __setattr__ to keep it from being set
    you also end up with the same results.

    So, modifications are,
    no __slots__
    created convineance pointer to the super's __setattr__function

    really very minimal change.
'''

class Immutable2:
    one:int
    two:int
    three:int

    def __init__(self, one: int, two: int, three: int) -> None:
        setter = super(Immutable2, self).__setattr__ # I'm lazy
        setter('one', one)
        setter('two', two)
        setter('three', three)

    def __setattr__(self, name: str, value: Any) -> None: # over-riding to make immutable
        raise AttributeError(f"attribute '{name}' of '{self.__class__.__name__}' objects is not writable")

    def other_method(self):
        print('other')

'''
    It's not that difficult but there is more boiler plate than I would like and
    there are things that are just not easy to remeber, like needing to use super's
    __setattr__ to do the original setting of the attributes during object creation.

    So I started looking for a class decorator that could do the same thing. ...
'''

'''
    I found an implementation of a class decorator that does the job:

        originally found here:
        https://code.activestate.com/recipes/578233-immutable-class-decorator/

        also hosted here:
        https://github.com/ActiveState/code/blob/master/recipes/Python/578233_Immutable_class_decorator/recipe-578233.py


'''

def immutableA(mutableclass):
    """ Decorator for making a slot-based class immutable """

    if not isinstance(type(mutableclass), type):
        raise TypeError('@immutable: must be applied to a new-style class')
    if not hasattr(mutableclass, '__slots__'):
        raise TypeError('@immutable: class must have __slots__')

    class immutableclass(mutableclass):
        __slots__ = ()                      # No __dict__, please

        def __new__(cls, *args: Any, **kw: Any) -> 'immutableclass':
            new = mutableclass(*args, **kw) # __init__ gets called while still mutable
            new.__class__ = immutableclass  # locked for writing now
            return new

        def __init__(self, *args: Any, **kw: Any) -> None:    # Prevent re-init after __new__
            pass

    # Copy class identity:
    immutableclass.__name__ = mutableclass.__name__
    immutableclass.__module__ = mutableclass.__module__

    # Make read-only:
    for name, member in mutableclass.__dict__.items():
        if hasattr(member, '__set__'):
            setattr(immutableclass, name, property(member.__get__))

    return immutableclass

'''
        Now while the decorator is quite a bit more difficult to understand directly
        if you look at how it is used then you can see that it is much cleaner.
'''


@immutableA
class Immutable3:
    __slots__ = ('one', 'two', 'three')
    def __init__(self, one: int, two: int, three: int) -> None:
        self.one = one
        self.two = two
        self.three = three

    def other_method(self):
        print('other')


'''
    I tried to clean it up by not using __slots__ or make the 'new style objects'
    test and use __setattr__ instead of the setattr() read only work around but I
    could never get it fully work properly. Either it's not posible or I'm missing
    something in my understanding. (most likely the second).


def immutableA2(mutableclass):
    class immutableclass:

        class _Init(mutableclass):
            pass

        def __new__(cls, *args: Any, **kw: Any) -> 'immutableclass':
            new = immutableclass._Init(*args, **kw) # __init__ gets called while still mutable
            new.__class__ = immutableclass  # locked for writing now
            return new

        def __getattribute__(self, s: str) -> Any:
            # first get from wrapping object ...
            try:
                return super(immutableclass,self).__getattribute__(s)
            # ... then from wrapped object
            except AttributeError:
                return immutableclass._Init.__getattribute__(s)

        def __setattr__(self, name: str, value: None) -> None: # over-riding to make immutable
            # no matter what if someone trys to set an attribute raise an error
            raise AttributeError(f"attribute '{name}' of '{self.__class__.__name__}' objects is not writable")

    # Copy class identity:
    immutableclass.__name__ = mutableclass.__name__
    immutableclass.__module__ = mutableclass.__module__


    return immutableclass


@immutableA2
class Immutable3B:
    one: int
    two: int
    three: int
    def __init__(self, one: int, two: int, three: int) -> None:
        self.one = one
        self.two = two
        self.three = three

    def other_method(self):
        print('other')
'''

"""
    The main thing I don't like is the requirement to use __slots__. Otherwise it's
    great. So I worked at trying to simplify it just that little bit more. Just add
    a way to add a __setattr__ after the creation of the instance. After several
    attemps I ended up starting from scratch with an example from this page:
    "https://www.codementor.io/sheena/advanced-use-python-decorators-class-function-du107nxsv"
"""

'''
    The way this one works is just by wrapping the original class and proxying calls
    to the class while blocking any calls to __setattr__ from passing through.
    It would be up to the creator of the class that is to be wrapped to keep anything
    from changing as a side effect of any calls to the methods of the object but
    since they want to decorate it as 'immutable' we can give them the responsibility
    of fulfilling that side of the promise without the need to do weird jirations
    to keep people from accedentally making a change.

'''


def immutableB(mutableclass):

    class immutable:
        def __init__(self,*args: Any, **kwds: Any) -> None:
            # initiate mutable class and store it away
            super(immutable, self).__setattr__('_mutable', mutableclass(*args,**kwds))

        def __getattribute__(self, s: str) -> Any:
            # first get from wrapping object (this would be for __init__, __getattribute__,
            # __setattr__ and __dict__ [and maybe others that are default]) ...
            try:
                return super(immutable,self).__getattribute__(s)
            # ... then from wrapped object
            except AttributeError:
                return self._mutable.__getattribute__(s)

        def __setattr__(self, name: str, value: None) -> None: # over-riding to make immutable
            # no matter what if someone trys to set an attribute raise an error
            raise AttributeError(f"attribute '{name}' of '{self.__class__.__name__}' objects is not writable")

    # Copy class identity:
    immutable.__name__ = mutableclass.__name__
    immutable.__module__ = mutableclass.__module__

    return immutable


@immutableB
class Immutable4:
    def __init__(self, one: int, two: int, three: int) -> None:
        self.one = one
        self.two = two
        self.three = three

    def other_method(self):
        print('other')

'''
    This is basically what I was looking for but I did find mention of other methods
    and I thought I would play with those too.
'''


class ImmutableBase:
    one: int
    two: int
    three: int

    class _Init:
        def __init__(self) -> None:...


    def __new__(cls, *args, **kwargs) -> 'ImmutableBase._Init':
        self = cls._Init(*args, **kwargs)
        self.__class__ = cls
        return self

    def __setattr__(self, name: str, value: None) -> None: # over-riding to make immutable
        # no matter what if someone trys to set an attribute raise an error
        raise AttributeError(f"attribute '{name}' of '{self.__class__.__name__}' objects is not writable")


class Immutable5(ImmutableBase):
    one: int
    two: int
    three: int
    class _Init:
        def __init__(self, one:int, two: int, three: int) -> None:
            self.one = one
            self.two = two
            self.three = three

    def other_method(self):
        print('other')



'''
    Something that I thought should work but didn't is monkey patching __setattr__
    at the tail end of __init__. No apparent change. The attribute was still settable.
    After banging my head against it a bit I found that to affectivly monkey patch it
    you need to attach it to the __class__ object and not the instance. This means
    that all objects of that class are now locked (and no new ones will be creatable).
    here's an example:

    def immutable_setaddr(self:object, name: str, value: None) -> None: # over-riding to make immutable
        # no matter what if someone trys to set an attribute raise an error
        raise AttributeError(f"attribute '{name}' of '{self.__class__.__name__}' objects is not writable")


    class Test:
        def __init__(self, a:int) -> None:
            self.a = a
            #self.__setattr__ = types.MethodType(immutable_setaddr, self) # only runs if dirrectly called
            self.__class__.__setattr__ = types.MethodType(immutable_setaddr, self) #can't make any new instances anymore


'''

'''
    NamedTuples were mentioned as a solution. But they will only work if you don't
    need to do anything special in the __init__ or __new__ methods.
'''

'''
    The new dataclass feature of python3.7 then came to mind. After some hacking
    here's a posible aproach. Still not as clean as a good decorator. (This methods
    actually inspired my Subclassing method above)
'''
if float(sys.version[0:3]) >= 3.7:
    from dataclasses import dataclass
    @dataclass(frozen=True, init=False)
    class Immutable6:
        one: int
        two: int
        three: int

        class _Init:
            def __init__(self, one: int, two: int, three: int) -> None:
                self.one = one
                self.two = two
                self.three = three

        def __new__(cls, one:int, two:int, three:int) -> 'Immutable6._Init':
            self = cls._Init(one, two, three)
            self.__class__ = cls
            return self

        def other_method(self):
            print('other')







if __name__ == '__main__':
    to_test:Dict[str, Any] = {}
    #immutable testing
    A = Immutable1(1, 2, 3)
    to_test['Mouse vs Python'] = A
    B = Immutable2(1, 2, 3)
    to_test['Simplified: Mouse vs Python'] = B
    C = Immutable3(1, 2, 3)
    to_test['Use of Immutable Decorator'] = C
    #C2 = Immutable3B(1, 2, 3)
    #`to_test['Use of Immutable Decorator(modified)'] = C2
    D = Immutable4(1, 2, 3)
    to_test['My modified Use of Immutable Decorator'] = D
    E = Immutable5(1, 2, 3)
    to_test['Subclass'] = E
    if float(sys.version[0:3]) >= 3.7:
        F = Immutable6(1, 2, 3)
        to_test['3.7 dataclass'] = F



    for name, instance in to_test.items():
        print('#############')
        print (name)
        instance.other_method()
        print(f'obj.one: {instance.one}')
        print(f'obj.two: {instance.two}')
        print(f'obj.three: {instance.three}')

        try:
            print('try to change ".one":')
            instance.one = 2
            print(f'obj.one after change {instance.one}')
        except Exception as e:
            print(e.__class__.__name__)
            print(e)

        try:
            print('try to monkey patch ".four"')
            instance.four = 4
            print(f'obj.four after monkey patch attempt {instance.four}')
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        print('#############')
