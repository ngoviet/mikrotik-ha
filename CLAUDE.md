# mikrotik-ha — Home Assistant MikroTik Router Integration

Fork of [`tomaae/homeassistant-mikrotik_router`](https://github.com/tomaae/homeassistant-mikrotik_router) maintained at [`ngoviet/mikrotik-ha`](https://github.com/ngoviet/mikrotik-ha). Apache-2.0 license.

## Project overview

HACS custom integration to monitor and control MikroTik RouterOS devices from Home Assistant. Supports RouterOS v6.43+ / v7.1+ and HA 2024.3+. Distributed as a HACS zip release.

### Platforms (6)
`sensor`, `binary_sensor`, `device_tracker`, `switch`, `button`, `update`

### Features
Interface management (enable/disable, SFP, PoE, traffic), NAT/mangle/filter rule toggling, PPP user control, device presence tracking (ARP, wireless, CAPsMAN, Netwatch), Kid Control, client traffic monitoring (Accounting v6 / Kid Control v7), system health (CPU, memory, HDD, temperature, fans, PSU), UPS, GPS, firmware upgrades (RouterOS + RouterBOARD), script execution. 26 translations via Lokalise.

## Architecture

```
custom_components/mikrotik_router/
├── __init__.py          # Integration entry point — async_setup_entry
├── const.py             # Config keys, defaults, PLATFORMS list
├── config_flow.py       # ConfigFlow + OptionsFlow (version 2, migrate from v1)
├── coordinator.py       # MikrotikCoordinator (30s) + MikrotikTrackerCoordinator (10s)
├── mikrotikapi.py       # Low-level librouteros wrapper (connect, query, set_value, execute)
├── apiparser.py         # Declarative API response → dict parser (parse_api, from_entry)
├── entity.py            # MikrotikEntity base class + shared async_add_entities
├── sensor.py            # MikrotikSensor, MikrotikInterfaceTrafficSensor, MikrotikClientTrafficSensor
├── sensor_types.py      # 45 sensor EntityDescriptions
├── binary_sensor.py     # MikrotikBinarySensor, MikrotikPPPSecretBinarySensor, MikrotikPortBinarySensor
├── binary_sensor_types.py
├── switch.py            # Port/NAT/Mangle/Filter/Queue/KidControl switches
├── switch_types.py      # 8 switch EntityDescriptions
├── button.py            # MikrotikScriptButton
├── button_types.py
├── device_tracker.py    # MikrotikHostDeviceTracker (ScannerEntity-based)
├── device_tracker_types.py
├── update.py            # RouterOS firmware + RouterBOARD firmware update entities
├── update_types.py
├── diagnostics.py       # async_get_config_entry_diagnostics
├── helper.py            # format_attribute, format_value
├── exceptions.py        # ApiEntryNotFound
├── services.yaml        # Empty (no custom services)
├── strings.json         # Config flow translations
├── manifest.json        # domain=mikrotik_router, deps: librouteros>=3.4.1, mac-vendor-lookup>=0.1.12
└── translations/        # 26 locale JSON files
```

### Data flow

1. `config_flow` validates connection, creates `ConfigEntry`
2. `__init__.py:async_setup_entry` creates two coordinators:
   - `MikrotikCoordinator` — polls RouterOS every 30s (configurable), 30+ API queries per cycle
   - `MikrotikTrackerCoordinator` — polls every 10s, ARP-pings tracked hosts
   - Both write into shared `coordinator.ds["host"]` dict (**not thread-safe**)
3. Each platform's `async_setup_entry` calls `async_add_entities` which listens on signal `"update_sensors"` for dynamic entity creation
4. Entities read from coordinator data via `_handle_coordinator_update()`
5. Switches/buttons write back via `coordinator.set_value()` / `coordinator.execute()`

### Key patterns
- **Dual coordinator**: Data coordinator (30s) and tracker coordinator (10s) share `ds["host"]` dict — race condition risk
- **Declarative parsing**: `apiparser.parse_api()` maps RouterOS key-value responses to structured dicts with type coercion, defaults, composite keys, and filters
- **Dynamic entity creation**: Signal-based `async_dispatcher_connect("update_sensors", ...)` pattern in each platform
- **Entity grouping**: Virtual device entries in the HA device registry for NAT, Mangle, Filter, PPP, Queue groups

## Stack
- **Language**: Python 3.13
- **Key deps**: `librouteros>=3.4.1` (RouterOS API), `mac-vendor-lookup>=0.1.12`
- **Dev deps**: pytest, homeassistant, pylint, flake8, bandit, black, mypy, pre-commit
- **CI**: GitHub Actions — ci.yml (black, flake8, bandit, hassfest, pytest-commented-out), release.yml, hacs.yml, sonarcloud.yml

## Commands

```bash
# Formatting
black --check custom_components/

# Linting
flake8 custom_components/
pylint --rcfile=setup.cfg custom_components/

# Security scan
bandit -r custom_components/

# HA manifest validation
hassfest

# Install deps (generate requirements from Pipfile first)
python .github/generate_requirements.py
pip install -r requirements.txt -r requirements_tests.txt

# Tests (currently no tests exist)
pytest
```

## Coding conventions
- Python 3.13 target, HA 2024.3+ minimum
- `CoordinatorEntity` for all entities, `_attr_has_entity_name = True`
- Entity descriptions in separate `*_types.py` files as frozen dataclass tuples
- `async_add_entities` pattern per platform with signal-based dynamic addition
- Use `homeassistant.const` units (`UnitOfTemperature.CELSIUS`, etc.)
- Translations managed externally via Lokalise
- Line length 220 (flake8), complexity max 10 (mccabe)

## Known bugs — high priority

| File | Issue |
|------|-------|
| `mikrotikapi.py:124-230` | **Reentrant lock deadlock**: `query()` acquires `threading.Lock`, calls `connection_check()` → `connect()` which tries to acquire the same lock. Use `threading.RLock()`. |
| `coordinator.py:153-204` | **Shared mutable state race**: Both coordinators write to `coordinator.ds["host"]` without synchronization (30s vs 10s timers). |
| `update.py:144` | **Crash**: `self.data["routerboard"]` should be `self.coordinator.data["routerboard"]`. `self.data` does not exist on the entity class. |
| `update.py:181-209` | **Infinite loop risk**: `generate_version_list` + `decrement_version` iterates every micro version between two RouterOS versions. From 7.x to 6.x this generates millions of iterations. |
| `device_tracker.py:196,211` | **TypeError**: `utcnow() - self._data["last-seen"]` crashes when `last-seen` is `False` (initial state). |
| `switch.py:149,171` | **KeyError**: `self._data["about"]` raises when the `about` field is missing from the interface data dict. |
| `button.py:60` | **Blocking call in async**: `self.coordinator.api.run_script()` is synchronous, blocks event loop. |

## Known bugs — medium priority

| File | Issue |
|------|-------|
| `coordinator.py:85, apiparser.py:21` | **Deprecated**: `datetime.utcfromtimestamp()` — Python 3.12+ deprecation. Use `datetime.fromtimestamp(ts, tz=timezone.utc)`. |
| `entity.py:280-281` | **Deprecated**: `DeviceInfo` uses `default_name`/`default_manufacturer` (HA 2024.6+). Use `name`/`manufacturer`. |
| `diagnostics.py:16` | **Wrong coordinator**: `tracker_coordinator` assigned from `data_coordinator` instead of `tracker_coordinator`. |
| `sensor_types.py:257,334` | **Duplicate key**: `system_poe_out_consumption` defined twice. |
| `switch.py:52` | **Dead RestoreEntity**: `RestoreEntity` mixin inherited but no restore logic implemented. |
| `device_tracker_types.py:9` | **Wrong parent**: Inherits `SwitchEntityDescription` instead of device tracker description. |
| `button_types.py:21` | **Wrong parent**: Inherits `SensorEntityDescription` instead of `ButtonEntityDescription`. |
| `coordinator.py:1432-1467` | **Over-restrictive permissions**: System health requires `write`/`policy`/`reboot` permissions but health is read-only data. |

## Known bugs — low priority

| File | Issue |
|------|-------|
| `__init__.py:18` | Dead code: `SCRIPT_SCHEMA` defined but never used. |
| `helper.py:21` | Dead code: `format_value()` never called. |
| `coordinator.py:83-95` | Dead code: `as_local()` function uses `DEFAULT_TIME_ZONE = None` which would raise on call. |
| `update.py:26` | Undeclared dependency on `packaging.version` (transitive from HA). |
| `config_flow.py:76-80` | `configured_instances()` has incorrect `@callback` on a non-callback function. |
| `config_flow.py:138` | Password field defaults to visible `admin` in UI. |

## HA compatibility upgrades needed

1. **Python 3.14 readiness**: Replace `datetime.utcfromtimestamp()` → `datetime.fromtimestamp(ts, tz=timezone.utc)` in `coordinator.py` + `apiparser.py`
2. **zoneinfo migration**: Replace `pytz.utc.localize()` → `zoneinfo.ZoneInfo("UTC")`
3. **DeviceInfo**: `default_name`/`default_manufacturer` → `name`/`manufacturer` (HA 2024.6+)
4. **CONN_CLASS_LOCAL_POLL**: Deprecated since HA 2024.4, remove/replace
5. **ConfigEntry version**: Already v2, migration from v1 handles `verify_ssl`
6. **Entity features**: `UpdateEntityFeature` bitmask already in use (correct for HA 2024+)

## Development workflow

- **Main branch**: `master` (sync with upstream `tomaae/homeassistant-mikrotik_router`)
- **Dev branch**: Create feature/fix branches off `master`
- **Testing**: No test suite exists yet. Test manually against a real RouterOS device via HA dev container or HACS local install
- **CI**: Runs on push/PR to `custom_components/**` — black, flake8, bandit, hassfest, SonarCloud
- **Releases**: GitHub release triggers `release.yml` — zips `custom_components/mikrotik_router/` and uploads as release asset
- **HACS**: Validated daily via `hacs.yml` workflow
