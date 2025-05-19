import argparse
import yaml
from pyspark.sql import SparkSession
from delta_ingestion_contract.contract import IngestionContract
from delta_ingestion_contract.validator import ContractValidator

def main():
    parser = argparse.ArgumentParser(description="Validate Delta ingestion contracts.")
    parser.add_argument("--contract", type=str, required=True, help="Path to the ingestion contract YAML")
    args = parser.parse_args()

    with open(args.contract) as f:
        contract_data = yaml.safe_load(f)
        contract = IngestionContract(**contract_data)

    spark = SparkSession.builder.appName("DeltaContractValidator").getOrCreate()
    validator = ContractValidator(spark, contract)
    validator.validate()

if __name__ == "__main__":
    main()
