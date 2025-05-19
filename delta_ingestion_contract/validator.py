from pyspark.sql import SparkSession
from delta_ingestion_contract.contract import IngestionContract

class ContractValidator:
    def __init__(self, spark: SparkSession, contract: IngestionContract):
        self.spark = spark
        self.contract = contract

    def validate_table_exists(self):
        try:
            self.spark.read.table(self.contract.table).limit(1).collect()
        except Exception:
            raise ValueError(f"Table {self.contract.table} does not exist")

    def validate_table_properties(self):
        if self.contract.mode == "streaming" and self.contract.streaming:
            props = self.spark.sql(f"DESCRIBE TABLE EXTENDED {self.contract.table}").collect()
            kv = {row.col_name.strip(): row.data_type.strip() for row in props if row.col_name and row.data_type}
            checkpoint = kv.get("ingestion.checkpoint")
            if checkpoint and checkpoint != self.contract.streaming.checkpoint_path:
                raise ValueError(f"Checkpoint mismatch: {checkpoint} != {self.contract.streaming.checkpoint_path}")

    def validate_schema_consistency(self):
        if self.contract.schema_version:
            table_schema = self.spark.read.table(self.contract.table).schema.json()
            hash_val = str(hash(table_schema))
            if hash_val != self.contract.schema_version:
                raise ValueError(f"Schema hash mismatch: expected {self.contract.schema_version}, got {hash_val}")

    def validate(self):
        self.validate_table_exists()
        self.validate_table_properties()
        self.validate_schema_consistency()
        print("Contract validated successfully.")
