from typing import List, Optional
from pydantic import BaseModel, Field, confloat


class WatchListing(BaseModel):
    title: str = Field(description="Listing title with brand and model")
    price_usd: Optional[float] = Field(description="Price in USD", default=None)
    shipping_price_usd: Optional[float] = Field(description="Shipping cost in USD", default=None)
    total_cost_usd: Optional[float] = Field(description="Price + shipping", default=None)
    condition: str = Field(description="Watch condition: New, Used, Pre-owned, etc.")
    seller: str = Field(description="Seller/dealer name")
    source_site: str = Field(description="Source marketplace: chrono24 or jomashop")
    url: str = Field(description="Direct URL to listing")
    location: Optional[str] = Field(description="Seller location", default=None)


class WatchSearchResults(BaseModel):
    query: str = Field(description="Search query used")
    source_site: str = Field(description="Marketplace searched")
    target_zip_code: str = Field(description="Target US zip code for shipping")
    total_new_found: int = Field(description="Total new listings found", default=0)
    total_used_found: int = Field(description="Total used/pre-owned listings found", default=0)
    cheapest_new: List[WatchListing] = Field(description="Cheapest new listings", default_factory=list)
    cheapest_used: List[WatchListing] = Field(description="Cheapest used listings", default_factory=list)


class PriceStats(BaseModel):
    min_price: float = Field(description="Minimum price in USD")
    max_price: float = Field(description="Maximum price in USD")
    median_price: float = Field(description="Median price in USD")
    average_price: float = Field(description="Average price in USD")
    count: int = Field(description="Number of listings")


class ListingRecommendation(BaseModel):
    listing: WatchListing = Field(description="The recommended listing")
    reasoning: str = Field(description="Why this listing is recommended")
    value_score: confloat(ge=0, le=100) = Field(description="Value score 0-100")


class SiteStats(BaseModel):
    site_key: str = Field(description="Site identifier (e.g. chrono24, jomashop)")
    site_name: str = Field(description="Human-readable site name")
    new_stats: Optional[PriceStats] = Field(description="New listing price stats", default=None)
    used_stats: Optional[PriceStats] = Field(description="Used/pre-owned listing price stats", default=None)


class WatchPriceAnalysis(BaseModel):
    watch_query: str = Field(description="Watch model analyzed")
    site_statistics: List[SiteStats] = Field(description="Price statistics per site", default_factory=list)
    best_new_listing: ListingRecommendation = Field(description="Best value new listing across all sites")
    best_used_listing: ListingRecommendation = Field(description="Best value used listing across all sites")
    best_overall: ListingRecommendation = Field(description="Single best deal overall")
    buy_new_vs_used: str = Field(description="Recommendation on new vs used with reasoning")
    cross_site_observations: List[str] = Field(description="Price comparison insights across sellers", default_factory=list)
    price_anomalies: List[str] = Field(description="Unusual pricing notes", default_factory=list)
