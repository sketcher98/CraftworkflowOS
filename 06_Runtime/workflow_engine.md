# Workflow Engine Specification

Complete client lifecycle modeled as executable workflows with rollback, retries, timeouts, and escalation.

---

## Workflow Definition

A workflow is a directed acyclic graph (DAG) of states with transitions.

```python
@dataclass
class WorkflowDefinition:
    name: str
    version: str
    initial_state: str
    states: Dict[str, WorkflowState]
    transitions: List[WorkflowTransition]
    compensation_map: Dict[str, CompensationAction]  # For rollback
```

---

## Client Lifecycle Workflow

```python
CLIENT_LIFECYCLE_WORKFLOW = WorkflowDefinition(
    name="client_lifecycle",
    version="1.0.0",
    initial_state="LEAD_GENERATION",
    states={
        "LEAD_GENERATION": WorkflowState(
            name="LEAD_GENERATION",
            owner="Marketing.ContentStrategist",
            entry_actions=["create_content_calendar", "launch_campaign"],
            exit_condition="lead.captured",
            timeout_hours=168,  # 1 week
            escalation="Marketing.Director"
        ),
        "QUALIFICATION": WorkflowState(
            name="QUALIFICATION",
            owner="Commercial.LeadIntelligence",
            entry_actions=["score_lead", "assign_tier"],
            exit_condition="lead.qualified",
            timeout_hours=24,
            escalation="Commercial.Director"
        ),
        "DISCOVERY": WorkflowState(
            name="DISCOVERY",
            owner="Commercial.Discovery",
            entry_actions=["schedule_call", "prepare_questions"],
            exit_condition="discovery.complete",
            timeout_hours=72,
            escalation="Commercial.Director"
        ),
        "PROPOSAL": WorkflowState(
            name="PROPOSAL",
            owner="Commercial.Proposal",
            entry_actions=["validate_pricing", "draft_proposal"],
            exit_condition="proposal.sent",
            timeout_hours=24,
            escalation="Commercial.Director"
        ),
        "NEGOTIATION": WorkflowState(
            name="NEGOTIATION",
            owner="Commercial.DealStrategist",
            entry_actions=["track_objections", "prepare_counters"],
            exit_condition="proposal.accepted OR proposal.rejected",
            timeout_hours=168,
            escalation="Commercial.Director"
        ),
        "CLOSED_WON": WorkflowState(
            name="CLOSED_WON",
            owner="Commercial.Pipeline",
            entry_actions=["record_deal", "trigger_onboarding"],
            exit_condition="contract.signed AND deposit.received",
            timeout_hours=72,
            escalation="Finance.Director"
        ),
        "ONBOARDING": WorkflowState(
            name="ONBOARDING",
            owner="Delivery.ClientOnboarding",
            entry_actions=["create_plan", "provision_access", "schedule_kickoff"],
            exit_condition="onboarding.complete",
            timeout_hours=120,  # 5 days
            escalation="Delivery.Director"
        ),
        "EXECUTION": WorkflowState(
            name="EXECUTION",
            owner="Delivery.ProjectManager",
            entry_actions=["create_project_plan", "assign_team"],
            exit_condition="all_milestones.delivered",
            timeout_hours=720,  # 30 days (configurable per tier)
            escalation="Delivery.Director"
        ),
        "QA": WorkflowState(
            name="QA",
            owner="Delivery.QualityEngineer",
            entry_actions=["run_tests", "validate_acceptance"],
            exit_condition="qa.passed",
            timeout_hours=48,
            escalation="Delivery.Director"
        ),
        "CLIENT_SUCCESS": WorkflowState(
            name="CLIENT_SUCCESS",
            owner="Delivery.ClientSuccess",
            entry_actions=["measure_health", "schedule_qbr"],
            exit_condition="health_score >= 80 AND qbr.complete",
            timeout_hours=720,  # Ongoing
            escalation="Delivery.Director"
        ),
        "EXPANSION": WorkflowState(
            name="EXPANSION",
            owner="Delivery.ExpansionReferral",
            entry_actions=["identify_signals", "draft_proposal"],
            exit_condition="expansion.accepted OR expansion.declined",
            timeout_hours=168,
            escalation="Commercial.Director"
        ),
        "FINANCE": WorkflowState(
            name="FINANCE",
            owner="Finance.BillingInvoicing",
            entry_actions=["generate_invoice", "track_payment"],
            exit_condition="payment.received AND revenue.recognized",
            timeout_hours=720,  # Net 30 + buffer
            escalation="Finance.Director"
        ),
        "EXECUTIVE_REVIEW": WorkflowState(
            name="EXECUTIVE_REVIEW",
            owner="COO",
            entry_actions=["compile_dashboard", "review_metrics"],
            exit_condition="review.complete AND decisions.recorded",
            timeout_hours=24,  # Monthly
            escalation="CEO"
        )
    },
    transitions=[
        # Happy path
        WorkflowTransition("LEAD_GENERATION", "QUALIFICATION", trigger="lead.captured"),
        WorkflowTransition("QUALIFICATION", "DISCOVERY", trigger="lead.qualified"),
        WorkflowTransition("DISCOVERY", "PROPOSAL", trigger="discovery.complete"),
        WorkflowTransition("PROPOSAL", "NEGOTIATION", trigger="proposal.sent"),
        WorkflowTransition("NEGOTIATION", "CLOSED_WON", trigger="proposal.accepted"),
        WorkflowTransition("CLOSED_WON", "ONBOARDING", trigger="contract.signed"),
        WorkflowTransition("ONBOARDING", "EXECUTION", trigger="onboarding.complete"),
        WorkflowTransition("EXECUTION", "QA", trigger="milestone.delivered"),
        WorkflowTransition("QA", "CLIENT_SUCCESS", trigger="qa.passed"),
        WorkflowTransition("CLIENT_SUCCESS", "EXPANSION", trigger="health_score.high"),
        WorkflowTransition("EXPANSION", "FINANCE", trigger="expansion.accepted"),
        WorkflowTransition("CLOSED_WON", "FINANCE", trigger="contract.signed"),  # Parallel
        WorkflowTransition("EXECUTION", "FINANCE", trigger="milestone.complete"),  # Parallel
        WorkflowTransition("CLIENT_SUCCESS", "EXECUTIVE_REVIEW", trigger="monthly_cycle"),
        WorkflowTransition("FINANCE", "EXECUTIVE_REVIEW", trigger="monthly_cycle"),
        
        # Rejection paths
        WorkflowTransition("NEGOTIATION", "LEAD_GENERATION", trigger="proposal.rejected"),
        WorkflowTransition("QUALIFICATION", "LEAD_GENERATION", trigger="lead.unqualified"),
        WorkflowTransition("DISCOVERY", "LEAD_GENERATION", trigger="discovery.abandoned"),
        
        # Failure paths
        WorkflowTransition("ONBOARDING", "CLOSED_WON", trigger="onboarding.failed", compensation="refund_deposit"),
        WorkflowTransition("EXECUTION", "ONBOARDING", trigger="execution.blocked", compensation="adjust_scope"),
        WorkflowTransition("QA", "EXECUTION", trigger="qa.failed", compensation="fix_and_retest"),
        WorkflowTransition("FINANCE", "CLIENT_SUCCESS", trigger="payment.failed", compensation="payment_plan"),
    ],
    compensation_map={
        "refund_deposit": CompensationAction(
            action="finance.refund",
            params={"amount": "deposit", "reason": "onboarding_failed"}
        ),
        "adjust_scope": CompensationAction(
            action="delivery.adjust_scope",
            params={"reason": "blocked"}
        ),
        "fix_and_retest": CompensationAction(
            action="delivery.fix_defects",
            params={"retry_qa": True}
        ),
        "payment_plan": CompensationAction(
            action="finance.create_payment_plan",
            params={"max_months": 3}
        )
    }
)
```

