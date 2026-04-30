"""Helper functions for Mikrotik Router."""


# ---------------------------
#   format_attribute
# ---------------------------
def format_attribute(attr):
    res = attr.replace("-", "_")
    res = res.replace(" ", "_")
    res = res.lower()
    return res
