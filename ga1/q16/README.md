# E-Commerce Database Schema Design

## Scenario

You've been given CSV exports from a legacy e-commerce system. Your task is to design a proper SQL database schema.

## Data Files

1. **customers.csv** - Customer information
2. **products.csv** - Product catalog
3. **orders.csv** - Order records
4. **order_items.csv** - Line items for each order

## Your Task

Analyze the CSVs and create SQL DDL statements that:

1. Create tables for all 4 CSV files
2. Use appropriate SQLite data types (INTEGER, TEXT, REAL, BLOB, NULL)
3. Add PRIMARY KEY constraints
4. Add FOREIGN KEY constraints for relationships
5. Add NOT NULL constraints where appropriate
6. Add CHECK constraints for business rules (e.g., price > 0, quantity > 0)
7. Add UNIQUE constraints where needed

## Requirements

- **Narrow types:** Use the most specific type (INTEGER for IDs, not TEXT)
- **Constraints:** Add all appropriate constraints
- **Relationships:** Define all foreign keys between tables
- **Normalization:** Ensure the schema is properly normalized

## Example

```sql
CREATE TABLE example (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price REAL CHECK (price > 0),
    category_id INTEGER NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);
```
