# Copilot Instructions

You are assisting with the Music Programming project.

Before answering, read:

- docs/project-brief.md

- docs/dogma.md

- docs/architecture-notes.md

- docs/decision-log.md

- docs/questions.md

Respect the project dogma:

- Performance must feel like music-playing, not engineering.

- The interface during performance is piano/keyboards/pads/pedals/score, not laptop/screen.

- Prefer MIDI-level structure over audio-level manipulation where possible.

- Configuration can be engineered; performance should be immediate and physical.

When proposing code or architecture:

- Separate practice mode from performance mode.

- Separate artistic dogma from implementation convenience.

- Record decisions in decision-log.md when they harden.

- Prefer inspectable, testable, text-based configuration.

Python environment note:

- This repository uses `venv` at the project root.

- Do not create or reference `.venv`.

Security note:

- This is a public repository. Never commit secrets, API keys, tokens, passwords, private keys, or credentials of any kind.

- Before committing, verify that fixture files and test data do not expose authentication material, even in encoded or binary form.

- .gitignore is configured to exclude common secret file patterns (.env, *.pem, *.key, etc.) but always check before committing.