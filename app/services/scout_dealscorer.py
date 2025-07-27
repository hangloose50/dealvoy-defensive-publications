def score_deal(product: dict, profit_threshold: float = 5.0) -> dict:
    """
    Scores a product deal from 1 (worst) to 10 (best) based on profit, sales rank, and reviews.
    Returns a dict with 'score' and 'reason'.
    """
    price = float(product.get("price", 0) or 0)
    cost = float(product.get("cost", 0) or 0)
    profit = price - cost
    sales_rank = int(product.get("sales_rank", 0) or 0)
    reviews = int(product.get("reviews", 0) or 0)
    rating = float(product.get("rating", 0) or 0)

    score = 1
    reasons = []

    # Profit logic
    if profit < profit_threshold:
        reasons.append("Low profit")
    elif profit < profit_threshold * 2:
        score += 2
        reasons.append("Moderate profit")
    else:
        score += 4
        reasons.append("High profit")

    # Sales rank logic (lower is better)
    if sales_rank > 0:
        if sales_rank < 10000:
            score += 3
            reasons.append("Excellent sales rank")
        elif sales_rank < 50000:
            score += 2
            reasons.append("Good sales rank")
        else:
            reasons.append("Poor sales rank")

    # Reviews logic
    if reviews > 100:
        score += 2
        reasons.append("Many reviews")
    elif reviews > 20:
        score += 1
        reasons.append("Some reviews")
    else:
        reasons.append("Few reviews")

    # Rating logic
    if rating >= 4.5:
        score += 1
        reasons.append("High rating")
    elif rating < 3.0:
        reasons.append("Low rating")

    # Clamp score to 1-10
    score = max(1, min(score, 10))

    return {"score": score, "reason": "; ".join(reasons)}