Configuration Merge Analysis

This archive contains three configuration files:
- base.json: Original configuration (common ancestor)
- branch_a.json: Configuration from branch A
- branch_b.json: Configuration from branch B

Task: Perform a three-way merge analysis to detect conflicts.

A CONFLICT occurs when:
1. The same setting is modified in BOTH branch_a and branch_b
2. The 'value' field differs between the two branches
3. Compared to the base configuration

Count the total number of conflicting settings.
