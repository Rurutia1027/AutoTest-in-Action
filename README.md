# AutoTest-in-Action

**_BDD-Orchestrated Visual Regression Testing Project_**

## Overview 
Autotest-in-Action is a Python-based automation testing project that combines **Behavior-Driven Development (BDD)** with **Visual Regression Testing (VRT)** to validate UI-heavy systems. 

BDD is used to **describe and organize scenarios**, while Visual Regression Testing is used to **access outcomes based on visual state**.

Together, they form a **clear**, **scenario-driven testing framework** where: 
- Test intent is expressed in **human-readable scenarios**
- System behavior is validated through **visual evidence**
- UI regression are detected automatically and reproducibly

This project is designed as a **professional automation practice repository**, demostrating how backend engineers can build **enterprise-grade UI automation and regression testing solutions** without developing frontend code. 

## Key Objectives
- Use **BDD** to organize test scenarios and behavior
- Use **Visual Regression Testing** to validate UI outcomes
- Replace manual UI verification with automated visual checks
- Capture UI snapshots as **test artifacts**
- Detect unintended UI changes early
- Provide clear and repeatable regression reports

## Main Framework: BDD + Visual-Driven Testing 
This project use **BDD** and **Visual-Driven Testing** together as the main thread. 

### Role of BDD 
BDD focuses on **what behavior is expected**, not how it is implemented. 

BDD is used to: 
- Define scenarios in a readable, structured way 
- Describe system behavior and user intent
- Group test cases by feature, scenario, or topic 
- Keep test logic understandable and maintainable 

### Role of Visual-Driven Testing (VRT/VDT)
Visual-Driven Testing focuses on **how the system actually appears to users**

VRT is used to: 
- Capture UI snapshots after scenario execution 
- Compare visuals against approved baselines
- Detect layout, chart, and dashboard regressions
- Provide visual evidence for test results 

### Why They Work Together 
- **BDD defines the story**
- **VRT validates the outcome** 

BDD answers "What should happen?"
VRT answers "Did it look correct?"

## Visual Regression Testing (VRT)
Visual Regression Testing is a **core validation strategy** in this project. 

### What is validated 
- Page layout and structure 
- Dashboards, charts, and graphs
- Key UI elements and indicators
- Overall visual state after interactions 


### How VRT works 
- Execute a BDD scenario
- Automate UI interactions
- Capture UI snapshots 
- Compare snapshots with baselines 
- Report visual differences as regressions

This approach is especially effective for: 
- Observability platforms (Kiali, Grafana, Prometheus)
- Configuration-driven UIs
- Systems where visual correctness is critical
- Complex dashboards that are hard to assert via APIs

## Technology Stack 
### Python (Primary Language)
- Fast iteration and scripting 
- Strong automation ecosystem 
- Backend-friendly and CI ready 

### BDD Framework (Behave / PyTest-BDD)
- Scenario definition and organization 
- Human-readable test description 
- Clear mapping between behavior and validation 


### PyTest 
- Test execution engine 
- Fixture and lifecycle management 
- Parallel execution support 
- Report generation 

### Playwright (Primary UI Automation)
- Modern browser automation 
- Reliable interaction with dynamic pages
- Native screenshot and snapshot support 
- Ideal for dashboard-style UIs


### Selenium (Secondary / Comparative)
- Classical UI automation framework
- Included for legacy compatibility and comparison 


## Repository Structure 
```text
autotest-in-action/
│
├── README.md
│
├── bdd/                         # BDD scenarios and step definitions
│   ├── features/
│   │   └── visual_regression.feature
│   └── steps/
│       └── ui_steps.py
│
├── tests/
│   ├── pytest/
│   │   ├── test_basic_cases.py
│   │   └── test_visual_regression.py
│   │
│   ├── playwright/
│   │   ├── pages/
│   │   │   ├── base_page.py
│   │   │   └── dashboard_page.py
│   │   ├── test_ui_flow.py
│   │   └── test_ui_snapshot.py
│   │
│   └── selenium/
│       ├── test_legacy_ui.py
│       └── test_navigation.py
│
├── vrt/                         # Visual Regression Testing core
│   ├── snapshot_manager.py
│   ├── baseline/
│   ├── current/
│   ├── diff/
│   └── comparison_rules.py
│
├── reports/
│   ├── html/
│   ├── snapshots/
│   └── regression_summary.json
│
├── ci/
│   └── pipeline.yml
│
├── requirements.txt
└── .gitignore
```

### Typical Workflow 
- Write a **BDD scenario**
- Execute UI interactions defined in steps
- Capture UI snapshots
- Perform visual comparison 
- Generate regression reports
- Re-run safely after UI or configuration changes 

## Why This Project is Valuable 
This project demostrates: 
- Practical use of **BDD beyond business logic**
- Strong **Visual Regression Testing** skills
- Automation architecture design
- UI testing without frontend development
- Scenario-driven, enterprise-oriented testing mindest

It positions you as a backend engineer who understands: 
- Testing strategy
- Automation frameworks
- UI regression risks
- Maintainable test design 

## Future Extensions 
- CI/CD integration for automated visual checks
- Support for additional platforms (Grafana, Kiali, Prometheus)
- Baseline approval and versioning workflows 
- Parallel execution for large UI suites