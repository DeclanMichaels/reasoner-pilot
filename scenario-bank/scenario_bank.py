"""
Scenario Bank: core data model and validation.

A Scenario Bank defines a measurement instrument as a JSON structure:
dimensions with poles, scenarios with options and pole values, and
rotation rules for presenting subsets to respondents.
"""

import json


# Required top-level keys
REQUIRED_BANK_KEYS = {"id", "name", "version", "dimensions", "scenarios"}

# Required keys per dimension
REQUIRED_DIMENSION_KEYS = {"id", "name", "pole_a", "pole_b"}

# Required keys per scenario
REQUIRED_SCENARIO_KEYS = {"id", "dimension_id", "stimulus", "judgment", "reasoning"}

# Required keys per question block (judgment or reasoning)
REQUIRED_QUESTION_KEYS = {"question", "options"}

# Required keys per option
REQUIRED_OPTION_KEYS = {"text", "pole"}


def validate_bank(bank: dict) -> list[str]:
    """
    Validate a scenario bank definition.
    Returns a list of error strings. Empty list means valid.
    """
    errors = []

    # Top-level keys
    missing = REQUIRED_BANK_KEYS - set(bank.keys())
    if missing:
        errors.append(f"Missing top-level keys: {missing}")
        return errors  # can't validate further

    # Dimensions
    dim_ids = set()
    if not isinstance(bank["dimensions"], list) or len(bank["dimensions"]) == 0:
        errors.append("'dimensions' must be a non-empty list")
    else:
        for i, dim in enumerate(bank["dimensions"]):
            missing_d = REQUIRED_DIMENSION_KEYS - set(dim.keys())
            if missing_d:
                errors.append(f"Dimension [{i}] missing keys: {missing_d}")
            else:
                if dim["id"] in dim_ids:
                    errors.append(f"Duplicate dimension id: '{dim['id']}'")
                dim_ids.add(dim["id"])

    # Scenarios
    scenario_ids = set()
    dim_scenario_counts = {d: 0 for d in dim_ids}
    if not isinstance(bank["scenarios"], list) or len(bank["scenarios"]) == 0:
        errors.append("'scenarios' must be a non-empty list")
    else:
        for i, sc in enumerate(bank["scenarios"]):
            missing_s = REQUIRED_SCENARIO_KEYS - set(sc.keys())
            if missing_s:
                errors.append(f"Scenario [{i}] missing keys: {missing_s}")
                continue

            if sc["id"] in scenario_ids:
                errors.append(f"Duplicate scenario id: '{sc['id']}'")
            scenario_ids.add(sc["id"])

            if sc["dimension_id"] not in dim_ids:
                errors.append(
                    f"Scenario '{sc['id']}' references unknown dimension: '{sc['dimension_id']}'"
                )
            else:
                dim_scenario_counts[sc["dimension_id"]] += 1

            # Validate judgment and reasoning blocks
            for block_name in ("judgment", "reasoning"):
                block = sc.get(block_name)
                if not isinstance(block, dict):
                    errors.append(f"Scenario '{sc['id']}' {block_name} must be a dict")
                    continue
                missing_q = REQUIRED_QUESTION_KEYS - set(block.keys())
                if missing_q:
                    errors.append(
                        f"Scenario '{sc['id']}' {block_name} missing keys: {missing_q}"
                    )
                    continue
                if not isinstance(block["options"], list) or len(block["options"]) < 2:
                    errors.append(
                        f"Scenario '{sc['id']}' {block_name} must have at least 2 options"
                    )
                    continue
                for j, opt in enumerate(block["options"]):
                    missing_o = REQUIRED_OPTION_KEYS - set(opt.keys())
                    if missing_o:
                        errors.append(
                            f"Scenario '{sc['id']}' {block_name} option [{j}] missing keys: {missing_o}"
                        )
                    elif not isinstance(opt["pole"], (int, float)):
                        errors.append(
                            f"Scenario '{sc['id']}' {block_name} option [{j}] pole must be numeric"
                        )

    # Every dimension must have at least one scenario
    for dim_id, count in dim_scenario_counts.items():
        if count == 0:
            errors.append(f"Dimension '{dim_id}' has no scenarios")

    # All dimensions must have equal scenario counts
    counts = list(dim_scenario_counts.values())
    if counts and len(set(counts)) > 1:
        detail = ', '.join(f"'{d}': {c}" for d, c in dim_scenario_counts.items())
        errors.append(f"All dimensions must have equal scenario counts. Found: {detail}")

    return errors


def load_bank(path: str) -> dict:
    """Load and validate a scenario bank from a JSON file."""
    with open(path, "r") as f:
        bank = json.load(f)
    errors = validate_bank(bank)
    if errors:
        raise ValueError(f"Invalid scenario bank: {'; '.join(errors)}")
    return bank


