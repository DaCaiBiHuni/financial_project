# Investment Tracker

A desktop investment portfolio tracker focused on product trend tracking, portfolio visibility, financial analytics, and future extensibility.

## Product Positioning
This project is designed as a desktop-native investment tracking and portfolio analysis tool rather than a template-based information manager.

## Current Status
- Product concept defined
- Technical design document added
- PRD and implementation plan added
- Positioning and differentiation document added
- Progress snapshot maintained
- Desktop scaffold implemented
- Products module implemented
- Portfolio module implemented
- Dashboard card layout implemented
- Price refresh, yearly history, and trend chart implemented
- Provider settings implemented
- Yahoo and Alpha Vantage provider architecture added
- Recommended product entries implemented in Add Product dialog
- Strict refresh logic implemented for real provider failures
- Split refresh actions implemented for current price vs 1Y trend

## Main Features Implemented
- Product management
- Recommended product quick-add
- Portfolio tracking
- Dashboard summary cards
- Current price refresh
- 1-year monthly trend refresh
- Price history persistence
- Trend preview + chart
- Switchable market providers
- Settings-driven provider selection

## Repository Structure
- `docs/` product, technical, positioning, and progress documentation
- `app/` desktop application source code
- `data/` local app data and database files

## Recommended Next Steps
1. Validate Alpha Vantage data in-app with throttling
2. Add provider-specific error states per symbol
3. Add time range switching for chart history
4. Improve dashboard with charts
5. Package current prototype as an executable for hands-on testing
