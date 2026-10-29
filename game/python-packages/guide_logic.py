# -*- coding: utf-8 -*-
"""Pure-Python helpers for the Interactive Guide.

Lives in game/python-packages so Ren'Py can import it AND the pytest
suite (devtools/tests/test_guide_logic.py) can exercise it without an
engine.
"""

# ----------------------------------------------------------------------------
# Safe Shinobi MOD System Bootstrap
# ----------------------------------------------------------------------------
try:
    import hos_mod
    hos_mod.install_mod()
except Exception as _mod_err:
    import traceback
    print(f"[HoS-MOD] Bootstrap notice: {_mod_err}")
    traceback.print_exc()

# ----------------------------------------------------------------------------
# Interactive Guide Pure-Python Logic
# ----------------------------------------------------------------------------

# Pixel heights used by estimate_scroll_offset. Tuned to the styles in
# guide_screen.rpy (header paddings, text sizes, vbox spacing). These do
# not need to be exact - the offset is clamped so an over-estimate can
# never push the target row above the viewport top by more than the
# safety margin applied by the caller.
CATEGORY_HEADER_PX = 54
CHAPTER_HEADER_PX = 42
SUBCHAPTER_HEADER_PX = 36
SUBLEVEL_HEADER_PX = 32
GOAL_ROW_PX = 32
SEPARATOR_PX = 3


def _group(metas, attr, none_pos=None):
    """Group metas by attr preserving first-occurrence order.

    Mirrors _guide_build_subgroups in guide_screen.rpy:
    none_pos None = natural order, 'first'/'last' relocate the None group.
    Returns a list of (key, [metas]) pairs.
    """
    order = []
    groups = {}
    for m in metas:
        key = m.get(attr)
        if key not in groups:
            groups[key] = []
            order.append(key)
        groups[key].append(m)
    if None in groups and len(order) > 1 and none_pos:
        order.remove(None)
        if none_pos == "first":
            order.insert(0, None)
        else:
            order.append(None)
    return [(k, groups[k]) for k in order]


def _flat_rows_until(metas, target_id, counts):
    """Count visible flat rows before target_id. Returns True if found."""
    for m in metas:
        if m["id"] == target_id:
            return True
        if m.get("row_visible", True):
            counts["goal_rows"] += 1
    return False


def count_rows_above(goal_metas, target_id):
    """Replicate the post-jump guide layout and count rendered rows that
    sit above the target goal within its own category.

    goal_metas: list of dicts for every goal in the target's category,
    in data order, with keys id, chapter, subchapter, sublevel,
    rank (guide_goal_sort_key value) and row_visible (False when the
    goal is excluded or filtered and renders nothing).

    Assumes the state guide_jump_to_goal creates: only the target's
    chapter/subchapter/sublevel chain is expanded, sibling groups are
    collapsed to their header row.
    """
    counts = {"chapter_headers": 0, "subchapter_headers": 0,
              "sublevel_headers": 0, "goal_rows": 0, "separators": 0}
    metas = sorted(goal_metas, key=lambda m: m.get("rank", 1))

    for ch_name, ch_goals in _group(metas, "chapter", none_pos=None):
        in_here = any(g["id"] == target_id for g in ch_goals)
        if not in_here:
            if ch_name is None:
                counts["goal_rows"] += sum(
                    1 for g in ch_goals if g.get("row_visible", True))
            elif any(g.get("row_visible", True) for g in ch_goals):
                counts["chapter_headers"] += 1
            continue

        if ch_name is None:
            _flat_rows_until(ch_goals, target_id, counts)
            return counts

        counts["chapter_headers"] += 1
        for sub_name, sub_goals in _group(ch_goals, "subchapter", none_pos="last"):
            sub_has_target = any(g["id"] == target_id for g in sub_goals)
            if not sub_has_target:
                if sub_name is None:
                    counts["goal_rows"] += sum(
                        1 for g in sub_goals if g.get("row_visible", True))
                elif any(g.get("row_visible", True) for g in sub_goals):
                    counts["subchapter_headers"] += 1
                counts["separators"] += 1
                continue

            if sub_name is None:
                _flat_rows_until(sub_goals, target_id, counts)
                return counts

            counts["subchapter_headers"] += 1
            for lv_name, lv_goals in _group(sub_goals, "sublevel", none_pos="first"):
                lv_has_target = any(g["id"] == target_id for g in lv_goals)
                if not lv_has_target:
                    if lv_name is None:
                        counts["goal_rows"] += sum(
                            1 for g in lv_goals if g.get("row_visible", True))
                    elif any(g.get("row_visible", True) for g in lv_goals):
                        counts["sublevel_headers"] += 1
                    continue
                if lv_name is not None:
                    counts["sublevel_headers"] += 1
                _flat_rows_until(lv_goals, target_id, counts)
                return counts
            return counts

    return counts


def estimate_scroll_offset(categories_above, goal_metas, target_id):
    """Pixel offset that puts the target goal row near the viewport top."""
    counts = count_rows_above(goal_metas, target_id)
    return (categories_above * CATEGORY_HEADER_PX
            + counts["chapter_headers"] * CHAPTER_HEADER_PX
            + counts["subchapter_headers"] * SUBCHAPTER_HEADER_PX
            + counts["sublevel_headers"] * SUBLEVEL_HEADER_PX
            + counts["goal_rows"] * GOAL_ROW_PX
            + counts["separators"] * SEPARATOR_PX)


def pick_up_next(candidates, limit=3):
    """Rank goal candidates for the Up Next section.

    candidates: iterable of (goal_id, met_count, total_count).
    Closest-to-completion first, ties broken by absolute steps done,
    then by original order (stable). Goals with no conditions are
    skipped - there is no 'next step' to surface for them.
    """
    ranked = [c for c in candidates if c[2] > 0]
    ranked.sort(key=lambda c: (-(float(c[1]) / c[2]), -c[1]))
    return [c[0] for c in ranked[:limit]]


# day_part semantics (from functionsrooms.rpy room routing):
# 1 = morning/day, 2 = evening, 3 = night, 4 = midnight
_TIME_TO_DAY_PARTS = {
    "morning": (1,),
    "day": (1, 2),
    "evening": (2,),
    "night": (3,),
    "midnight": (4,),
}


def time_matches(goal_time, day_part):
    """True when a goal's time_of_day window includes the current day_part."""
    if goal_time is None or goal_time == "any":
        return True
    return day_part in _TIME_TO_DAY_PARTS.get(goal_time, ())


def pick_quest_goal(goal_ids, completed_ids):
    """Pick the guide goal a journal quest should jump to.

    goal_ids: a single id string or an ordered list of ids.
    Returns the first goal not yet completed, falling back to the last
    entry (the chain's finale) when everything is done.
    """
    if isinstance(goal_ids, str):
        return goal_ids
    if not goal_ids:
        return None
    for gid in goal_ids:
        if gid not in completed_ids:
            return gid
    return goal_ids[-1]


def resolve_prereq_candidate(candidate_ids, excluded):
    """Pick a cross-link target from goals sharing a completion flag.

    Prefers the first candidate that is not path-excluded so love-path
    players land on the love variant and vice versa. Falls back to the
    first candidate when every variant is excluded (better a greyed
    target than a dead click).
    """
    for cid in candidate_ids:
        if cid not in excluded:
            return cid
    return candidate_ids[0] if candidate_ids else None
