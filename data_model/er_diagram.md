# Nuclear Outages - ER Diagram
```mermaid
erDiagram
    facilities {
        int facility_id PK
        string facility_name
    }

    facility_outages {
        string period PK
        int facility_id PK, FK
        float capacity
        float outage
        float percent_outage
    }

    generator_outages {
        string period PK
        int facility_id PK, FK
        int generator_id PK
        float capacity
        float outage
        float percent_outage
    }

    facilities ||--o{ facility_outages : "has"
    facilities ||--o{ generator_outages : "has"
```

## Tables

### facilities
Primary key: `facility_id`
One row per nuclear plant (66 total).

### facility_outages
Primary key: `(period, facility_id)`
One row per plant per day. Foreign key to facilities.

### generator_outages
Primary key: `(period, facility_id, generator_id)`
One row per generator per day. Foreign key to facilities.

## Relationships
- One facility → many facility_outages (one per day)
- One facility → many generator_outages (one per generator per day)