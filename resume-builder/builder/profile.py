"""Matt's constant identity data. Content JSONs may override any key via a
top-level "profile" object, but normally never need to."""

DEFAULT_PROFILE = {
    "full_name": "Matthew Scott Jones",
    "display_name": "Matt Jones",
    "location": "Houston, TX",
    "phone": "(713) 824-6629",
    "phone_plain": "713-824-6629",
    "email": "mscottjones24@gmail.com",
    "linkedin": "linkedin.com/in/mattjoneshtx",
    "website": "matt-jones.org",
    "letterhead_footer": "HOUSTON, TX · REMOTE-READY · MATT-JONES.ORG",
}


def merge_profile(content: dict) -> dict:
    profile = dict(DEFAULT_PROFILE)
    profile.update(content.get("profile", {}))
    return profile
