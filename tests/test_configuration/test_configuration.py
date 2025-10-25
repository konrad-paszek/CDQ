from cdq.configuration.properties import Property


class Foo(Property):
    key = "foo.str"


class FooBar(Property):
    key = "foo.int"


class TestSettings:
    foo = Foo()
    bar = FooBar(astype=int)


def test_env_var_is_picked_up_by_the_descriptor(monkeypatch):
    monkeypatch.setenv("CDQ__FOO__STR", "foo")
    assert TestSettings.foo == "foo"


def test_env_var_is_cast_to_requested_type(monkeypatch):
    monkeypatch.setenv("CDQ__FOO__INT", 10)
    assert TestSettings.bar == 10
