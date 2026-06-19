def format_recommendations(assessments):
    recommendations = []

    for a in assessments:
        recommendations.append(
            {
                "name": a["name"],
                "url": a["url"]
            }
        )
    return recommendations