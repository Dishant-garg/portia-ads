from portia import PlanBuilderV2, StepOutput, Input
from ..schema.content_schemas import ContentPlan, ContentPackage, FactCheckReport

def create_content_planning_system():
    """Create comprehensive content planning system."""
    return (
        PlanBuilderV2("Content Strategy & Planning Pipeline")
        
        .input(name="research_summary", description="Market research results")
        .input(name="content_goals", description="Content marketing goals")
        .input(name="brand_guidelines", description="Brand voice and style guidelines")
        .input(name="publishing_frequency", description="How often to publish", default_value="3x per week")
        
        # Step 1: Analyze Optimal Posting Times
        .invoke_tool_step(
            step_name="research_posting_times",
            tool="search_tool",
            args={
                "search_query": "best times to post content social media blog articles 2024 audience engagement data"
            }
        )
        
        # Step 2: Create Content Calendar
        .llm_step(
            step_name="create_content_calendar",
            task="""
            Create a comprehensive 30-day content calendar based on:
            
            Research insights: {research_summary}
            Content goals: {content_goals}
            Brand guidelines: {brand_guidelines}
            Publishing frequency: {publishing_frequency}
            Optimal timing data: {research_posting_times}
            
            For each day, specify:
            1. Content topic and angle
            2. Content format (blog post, video, podcast, social post)
            3. Target platform(s)
            4. Primary keywords
            5. Target audience segment
            6. Success metrics to track
            7. Cross-promotion opportunities
            8. Optimal posting time
            
            Ensure variety in topics, formats, and audience segments while maintaining consistency with brand voice.
            """,
            inputs=[
                Input("research_summary"),
                Input("content_goals"), 
                Input("brand_guidelines"),
                Input("publishing_frequency"),
                StepOutput("research_posting_times")
            ]
        )
        
        # Step 3: Develop Cross-Platform Strategy
        .llm_step(
            step_name="develop_cross_platform_strategy",
            task="""
            Develop cross-platform content strategy:
            
            Content calendar: {create_content_calendar}
            
            Create strategy for:
            1. Content adaptation across platforms (blog → social → video → podcast)
            2. Cross-promotion timing and messaging
            3. Platform-specific optimization techniques
            4. Repurposing content efficiently
            5. Building content series and themes
            6. Community engagement approach
            """,
            inputs=[StepOutput("create_content_calendar")]
        )
        
        # Step 4: Save Content Plan
        .invoke_tool_step(
            step_name="save_content_plan",
            tool="file_writer_tool",
            args={
                "filename": "content_plans/master_content_plan.json",
                "content": StepOutput("develop_cross_platform_strategy")
            }
        )
        
        .final_output(output_schema=ContentPlan)
        .build()
    )

def create_article_writing_system():
    """Create comprehensive article writing system."""
    return (
        PlanBuilderV2("Article Writing & Optimization Pipeline")
        
        .input(name="topic", description="Article topic")
        .input(name="target_keywords", description="SEO keywords to target")
        .input(name="word_count_target", description="Target word count", default_value=2000)
        .input(name="audience_level", description="beginner/intermediate/advanced", default_value="intermediate")
        .input(name="content_angle", description="Unique angle or approach")
        
        # Step 1: Research Specific Topic
        .invoke_tool_step(
            step_name="research_topic_details",
            tool="search_tool",
            args={
                "query": f"{Input('topic')} comprehensive guide examples case studies {Input('target_keywords')} 2024"
            }
        )
        
        # Step 2: Analyze Top Performing Content
        .invoke_tool_step(
            step_name="analyze_top_content",
            tool="search_tool",
            args={
                "query": f"best {Input('topic')} articles high engagement popular content"
            }
        )
        
        # Step 3: Create Article Outline
        .llm_step(
            step_name="create_article_outline",
            task="""
            Create detailed article outline for: {topic}
            
            Research data: {research_topic_details}
            Top content analysis: {analyze_top_content}
            Target keywords: {target_keywords}
            Word count target: {word_count_target}
            Audience level: {audience_level}
            Content angle: {content_angle}
            
            Create outline with:
            1. Compelling headline (5 variations)
            2. Introduction hook and value proposition
            3. Main sections with subheadings (H2, H3)
            4. Key points for each section
            5. Examples and case studies to include
            6. Internal linking opportunities
            7. Call-to-action suggestions
            8. Meta description
            9. Keyword placement strategy
            """,
            inputs=[
                Input("topic"),
                StepOutput("research_topic_details"),
                StepOutput("analyze_top_content"),
                Input("target_keywords"),
                Input("word_count_target"),
                Input("audience_level"),
                Input("content_angle")
            ]
        )
        
        # Step 4: Write Complete Article
        .llm_step(
            step_name="write_full_article",
            task="""
            Write complete article based on outline: {create_article_outline}
            
            Requirements:
            - Follow the outline structure exactly
            - Write in engaging, conversational tone
            - Include specific examples and actionable tips
            - Naturally incorporate target keywords
            - Use short paragraphs and bullet points for readability
            - Add transition sentences between sections
            - Include compelling introduction and conclusion
            - Target word count: {word_count_target}
            - Audience level: {audience_level}
            
            Format in clean markdown with proper headings.
            """,
            inputs=[
                StepOutput("create_article_outline"),
                Input("word_count_target"),
                Input("audience_level")
            ]
        )
        
        # Step 5: Create Social Media Variants
        .llm_step(
            step_name="create_social_variants",
            task="""
            Create social media variants from article: {write_full_article}
            
            Generate:
            1. Twitter thread (8-10 tweets) with key takeaways
            2. LinkedIn post (professional, value-focused)
            3. Instagram caption with relevant hashtags
            4. Facebook post (engaging, community-focused)  
            5. YouTube video description
            6. Email newsletter snippet
            
            Maintain core message while adapting to platform requirements and audiences.
            """,
            inputs=[StepOutput("write_full_article")]
        )
        
        # Step 6: SEO Optimization Check
        .llm_step(
            step_name="seo_optimization_check",
            task="""
            Analyze article for SEO optimization: {write_full_article}
            
            Target keywords: {target_keywords}
            
            Check and optimize:
            1. Keyword density (1-2% for primary keyword)
            2. Header tag optimization (H1, H2, H3)
            3. Meta description quality
            4. Internal linking opportunities
            5. Image alt text suggestions
            6. URL slug recommendation
            7. Featured snippet optimization
            8. Readability score assessment
            
            Provide specific optimization recommendations.
            """,
            inputs=[
                StepOutput("write_full_article"),
                Input("target_keywords")
            ]
        )
        
        # Step 7: Save Content Package
        .function_step(
            step_name="package_content",
            function=lambda article, social, seo, keywords: {
                "main_article": article,
                "social_variants": social,
                "seo_analysis": seo,
                "target_keywords": keywords,
                "word_count": len(article.split()),
                "created_at": "2025-08-24T04:30:00Z"
            },
            args={
                "article": StepOutput("write_full_article"),
                "social": StepOutput("create_social_variants"),
                "seo": StepOutput("seo_optimization_check"),
                "keywords": Input("target_keywords")
            }
        )
        
        .invoke_tool_step(
            step_name="save_content_package",
            tool="file_writer_tool",
            args={
                "filename": f"content_drafts/{Input('topic')}_package.json",
                "content": StepOutput("package_content")
            }
        )
        
        .final_output(output_schema=ContentPackage)
        .build()
    )

