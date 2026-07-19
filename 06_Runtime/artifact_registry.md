# Artifact Registry Specification

Canonical artifact schemas, versioning, validation, and registry operations.

---

## Artifact Schema

Every artifact follows a canonical envelope:

```json
{
  "artifact_id": "art_abc123",
  "artifact_type": "proposal-draft",
  "version": "1.0.0",
  "title": "Proposal for AgencyCo - Goldilocks Tier",
  "content": {...},
  "created_by": "Commercial.Proposal",
  "created_at": "2025-01-19T10:30:00Z",
  "updated_at": "2025-01-19T10:30:00Z",
  "tags": ["commercial", "proposal", "goldilocks"],
  "metadata": {
    "client_id": "client_456",
    "tier": "goldilocks",
    "amount": 9500
  },
  "schema_version": "1.0",
  "checksum": "sha256:abc123..."
}
```

---

## Canonical Artifact Types

### Commercial Artifacts
```
proposal-draft           # Proposal document
outreach-message         # DM/email outreach
research-report          # ICP research, lead intelligence
gap-analysis             # Discovery gap analysis
stakeholder-map          # Decision maker mapping
deal-structure           # Deal terms, pricing, structure
pricing-rationale        # Margin analysis, discount justification
negotiation-plan         # Objection handling, counter-strategies
pipeline-forecast        # Weekly/monthly forecast
win-loss-analysis        # Closed deal postmortem
```

### Marketing Artifacts
```
content-calendar         # Monthly content plan
linkedin-post            # Founder/brand LinkedIn content
twitter-thread           # Twitter/X thread
blog-article             # SEO blog post
newsletter-issue         # Email newsletter
lead-magnet              # PDF guide, checklist, template
landing-page             # Campaign landing page copy
media-pitch              # PR outreach
speaking-proposal        # Conference/event submission
case-study-draft         # Client success story
```

### Sales Enablement Artifacts
```
battlecard               # Competitor comparison
objection-armor          # Objection handling scripts
proof-asset              # Testimonial, metric, logo
proposal-template        # Tier-specific proposal template
pre-call-sequence        # 4-email pre-call nurture
```

### Delivery Artifacts
```
onboarding-plan          # Client onboarding roadmap
access-provisioning      # Tool access, credentials
kickoff-deck             # Kickoff meeting slides
project-plan             # Timeline, milestones, resources
technical-spec           # Architecture, integrations, APIs
test-plan                # QA test cases, acceptance criteria
test-results             # Test execution results
quality-gate-report      # Gate pass/fail with evidence
uat-signoff              # Client acceptance signature
health-report            # Client health scorecard
qbr-deck                 # Quarterly business review
success-plan             # Outcome mapping, milestones
renewal-package          # Renewal proposal, pricing
expansion-proposal       # Upsell/cross-sell proposal
referral-reward          # Referral program fulfillment
case-study               # Published case study
```

### Operations Artifacts
```
sop                      # Standard operating procedure
sop-audit                # SOP compliance audit
automation-spec          # Automation requirements
automation-runbook       # Runbook for automation
tool-evaluation          # Tool assessment
tool-rollout-plan        # Deployment plan
tool-health-report       # Adoption, ROI metrics
communication-rhythm     # Meeting cadence, templates
decision-log             # Decision record
escalation-path          # Escalation routing
planning-cycle           # Quarterly/annual plan
weekly-priorities        # Weekly priorities
monthly-review           # Monthly review notes
```

### Finance Artifacts
```
invoice                  # Client invoice
payment-receipt          # Payment confirmation
aging-report             # AR aging buckets
collection-action        # Dunning letter, call log
revenue-schedule         # Recognition timeline
margin-report            # Package/client margin
cash-forecast            # 13-week cash flow
burn-report              # Monthly burn analysis
unit-economics           # LTV, CAC, payback
board-package            # Monthly/quarterly board deck
tax-filing               # Tax return, supporting docs
```

### Engineering Artifacts
```
adr                      # Architecture decision record
technical-spec           # Module/component spec
api-contract             # OpenAPI/GraphQL schema
code-review              # PR review comments
deployment-manifest      # K8s/Helm/Terraform
runbook                  # Operational runbook
incident-postmortem      # Incident analysis
performance-baseline     # Benchmark results
security-audit           # Security findings
```

