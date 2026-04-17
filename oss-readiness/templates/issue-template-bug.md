# Bug Report Issue Template

Place this file at `.github/ISSUE_TEMPLATE/bug_report.yml` in the target repo.

```yaml
name: Bug Report
description: Report a bug or unexpected behavior
title: "[Bug]: "
labels: ["bug", "triage"]
body:
  - type: markdown
    attributes:
      value: |
        Thanks for reporting. Please fill out the sections below.

  - type: textarea
    id: what-happened
    attributes:
      label: What happened?
      description: Describe the bug clearly
      placeholder: When I do X, Y happens instead of Z
    validations:
      required: true

  - type: textarea
    id: steps
    attributes:
      label: Steps to reproduce
      description: Minimal steps to reproduce the issue
      placeholder: |
        1. Install the project
        2. Run command or workflow X
        3. See error
    validations:
      required: true

  - type: textarea
    id: expected
    attributes:
      label: Expected behavior
      description: What did you expect to happen?
    validations:
      required: true

  - type: textarea
    id: environment
    attributes:
      label: Environment
      description: Your setup details
      value: |
        - OS:
        - Runtime / language version:
        - Project version / commit:
        - Package manager / tooling:
    validations:
      required: true

  - type: textarea
    id: logs
    attributes:
      label: Relevant logs
      description: Paste any error output or stack traces
      render: shell
    validations:
      required: false

  - type: checkboxes
    id: checks
    attributes:
      label: Before submitting
      options:
        - label: I searched existing issues and this hasn't been reported
          required: true
        - label: I tested against the latest supported version when possible
          required: false
```

Also create `.github/ISSUE_TEMPLATE/config.yml`:

```yaml
blank_issues_enabled: false
contact_links:
  - name: Security Vulnerability
    url: {SECURITY_REPORTING_URL}
    about: Report security vulnerabilities privately
  - name: Support / Discussion
    url: {COMMUNITY_SUPPORT_URL}
    about: Ask questions or discuss usage
  - name: Project Homepage / Docs
    url: {PROJECT_HOMEPAGE}
    about: Learn more about the project
```
