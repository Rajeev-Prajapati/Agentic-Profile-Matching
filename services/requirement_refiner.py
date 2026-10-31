
from copy import deepcopy


def update_requirements(
    current: dict,
    changes: dict
) -> dict:

    updated = deepcopy(current)

    must = updated.setdefault("must_have", [])
    nice = updated.setdefault("nice_to_have", [])

    def remove_skills(target, skills):
        to_remove = {s.casefold() for s in skills}
        target[:] = [
            s for s in target
            if s.casefold() not in to_remove
        ]

    remove_skills(
        must,
        changes.get("remove_must_have", [])
    )
    remove_skills(
        nice,
        changes.get("remove_nice_to_have", [])
    )

    for skill in changes.get("add_must_have", []):
        remove_skills(nice, [skill])

        if skill.casefold() not in {
            s.casefold() for s in must
        }:
            must.append(skill)

    for skill in changes.get("add_nice_to_have", []):
        remove_skills(must, [skill])

        if skill.casefold() not in {
            s.casefold() for s in nice
        }:
            nice.append(skill)

    if changes.get("min_experience") is not None:
        years = changes["min_experience"]

        if years < 0:
            raise ValueError(
                "Experience cannot be negative"
            )

        updated["min_experience"] = years

    return updated
