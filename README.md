# delta-semantics

Validate ingestion contracts (batch vs streaming) for Delta Lake tables.

## Features

- Define ingestion contracts via YAML/JSON.
- Validate table existence, checkpoint paths, schema consistency.
- CLI tool for easy integration in CI/CD or jobs.
- Extendable to track streaming semantics, schema versions, etc.

## Installation

```bash
pip install delta-ingestion-contract
```

Or clone and install with Poetry:

```bash
git clone https://github.com/chanukyapekala/delta-semantics.git
cd delta-semantics
poetry install
```

## Usage

```bash
validate-contract --contract path/to/contract.yml
```

Example contract.yml:

```yaml
table: bronze.customer
mode: streaming
owner: data-team
streaming:
  checkpoint_path: dbfs:/checkpoints/customer
schema_version: '1234567890'
```

## Usage in Databricks

### 1. Using `delta-semantics` in a Databricks Notebook

You can validate ingestion contracts interactively inside a notebook.

**Steps:**

- Install the package on your cluster or notebook environment:

```python
# On a notebook cell
%pip install delta-ingestion-contract
```

- Prepare a YAML contract file (`contract.yml`) with your ingestion semantics, for example:

```yaml
table: bronze.customer
mode: streaming
owner: data-team
streaming:
  checkpoint_path: dbfs:/checkpoints/customer
schema_version: '1234567890'
```

- Load and validate the contract:

```python
import yaml
from delta_ingestion_contract.contract import IngestionContract
from delta_ingestion_contract.validator import ContractValidator
from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

# Load contract YAML
with open("/dbfs/path/to/contract.yml") as f:
    contract_data = yaml.safe_load(f)

contract = IngestionContract(**contract_data)

validator = ContractValidator(spark, contract)
validator.validate()
```

---

### 2. Using `delta-semantics` on a Databricks Cluster via Wheel or PyPI

- Build a wheel or install from PyPI on the cluster:

```bash
# To build wheel locally (run on your dev machine)
poetry build

# Upload the wheel (.whl) file to DBFS or directly to the cluster libraries UI

# Or directly install via PyPI on the cluster init scripts or notebook
pip install delta-ingestion-contract
```

- Run the CLI tool inside a notebook or a job:

```bash
!validate-contract --contract /dbfs/path/to/contract.yml
```

- Or invoke programmatically inside your batch or streaming jobs:

```python
from delta_ingestion_contract.contract import IngestionContract
from delta_ingestion_contract.validator import ContractValidator
from pyspark.sql import SparkSession
import yaml

spark = SparkSession.builder.getOrCreate()

with open("/dbfs/path/to/contract.yml") as f:
    contract_data = yaml.safe_load(f)
contract = IngestionContract(**contract_data)

validator = ContractValidator(spark, contract)
validator.validate()
```

---

### Notes:

- When running on Databricks, use `/dbfs/` prefix to access files stored in DBFS from standard Python file I/O.
- Ensure SparkSession is properly configured with Delta Lake enabled (default on Databricks).
- The CLI tool is useful for CI/CD pipelines, whereas the programmatic API fits well inside notebooks and jobs.
- Extend the contract YAML to include custom ingestion semantics relevant to your pipelines.

## Development

Run tests with:

```bash
pytest
```

## License

MIT