---

## State Definitions

```python
@dataclass
class WorkflowState:
    name: str
    owner: str                    # Employee identifier
    entry_actions: List[str]      # Actions to execute on entry
    exit_condition: str           # Boolean expression on events
    timeout_hours: int            # Max time in state
    escalation: str               # Who to escalate to on timeout
    retry_policy: RetryPolicy = field(default_factory=RetryPolicy)
    compensation: Optional[str] = None  # Compensation action name


@dataclass
class WorkflowTransition:
    from_state: str
    to_state: str
    trigger: str                  # Event that triggers transition
    condition: Optional[str] = None  # Additional condition
    compensation: Optional[str] = None  # Compensation action on reverse


@dataclass
class CompensationAction:
    action: str                   # Capability/action to execute
    params: dict                  # Parameters for compensation


@dataclass
class RetryPolicy:
    max_retries: int = 3
    base_delay_seconds: int = 60
    max_delay_seconds: int = 3600
    exponential_base: float = 2.0
    retry_on: List[str] = field(default_factory=lambda: ["timeout", "transient_error"])
```

---

## Workflow Instance

```python
@dataclass
class WorkflowInstance:
    instance_id: str
    definition: WorkflowDefinition
    current_state: str
    correlation_id: str
    created_at: datetime
    updated_at: datetime
    context: dict                 # Runtime context (client_id, deal_id, etc.)
    state_history: List[StateTransition]
    pending_t]
    status: WorkflowStatus        # RUNNING, COMPLETED, FAILED, COMPENSATING, COMPENSATED
    metadata: dict


@dataclass
class StateTransition:
    from_state: str
    to_state: str
    trigger: str
    timestamp: datetime
    success: bool
    compensation_executed: bool = False
```