### Creative Artifacts
```
brand-system             # Tokens, components, guidelines
design-system            # Component library
ui-spec                  # Interface specification
interaction-spec         # Micro-interaction design
landing-page-design      # Figma design file
social-graphic           # Post, carousel, story
proposal-asset           # Designed proposal PDF
battlecard-design        # Designed battlecard
onboarding-deck          # Welcome deck
qbr-deck-template        # QBR template
case-study-layout        # Case study design
email-template           # Email design
motion-spec              # Animation tokens, patterns
video-asset              # MP4/WebM video
lottie-animation         # Lottie JSON
```

---

## JSON Schemas

### Base Schema (All Artifacts)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["artifact_id", "artifact_type", "version", "title", "content", "created_by", "created_at"],
  "properties": {
    "artifact_id": {"type": "string", "pattern": "^art_[a-z0-9]{8,}$"},
    "artifact_type": {"type": "string", "enum": [...]},
    "version": {"type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$"},
    "title": {"type": "string", "minLength": 1, "maxLength": 200},
    "content": {"type": "object"},
    "created_by": {"type": "string", "pattern": "^[A-Z][a-z]+(\\.[A-Z][a-z]+)*$"},
    "created_at": {"type": "string", "format": "date-time"},
    "updated_at": {"type": "string", "format": "date-time"},
    "tags": {"type": "array", "items": {"type": "string"}},
    "metadata": {"type": "object"},
    "schema_version": {"type": "string", "const": "1.0"},
    "checksum": {"type": "string", "pattern": "^sha256:[a-f0-9]{64}$"}
  }
}
```

### Proposal Draft Schema

```json
{
  "artifact_type": "proposal-draft",
  "content": {
    "type": "object",
    "required": ["client_id", "tier", "amount", "deliverables", "timeline", "guarantee"],
    "properties": {
      "client_id": {"type": "string"},
      "tier": {"type": "string", "enum": ["jumpstart", "goldilocks", "visionary"]},
      "amount": {"type": "number", "minimum": 2500},
      "deliverables": {"type": "array", "items": {"type": "string"}},
      "timeline": {"type": "string"},
      "guarantee": {"type": "string", "enum": ["standard", "enhanced"]},
      "stakeholder_map": {"type": "object"},
      "anticipated_objections": {"type": "array", "items": {"type": "string"}}
    }
  }
}
```

### Research Report Schema

```json
{
  "artifact_type": "research-report",
  "content": {
    "type": "object",
    "required": ["objective", "findings", "recommendations"],
    "properties": {
      "objective": {"type": "string"},
      "findings": {
        "type": "array",
        "items": {
          "type": "object",
          "required": ["company", "industry", "location", "size", "signals"],
          "properties": {
            "company": {"type": "string"},
            "industry": {"type": "string"},
            "location": {"type": "string"},
            "size": {"type": "string"},
            "signals": {"type": "array", "items": {"type": "string"}},
            "linkedin_url": {"type": "string", "format": "uri"}
          }
        }
      },
      "recommendations": {"type": "array", "items": {"type": "string"}}
    }
  }
}
```

---

## Artifact Registry Interface

```python
class ArtifactRegistry:
    def __init__(self, storage_path: Path):
        self.storage_path = storage_path
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.index: Dict[str, ArtifactIndexEntry] = {}
        self.schemas: Dict[str, Dict] = {}
        self._load_schemas()
        self._build_index()
    
    def _load_schemas(self):
        """Load all JSON schemas from registry/schemas/"""
        schema_dir = Path(__file__).parent / "schemas"
        for schema_file in schema_dir.glob("*.json"):
            artifact_type = schema_file.stem
            with open(schema_file) as f:
                self.schemas[artifact_type] = json.load(f)
    
    def register(self, artifact: Artifact) -> ArtifactRegistrationResult:
        """Register new artifact with validation."""
        # 1. Validate against schema
        schema = self.schemas.get(artifact.artifact_type)
        if schema:
            validator = jsonschema.Draft7Validator(schema)
            errors = list(validator.iter_errors(artifact.to_dict()))
            if errors:
                return ArtifactRegistrationResult(
                    success=False,
                    errors=[e.message for e in errors]
                )
        
        # 2. Compute checksum
        artifact.checksum = self._compute_checksum(artifact.content)
        
        # 3. Store artifact
        file_path = self._get_storage_path(artifact)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w") as f:
            json.dump(artifact.to_dict(), f, indent=2, default=str)
        
        # 4. Update index
        self.index[artifact.artifact_id] = ArtifactIndexEntry(
            artifact_id=artifact.artifact_id,
            artifact_type=artifact.artifact_type,
            title=artifact.title,
            created_by=artifact.created_by,
            created_at=artifact.created_at,
            tags=artifact.tags,
            file_path=str(file_path.relative_to(self.storage_path))
        )
        
        return ArtifactRegistrationResult(success=True, artifact_id=artifact.artifact_id)
    
    def get(self, artifact_id: str) -> Optional[Artifact]:
        """Retrieve artifact by ID."""
        entry = self.index.get(artifact_id)
        if not entry:
            return None
        file_path = self.storage_path / entry.file_path
        with open(file_path) as f:
            return Artifact.from_dict(json.load(f))
    
    def query(
        self,
        artifact_type: Optional[str] = None,
        created_by: Optional[str] = None,
        tags: Optional[List[str]] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        text_search: Optional[str] = None
    ) -> List[ArtifactIndexEntry]:
        """Query artifacts with filters."""
        results = list(self.index.values())
        
        if artifact_type:
            results = [r for r in results if r.artifact_type == artifact_type]
        if created_by:
            results = [r for r in results if r.created_by == created_by]
        if tags:
            results = [r for r in results if all(t in r.tags for t in tags)]
        if date_from:
            results = [r for r in results if r.created_at >= date_from]
        if date_to:
            results = [r for r in results if r.created_at <= date_to]
        if text_search:
            results = [r for r in results if text_search.lower() in r.title.lower()]
        
        return sorted(results, key=lambda r: r.created_at, reverse=True)
    
    def get_version_history(self, artifact_id: str) -> List[Artifact]:
        """Get all versions of an artifact."""
        # Artifacts are immutable; versioning is via artifact_id suffix
        base_id = artifact_id.rsplit("_v", 1)[0] if "_v" in artifact_id else artifact_id
        versions = [
            self.get(aid) for aid in self.index 
            if aid.startswith(base_id)
        ]
        return sorted([v for v in versions if v], key=lambda v: v.version)
    
    def validate_artifact(self, artifact: Artifact) -> ValidationResult:
        """Validate artifact against its schema."""
        schema = self.schemas.get(artifact.artifact_type)
        if not schema:
            return ValidationResult(valid=True, warnings=["No schema for artifact type"])
        
        validator = jsonschema.Draft7Validator(schema)
        errors = list(validator.iter_errors(artifact.to_dict()))
        return ValidationResult(
            valid=len(errors) == 0,
            errors=[e.message for e in errors]
        )
    
    def _compute_checksum(self, content: dict) -> str:
        """Compute SHA256 checksum of content."""
        content_str = json.dumps(content, sort_keys=True, default=str)
        return f"sha256:{hashlib.sha256(content_str.encode()).hexdigest()}"
    
    def _get_storage_path(self, artifact: Artifact) -> Path:
        """Generate storage path: {type}/{year}/{month}/{artifact_id}.json"""
        date = artifact.created_at
        return self.storage_path / artifact.artifact_type / f"{date.year}" / f"{date.month:02d}" / f"{artifact.artifact_id}.json"
