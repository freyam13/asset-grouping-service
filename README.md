# Asset Grouping Service

## Overview

A production-ready REST API service that enables dynamic grouping of cloud infrastructure assets based on configurable rules. This project demonstrates best practices in API design, clean code architecture, and robust error handling.

## Core Features

The service manages cloud infrastructure assets with the following model:
```json
{
  "id": "string",
  "name": "string",
  "type": "string",
  "tags": [
    {
      "key": "string",
      "value": "string"
    }
  ],
  "cloud_account": {
    "id": "string",
    "name": "string"
  },
  "owner_id": "string",
  "region": "string",
  "group_name": "string"
}
```

Key capabilities:
- dynamic asset grouping based on configurable rules
- support for complex matching conditions (type, name, tags)
- automatic group assignment when assets or rules are created/updated
- RESTful API with comprehensive OpenAPI documentation

### Example Use Cases

1. **Resource Organization**: Group all EC2 instances into an "instances" group:
   ```json
   {
     "group_name": "instances",
     "conditions": [
       {
         "field": "type",
         "operator": "equals",
         "value": "ec2-instance"
       }
     ]
   }
   ```

2. **Environment Segregation**: Group production resources:
   ```json
   {
     "group_name": "production-instances",
     "conditions": [
       {
         "field": "type",
         "operator": "equals",
         "value": "ec2-instance"
       },
       {
         "field": "tags",
         "operator": "contains",
         "key": "env",
         "value": "prod"
       }
     ]
   }
   ```

## Design Decisions

### Architecture
- FastAPI for robust API development with automatic OpenAPI documentation
- service layer pattern separating business logic from API handlers
- Pydantic for data validation and type safety

### Data Models
- distinct models for Assets, Tags, and GroupingRules
- type-safe Operator enum for condition matching
- optional group_name in Asset model
- flexible GroupingCondition model for various matching patterns

### Grouping Logic
- automatic rule evaluation during asset/rule creation and updates
- clear separation of concerns for future extensibility
- real-time group maintenance for data consistency

### Error Handling
- comprehensive exception handling
- structured for future error type expansion
- clear error messages and appropriate HTTP status codes

## Technical Implementation

The service implements:
- asset and rule creation with automatic grouping
- rule evaluation with multiple condition types
- asset retrieval and updates
- structured interfaces for asset/rule management

Future enhancements planned:
- database integration for persistence
- authentication and authorization
- pagination for large asset lists
- caching for frequently accessed rules
- metrics and monitoring integration

## Getting Started

1. Install dependencies:
```bash
pipenv install --dev
```

2. Run the service:
```bash
pipenv run python src/main.py
```

3. Access API documentation:
   - Visit `http://localhost:8000/docs` in your browser
   - Interactive OpenAPI documentation available

4. Run tests:
```bash
pipenv run pytest
```

## Project Structure

```
src/
├── api/          # API routes and handlers
├── models/       # Pydantic models
├── services/     # Business logic
└── utils/        # Helper functions

tests/            # Test suite
```

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details.