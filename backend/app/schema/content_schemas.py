from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime
from pydantic import ConfigDict

class WebRagResult(BaseModel):
    url: str | None = None      # match field names / optional values
    title: str | None = None
    snippet: str | None = None
    ...
    model_config = ConfigDict(extra="allow")  # ignore superfluous keys

class ResearchSummary(BaseModel):
    trending_topics: List[str] = Field(..., description="Top 10 trending topics and subtopics")
    competitor_content_gaps: List[str] = Field(..., description="Competitor content gaps and opportunities")
    audience_pain_points: List[str] = Field(..., description="Audience pain points and interests from discussions")
    popular_content_formats: List[str] = Field(..., description="Popular content formats and approaches")
    target_keywords: List[str] = Field(..., description="SEO keywords with high potential")
    recommended_angles: List[str] = Field(..., description="Recommended content angles and approaches")
    seasonal_trends: List[str] = Field(..., description="Seasonal trends and timing opportunities")
    emerging_trends: List[str] = Field(..., description="Emerging trends to watch")
    competitor_insights: Optional[Dict[str, Any]] = Field(default=None, description="Competitor analysis results")
    industry_reports: Optional[List[str]] = Field(default=None, description="Key findings from industry reports")
    video_content_trends: Optional[List[str]] = Field(default=None, description="Insights from video content analysis")
    raw_sources: Optional[Dict[str, Any]] = Field(default=None, description="Raw data sources used in research")

class ContentPlan(BaseModel):
    """Schema for content planning output."""
    content_calendar: List[Dict] = Field(description="30-day content calendar")
    posting_schedule: Dict[str, str] = Field(description="Optimal posting times per platform")
    content_themes: List[str] = Field(description="Monthly content themes")
    cross_promotion_strategy: Dict[str, Any] = Field(description="Cross-platform promotion plan")
    success_metrics: Dict[str, Any] = Field(description="KPIs and success metrics")

class ContentPackage(BaseModel):
    """Schema for content creation output."""
    main_article: str = Field(description="Primary article content")
    social_variants: Dict[str, str] = Field(description="Platform-specific content variants")
    meta_description: str = Field(description="SEO meta description")
    featured_image_suggestions: List[str] = Field(description="Featured image recommendations")
    internal_links: List[str] = Field(description="Internal linking opportunities")
    word_count: int = Field(description="Total word count")

class FactCheckReport(BaseModel):
    """Schema for fact-checking output."""
    claims_verified: int = Field(description="Number of claims checked")
    verification_results: List[Dict] = Field(description="Verification results per claim")
    confidence_score: float = Field(description="Overall confidence score 0-10")
    sources_cited: List[str] = Field(description="Reliable sources found")
    corrections_needed: List[str] = Field(description="Required corrections")
    approval_status: str = Field(description="ready_to_publish/needs_review/requires_changes")

class PodcastPackage(BaseModel):
    """Schema for podcast production output."""
    episode_script: str = Field(description="Complete podcast script")
    show_notes: str = Field(description="Detailed show notes")
    chapter_markers: List[Dict] = Field(description="Chapter markers with timestamps")
    episode_metadata: Dict[str, Any] = Field(description="Episode metadata")
    audio_instructions: str = Field(description="Audio production instructions")
    estimated_duration: str = Field(description="Estimated episode duration")

class VideoPackage(BaseModel):
    """Schema for video production output."""
    video_script: str = Field(description="Complete video script")
    shot_list: List[str] = Field(description="Shot list for the video")
    thumbnail_concepts: List[str] = Field(description="Thumbnail design concepts")
    video_metadata: Dict[str, Any] = Field(description="Video metadata (title, description, tags, etc.)")
    editing_instructions: str = Field(description="Video editing instructions")
    video_url: str = Field(description="URL to the generated video")
    production_details: Dict[str, Any] = Field(description="Additional production details such as topic, platform, estimated time, equipment, and status")

class PublishingResults(BaseModel):
    """Schema for publishing results."""
    platform_results: Dict[str, Dict] = Field(description="Results per platform")
    published_urls: List[str] = Field(description="Published content URLs")
    scheduling_status: Dict[str, str] = Field(description="Scheduling status per platform")
    performance_baseline: Dict[str, Any] = Field(description="Initial performance metrics")
    next_actions: List[str] = Field(description="Recommended next actions")

class FinalContentOutput(BaseModel):
    """Schema for final system output."""
    project_id: str = Field(description="Unique project identifier")
    content_summary: str = Field(description="Summary of all created content")
    deliverables: Dict[str, Any] = Field(description="All content deliverables")
    performance_targets: Dict[str, Any] = Field(description="Performance targets and metrics")
    total_execution_time: str = Field(description="Total production time")
    status: str = Field(description="Project completion status")
