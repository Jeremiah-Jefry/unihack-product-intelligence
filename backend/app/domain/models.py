"""Domain layer — conceptual types for the product intelligence model.

These are Python dataclasses/protocols defining the domain contract.
They are infrastructure-independent and will be implemented by concrete
ORM models and Pydantic schemas in later modules.
"""

from __future__ import annotations

import enum
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


# --- Enums (from product-intelligence-schema.json) ---


class LifecycleStatus(enum.Enum):
    ACTIVE = "active"
    DISCONTINUED = "discontinued"
    OBSOLETE = "obsolete"
    UNKNOWN = "unknown"


class AttributeDomain(enum.Enum):
    IDENTITY = "identity"
    CLASSIFICATION = "classification"
    SPECIFICATION = "specification"
    PHYSICAL = "physical"
    PERFORMANCE = "performance"
    ELECTRICAL = "electrical"
    MECHANICAL = "mechanical"
    ENVIRONMENTAL = "environmental"
    CERTIFICATION = "certification"
    COMMERCIAL = "commercial"
    COMPATIBILITY = "compatibility"
    DESCRIPTION = "description"
    MEDIA = "media"


class ValueType(enum.Enum):
    STRING = "string"
    NUMBER = "number"
    BOOLEAN = "boolean"
    ENUM = "enum"
    RANGE = "range"
    MEASUREMENT = "measurement"
    DIMENSION = "dimension"
    PERCENTAGE = "percentage"
    DATE = "date"
    DURATION = "duration"
    COMPOUND = "compound"
    LIST = "list"


class InformationCategory(enum.Enum):
    IDENTITY = "identity"
    SPECIFICATION = "specification"
    CLASSIFICATION = "classification"
    CERTIFICATION = "certification"
    SAFETY = "safety"
    COMMERCIAL = "commercial"
    PHYSICAL = "physical"
    COMPATIBILITY = "compatibility"
    DESCRIPTION = "description"
    MEDIA = "media"


class LifecycleState(enum.Enum):
    DISCOVERED = "discovered"
    EXTRACTED = "extracted"
    NORMALIZED = "normalized"
    ENRICHED = "enriched"
    VALIDATED = "validated"
    REVIEWED = "reviewed"
    APPROVED = "approved"
    REJECTED = "rejected"


class ValidationStatus(enum.Enum):
    PENDING = "pending"
    AUTO_VALIDATED = "auto_validated"
    HUMAN_VALIDATED = "human_validated"
    REJECTED = "rejected"


class ConflictStatus(enum.Enum):
    NONE = "none"
    PENDING_RESOLUTION = "pending_resolution"
    RESOLVED = "resolved"
    PERMANENTLY_CONFLICTING = "permanently_conflicting"


class ConflictType(enum.Enum):
    VALUE_MISMATCH = "value_mismatch"
    UNIT_MISMATCH = "unit_mismatch"
    SOURCE_CONTRADICTION = "source_contradiction"
    STALE_VS_CURRENT = "stale_vs_current"


class ExtractionMethod(enum.Enum):
    TEXT_EXTRACTION = "text_extraction"
    OCR = "ocr"
    TABLE_PARSING = "table_parsing"
    WEB_SCRAPING = "web_scraping"
    API_LOOKUP = "api_lookup"
    MANUAL_ENTRY = "manual_entry"
    INFERENCE = "inference"


class FreshnessStatus(enum.Enum):
    CURRENT = "current"
    OUTDATED = "outdated"
    UNKNOWN = "unknown"
    REQUIRES_REVERIFICATION = "requires_reverification"


class ReviewAction(enum.Enum):
    APPROVE = "approve"
    REJECT = "reject"
    CORRECT = "correct"
    DEFER = "defer"
    MERGE = "merge"


class SourceTrustLevel(enum.Enum):
    MANUFACTURER_OFFICIAL = "manufacturer_official"
    AUTHORIZED_DISTRIBUTOR = "authorized_distributor"
    THIRD_PARTY_VERIFIED = "third_party_verified"
    THIRD_PARTY_UNVERIFIED = "third_party_unverified"
    UNKNOWN = "unknown"


