LedgerLite

A banking application project built using modern backend, event-driven architecture, AI, and cloud-native technologies.

## Repository Structure

```text
ledgerlite/
├── services/
│   ├── accounts/                 # FastAPI + Postgres: accounts, ledger, transfers
│   ├── fraud-alerts/             # Kafka consumer: fraud rules and alerts
│   ├── bff/                      # Backend for Frontend
│   └── assistant/                # LangChain + LangGraph AI assistant
│
├── web/                          # Angular app
│
├── deploy/
│   ├── compose/                  # docker-compose files
│   └── k8s/                      # manifests / kustomize
│
├── infra/
│   └── terraform/                # IaC
│
├── loadtests/                    # k6 scripts
│
├── docs/                         # ADRs, diagrams, weekly notes
│
└── .github/
    └── workflows/                # CI/CD
```