def create_fact_checking_system():
    """Create comprehensive fact-checking system."""
    return (
        PlanBuilderV2("Fact-Checking & Verification Pipeline")
        
        .input(name="content_to_verify", description="Content that needs fact-checking")
        .input(name="verification_level", description="basic/thorough/comprehensive", default_value="thorough")
        
        # Step 1: Extract Claims
        .llm_step(
            step_name="extract_claims",
            task="""
            Extract all factual claims from content that need verification:
            
            Content: {content_to_verify}
            
            For each claim, identify:
            1. Exact claim statement
            2. Claim type (statistic, quote, historical fact, current event, etc.)
            3. Verification priority (critical/important/minor)
            4. Potential verification sources
            
            Focus on claims that could be disputed or need authoritative sources.
            """,
            inputs=[Input("content_to_verify")]
        )
        
        # Step 2: Verify Each Critical Claim
        .invoke_tool_step(
            step_name="verify_critical_claims",
            tool="search_tool",
            args={
                "query": f"verify fact check {StepOutput('extract_claims')} authoritative sources recent data"
            }
        )
        
        # Step 3: Find Academic/Official Sources
        .invoke_tool_step(
            step_name="find_authoritative_sources", 
            tool="search_tool",
            args={
                "query": f"site:edu OR site:gov OR site:org {StepOutput('extract_claims')} official data research"
            }
        )
        
        # Step 4: Extract Source Content
        .single_tool_agent_step(
            step_name="extract_verification_sources",
            tool="extract_tool",
            task="Extract detailed content from the most reliable sources found",
            inputs=[
                StepOutput("verify_critical_claims"),
                StepOutput("find_authoritative_sources")
            ]
        )
        
        # Step 5: Cross-Reference and Verify
        .llm_step(
            step_name="generate_verification_report",
            task="""
            Cross-reference claims with verification sources:
            
            Original claims: {extract_claims}
            General verification: {verify_critical_claims}
            Authoritative sources: {find_authoritative_sources}
            Source content: {extract_verification_sources}
            Verification level: {verification_level}
            
            For each claim provide:
            1. Verification status (verified/partially_verified/disputed/unverifiable)
            2. Confidence level (1-10)
            3. Supporting evidence summary
            4. Source citations (with URLs)
            5. Recommended corrections or clarifications
            6. Alternative phrasings if needed
            
            Prioritize claims marked as critical/important.
            """,
            inputs=[
                StepOutput("extract_claims"),
                StepOutput("verify_critical_claims"),
                StepOutput("find_authoritative_sources"),
                StepOutput("extract_verification_sources"),
                Input("verification_level")
            ]
        )
        
        # Step 6: Create Corrected Version (if needed)
        .if_(
            condition="Any claims need corrections or have low confidence scores",
            args={"verification_report": StepOutput("generate_verification_report")}
        )
        .llm_step(
            step_name="create_corrected_content",
            task="""
            Create corrected version of content based on fact-checking:
            
            Original content: {content_to_verify}
            Verification report: {generate_verification_report}
            
            Make necessary corrections while:
            1. Maintaining original tone and structure
            2. Replacing disputed claims with verified alternatives
            3. Adding proper citations where needed
            4. Flagging areas that still need human review
            """,
            inputs=[
                Input("content_to_verify"),
                StepOutput("generate_verification_report")
            ]
        )
        .endif()
        
        # Step 7: Save Fact-Check Report
        .invoke_tool_step(
            step_name="save_fact_check_report",
            tool="file_writer_tool",
            args={
                "filename": f"fact_check_reports/verification_report_{Input('content_id', 'default')}.json",
                "content": StepOutput("generate_verification_report")
            }
        )
        
        .final_output(output_schema=FactCheckReport)
        .build()
    )