---

## Workflow Engine

```python
class WorkflowEngine:
    def __init__(self, event_bus: EventBus, capability_router: CapabilityRouter):
        self.event_bus = event_bus
        self.capability_router = capability_router
        self.instances: Dict[str, WorkflowInstance] = {}
        self.definitions: Dict[str, WorkflowDefinition] = {}
        self._running = False
    
    def register_definition(self, definition: WorkflowDefinition):
        self.definitions[definition.name] = definition
    
    def start_workflow(
        self, 
        workflow_name: str, 
        correlation_id: str, 
        context: dict
    ) -> WorkflowInstance:
        definition = self.definitions[workflow_name]
        
        instance = WorkflowInstance(
            instance_id=f"wfi_{uuid.uuid4().hex[:8]}",
            definition=definition,
            current_state=definition.initial_state,
            correlation_id=correlation_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            context=context,
            state_history=[],
            status=WorkflowStatus.RUNNING,
            metadata={}
        )
        
        self.instances[instance.instance_id] = instance
        
        # Execute entry actions for initial state
        self._execute_entry_actions(instance)
        
        # Start timeout monitor
        self._start_timeout_monitor(instance)
        
        # Emit workflow started event
        asyncio.create_task(self.event_bus.emit(Event(
            event_type="workflow.started",
            payload={
                "instance_id": instance.instance_id,
                "workflow": workflow_name,
                "state": instance.current_state,
                "context": context
            },
            source="workflow_engine",
            correlation_id=correlation_id
        )))
        
        return instance
    
    async def on_event(self, event: Event):
        """Handle incoming events that may trigger transitions."""
        correlation_id = event.correlation_id
        instance = self._find_instance_by_correlation(correlation_id)
        
        if not instance:
            return
        
        current_state_def = instance.definition.states[instance.current_state]
        
        # Check if event matches exit condition
        if self._evaluates_exit_condition(current_state_def.exit_condition, event):
            # Find matching transition
            transition = self._find_transition(instance.current_state, event)
            
            if transition:
                await self._execute_transition(instance, transition, event)
            else:
                # No matching transition - might be terminal state
                if instance.current_state in ["EXECUTIVE_REVIEW"]:
                    await self._complete_workflow(instance)
    
    async def _execute_transition(
        self, 
        instance: WorkflowInstance, 
        transition: WorkflowTransition, 
        event: Event
    ):
        # Record transition
        state_transition = StateTransition(
            from_state=instance.current_state,
            to_state=transition.to_state,
            trigger=event.event_type,
            timestamp=datetime.utcnow(),
            success=True
        )
        instance.state_history.append(state_transition)
        
        # Update state
        old_state = instance.current_state
        instance.current_state = transition.to_state
        instance.updated_at = datetime.utcnow()
        
        # Execute compensation if defined (for reverse transitions)
        if transition.compensation:
            await self._execute_compensation(transition.compensation, instance.context)
        
        # Execute entry actions for new state
        new_state_def = instance.definition.states[transition.to_state]
        self._execute_entry_actions(instance)
        
        # Start timeout monitor for new state
        self._start_timeout_monitor(instance)
        
        # Emit transition event
        await self.event_bus.emit(Event(
            event_type="workflow.transitioned",
            payload={
                "instance_id": instance.instance_id,
                "from_state": old_state,
                "to_state": transition.to_state,
                "trigger": event.event_type
            },
            source="workflow_engine",
            correlation_id=instance.correlation_id
        ))
        
        # Check if terminal state
        if transition.to_state in ["EXECUTIVE_REVIEW"]:
            # Not terminal - continues monthly
            pass
    
    def _execute_entry_actions(self, instance: WorkflowInstance):
        state_def = instance.definition.states[instance.current_state]
        
        for action_name in state_def.entry_actions:
            # Parse action: capability.action or direct action
            if "." in action_name:
                capability, action = action_name.split(".", 1)
                # Route through capability router
                asyncio.create_task(self.capability_router.request(
                    capability=capability,
                    objective=f"Execute {action} for workflow {instance.instance_id}",
                    context=instance.context
                ))
            else:
                # Direct workflow engine action
                asyncio.create_task(self._execute_direct_action(action_name, instance))
    
    async def _execute_direct_action(self, action: str, instance: WorkflowInstance):
        # Built-in workflow actions
        if action == "trigger_onboarding":
            await self.start_workflow(
                "client_lifecycle",
                f"{instance.correlation_id}_onboarding",
                {**instance.context, "parent_workflow": instance.instance_id}
            )
        elif action == "compile_dashboard":
            await self.capability_router.request(
                "analysis",
                "Compile executive dashboard",
                instance.context
            )
        # ... other direct actions
    
    async def _execute_compensation(self, compensation_name: str, context: dict):
        compensation = self.definitions["client_lifecycle"].compensation_map.get(compensation_name)
        if compensation:
            await self.capability_router.request(
                capability=compensation.action.split(".")[0],
                objective=f"Execute compensation: {compensation_name}",
                context={**context, "compensation_params": compensation.params}
            )
    
    def _evaluates_exit_condition(self, condition: str, event: Event) -> bool:
        """Evaluate boolean condition against event."""
        # Simple pattern: "event.type" or "event.payload.field == value"
        # Full implementation would use expression evaluator
        if condition.startswith("event."):
            # Extract field path
            field = condition[6:]  # Remove "event."
            return self._get_event_field(event, field) is not None
        return False
    
    def _find_transition(self, from_state: str, event: Event) -> Optional[WorkflowTransition]:
        for transition in self.definitions["client_lifecycle"].transitions:
            if transition.from_state == from_state:
                # Check trigger match
                if self._matches_trigger(transition.trigger, event):
                    # Check additional condition
                    if transition.condition is None or self._evaluates_exit_condition(transition.condition, event):
                        return transition
        return None
    
    def _matches_trigger(self, trigger: str, event: Event) -> bool:
        # Trigger can be event type or event type + condition
        if trigger == event.event_type:
            return True
        if trigger == f"{event.event_type}.*":
            return event.event_type.startswith(trigger[:-1])
        return False
    
    def _start_timeout_monitor(self, instance: WorkflowInstance):
        state_def = instance.definition.states[instance.current_state]
        timeout_seconds = state_def.timeout_hours * 3600
        
        async def timeout_handler():
            await asyncio.sleep(timeout_seconds)
            # Check if still in same state
            current = self.instances.get(instance.instance_id)
            if current and current.current_state == instance.current_state:
                await self._handle_timeout(instance, state_def.escalation)
        
        asyncio.create_task(timeout_handler())
    
    async def _handle_timeout(self, instance: WorkflowInstance, escalation: str):
        """Handle state timeout - escalate and potentially transition."""
        await self.event_bus.emit(Event(
            event_type="workflow.timeout",
            payload={
                "instance_id": instance.instance_id,
                "state": instance.current_state,
                "escalation": escalation,
                "timeout_hours": instance.definition.states[instance.current_state].timeout_hours
            },
            source="workflow_engine",
            correlation_id=instance.correlation_id
        ))
        
        # Escalate to director
        await self.capability_router.request(
            "writing",
            f"ESCALATION: Workflow {instance.instance_id} timed out in state {instance.current_state}. "
            f"Escalating to {escalation}. Context: {instance.context}",
            instance.context
        )
    
    def _find_instance_by_correlation(self, correlation_id: str) -> Optional[WorkflowInstance]:
        for instance in self.instances.values():
            if instance.correlation_id == correlation_id:
                return instance
        return None
    
    async def _complete_workflow(self, instance: WorkflowInstance):
        instance.status = WorkflowStatus.COMPLETED
        instance.updated_at = datetime.utcnow()
        
        await self.event_bus.emit(Event(
            event_type="workflow.completed",
            payload={
                "instance_id": instance.instance_id,
                "workflow": instance.definition.name,
                "final_state": instance.current_state,
                "duration_seconds": (instance.updated_at - instance.created_at).total_seconds()
            },
            source="workflow_engine",
            correlation_id=instance.correlation_id
        ))
    
    async def rollback_workflow(self, instance_id: str, to_state: str = None):
        """Rollback workflow to previous state."""
        instance = self.instances.get(instance_id)
        if not instance:
            raise WorkflowNotFoundError(instance_id)
        
        instance.status = WorkflowStatus.COMPENSATING
        
        # Execute compensations in reverse order
        for transition in reversed(instance.state_history):
            if to_state and transition.from_state != to_state:
                continue
            
            # Find compensation for this transition
            definition = instance.definition
            for t in definition.transitions:
                if t.from_state == transition.from_state and t.to_state == transition.to_state:
                    if t.compensation:
                        await self._execute_compensation(t.compensation, instance.context)
                    break
        
        instance.status = WorkflowStatus.COMPENSATED
        
        await self.event_bus.emit(Event(
            event_type="workflow.compensated",
            payload={
                "instance_id": instance_id,
                "rolled_back_to": to_state or "initial"
            },
            source="workflow_engine"
        ))
```

