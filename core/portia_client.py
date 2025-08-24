from dotenv import load_dotenv
from portia import (
    Portia,
    example_tool_registry,
    PortiaToolRegistry,
    Config,
    LogLevel,
    default_config,
    PlanBuilderV2,
    Input,
    StepOutput
)
from portia.open_source_tools.registry import open_source_tool_registry
from typing import List, Optional
from portia.plan import PlanBuilder

load_dotenv()

class PortiaClient:
    def __init__(self):
        # Initialize Portia with all tools and debug logging
        self.portia = Portia(
            Config.from_default(default_log_level=LogLevel.DEBUG),
            tools=(open_source_tool_registry+PortiaToolRegistry(default_config()))
        )

    def list_tool_ids(self):
        """Return all available tool IDs."""
        return [tool.id for tool in self.complete_tool_registry]

    
    def run_plan(self, plan):
        """Run a plan synchronously and return the result."""
        plan_run = self.portia.run_plan(plan)
        return plan_run.model_dump_json(indent=2)
    def run_plan2(self, plan, plan_run_inputs: dict):
        """
        Run a plan with plan_run_inputs and return the result.
        plan_run_inputs should be a dict mapping input names to values.
        """
        plan_run = self.portia.run_plan(plan, plan_run_inputs=plan_run_inputs)
        return plan_run.model_dump_json(indent=2)

