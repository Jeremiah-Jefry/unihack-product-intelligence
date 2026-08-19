"""Tests for the domain model."""

from uuid import UUID

from app.domain.models import (
    AttributeDomain,
    CandidateValue,
    ConflictStatus,
    ConflictType,
    ExtractionMethod,
    FreshnessInfo,
    FreshnessStatus,
    InformationCategory,
    LifecycleState,
    LifecycleStatus,
    Product,
    ProductAttribute,
    QualityMetrics,
    SourceDocument,
    SourceLocation,
    SourceTrustLevel,
    SourceType,
    ValidationStatus,
    ValueType,
)


class TestEnums:
    """Tests for domain enum definitions."""

    def test_lifecycle_status_values(self):
        values = {s.value for s in LifecycleStatus}
        assert "active" in values
        assert "discontinued" in values
        assert "obsolete" in values
        assert "unknown" in values

    def test_attribute_domain_values(self):
        values = {d.value for d in AttributeDomain}
        assert "identity" in values
        assert "specification" in values
        assert "physical" in values
        assert "mechanical" in values

    def test_value_type_values(self):
        values = {t.value for t in ValueType}
        assert "string" in values
        assert "number" in values
        assert "measurement" in values

    def test_information_category_values(self):
        values = {c.value for c in InformationCategory}
        assert "identity" in values
        assert "safety" in values
        assert "commercial" in values

    def test_lifecycle_state_values(self):
        values = {s.value for s in LifecycleState}
        assert "discovered" in values
        assert "extracted" in values
        assert "approved" in values

    def test_validation_status_values(self):
        values = {v.value for v in ValidationStatus}
        assert "pending" in values
        assert "auto_validated" in values
        assert "rejected" in values

    def test_conflict_status_values(self):
        values = {c.value for c in ConflictStatus}
        assert "none" in values
        assert "pending_resolution" in values
        assert "resolved" in values

    def test_conflict_type_values(self):
        values = {t.value for t in ConflictType}
        assert "value_mismatch" in values
        assert "unit_mismatch" in values
        assert "source_contradiction" in values

    def test_extraction_method_values(self):
        values = {m.value for m in ExtractionMethod}
        assert "text_extraction" in values
        assert "ocr" in values
        assert "inference" in values

    def test_freshness_status_values(self):
        values = {f.value for f in FreshnessStatus}
        assert "current" in values
        assert "outdated" in values
        assert "unknown" in values

    def test_source_trust_level_values(self):
        values = {t.value for t in SourceTrustLevel}
        assert "manufacturer_official" in values
        assert "authorized_distributor" in values
        assert "unknown" in values

    def test_source_type_values(self):
        values = {t.value for t in SourceType}
        assert "pdf" in values
        assert "csv" in values
        assert "web_page" in values


class TestDomainDataclasses:
    """Tests for domain dataclass instantiation and defaults."""

    def test_source_location_defaults(self):
        loc = SourceLocation()
        assert loc.page is None
        assert loc.section is None
        assert loc.table_id is None
        assert loc.row is None
        assert loc.column is None
        assert loc.text_span is None

    def test_source_location_with_values(self):
        loc = SourceLocation(page=1, section="Table 1", row=3, column="Bore")
        assert loc.page == 1
        assert loc.section == "Table 1"
        assert loc.row == 3
        assert loc.column == "Bore"

    def test_freshness_info_defaults(self):
        info = FreshnessInfo()
        assert info.freshness_status == FreshnessStatus.UNKNOWN
        assert info.source_published_at is None

    def test_source_document_defaults(self):
        doc = SourceDocument()
        assert isinstance(doc.id, UUID)
        assert doc.type == SourceType.PDF
        assert doc.trust_level == SourceTrustLevel.UNKNOWN
        assert doc.extraction_status == "pending"

    def test_source_document_with_values(self):
        doc = SourceDocument(name="test.pdf", type=SourceType.PDF, location="/tmp/test.pdf")
        assert doc.name == "test.pdf"
        assert doc.location == "/tmp/test.pdf"

    def test_candidate_value_defaults(self):
        cv = CandidateValue()
        assert isinstance(cv.id, UUID)
        assert cv.value is None
        assert cv.extraction_method == ExtractionMethod.TEXT_EXTRACTION
        assert cv.extraction_confidence == 0.0

    def test_product_attribute_defaults(self):
        pa = ProductAttribute()
        assert isinstance(pa.id, UUID)
        assert pa.domain == AttributeDomain.SPECIFICATION
        assert pa.value_type == ValueType.STRING
        assert pa.conflict_status == ConflictStatus.NONE
        assert pa.validation_status == ValidationStatus.PENDING
        assert pa.lifecycle_state == LifecycleState.DISCOVERED
        assert pa.requires_review is False

    def test_product_attribute_with_candidates(self):
        cv = CandidateValue(value="30.163 mm", extraction_confidence=0.95)
        pa = ProductAttribute(
            name="bore",
            value="30.163 mm",
            unit="mm",
            candidates=[cv],
        )
        assert len(pa.candidates) == 1
        assert pa.candidates[0].value == "30.163 mm"

    def test_quality_metrics_defaults(self):
        qm = QualityMetrics()
        assert qm.completeness_score == 0.0
        assert qm.accuracy_score == 0.0
        assert qm.consistency_score == 0.0
        assert qm.conflict_count == 0

    def test_product_defaults(self):
        p = Product()
        assert isinstance(p.id, UUID)
        assert p.mpn == ""
        assert p.brand == ""
        assert p.lifecycle_status == LifecycleStatus.UNKNOWN
        assert p.version == 1

    def test_product_with_values(self):
        p = Product(
            mpn="UCF209-28",
            brand="Browning",
            name="UCF209-28 Bearing",
            manufacturer_name="Browning",
        )
        assert p.mpn == "UCF209-28"
        assert p.brand == "Browning"
        assert p.manufacturer_name == "Browning"

    def test_candidate_value_has_unique_ids(self):
        cv1 = CandidateValue()
        cv2 = CandidateValue()
        assert cv1.id != cv2.id

    def test_product_has_unique_ids(self):
        p1 = Product()
        p2 = Product()
        assert p1.id != p2.id
