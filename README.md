# Technologica Test Task

This repository contains solutions for two related tasks in the AEC (Architecture, Engineering, Construction) software domain.

## Repository Structure

```
technologica-test-task/
├── feature_delivery_estimation/     # Task 1: Feature effort estimation
└── api_integration_package/         # Task 2: Service integration demo
```

## Task 1: Feature Delivery Estimation

**[📁 feature_delivery_estimation/](feature_delivery_estimation/)**

Comprehensive effort estimation for 11 output formatting features in an AEC application.

**Key Deliverables:**
- Executive summary with critical path analysis
- Detailed Excel estimation spreadsheet
- Interactive Gantt chart visualization
- Actionable development strategy

**Results:**
- Total Effort: 198 hours
- Critical Path: 66 hours (CAD/GIS export chain)
- Timeline: ~11 business days (4 developers)

[📖 Read full documentation →](feature_delivery_estimation/README.md)

---

## Task 2: API Integration Package

**[📁 api_integration_package/](api_integration_package/)**

Demonstration package for bidirectional integration between Takeoff and Estimator services using webhook-based pull architecture.

**Key Deliverables:**
- Corrected OpenAPI specification (YAML)
- Two working FastAPI demo applications
- Docker Compose orchestration
- Complete documentation with Mermaid diagrams
- Example webhook payloads

**Architecture:**
- **Takeoff Service** (port 8000): Measurement data provider with GET endpoint
- **Estimator Service** (port 8001): Cost calculator with webhook endpoint
- **Integration Flow**: Webhook notification → Pull full state → Calculate estimate

**Quick Start:**
```bash
cd api_integration_package
docker-compose up
```

[📖 Read full documentation →](api_integration_package/README.md)

---

## Technologies Used

**Feature Estimation:**
- Excel for detailed breakdown and calculations
- Gantt chart visualization (HTML/JavaScript)
- Critical Path Method (CPM) for scheduling

**API Integration:**
- Python 3.11 + FastAPI for REST APIs
- Pydantic for data validation
- Docker Compose for orchestration
- Mermaid for architecture diagrams
- OpenAPI/Swagger for API documentation

---

## Project Context

Both tasks demonstrate skills in:
- **Requirements Analysis**: Understanding complex AEC domain requirements
- **Technical Planning**: Breaking down features into actionable tasks
- **Architecture Design**: Designing scalable integration patterns
- **Rapid Prototyping**: Building working demos within time constraints (30-min budget for Task 2)
- **Documentation**: Creating clear, comprehensive documentation

---

## Repository Navigation

| Task | Focus Area | Key Files |
|------|-----------|-----------|
| **Task 1** | Planning & Estimation | [summary_brief.md](feature_delivery_estimation/summary_brief.md), [estimate_final.xlsx](feature_delivery_estimation/estimate_final.xlsx), [gantt_final.html](feature_delivery_estimation/gantt_final.html) |
| **Task 2** | Implementation & Integration | [README.md](api_integration_package/README.md), [docker-compose.yml](api_integration_package/docker-compose.yml), [openapi_corrected.yaml](api_integration_package/openapi_corrected.yaml) |

---

## Next Steps

1. **Review Task 1 Estimation**: Open [feature_delivery_estimation/gantt_final.html](feature_delivery_estimation/gantt_final.html) in browser to see timeline
2. **Try Task 2 Demo**: Follow Quick Start in [api_integration_package/README.md](api_integration_package/README.md)
3. **Explore Architecture**: View Mermaid diagrams in [api_integration_package/](api_integration_package/) (use Mermaid Preview extension)

---

**Author:** Test Task Submission
**Domain:** AEC Software Development
**Date:** 2026