```

---

## Versioning

Artifacts are **immutable**. Versioning is handled by:
1. Creating new artifact with incremented version in `artifact_id`: `art_abc123_v2`
2. Original artifact remains unchanged
3. `get_version_history()` retrieves all versions

```python
def create_new_version(artifact: Artifact, updates: dict) -> Artifact:
    """Create new version of artifact with updates."""
    # Parse current version
    base_id, version = artifact.artifact_id.rsplit("_v", 1) if "_v" in artifact.artifact_id else (artifact.artifact_id, "1.0.0")
    major, minor, patch = map(int, version.split("."))
    
    # Determine version bump
    if updates.get("major"):
        major += 1; minor = 0; patch = 0
    elif updates.get("minor"):
        minor += 1; patch = 0
    else:
        patch += 1
    
    new_version = f"{major}.{minor}.{patch}"
    new_id = f"{base_id}_v{new_version}"
    
    new_artifact = Artifact(
        artifact_id=new_id,
        artifact_type=artifact.artifact_type,
        version=new_version,
        title=updates.get("title", artifact.title),
        content={**artifact.content, **updates.get("content", {})},
        created_by=artifact.created_by,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        tags=artifact.tags,
        metadata=artifact.metadata
    )
    
    return new_artifact
```

---

## Validation Pipeline

```python
class ValidationPipeline:
    def __init__(self, registry: ArtifactRegistry):
        self.registry = registry
        self.custom_validators: Dict[str, Callable] = {}
    
    def register_validator(self, artifact_type: str, validator: Callable):
        self.custom_validators[artifact_type] = validator
    
    def validate(self, artifact: Artifact) -> ValidationResult:
        # 1. Schema validation
        result = self.registry.validate_artifact(artifact)
        if not result.valid:
            return result
        
        # 2. Custom validation
        custom_validator = self.custom_validators.get(artifact.artifact_type)
        if custom_validator:
            custom_result = custom_validator(artifact)
            result.errors.extend(custom_result.errors)
            result.warnings.extend(custom_result.warnings)
            result.valid = len(result.errors) == 0
        
        return result


