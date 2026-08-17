# Home Assistant Label Manager

A Home Assistant custom integration that automatically **inherits labels
assigned to a device to all entities belonging to that device**.

Label Manager has one focused purpose: keeping device labels and entity labels
synchronized. It does not create sensors, virtual devices, statistics, or
other derived entities.

## Status

**Version: 0.1.2**

Stable maintenance release.

The core label inheritance functionality was completed in `0.1.1`.
Version `0.1.2` is a cleanup release that removes unused placeholder modules
without changing the integration's behaviour.

The current test suite contains **27 passing tests**.

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

Changes to the labels of a device are detected through the Home Assistant
Device Registry.

When a label is added to a device, it is added to the device's entities.

When a label is removed from a device, the corresponding inherited label is
removed from the entities.

### Daily consistency synchronization

Label Manager can perform a complete synchronization of all devices once per
day.

The synchronization time can be configured through the integration options.

The interval is fixed to once per day.

Automatic synchronization can be enabled or disabled independently of manual
synchronization.

Changing the synchronization time or enabling/disabling automatic
synchronization takes effect without requiring a Home Assistant restart.

### Manual synchronization

A complete synchronization can be triggered manually at any time using the
integration's synchronization button.

Manual synchronization is independent of the automatic daily synchronization.

### Multiple labels

Multiple labels assigned to a device are supported.

Removing one device label does not affect the other inherited labels.

### Preservation of manually assigned entity labels

Labels that are assigned directly to an entity and are not managed by Label
Manager are preserved.

For example:

```text
Device:
  Beleuchtung

Entity:
  Energie
```

After synchronization:

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

Label Manager keeps track of which labels it considers inherited for each
entity.

This allows the integration to distinguish between labels managed by the
device inheritance mechanism and labels assigned independently to an entity.

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

Copy the following directory to your Home Assistant configuration:

```text
custom_components/label_manager/
```

Target location:

```text
/config/custom_components/label_manager/
```

Restart Home Assistant and add **Label Manager** through the integrations
page.

## Configuration

After adding the integration, open the integration's options.

### Automatic daily synchronization

Enable or disable the automatic daily synchronization.

The default is **enabled**.

### Synchronization time

Select the time at which the daily synchronization is performed.

The interval is fixed to **once per day**.

The manual synchronization button remains available regardless of the
automatic synchronization setting.

## What Label Manager does not do

Label Manager intentionally focuses only on label inheritance.

It does **not**:

- create group sensors
- create statistics sensors
- create virtual devices or virtual entities
- aggregate sensor values
- maintain a history of label changes
- provide functionality unrelated to device-to-entity label inheritance

These responsibilities belong outside this integration.

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

Current test status:

```text
27 passed
```

The test suite covers, among other things:

- device label inheritance
- multiple device labels
- removal of inherited labels
- preservation of manually assigned entity labels
- replacement of inherited labels
- manual modification of inherited labels
- device registry event handling
- device/entity lookup
- complete device synchronization
- manual synchronization
- daily synchronization scheduler
- configurable synchronization time
- enabling and disabling automatic synchronization
- options update handling
- options flow validation

## Project structure

```text
label-manager/
├── custom_components/
│   └── label_manager/
│       ├── brand/
│       │   └── icon.png
│       ├── translations/
│       │   ├── de.json
│       │   └── en.json
│       ├── __init__.py
│       ├── button.py
│       ├── config_flow.py
│       ├── const.py
│       ├── label_sync.py
│       ├── manifest.json
│       ├── services.py
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

## License

This project is licensed under the **MIT License**.

See the `LICENSE` file for the complete license text.
