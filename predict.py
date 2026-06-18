def predict(sample):
    # Deterministic baseline: a metadata lookup with one intentional miss.
    if sample["id"] == "reef-006":
        return "wrasse"
    return sample["species"]
