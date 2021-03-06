from hypertype import *

def test_simple_types():
    assert String.valid("(↑t)")
    assert not String.valid(5)

    assert Integer.valid(1)
    assert not Integer.valid("(↑t)")

    assert Float.valid(3.14)
    assert not Float.valid("(↑t)")

    assert Boolean.valid(True)
    assert Boolean.valid(False)
    assert not Boolean.valid("(↑t)")
    assert not Boolean.valid(3.14)

    assert Nothing.valid(None)
    assert not Nothing.valid(5)
    assert not Nothing.valid("")

    assert Any.valid(None)
    assert Any.valid("(↑t)")
    assert Any.valid(1)
    assert Any.valid(3.14)
    assert Any.valid(False)

def test_list():
    Names = List(String)
    assert Names.valid([])
    assert Names.valid(["a", "b"])
    assert not Names.valid(["a", "b", 3])

def test_tuple():
    Point = Tuple(Integer, Integer)
    assert Point.valid([1, 2]) is True
    assert Point.valid([1, 2, 3]) is False
    assert Point.valid([1, "a"]) is False

def test_record():
    Person = Record({
        "name": String,
        "age": Integer,
        "phone_numbers": List(String)
    })
    assert Person.valid({
        "name": "Alice",
        "age": 42,
        "phone_numbers": ["123-456-7890", "123-456-7891"]
    })
    assert not Person.valid("Alice")
    assert not Person.valid({
        "name": "Alice",
        "age": 42
    })
    assert not Person.valid({
        "name": "Alice",
        "age": 42,
        "phone_numbers": "123-456-7890"
    })


def type_dict():
    PriceList = Dict(String, Float)
    assert PriceList.valid({})
    assert PriceList.valid({
        "apple": 10.0,
        "mango": 10.0,
    })
    assert not PriceList.valid({"apple": "x"})

def test_one_of():
    Value = Integer | List(Integer)
    assert Value.valid(1)
    assert Value.valid([1, 2])
    assert not Value.valid("foo")
    assert not Value.valid(["a", "b"])

def test_literal():
    Plus = Literal("+")
    assert Plus.valid("+")
    assert not Plus.valid("foo")

def test_reference():
    BinOp = Literal("+") | Literal("*")
    Expr = Reference()
    Expr.set(
        Integer
        | Record({"left": Expr, "op": BinOp, "right": Expr})
        )

    assert Expr.valid(1)
    assert Expr.valid({"left": 1, "op": "+", "right": 2})
    assert Expr.valid({
        "left": 1,
        "op": "+",
        "right": {
            "left": 2,
            "op": "*",
            "right": 3
        }})

def test_method():
    Value = Reference()
    Value.set(Integer | List(Value))

    @method
    def total(value: Integer):
        return value

    @method
    def total(value: List(Value)):
        return sum(total(v) for v in value)

    assert total(1) == 1
    assert total([1, 2, 3, 4]) == 10
    assert total([1, [2, 3], 4]) == 10
