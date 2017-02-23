# Change Log of user_agent Library

## [0.1.9] - Unreleased

## [0.1.8] - 2017-02-23
### Changed
- Update mobile device IDs

## [0.1.7] - 2017-02-20
### Added
- The `ua` script for generating user-agent data in console
- Add product, productSub, vendor, buildID features
- New OS: android
- Add new option `device_type`
- If no os given then device type is "desktop" by default
- Add smartphone and tablet device IDs
- Add chrome and android navigators for android OS

### Changed
- Rename `platform` option to `os` option

### Fixed
- Better validation platform/navigator options
- Fix bugs in appVersion feature

## [0.1.6] - 2017-02-17
### Added
- Extend CI test environments: py35, py36, Windows.

### Changed
- Add recent chrome and firefox versions, by @pawelmhm
- Add recent Mac OS releases, by @pawelmhm
- Remove deprecated chrome/firefox versions

### Fixed
- Fix bug in generating chrome user agent on mac platform, by @pawelmhm

## [0.1.5] - 2016-09-13
### Changed
- Add recent chrome and firefox versions, by @pawelmhm

## [0.1.4] - 2016-05-01
### Added
- Add `oscpu` key to result of call to generate_navigotr_js

### Fixed
- Fix `oscpu` value for mac platform.

## [0.1.3] - 2016-04-12
### Fixed
- Fix `platform` key bug

## [0.1.2] - 2016-04-12
### Added
- Add generate_navigator_js function

## [0.1.1] - 2015-12-20
### Added
- Add IE user agents
