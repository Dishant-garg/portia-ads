from portia import PlanBuilderV2, StepOutput, Input
from ..schema.content_schemas import ResearchSummary, WebRagResult

def create_market_research_plan():
    """Creates comprehensive market research plan using PlanBuilderV2."""
    return (
        PlanBuilderV2("Market Research & Trend Analysis Pipeline")
        
        # Define inputs
        .input(
            name="topic",
            description="Main topic to research"
        )
        .input(
            name="target_audience", 
            description="Target audience demographics and interests"
        )
        .input(
            name="competitor_domains",
            description="List of competitor website domains",
            default_value=[]
        )
        .input(
            name="research_depth",
            description="Research depth level: basic, comprehensive, advanced",
            default_value="comprehensive"
        )
        
        # Step 1: Google Trends Analysis
        .invoke_tool_step(
            step_name="analyze_google_trends",
            tool="search_tool",
            args={
                "search_query": f"{Input('topic')} trends 2024 2025 statistics market analysis data insights"
            }
        )
        
        # # Step 2: Social Media Trend Mining
        # .invoke_tool_step(
        #     step_name="mine_social_trends",
        #     tool="portia:mcp:actors-mcp-server.apify.actor:apify_slash_rag_web_browser",
        #     args={
        #     "query": Input("topic"),
        #     "maxresults": 5  
        # }
        # )
        
        
        .invoke_tool_step(
            step_name="crawl_competitor_sites",
            tool="crawl_tool",
            args={
                "url":"https://medicalfuturist.com",
                "instructions":"Find all blog posts about AI in Healthcare from the last 6 months.",
                "max_depth":2,
                "limit":30,
                "select_paths":["/blog/.*"],
               "allow_external":False
        }
        )
        .invoke_tool_step(
            step_name="extract_competitor_content",
            tool="extract_tool", 
            args={
                "urls": "https://medicalfuturist.com"
            }
        )
        .invoke_tool_step(
            step_name="search_competitor_content",
            tool="search_tool",
            args={
                "search_query": f"best {Input('topic')} content marketing examples case studies 2024"
            }
        )
        
        # Step 4: Industry Reports & Data
        .invoke_tool_step(
            step_name="find_industry_reports",
            tool="search_tool",
            args={
                "search_query": f"{Input('topic')} industry report 2024 statistics market research data whitepaper"
            }
        )
        
        # Step 6: YouTube Content Analysis
        .invoke_tool_step(
            step_name="analyze_youtube_content",
            tool="search_tool",
            args={
                "search_query": f"site:youtube.com {Input('topic')} popular videos high engagement 2024"
            }
        )
        
        # Step 7: Synthesize Research Findings
        .llm_step(
            step_name="synthesize_research",
            task=f"""
            Analyze all research data and create comprehensive market research summary for {Input('topic')}:
            
            Data sources:
            - Google trends: {{analyze_google_trends}}
            - Competitor crawl: {{crawl_competitor_sites}}
            - Competitor analysis: {{extract_competitor_content}}
            - Competitor content: {{search_competitor_content}}
            - Industry reports: {{find_industry_reports}}
            - Video content trends: {{analyze_youtube_content}}
            - Target audience: {Input('target_audience')}
            
            Generate insights on:
            1. Top 10 trending topics and subtopics
            2. Competitor content gaps and opportunities
            3. Audience pain points and interests from discussions
            4. Popular content formats and approaches
            5. SEO keywords with high potential
            6. Recommended content angles and approaches
            7. Seasonal trends and timing opportunities
            8. Emerging trends to watch
            """,
            inputs=[
                StepOutput("analyze_google_trends"),
                StepOutput("crawl_competitor_sites"),
                StepOutput("extract_competitor_content"),
                StepOutput("search_competitor_content"),
                StepOutput("find_industry_reports"),
                StepOutput("analyze_youtube_content"),
                Input("topic"),
                Input("target_audience")
            ]
        )
        
        # Step 8: Save Research Report
        .invoke_tool_step(
            step_name="save_research_report",
            tool="file_writer_tool",
            args={
                "filename": f"research_reports/{Input('topic')}_market_research.json",
                "content": StepOutput("synthesize_research")
            }
        )
        .build()
    )

def create_content_gap_analysis_plan():
    """Analyze content gaps in the market."""
    return (
        PlanBuilderV2("Content Gap Analysis Pipeline")
        
        .input(name="research_data", description="Market research results")
        .input(name="existing_content_urls", description="Our existing content URLs", default_value=[])
        
        # Analyze our existing content
        .if_(
            condition=lambda urls: len(urls) > 0,
            args={"urls": Input("existing_content_urls")}
        )
        .invoke_tool_step(
            step_name="analyze_existing_content",
            tool="extract_tool",
            args={"urls": Input("existing_content_urls")}
        )
        .else_()
        .function_step(
            function=lambda: {"message": "No existing content to analyze"},
            args={}
        )
        .endif()
        
        # Identify gaps using LLM analysis
        .llm_step(
            task="""
            Based on market research and existing content analysis, identify content gaps:
            
            Market research: {research_data}
            Existing content: {analyze_existing_content if existing_content_urls else no_existing_content}
            
            Identify:
            1. Topics competitors cover that we don't
            2. Audience questions not being answered
            3. Content formats underutilized  
            4. Seasonal opportunities missed
            5. Keyword opportunities with low competition
            6. Trending topics we should cover
            """,
            inputs=[Input("research_data"), StepOutput("analyze_existing_content")]
        )
        
        .final_output(output_schema=ResearchSummary)
        .build()
    )
