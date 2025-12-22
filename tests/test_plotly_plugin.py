import pytest

pd = pytest.importorskip('pandas')
go = pytest.importorskip('plotly.graph_objects')

from vizdantic.plugins.plotly import render as plotly_render
from vizdantic.spec import FlowSpec, PointsSpec


def test_plotly_render_points_returns_figure():
    df = pd.DataFrame(
        {
            'x': [1, 2],
            'y': [3, 4],
            'group': ['a', 'b'],
        }
    )
    spec = PointsSpec(
        kind='points',
        chart='scatter',
        x='x',
        y='y',
        series='group',
        title='Points',
        legend_title='Group',
    )

    fig = plotly_render(spec, df)
    assert isinstance(fig, go.Figure)
    assert fig.layout.title.text == 'Points'
    assert fig.layout.legend.title.text == 'Group'


def test_plotly_render_flow_default_values():
    df = pd.DataFrame({'source': ['a', 'b'], 'target': ['c', 'd']})
    spec = FlowSpec(kind='flow', chart='sankey', source='source', target='target')

    fig = plotly_render(spec, df)
    assert isinstance(fig, go.Figure)
    assert fig.data[0].type == 'sankey'
    assert list(fig.data[0].link.value) == [1, 1]
