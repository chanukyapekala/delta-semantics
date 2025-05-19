import click
import yaml
from delta_ingestion_contract.contract import IngestionContract
from delta_ingestion_contract.validator import ContractValidator
from pyspark.sql import SparkSession

@click.command()
@click.option('--contract', '-c', required=True, help='Path to ingestion contract YAML file.')
def validate_contract(contract):
    spark = SparkSession.builder.appName("DeltaSemanticsValidator").getOrCreate()
    with open(contract) as f:
        contract_data = yaml.safe_load(f)
    ingestion_contract = IngestionContract(**contract_data)
    validator = ContractValidator(spark, ingestion_contract)
    validator.validate()

if __name__ == '__main__':
    validate_contract()
