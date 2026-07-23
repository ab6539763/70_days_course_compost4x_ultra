"""Aggregate all 70 day plans."""
from day_definitions.week01 import DAYS_01_TO_07
from day_definitions.week02 import DAYS_08_TO_14
from day_definitions.week03_04 import DAYS_15_TO_24
from day_definitions.week05_07 import DAYS_25_TO_50
from day_definitions.week08_10 import DAYS_51_TO_70

ALL_DAYS = (
    DAYS_01_TO_07
    + DAYS_08_TO_14
    + DAYS_15_TO_24
    + DAYS_25_TO_50
    + DAYS_51_TO_70
)

assert len(ALL_DAYS) == 70, f"Expected 70 days, got {len(ALL_DAYS)}"
