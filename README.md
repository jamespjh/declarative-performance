# Declarative Performance

Python framework scaffold for a declarative musical performance system.

## Carla generation

Generate a Carla project from declarative YAML:

```bash
declarative-performance --carla --defaults src/carla_defaults.yml config.yml --outfile example.carxp
```

Defaults:

- `--carla` is the current default backend.
- `--defaults` defaults to `src/carla_defaults.yml`.
- `--outfile` defaults to `out.carxp`.
