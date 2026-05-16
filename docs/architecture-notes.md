# Current Technical Direction

## Host and plugin architecture

The current likely direction is:

- Carla as programmable plugin host;

- OSC control;

- generated `.carxp` project files;

- backend abstraction to support future hosts.

The system should eventually support:

- AU on macOS;

- VST/VST3 cross-platform;

- Linux-native open audio ecosystems.

## Operating system strategy

Current realities:

- primary personal machine is macOS;

- existing instrument rig is connected to MacBook;

- AU ecosystem already established;

- Linux ecosystem appears attractive architecturally.

Likely direction:

- macOS for near-term integration and performance;

- Linux/open audio ecosystem for long-term infrastructure learning and portability.

Migration should be gradual and pragmatic.

## Text-first configuration

Configurations should preferably be:

- declarative;

- version-controllable;

- human-readable;

- generatable programmatically;

- testable.

Opaque binary project formats are undesirable unless wrapped by generated tooling.

## Reproducibility

The project should support:

- deterministic configuration generation;

- fixture MIDI sequences;

- automated rendering tests;

- CI/CD validation;

- regression testing of audio pipelines.

Example future pipeline:

- generate host session;

- load plugins automatically;

- play reference MIDI;

- render audio;

- validate expected properties.
