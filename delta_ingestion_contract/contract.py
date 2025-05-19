from typing import Literal, Optional
from pydantic import BaseModel, Field

class StreamingConfig(BaseModel):
    checkpoint_path: str
    trigger: Optional[str] = Field(None, description="Trigger interval, e.g. '5 minutes'")
    source: Optional[str] = Field(None, description="Source system, e.g. 'kafka'")
    deduplication_keys: Optional[list[str]] = None

class IngestionContract(BaseModel):
    table: str
    mode: Literal["batch", "streaming"]
    owner: Optional[str] = None
    schema_version: Optional[str] = None
    streaming: Optional[StreamingConfig] = None
