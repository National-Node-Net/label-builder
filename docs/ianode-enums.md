### IANode Security Labels ENUMS

#### Overview

IANode Security Labels provide enumerations to use with the Security Label Builder. They define specific default labels for the 
IANode environment. The system supports multiple and single value labels, 
as well as complex group logic.

> ### ⚠️ Warning
> This is conceptual implementation for illustrative purposes built for IANodeModel.

#### Classes and Enums

1. **IANodeSecurityLabelsV1 (Enum)**: Represents a simplified version of the default IANode model used in the IANode environment.
   - `PERMITTED_ORGANISATIONS`: A `MultiValueLabel` for specifying multiple allowed organizations.
   - `PERMITTED_NATIONALITIES`: A `MultiValueLabel` for defining multiple permitted nationalities.
   - `CLASSIFICATION`: A `SingleValueLabel` for indicating the clearance level.

2. **AndGroups (inherits MultiValueLabel)**: Used for creating conditions where all specified groups must be met (AND logic).
   - `construct(self, *values)`: Constructs a label expression where all values must be true.
   - `create_label(self, value: str)`: Formats the value for AND group logic.

3. **OrGroups (inherits MultiValueLabel)**: Used for creating conditions where any of the specified groups must be met (OR logic).
   - `construct(self, *values)`: Constructs a label expression where any value can be true.
   - `create_label(self, value: str)`: Formats the value for OR group logic.

4. **IANodeSecurityLabelsV2 (Enum)**: A more comprehensive representation of the .
   - `PERMITTED_ORGANISATIONS`: A `MultiValueLabel` for multiple allowed organizations.
   - `PERMITTED_NATIONALITIES`: A `MultiValueLabel` for multiple permitted nationalities.
   - `CLASSIFICATION`: A `SingleValueLabel` for clearance level.
   - `AND_GROUPS`: An `AndGroups` label for specifying groups where all conditions must be met.
   - `OR_GROUPS`: An `OrGroups` label for specifying groups where any condition can be met.

#### Usage Examples

1. **Using IANodeSecurityLabelsV1**
   ```python
   builder = SecurityLabelBuilder()
   builder.add(IANodeSecurityLabelsV1.CLASSIFICATION.value, "TopSecret")
   builder.add_multiple(IANodeSecurityLabelsV1.PERMITTED_ORGANISATIONS.value, "Org1", "Org2")
   label_expression = builder.build()
   ```