---

## Workflow Persistence

```python
class WorkflowRepository:
    def __init__(self, storage_path: Path):
        self.storage_path = storage_path
        self.storage_path.mkdir(parents=True, exist_ok=True)
    
    def save(self, instance: WorkflowInstance):
        file_path = self.storage_path / f"{instance.instance_id}.json"
        with open(file_path, "w") as f:
            json.dump(instance.to_dict(), f, indent=2, default=str)
    
    def load(self, instance_id: str) -> Optional[WorkflowInstance]:
        file_path = self.storage_path / f"{instance_id}.json"
        if not file_path.exists():
            return None
        with open(file_path, "r") as f:
            data = json.load(f)
        return WorkflowInstance.from_dict(data)
    
    def load_all(self) -> List[WorkflowInstance]:
        instances = []
        for file_path in self.storage_path.glob("*.json"):
            instance = self.load(file_path.stem)
            if instance:
                instances.append(instance)
        return instances
    
    def query(
        self, 
        status: Optional[WorkflowStatus] = None,
        workflow_name: Optional[str] = None,
        correlation_id: Optional[str] = None
    ) -> List[WorkflowInstance]:
        instances = self.load_all()
        if status:
            instances = [i for i in instances if i.status == status]
        if workflow_name:
            instances = [i for i in instances if i.definition.name == workflow_name]
        if correlation_id:
            instances = [i for i in instances if i.correlation_id == correlation_id]
        return instances
```

