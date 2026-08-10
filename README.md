# Home Assistant Label Manager

A Home Assistant custom integration for managing labels and automatically
inheriting device labels to the entities belonging to a device.

## Status

**Version: 0.1.1**

The first stable release of the Label Manager.

Device-to-entity label inheritance, manual synchronization, and automatic
daily synchronization are implemented and covered by automated tests.

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

### Daily consistency synchronization

The integration can automatically synchronize all registered devices once
per day.

The synchronization time can be configured through the integration options.
The interval is fixed to once per day.

Automatic synchronization can be enabled or disabled independently of the
manual synchronization.

Changing the synchronization settings takes effect without requiring a
Home Assistant restart.

### Manual synchronization

A manual synchronization of all registered devices can be triggered at any
time using the integration's synchronization button.

Manual synchronization is independent of the automatic daily synchronization
and is useful for testing or for immediately applying label changes.

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

### HACS

The Label Manager can be installed through HACS.

If the repository is not yet available in your HACS instance, add the GitHub
repository as a custom repository:

```text
https://github.com/ekkehard-lutz/label-manager
```

Select **Integration** as the repository category and install **Label Manager**.

After installation, restart Home Assistant if requested by HACS.

Then add **Label Manager** through:

```text
Settings → Devices & services → Add integration
```

### Manual installation

The integration files are located in:

```text
custom_components/label_manager/
```

For a manual installation, copy that directory to:

```text
/config/custom_components/label_manager/
```

Then restart Home Assistant and add **Label Manager** through the integrations
page.

## Configuration

After adding the integration, open its configuration/options dialog.

The following options are available:

### Automatic daily synchronization

Enable or disable the automatic daily synchronization.

The default is **enabled**.

### Synchronization time

Select the time at which the daily synchronization is performed.

The interval is fixed to **once per day**.

Changing the time or enabling/disabling automatic synchronization does not
require a Home Assistant restart.

The manual synchronization button remains available regardless of the
automatic synchronization setting.

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
- complete device synchronization
- manual synchronization
- daily synchronization scheduler
- configurable synchronization time
- enabling and disabling automatic synchronization
- options update handling
- options flow validation

Current status:

```text
27 passed
```

## Project structure

```text
label-manager/
├── custom_components/
│   └── label_manager/
│       ├── brand/
│       ├── translations/
│       ├── __init__.py
│       ├── button.py
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
│       └── strings.json
├── tests/
│   ├── test_init.py
│   ├── test_label_sync.py
│   ├── test_scheduler.py
│   └── test_services.py
├── .gitignore
├── LICENSE
├── README.md
├── hacs.json
├── pyproject.toml
└── requirements-dev.txt
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
- Manual full synchronization
- Configurable daily consistency synchronization
- Enable or disable automatic synchronization
- Configurable synchronization time

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

### 1.0.0 – Extended Stable Release

- Extended documentation
- Further features based on practical usage
- Stable long-term configuration and synchronization behaviour

## License

This project is licensed under the **MIT License**.

See the `LICENSE` file for the complete license text.
