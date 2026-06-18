def map_shift(old_shift, old_time):
    old_shift = (old_shift or "").strip()
    old_time = (old_time or "").strip()

    if old_shift == "Morning":
        return "Morning"

    if old_shift == "Afternoon":
        return "Afternoon"

    if old_shift == "Evening":
        return "Evening"

    if old_shift == "Night":
        return "Night"

    if old_shift in ["24 Hours", "24Hours"]:
        return "Full"

    if old_shift == "Double":

        if "07:00" in old_time and "03:00" in old_time:
            return "Double Morning"

        if "11:00" in old_time and "07:00" in old_time:
            return "Double Noon"

        return "Double Noon"

    return None