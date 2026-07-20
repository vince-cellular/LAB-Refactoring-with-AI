 source "/c/Users/zotec/OneDrive/Desktop/IRONHACK TRAINING LABS/LAB-Refactoring-with-AI/venv/Scripts/activate"
# Lab Proof - From Hacky Script to Production Workflow

## Workflow Overview

The original product generator script was refactored into a modular workflow.

Workflow:

INPUT
- Product JSON payload from valid_products.json

TRANSFORM
- Load JSON data
- Validate product fields using Pydantic
- Generate product listing using OpenAI API

OUTPUT
- Validated product object
- Generated product listing


---

## Workflow Configuration

Trigger:
Python script execution

Input Source:
valid_products.json

Validation:
ProductRequest Pydantic model

Processing:
Product data is transformed into validated objects.

Action:
OpenAI API generates an e-commerce listing.

Destination:
Console output containing product data and listing.


---

## Input Payload

Example:

```json
{
  "name": "Smart Watch",
  "price": 150,
  "category": "Accessories",
  "additional_info": "Fitness tracking smartwatch",
  "quantity": 3
}

