# CHANGELOG

All notable changes to this project should be recorded in this file.

The goal of this changelog is to provide a readable, high-level view of how the project evolves over time.

---

## [Unreleased]

### Planned
- further provider validation and throttling improvements
- dashboard chart enhancements
- time range switching for trend charts
- executable packaging and delivery improvements

---

## [v0.1.0-prototype] - 2026-03-26

### Added
- project repository initialized
- GitHub repository connected and first commits pushed
- product documentation added:
  - PRD
  - technical design
  - implementation plan
  - positioning and differentiation
  - progress snapshot
  - documentation index
- desktop scaffold created with PySide6
- SQLite database integration added
- Products page implemented
- Portfolio page implemented
- Dashboard page implemented
- Settings page implemented
- recommended product quick-add entries added
- product trend chart added
- price history storage added
- provider abstraction added
- Yahoo provider skeleton added
- Alpha Vantage provider option added
- settings-driven provider configuration added
- asynchronous refresh support added
- bottom-right loading indicator added
- dashboard summary card layout added

### Changed
- Products page layout changed to vertical segmented layout
- product detail area simplified into a concise summary presentation
- price refresh and one-year trend refresh were split into separate actions
- real-data refresh logic changed to strict mode to avoid silently overwriting data with mock fallback
- repository documentation restructured for better readability and consistency
- PRD, technical design, and implementation plan were reformatted for consistent structure and tone

### Fixed
- improved handling for provider-related refresh failures
- reduced UI blocking during refresh operations by moving refresh work to background threads
- improved user feedback during slow data refresh operations

---

## Versioning Note

This project is currently in a prototype stage.

Version labels are being used to mark meaningful milestones rather than production-ready releases.
