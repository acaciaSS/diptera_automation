"""
iNaturalist Diptera Image Downloader
=====================================
Downloads images from iNaturalist for Diptera species of biomedical interest.
Uses the iNaturalist API v1 (no API key required for read-only access).

Taxon IDs are resolved automatically from species names via the API,
so no hardcoded IDs that could be wrong.

Usage:
    python download_inaturalist.py

All images are saved to: ./dataset/<taxon_name>/
"""

import time
import requests
from pathlib import Path

# ─────────────────────────────────────────────
# CONFIGURATION — edit this section as needed
# ─────────────────────────────────────────────

# Diptera taxa of biomedical interest — use exact scientific names
TAXA_NAMES = [
    "Aedes aegypti",        # Yellow fever mosquito
    "Aedes albopictus",     # Tiger mosquito
    "Culex pipiens",        # Common house mosquito
    "Anopheles gambiae",    # African malaria mosquito
    "Phlebotomus papatasi", # Sandfly
    "Culicoides imicola",   # Biting midge
    "Musca domestica",      # House fly
    "Calliphora vicina",    # Blue bottle fly
]

# How many images to download per taxon
IMAGES_PER_TAXON = 5

# Only use research-grade observations (verified ID)
QUALITY_GRADE = "research"

# Output directory (relative to this script)
OUTPUT_DIR = Path("dataset")

# Pause between requests (be polite to the API)
SLEEP_BETWEEN_REQUESTS = 0.5  # seconds

# ─────────────────────────────────────────────
# API HELPERS
# ─────────────────────────────────────────────

API_BASE = "https://api.inaturalist.org/v1"


def resolve_taxon_id(name: str) -> tuple:
    """
    Look up the iNaturalist taxon ID for a scientific name.
    Returns (taxon_id, matched_name) or (None, None) if not found.
    """
    url = f"{API_BASE}/taxa"
    params = {"q": name, "rank": "species,genus", "per_page": 1}
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    results = r.json().get("results", [])
    if not results:
        return None, None
    taxon = results[0]
    return taxon["id"], taxon["name"]


def fetch_observations(taxon_id: int, per_page: int = 100, quality: str = "research") -> list:
    """Fetch observations with photos for a given taxon ID."""
    params = {
        "taxon_id": taxon_id,
        "per_page": per_page,
        "order_by": "votes",
        "photos": "true",
        "photo_license": "any",
    }
    if quality:
        params["quality_grade"] = quality

    url = f"{API_BASE}/observations"
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    return r.json().get("results", [])


def get_photo_url(photo: dict, size: str = "large") -> str:
    """
    Get image URL at desired size.
    Sizes: square (75px), small (240px), medium (500px), large (1024px), original
    """
    url = photo.get("url", "")
    if not url:
        return None
    for suffix in ["square", "small", "medium", "large", "original"]:
        url = url.replace(suffix, size)
    return url


def download_image(url: str, save_path: Path) -> bool:
    """Download a single image."""
    try:
        r = requests.get(url, timeout=30, stream=True)
        r.raise_for_status()
        content_type = r.headers.get("Content-Type", "")
        if "image" not in content_type:
            print(f"    ! Not an image (got {content_type}): {url}")
            return False
        save_path.write_bytes(r.content)
        return True
    except Exception as e:
        print(f"    ! Download error: {e}")
        return False


# ─────────────────────────────────────────────
# MAIN LOGIC
# ─────────────────────────────────────────────

def download_taxon(name: str) -> int:
    """Resolve taxon ID and download images for one species."""

    print(f"\n{'─'*55}")
    print(f"  Resolving: {name}")

    taxon_id, matched_name = resolve_taxon_id(name)
    if taxon_id is None:
        print(f"  ! Could not find '{name}' on iNaturalist. Skipping.")
        return 0

    print(f"  Matched  : {matched_name} (ID: {taxon_id})")

    folder_name = matched_name.replace(" ", "_")
    taxon_dir = OUTPUT_DIR / folder_name
    taxon_dir.mkdir(parents=True, exist_ok=True)
    print(f"  Saving to: {taxon_dir}/")
    print(f"{'─'*55}")

    time.sleep(SLEEP_BETWEEN_REQUESTS)

    observations = fetch_observations(taxon_id, per_page=IMAGES_PER_TAXON, quality=QUALITY_GRADE)
    print(f"  Found {len(observations)} observations")

    downloaded = 0
    skipped = 0

    for obs in observations:
        photos = obs.get("photos", [])
        obs_id = obs.get("id", "unknown")

        for photo in photos[:1]:  # one photo per observation keeps variety
            photo_id = photo.get("id", f"{obs_id}_0")
            filename = taxon_dir / f"{folder_name}_{photo_id}.jpg"

            if filename.exists():
                skipped += 1
                continue

            url = get_photo_url(photo, size="large")
            if not url:
                continue

            success = download_image(url, filename)
            if success:
                downloaded += 1
                print(f"  + [{downloaded:>3}] obs {obs_id} -> {filename.name}")

            time.sleep(SLEEP_BETWEEN_REQUESTS)

    print(f"\n  Done: {downloaded} downloaded, {skipped} already existed.")
    return downloaded


def main():
    print("=" * 55)
    print("  iNaturalist Diptera Dataset Downloader")
    print("=" * 55)
    print(f"  Output folder : {OUTPUT_DIR.resolve()}")
    print(f"  Quality grade : {QUALITY_GRADE or 'all'}")
    print(f"  Images/taxon  : {IMAGES_PER_TAXON}")
    print(f"  Taxa count    : {len(TAXA_NAMES)}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    total = 0
    failed = []

    for name in TAXA_NAMES:
        count = download_taxon(name)
        total += count
        if count == 0:
            failed.append(name)

    print(f"\n{'='*55}")
    print(f"  TOTAL DOWNLOADED : {total} images")
    print(f"  Saved to         : {OUTPUT_DIR.resolve()}")
    if failed:
        print(f"\n  Not found        : {', '.join(failed)}")
        print("  Check spelling or try a genus name instead.")
    print("=" * 55)

if __name__ == "__main__":
    main()