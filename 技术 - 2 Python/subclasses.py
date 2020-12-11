import os
import sys
import inspect


class A(object):
    def __init__(self,x):
        self.x = x
        print('I am in A:', x)


class B(A):
    def __init__(self,x):
        super().__init__(x)
        print('I am in B:', x)

class C(B):
    def __init__(self,x):
        super().__init__(x)
        print('I am in C:', x)

class D(B):
    def __init__(self,x):
        super().__init__(x)
        print('I am in D:', x)

def get_subclasses(klass):
    subclasses = klass.__subclasses__()
    result = []
    for subclass in subclasses:
        result.extend(get_subclasses(subclass))
    if not result:
        result = [klass]
    '''else:
        result.append(klass)'''
    return result

cls = A
subclasses = get_subclasses(cls)
print(subclasses)

if subclasses:
    name = "%s (extended by %s)" % (cls.__name__, ', '.join(sub.__name__ for sub in subclasses))
    tu = tuple(reversed(subclasses))
    print('name is:', name)
    print('tu is:', tu)

    cls = type(name, tu, {})

o = cls(100)
members = inspect.getmembers(o, inspect.ismethod)

for method_name, mv in members:
    print('method_name is:',method_name)
    print('mv is %r:' % mv)
    print('__name__ is:',mv.__name__)

    for claz in reversed(mv.__self__.__class__.mro()):
        print('claz is:',claz)
        fn = getattr(claz, mv.__name__, None)
        print('fn is:',fn)