# Example custom validators
def validate_proposal_draft(artifact: Artifact) -> ValidationResult:
    errors = []
    content = artifact.content
    
    # Check tier-appropriate pricing
    tier_prices = {"jumpstart": (2500, 4000), "goldilocks": (6000, 12000), "visionary": (15000, 30000)}
    if content.get("tier") in tier_prices:
        min_price, max_price = tier_prices[content["tier"]]
        if not (min_price <= content.get("amount", 0) <= max_price):
            errors.append(f"Amount {content['amount']} outside {content['tier']} range ({min_price}-{max_price})")
    
    # Check deliverables exist
    if not content.get("deliverables"):
        errors.append("Proposal must have at least one deliverable")
    
    return ValidationResult(valid=len(errors) == 0, errors=errors)
```

---

## Storage Layout

```
artifacts/
├── proposal-draft/
│   ├── 2025/
│   │   ├── 01/
│   │   │   ├── art_abc123_v1.0.0.json
│   │   │   └── art_def456_v1.0.0.json
│   │   └── 02/
├── research-report/
│   ├── 2025/
│   │   └── 01/
├── invoice/
│   ├── 2025/
│   │   └── 01/
└── index.json          # Master index (optional, for fast startup)
```

---

## Testing Requirements

```python
def test_artifact_registry():
    registry = ArtifactRegistry(Path("/tmp/test_artifacts"))
    
    # Test registration
    artifact = Artifact(
        artifact_id="art_test001",
        artifact_type="proposal-draft",
        version="1.0.0",
        title="Test Proposal",
        content={
            "client_id": "client_123",
            "tier": "goldilocks",
            "amount": 9500,
            "deliverables": ["Item 1", "Item 2"],
            "timeline": "14 days",
            "guarantee": "standard"
        },
        created_by="Commercial.Proposal",
        created_at=datetime.utcnow()
    )
    
    result = registry.register(artifact)
    assert result.success
    
    # Test retrieval
    retrieved = registry.get("art_test001")
    assert retrieved.artifact_id == "art_test001"
    assert retrieved.content["amount"] == 9500
    
    # Test query
    results = registry.query(artifact_type="proposal-draft")
    assert len(results) == 1
    
    # Test validation failure
    bad_artifact = Artifact(
        artifact_id="art_bad001",
        artifact_type="proposal-draft",
        version="1.0.0",
        title="Bad Proposal",
        content={"client_id": "client_123", "tier": "goldilocks", "amount": 100},  # Too low
        created_by="Commercial.Proposal"
    )
    result = registry.register(bad_artifact)
    assert not result.success
    assert "outside" in result.errors[0]
    
    # Test versioning
    v2 = create_new_version(artifact, {"minor": True})
    assert v2.version == "1.1.0"
    assert v2.artifact_id.endswith("_v1.1.0")
```