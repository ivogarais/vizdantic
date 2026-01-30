# Vizdantic Spec Quick Reference

Source of truth: `vizdantic/spec.py` and `vizdantic.schema()`.

Optional metadata fields on any spec:
- `title`, `legend_title`, `backend`

Kinds, charts, and required fields

- cartesian
  - chart: bar | line | area | scatter
  - required: x, y
  - optional: series, facet

- points
  - chart: scatter
  - required: x, y
  - optional: series, size

- distribution
  - chart: histogram | box | violin | strip
  - required: value
  - optional: category

- parts
  - chart: pie
  - required: label, value

- matrix
  - chart: density_heatmap | imshow
  - required: x, y, value
  - note: Plotly plugin currently renders as density_heatmap.

- flow
  - chart: sankey
  - required: source, target
  - optional: value

- hierarchy
  - chart: treemap | sunburst | icicle
  - required: path (list)
  - optional: value

- geo
  - chart: scatter_geo | line_geo | choropleth | scatter_mapbox | choropleth_mapbox
  - optional: location, lat, lon, value
  - note: Plotly needs either location or lat/lon.

- polar
  - chart: scatter_polar | line_polar | bar_polar
  - required: r, theta
  - optional: series

- ternary
  - chart: scatter_ternary | line_ternary
  - required: a, b, c
  - optional: series, size

- 3d
  - chart: scatter_3d | line_3d
  - required: x, y, z
  - optional: series, size

- financial
  - chart: funnel | funnel_area
  - optional: x, y, value, label
  - note: Plotly plugin uses x/y for funnel and funnel_area.

- parallel
  - chart: parallel_coordinates | parallel_categories
  - required: dimensions (list)
  - optional: color

- timeline
  - chart: timeline
  - required: x_start, x_end, y
  - optional: series
