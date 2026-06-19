def build_search_queries(requirements):
    queries = []
    role = requirements.get(
        "role",
        ""
    )
    skills = requirements.get(
        "skills",
        []
    )

    if role:
        queries.append(role)
    queries.extend(skills)

    queries.append(
        "cognitive ability"
    )

    if role:
        queries.append(
            "communication collaboration"
        )

    if (
        requirements.get(
            "needs_personality"
        )
        or requirements.get(
            "stakeholder_interaction"
        )
    ):
        queries.append(
            "personality behavior"
        )

    queries.append(
        "simulation"
    )

    if (
        requirements.get(
            "stakeholder_interaction"
        )
        or requirements.get(
            "needs_personality"
        )
    ):

        queries.append(
            "leadership"
        )

    return list(
        dict.fromkeys(
            queries
        )
    )