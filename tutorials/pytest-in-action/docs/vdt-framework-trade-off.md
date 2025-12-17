# Evaluation Report: PyTest for Page Navigation & Visual Driven Testing 

## Background 
In our current testing scenario, we aim to:
- Automate **page navigation** and **UI interactions**
- Capture **page snapshots** for **visual regiression**
- Integrate with **BDD-driven scenarios**
- Use **Python-based frameworks** for backend and frontend test orchestration

The question: Can PyTest alone handle page navigation and visual regression, or do we need additional tools?

--- 

## PyTest Capabilities 

### Feature: Page Navigation
- PyTest Native: **None**
- Required Extensions / Tools: Playwright, Selenium
- Evaluation: PyTest cannot operate browser page on its own; needs a browser automation library

### Feature: Page Scereenshot / Snapshot
- PyTest Native: **None**
- Required Extensions / Tools: Playwright, Selenium, Pillow
- Evaluation: Screenshot functionality requires external libraries

### Feature: Scenario Organization / BDD Integration
- PyTest Native: Supported via **pytest-bdd**
- Required Extensions / Tools: Behave alternative 
- Evaluation: PyTest can organize scenarios and drive test execution 

### Feature: Visual Regression / Snapshot Comparision
- PyTest Native: None
- Required Extensions / Tools: VRT frameworks,image comparision libs 
- Evaluation: PyTest alone cannot compare images; requires VDT integration 

**Conclusion**
- PyTest cannot indepedently handle UI page navigation or snapshot capture
- PyTest serves as a **robust execution engine** and can orchestrate tests, assertions, and BDD scenarios.
- Browser automation and snapshot capture must rely on tools like **Playwright** or **Selenium**.

## Visual Driven Test (VDT/VRT) Feasiblility 
**Current Context**:
- Testing UI-heavy application (e.g., Kiali dashboards, Prometheus UI)
- Need repeatable regression tests for visual consistency
- Scenarios include page interaction, configuration changes, snapshot comparisions

### Requirement: UI Interaction 
- Options: Playwright, Selenium 
- Evalution: Essential for automating button clicks, page navigation

### Requirements: Snapshot Capture 
- Options: Playwright screenshots API, Selenium screenshot
- Evaluation: Required for VRT 

### Requirements: Scenario Orchestration 
- Options: PyTest + pytest-bdd / Behave 
- Evaluation: Provides main thread to organize assignments and steps 

### Requirements: Regression Analysis
- Options: Image diff libraries (Pillow, BackstopJS)
- Evaluation: Required to detect visual changes 


**Conclusion**:
- VDT is **feasible** in our scenario using **PyTest as the orchestration framework** + **Playwright/Selenium for page automation** + **snapshot/image comparision libraries**.
- BDD can be used to structure test scenarios clearly.
- This setup provides an **enterprise-grade Visual Regression Testing pipeline**, even though PyTest alone cannot handle browser interaction. 


--- 

## Technical Recommendation 
Recommended Stack for Current Scenario: 

### Layer: Test Execution 
- Recommended Tool / Library: PyTest 
- Role: Organize and run tests, manage fixtures, generate reports

### Layer: BDD / Scenario Organization 
- Recomended Tool / Library: ptest-bdd / Behave 
- Role: Scenario-driven orchestration 

### Layer: Browser Automation 
- Recommended Tool / Library: Playwright (Python)
- Role: Page navigation, button clicks, element interaction 


### Layer: Snapshot / VDT 
- Recommended Tool / Library: Playwright screenshot API + imgdiff / Pillow 
- Role: Capture snapshots, compare UI changes 


### Layer: Reporting
- Recommended Tool / Library: PyTest HTML / JSON reports 
- Role: Consolidate results with VDT evidence

**Trade-Offs**:
- **Playwright vs Selenium**: Playwright provides more modern API, better support for dynamic UIs, headless execution, and snapshotting; Selenium is legacy but widely used. 
- **Behave vs PyTest-BDD**: Behave is more Pythonic and integrates well with snapshot-based VDT; PyTest-BDD keeps the stack within PyTest ecosystem. 