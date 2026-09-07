# Glossary

Use these terms consistently in code, API fields, UI copy, tests, and documentation.

| Term | Meaning |
| --- | --- |
| Base route | The OSRM bicycle-oriented route between origin and destination before an optional POI is added |
| Candidate POI | A cached point of interest that meets category and route-corridor filters but is not necessarily selected |
| Cavite coverage boundary | The v1 geographic area the app is prepared to route within; its exact geometry is still to be defined |
| Detour radius | The user-selected maximum corridor distance used to look for POIs, constrained to 0.5 km to 5 km |
| Detour cost | Extra route distance, duration, or other measured route impact caused by adding a POI; define the final scoring metric before use |
| Elevation profile | Ordered elevation samples along a route, with source and sampling metadata |
| ETL run | One controlled extract, transform, validate, and load execution with provenance and outcome metrics |
| POI | Point of interest such as a cafe, bicycle repair shop, vulcanizing shop, or scenic viewpoint |
| Route corridor | The bounded geographic area near the base route used to query candidate POIs |
| Source provenance | Metadata identifying where a record came from, its external identity, retrieval time, and relevant query/version |
| Steep-climb summary | A pre-ride summary of route segments over the documented gradient threshold; it is not a guarantee of every road condition |
