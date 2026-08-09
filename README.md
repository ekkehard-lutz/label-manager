# Home Assistant Label Manager

A Home Assistant custom integration for managing labels and automatically
inheriting device labels to the entities belonging to a device.

## Status

**Version: 0.1.0**

The project is currently under active development.

The first implementation of automatic device-to-entity label inheritance
is working and covered by automated tests.

## Features

### Device label inheritance

Labels assigned to a Home Assistant device are automatically inherited by
all entities belonging to that device.

For example:

```text
Device
├── Label: Beleuchtung
└── Label: Wohnzimmer

        ↓ inheritance

Entity 1
├── Label: Beleuchtung
└── Label: Wohnzimmer

Entity 2
├── Label: Beleuchtung
└── Label: Wohnzimmer
```

### Automatic synchronization

Changes to the labels of a device are automatically detected through the
Home Assistant Device Registry.

When a label is added to a device, it is added to the device's entities.

When a label is removed from a device, the corresponding inherited label is
removed from the entities.

### Multiple labels

Multiple device labels are supported.

Removing one label does not affect the other inherited labels.

### Manual entity labels

Labels that are assigned directly to an entity and are not inherited from
the device are preserved.

For example:

```text
Device:
  Beleuchtung

Entity:
  Energie
```

Results in:

```text
Entity:
  Energie
  Beleuchtung
```

If `Beleuchtung` is subsequently removed from the device, the entity keeps:

```text
Energie
```

### Tracking inherited labels

The integration keeps a separate record of which labels are considered
inherited for each entity.

This makes it possible to correctly handle cases where an inherited label
is manually removed and later manually added again.

For example:

1. The device has the label `Beleuchtung`.
2. The entity inherits `Beleuchtung`.
3. `Beleuchtung` is manually removed from the entity.
4. `Beleuchtung` is manually added to the entity again.
5. `Beleuchtung` is removed from the device.
6. `Beleuchtung` is also removed from the entity.

The integration therefore distinguishes between the current labels of an
entity and the labels that are managed through device inheritance.

## Installation

The integration is currently developed as a Home Assistant custom
integration.

The repository contains the integration in:

```text
custom_components/label_manager/
```

For development, the repository can be cloned separately:

```bash
cd /config
git clone https://github.com/ekkehard-lutz/label-manager.git label-manager-git
```

The integration files can then be copied to the active Home Assistant
configuration:

```text
/config/custom_components/label_manager/
```

> Installation and HACS support are currently being further developed.

## Development

The project uses a Python virtual environment for development and testing.

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Run the complete test suite:

```bash
python -m pytest -q
```

The current test suite contains tests for:

- device label inheritance
- multiple device labels
- removal of inherited labels
- preservation of manually assigned labels
- replacement of inherited labels
- manual modification of inherited labels
- device registry event handling
- device entity lookup

Current status:

```text
15 passed
```

## Project structure

```text
label-manager/
├── custom_components/
│   └── label_manager/
│       ├── __init__.py
│       ├── config_flow.py
│       ├── const.py
│       ├── coordinator.py
│       ├── entity.py
│       ├── exceptions.py
│       ├── label_sync.py
│       ├── manifest.json
│       ├── models.py
│       ├── sensor.py
│       ├── services.py
│       ├── statistics.py
│       ├── storage.py
│       ├── strings.json
│       └── translations/
├── tests/
│   ├── test_label_sync.py
│   └── test_services.py
├── README.md
└── LICENSE
```

## Roadmap

### 0.0.x – Foundation

- Home Assistant integration
- Config Flow
- Basic persistent storage
- Technical foundation for label synchronization

### 0.1.x – Label Inheritance

- Inherit device labels to all entities belonging to the device
- Support multiple device labels
- Automatically synchronize label changes
- Remove inherited labels when they are removed from the device
- Distinguish inherited labels from entity-only labels
- **Planned:** Periodic consistency synchronization (e.g. once per day/night)
  to recover from missed events or inconsistent states

### 0.2.x – Group Sensors

- Automatic creation and management of group sensors based on labels
- Configuration of group sensor behaviour

### 0.3.x – Statistics

- Statistics based on labels and grouped entities
- Additional statistics-related sensors and information

### 0.4.x – History

- History of label changes
- History of synchronization activities
- Improved visibility into label inheritance

### 1.0.0 – First Stable Release

- First stable release
- Complete documentation
- Stable configuration and synchronization behaviour
- Comprehensive automated test coverage

## License

This project is licensed under the **MIT License**.

See the `LICENSE` file for the complete license text.
