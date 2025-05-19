import yaml
from pyspark.sql import SparkSession
from delta_ingestion_contract.contract import IngestionContract
from delta_ingestion_contract.validator import ContractValidator

spark = SparkSession.builder \
    .appName("ValidateIngestionContract") \
    .getOrCreate()

# Load contract
with open("examples/contract.yml", "r") as f:
    contract_dict = yaml.safe_load(f)

# Validate
contract = IngestionContract(**contract_dict)
validator = ContractValidator(spark, contract)
validator.validate()