def save_bank(bank: dict, path: str) -> None:
    """Validate and save a scenario bank to a JSON file."""
    errors = validate_bank(bank)
    if errors:
        raise ValueError(f"Invalid scenario bank: {'; '.join(errors)}")
    with open(path, "w") as f:
        json.dump(bank, f, indent=2)


def get_scenarios_by_dimension(bank: dict) -> dict[str, list[dict]]:
    """Group scenarios by their dimension_id."""
    by_dim = {}
    for sc in bank["scenarios"]:
        dim_id = sc["dimension_id"]
        if dim_id not in by_dim:
            by_dim[dim_id] = []
        by_dim[dim_id].append(sc)
    return by_dim


def build_cycle(bank: dict) -> list[dict]:
    """
    Build the deterministic scenario cycle from a bank.

    Interleaves scenarios across dimensions in round-robin order:
    dim1_sc1, dim2_sc1, dim3_sc1, ..., dim1_sc2, dim2_sc2, ...

    Scenarios are grouped by dimension first, so the order they
    appear in the bank JSON does not affect the cycle structure.
    Any sliding window of num_dimensions consecutive positions
    is guaranteed to contain exactly one scenario per dimension.

    Requires all dimensions to have equal scenario counts.
    """
    by_dim = get_scenarios_by_dimension(bank)
    dim_ids = [d["id"] for d in bank["dimensions"]]
    scenarios_per_dim = len(by_dim[dim_ids[0]])
    cycle = []
    for round_idx in range(scenarios_per_dim):
        for dim_id in dim_ids:
            cycle.append(by_dim[dim_id][round_idx])
    return cycle


def generate_rotation(bank: dict, respondent_index: int = 0) -> list[dict]:
    """
    Generate a scenario rotation for one respondent.

    Uses a sequential sliding window over the bank's dimension cycle.
    Each respondent sees one scenario per dimension. Consecutive
    respondent indices rotate through different scenarios and
    dimension orderings.

    Args:
        bank: A validated scenario bank.
        respondent_index: Zero-based respondent number.

    Returns:
        List of scenario dicts in presentation order.
    """
    cycle = build_cycle(bank)
    num_dims = len(bank["dimensions"])
    total = len(cycle)
    start = respondent_index % total
    return [cycle[(start + i) % total] for i in range(num_dims)]


def normalize_weights(values: list[float]) -> list[float]:
    """Normalize a list of values to sum to 1.0. Returns zeros if sum is 0."""
    total = sum(values)
    if total == 0:
        return [0.0] * len(values)
    return [v / total for v in values]


def compute_dimensional_score(
    responses: list[dict],
    bank: dict,
    judgment_weight: float = 0.6,
    reasoning_weight: float = 0.4
) -> list[dict]:
    """
    Compute dimensional scores from a set of responses.

    Each response must have:
        scenario_id: str
        judgment_weights: list[float] (normalized)
        reasoning_weights: list[float] (normalized)

    Returns a list of score dicts, one per dimension.
    """
    scenario_lookup = {sc["id"]: sc for sc in bank["scenarios"]}
    scores = []

    for dim in bank["dimensions"]:
        j_weighted_pole = 0.0
        j_total_weight = 0.0
        r_weighted_pole = 0.0
        r_total_weight = 0.0

        for resp in responses:
            sc = scenario_lookup.get(resp["scenario_id"])
            if not sc or sc["dimension_id"] != dim["id"]:
                continue

            j_weights = resp.get("judgment_weights", [])
            for k, opt in enumerate(sc["judgment"]["options"]):
                if k < len(j_weights) and j_weights[k] > 0:
                    j_weighted_pole += opt["pole"] * j_weights[k]
                    j_total_weight += j_weights[k]

            r_weights = resp.get("reasoning_weights", [])
            for k, opt in enumerate(sc["reasoning"]["options"]):
                if k < len(r_weights) and r_weights[k] > 0:
                    r_weighted_pole += opt["pole"] * r_weights[k]
                    r_total_weight += r_weights[k]

        j_score = j_weighted_pole / j_total_weight if j_total_weight > 0 else 0.0
        r_score = r_weighted_pole / r_total_weight if r_total_weight > 0 else 0.0

        # When one signal is missing (zero total weight), use the other at full
        # weight rather than deflating toward zero.
        if j_total_weight > 0 and r_total_weight > 0:
            combined = j_score * judgment_weight + r_score * reasoning_weight
        elif j_total_weight > 0:
            combined = j_score
        elif r_total_weight > 0:
            combined = r_score
        else:
            combined = 0.0

        scores.append({
            "dimension_id": dim["id"],
            "name": dim["name"],
            "pole_a": dim["pole_a"],
            "pole_b": dim["pole_b"],
            "j_score": round(j_score, 4),
            "r_score": round(r_score, 4),
            "combined": round(combined, 4),
        })

    return scores
