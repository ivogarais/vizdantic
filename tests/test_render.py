import pytest

from vizdantic.render import render
from vizdantic.spec import CartesianSpec


def test_render_dispatches_to_matching_binding():
    spec = CartesianSpec(kind='cartesian', chart='line', x='x', y='y')
    calls = {}

    def renderer(lib, spec_arg, data_arg):
        calls['args'] = (lib, spec_arg, data_arg)
        return 'ok'

    result = render(spec, data='data', lib='lib', bindings={CartesianSpec: renderer})
    assert result == 'ok'
    assert calls['args'] == ('lib', spec, 'data')


def test_render_raises_when_no_binding_matches():
    spec = CartesianSpec(kind='cartesian', chart='line', x='x', y='y')

    with pytest.raises(TypeError):
        render(spec, data='data', lib='lib', bindings={})