class SourceType(enum.Enum):
    PDF = "pdf"
    CSV = "csv"
    EXCEL = "excel"
    WEB_PAGE = "web_page"
    IMAGE = "image"
    SCANNED_DOCUMENT = "scanned_document"
    ERP_EXPORT = "erp_export"
    API_RESPONSE = "api_response"


# --- Domain Dataclasses ---


@dataclass
class SourceLocation:
    """Precise location within a source document."""
    page: Optional[int] = None
    section: Optional[str] = None
    table_id: Optional[str] = None
    row: Optional[int] = None
    column: Optional[str] = None
    text_span: Optional[str] = None


@dataclass
class FreshnessInfo:
    """Source freshness tracking."""
    freshness_status: FreshnessStatus = FreshnessStatus.UNKNOWN
    source_published_at: Optional[datetime] = None
    source_version: Optional[str] = None
    source_last_verified_at: Optional[datetime] = None
    freshness_reason: Optional[str] = None


@dataclass
class SourceDocument:
    """A source document containing product information."""
    id: UUID = field(default_factory=uuid4)
    name: str = ""
    type: SourceType = SourceType.PDF
    location: str = ""
    content_hash: str = ""
    acquired_at: datetime = field(default_factory=datetime.utcnow)
    published_at: Optional[datetime] = None
    trust_level: SourceTrustLevel = SourceTrustLevel.UNKNOWN
    extraction_status: str = "pending"
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass
class CandidateValue:
    """A candidate value extracted from a specific source."""
    id: UUID = field(default_factory=uuid4)
    attribute_id: UUID = field(default_factory=uuid4)
    value: Optional[str] = None
    unit: Optional[str] = None
    source_id: UUID = field(default_factory=uuid4)
    source_location: SourceLocation = field(default_factory=SourceLocation)
    extraction_method: ExtractionMethod = ExtractionMethod.TEXT_EXTRACTION
    extraction_confidence: float = 0.0
    source_trust_score: float = 0.0
    freshness: FreshnessInfo = field(default_factory=FreshnessInfo)
    extracted_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class ProductAttribute:
    """A single attribute of a product with full provenance."""
    id: UUID = field(default_factory=uuid4)
    product_id: UUID = field(default_factory=uuid4)
    name: str = ""
    domain: AttributeDomain = AttributeDomain.SPECIFICATION
    value_type: ValueType = ValueType.STRING
    value: Optional[str] = None
    original_value: Optional[str] = None
    unit: Optional[str] = None
    missing_status: Optional[str] = None
    information_category: InformationCategory = InformationCategory.SPECIFICATION
    candidates: list[CandidateValue] = field(default_factory=list)
    selected_candidate_id: Optional[UUID] = None
    conflict_status: ConflictStatus = ConflictStatus.NONE
    confidence: float = 0.0
    validation_status: ValidationStatus = ValidationStatus.PENDING
    lifecycle_state: LifecycleState = LifecycleState.DISCOVERED
    requires_review: bool = False
    review_reason: Optional[str] = None
    extracted_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class QualityMetrics:
    """Quality scores for a product record."""
    completeness_score: float = 0.0
    accuracy_score: float = 0.0
    consistency_score: float = 0.0
    freshness_score: float = 0.0
    evidence_coverage: float = 0.0
    validation_coverage: float = 0.0
    conflict_count: int = 0
    review_pending_count: int = 0


@dataclass
class Product:
    """Core product entity."""
    id: UUID = field(default_factory=uuid4)
    mpn: str = ""
    brand: str = ""
    name: Optional[str] = None
    model: Optional[str] = None
    lifecycle_status: LifecycleStatus = LifecycleStatus.UNKNOWN
    primary_category: str = ""
    category_confidence: float = 0.0
    manufacturer_name: str = ""
    manufacturer_id: Optional[str] = None
    short_description: Optional[str] = None
    long_description: Optional[str] = None
    confidence: float = 0.0
    validation_status: str = "pending"
    review_status: str = "not_required"
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    version: int = 1
