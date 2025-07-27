def predict_ungating(product_info: dict, seller_account=None) -> dict:
    """
    Predicts ungating likelihood for a product.
    If seller_account is provided, checks if already approved.
    Returns dict with 'can_ungate' (bool), 'confidence' (0-1), and 'already_approved' (bool).
    """
    restricted_brands = {"Nike", "Apple", "LEGO"}
    brand = product_info.get("brand", "").lower()
    can_ungate = brand not in {b.lower() for b in restricted_brands}
    confidence = 0.9 if can_ungate else 0.3

    already_approved = False
    if seller_account:
        # Placeholder: Replace with real API call to check approval
        already_approved = seller_account.is_approved_for_brand(brand)
        if already_approved:
            can_ungate = True
            confidence = 1.0

    return {
        "can_ungate": can_ungate,
        "confidence": confidence,
        "already_approved": already_approved
    }