---

## Integration with Executive Loop

```python
# In executive.py
workflow_engine = WorkflowEngine(EVENT_BUS, capability_router)

def execute(task: str, runtime):
    # Check if task maps to workflow
    if task.lower().startswith("start client lifecycle"):
        client_name = extract_client_name(task)
        instance = workflow_engine.start_workflow(
            "client_lifecycle",
            f"client_{client_name}_{uuid.uuid4().hex[:8]}",
            {"client_name": client_name, "triggered_by": "manual"}
        )
        return f"Started client lifecycle workflow: {instance.instance_id}"
    
    elif task.lower().startswith("workflow status"):
        # Query workflow instances
        instances = workflow_repository.query()
        return format_workflow_status(instances)
    
    # ... existing execute logic
```

---

## Testing Requirements

```python
def test_workflow_engine():
    engine = WorkflowEngine(EVENT_BUS, capability_router)
    engine.register_definition(CLIENT_LIFECYCLE_WORKFLOW)
    
    # Test workflow start
    instance = engine.start_workflow(
        "client_lifecycle",
        "test_correlation_123",
        {"client_name": "Test Agency"}
    )
    assert instance.current_state == "LEAD_GENERATION"
    assert instance.status == WorkflowStatus.RUNNING
    
    # Test transition on event
    asyncio.run(engine.on_event(Event(
        event_type="lead.captured",
        payload={"lead_id": "lead_456"},
        correlation_id="test_correlation_123"
    )))
    
    # Wait for async processing
    asyncio.sleep(0.1)
    
    # Should transition to QUALIFICATION
    updated = engine.instances[instance.instance_id]
    assert updated.current_state == "QUALIFICATION"
    
    # Test rejection path
    asyncio.run(engine.on_event(Event(
        event_type="lead.unqualified",
        payload={"lead_id": "lead_456", "reason": "not_icp"},
        correlation_id="test_correlation_123"
    )))
    
    asyncio.sleep(0.1)
    
    # Should transition back to LEAD_GENERATION
    updated = engine.instances[instance.instance_id]
    assert updated.current_state == "LEAD_GENERATION"
    
    # Test timeout handling (mock time)
    # ...

    # Test compensation/rollback
    # ...
    
    # Test persistence
    workflow_repository.save(instance)
    loaded = workflow_repository.load(instance.instance_id)
    assert loaded.instance_id == instance.instance_id
    assert loaded.current_state == instance.current_state
```