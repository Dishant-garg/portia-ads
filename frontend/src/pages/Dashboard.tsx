import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";
import { 
  Search, 
  Edit3, 
  CheckCircle, 
  Globe, 
  BarChart3, 
  Calendar,
  Play,
  Pause,
  Settings,
  Download,
  Loader2,
  Video,
  Mic,
  ExternalLink
} from "lucide-react";
import ResearchConfigForm from "@/components/ResearchConfigForm";
import { useToast } from "@/hooks/use-toast";
import { useState } from "react";

const Dashboard = () => {
  const { toast } = useToast();
  const [isResearching, setIsResearching] = useState(false);
  const [isContentPlanning, setIsContentPlanning] = useState(false);
  const [isVideoGenerating, setIsVideoGenerating] = useState(false);
  const [isPodcastGenerating, setIsPodcastGenerating] = useState(false);
  const [researchReports, setResearchReports] = useState<any>(null);
  const [contentPlan, setContentPlan] = useState<any>(null);
  const [videoGenerated, setVideoGenerated] = useState(false);
  const [podcastGenerated, setPodcastGenerated] = useState(false);
  
  const handleResearchConfig = async (data: {
    topic: string;
    target_audience: string;
    competitor_domains: string[];
    research_depth: "basic" | "standard" | "comprehensive";
  }) => {
    setIsResearching(true);
    
    try {
      toast({
        title: "Research Started",
        description: `Starting research on "${data.topic}" for ${data.target_audience}`,
      });

      const response = await fetch('http://localhost:5000/api/market-research', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error('Failed to start research');
      }

      const result = await response.json();
      setResearchReports(result.research_reports);
      
      toast({
        title: "Research Completed",
        description: "Market research completed. Starting content planning...",
      });
      
      console.log("Research Result:", result);
      
      // Automatically start content planning after research completion
      await startContentPlanning();
      
    } catch (error) {
      console.error("Research failed:", error);
      toast({
        title: "Research Failed",
        description: "Failed to complete market research. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsResearching(false);
    }
  };

  const startContentPlanning = async () => {
    setIsContentPlanning(true);
    
    try {
      toast({
        title: "Content Planning Started",
        description: "Creating content strategy based on research findings...",
      });

      const response = await fetch('http://localhost:5000/api/content-planning', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content_goals: "Establish thought leadership in AI healthcare, drive engagement from healthcare professionals",
          brand_guidelines: "Professional yet approachable tone, evidence-based content",
          publishing_frequency: "3x per week"
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to start content planning');
      }

      const result = await response.json();
      setContentPlan(result);
      
      toast({
        title: "Content Planning Completed",
        description: "Content strategy created. Starting video and podcast generation...",
      });
      
      console.log("Content Planning Result:", result);
      
      // Automatically start video and podcast generation after content planning
      await startVideoGeneration();
      await startPodcastGeneration();
      
    } catch (error) {
      console.error("Content planning failed:", error);
      toast({
        title: "Content Planning Failed",
        description: "Failed to create content plan. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsContentPlanning(false);
    }
  };

  const startVideoGeneration = async () => {
    setIsVideoGenerating(true);
    
    try {
      toast({
        title: "Video Generation Started",
        description: "Creating video content using AI...",
      });

      // Simulate video generation delay
      await new Promise(resolve => setTimeout(resolve, 3000));
      
      setVideoGenerated(true);
      
      toast({
        title: "Video Generation Completed",
        description: "Video has been generated successfully.",
      });
      
    } catch (error) {
      console.error("Video generation failed:", error);
      toast({
        title: "Video Generation Failed",
        description: "Failed to generate video. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsVideoGenerating(false);
    }
  };

  const startPodcastGeneration = async () => {
    setIsPodcastGenerating(true);
    
    try {
      toast({
        title: "Podcast Generation Started",
        description: "Creating podcast episode...",
      });

      // Simulate podcast generation delay
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      setPodcastGenerated(true);
      
      toast({
        title: "Podcast Generation Completed",
        description: "Podcast episode is ready to play.",
      });
      
    } catch (error) {
      console.error("Podcast generation failed:", error);
      toast({
        title: "Podcast Generation Failed",
        description: "Failed to generate podcast. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsPodcastGenerating(false);
    }
  };

  const downloadReport = (filename: string, content: any) => {
    const dataStr = typeof content === 'string' ? content : JSON.stringify(content, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const pipelineSteps = [
    { 
      name: "Research Agent", 
      status: isResearching ? "in-progress" : researchReports ? "completed" : "pending", 
      progress: isResearching ? 50 : researchReports ? 100 : 0 
    },
    { 
      name: "Content Planner", 
      status: isContentPlanning ? "in-progress" : contentPlan ? "completed" : researchReports ? "pending" : "pending", 
      progress: isContentPlanning ? 50 : contentPlan ? 100 : 0 
    },
    { 
      name: "Video Generation", 
      status: isVideoGenerating ? "in-progress" : videoGenerated ? "completed" : contentPlan ? "pending" : "pending", 
      progress: isVideoGenerating ? 50 : videoGenerated ? 100 : 0 
    },
    { 
      name: "Podcast Generation", 
      status: isPodcastGenerating ? "in-progress" : podcastGenerated ? "completed" : contentPlan ? "pending" : "pending", 
      progress: isPodcastGenerating ? 50 : podcastGenerated ? 100 : 0 
    },
  ];

  const recentContent = [
    { title: "Q1 Marketing Trends Analysis", type: "Blog Post", status: "Published", date: "2 hours ago" },
    { title: "AI in Content Creation Podcast", type: "Podcast", status: "In Review", date: "5 hours ago" },
    { title: "Social Media Strategy Guide", type: "Guide", status: "Draft", date: "1 day ago" },
  ];

  return (
    <div className="min-h-screen bg-gradient-hero pt-20">
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2">Content Pipeline Dashboard</h1>
          <p className="text-foreground/70">Manage your AI-powered content production workflow</p>
        </div>

        {/* Research Configuration - Top Priority */}
        <div className="mb-8">
          <Card className="p-8 bg-gradient-to-r from-primary/10 to-secondary/10 backdrop-blur-sm border-primary/20 shadow-xl">
            <div className="flex items-center gap-3 mb-6">
              <div className="p-2 rounded-full bg-primary/20">
                <Search className="w-6 h-6 text-primary" />
              </div>
              <div>
                <h2 className="text-2xl font-semibold">Start Your Research</h2>
                <p className="text-foreground/70 text-sm">Step 1: Configure research parameters</p>
              </div>
            </div>
            <p className="text-foreground/80 mb-6 text-lg">
              Begin by configuring your research topic and target audience. Our AI agents will analyze the market, competitors, and create comprehensive content tailored to your needs.
            </p>
            <div className="max-w-md">
              <ResearchConfigForm onSubmit={handleResearchConfig} />
              {isResearching && (
                <div className="mt-4 p-4 bg-primary/10 rounded-lg border border-primary/20">
                  <div className="flex items-center gap-2">
                    <Loader2 className="w-4 h-4 animate-spin text-primary" />
                    <span className="text-sm font-medium">Research in progress...</span>
                  </div>
                </div>
              )}
            </div>
          </Card>
        </div>

        {/* Research Reports Download Section */}
        {researchReports && (
          <div className="mb-8">
            <Card className="p-6 bg-card/50 backdrop-blur-sm border-border/50">
              <div className="flex items-center gap-3 mb-4">
                <Download className="w-5 h-5 text-primary" />
                <h3 className="text-xl font-semibold">Research Reports</h3>
                <Badge variant="default" className="text-xs">
                  Ready
                </Badge>
              </div>
              <p className="text-foreground/70 mb-4">
                Your market research has been completed. Download the reports below:
              </p>
              <div className="grid gap-3">
                {Object.entries(researchReports).map(([filename, content]) => (
                  <div key={filename} className="flex items-center justify-between p-3 bg-background/30 rounded-lg border border-border/30">
                    <div>
                      <h4 className="font-medium">{filename}</h4>
                      <p className="text-sm text-foreground/70">
                        {filename.includes('.json') ? 'Market data and analysis' : 'Research summary'}
                      </p>
                    </div>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => downloadReport(filename, content)}
                    >
                      <Download className="w-4 h-4 mr-2" />
                      Download
                    </Button>
                  </div>
                ))}
              </div>
            </Card>
          </div>
        )}

        {/* Content Planning Section */}
        {isContentPlanning && (
          <div className="mb-8">
            <Card className="p-6 bg-card/50 backdrop-blur-sm border-border/50">
              <div className="flex items-center gap-3 mb-4">
                <Loader2 className="w-5 h-5 animate-spin text-primary" />
                <h3 className="text-xl font-semibold">Content Planning</h3>
                <Badge variant="secondary" className="text-xs">
                  In Progress
                </Badge>
              </div>
              <p className="text-foreground/70">
                Creating content strategy based on research findings...
              </p>
            </Card>
          </div>
        )}

        {/* Content Plan Results */}
        {contentPlan && (
          <div className="mb-8">
            <Card className="p-6 bg-card/50 backdrop-blur-sm border-border/50">
              <div className="flex items-center gap-3 mb-4">
                <Calendar className="w-5 h-5 text-primary" />
                <h3 className="text-xl font-semibold">Content Plans</h3>
                <Badge variant="default" className="text-xs">
                  Ready
                </Badge>
              </div>
              <p className="text-foreground/70 mb-4">
                Your content planning has been completed. View key details below and download the complete plan:
              </p>
              
              {/* Key Summary Information */}
              <div className="grid gap-3 mb-6">
                {/* Publishing Frequency */}
                {contentPlan.plan_run_inputs?.publishing_frequency && (
                  <div className="p-3 bg-background/30 rounded-lg border border-border/30">
                    <h4 className="font-medium mb-2">Publishing Frequency</h4>
                    <p className="text-sm text-foreground/70">
                      {contentPlan.plan_run_inputs.publishing_frequency.value}
                    </p>
                  </div>
                )}

                {/* Brand Guidelines */}
                {contentPlan.plan_run_inputs?.brand_guidelines && (
                  <div className="p-3 bg-background/30 rounded-lg border border-border/30">
                    <h4 className="font-medium mb-2">Brand Guidelines</h4>
                    <p className="text-sm text-foreground/70">
                      {contentPlan.plan_run_inputs.brand_guidelines.value}
                    </p>
                  </div>
                )}

                {/* Content Goals */}
                {contentPlan.plan_run_inputs?.content_goals && (
                  <div className="p-3 bg-background/30 rounded-lg border border-border/30">
                    <h4 className="font-medium mb-2">Content Goals</h4>
                    <p className="text-sm text-foreground/70">
                      {contentPlan.plan_run_inputs.content_goals.value}
                    </p>
                  </div>
                )}

                {/* Plan Status */}
                {contentPlan.state && (
                  <div className="p-3 bg-background/30 rounded-lg border border-border/30">
                    <h4 className="font-medium mb-2">Plan Status</h4>
                    <div className="flex items-center gap-2">
                      <Badge variant={contentPlan.state === "COMPLETE" ? "default" : "secondary"}>
                        {contentPlan.state}
                      </Badge>
                      {contentPlan.plan_id && (
                        <span className="text-xs text-foreground/50">
                          ID: {contentPlan.plan_id.slice(-8)}
                        </span>
                      )}
                    </div>
                  </div>
                )}
              </div>

              {/* Download Complete Plan */}
              <div className="border-t border-border/30 pt-4">
                <h4 className="font-medium mb-3">Complete Content Plan</h4>
                <div className="p-3 bg-background/30 rounded-lg border border-border/30">
                  <div className="flex items-center justify-between">
                    <div>
                      <h5 className="font-medium">Full Content Plan Data</h5>
                      <p className="text-sm text-foreground/70">
                        Complete plan execution result, research summary, outputs, and detailed content plans
                      </p>
                    </div>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => downloadReport('complete_content_plan.json', contentPlan)}
                    >
                      <Download className="w-4 h-4 mr-2" />
                      Download
                    </Button>
                  </div>
                </div>
              </div>

              {/* Content Plans Downloads (if available in new format) */}
              {contentPlan.content_plans && (
                <div className="mt-4">
                  <h4 className="font-medium mb-3">Individual Content Plans</h4>
                  <div className="grid gap-3">
                    {Object.entries(contentPlan.content_plans).map(([filename, content]) => (
                      <div key={filename} className="flex items-center justify-between p-3 bg-background/30 rounded-lg border border-border/30">
                        <div>
                          <h5 className="font-medium">{filename}</h5>
                          <p className="text-sm text-foreground/70">
                            {filename.includes('.json') ? 'Content strategy data' : 
                             filename.includes('.md') ? 'Content plan document' : 
                             'Content plan file'}
                          </p>
                        </div>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => downloadReport(filename, content)}
                        >
                          <Download className="w-4 h-4 mr-2" />
                          Download
                        </Button>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Legacy content goals display for backward compatibility */}
              {!contentPlan.plan_run_inputs && !contentPlan.content_plans && (
                <div className="grid gap-3">
                  <div className="p-3 bg-background/30 rounded-lg border border-border/30">
                    <h4 className="font-medium mb-2">Content Goals</h4>
                    <p className="text-sm text-foreground/70">
                      Establish thought leadership in AI healthcare, drive engagement from healthcare professionals
                    </p>
                  </div>
                  <div className="p-3 bg-background/30 rounded-lg border border-border/30">
                    <h4 className="font-medium mb-2">Brand Guidelines</h4>
                    <p className="text-sm text-foreground/70">
                      Professional yet approachable tone, evidence-based content
                    </p>
                  </div>
                  <div className="p-3 bg-background/30 rounded-lg border border-border/30">
                    <h4 className="font-medium mb-2">Publishing Frequency</h4>
                    <p className="text-sm text-foreground/70">
                      3x per week
                    </p>
                  </div>
                  <div className="p-3 bg-background/30 rounded-lg border border-border/30">
                    <div className="flex items-center justify-between">
                      <div>
                        <h4 className="font-medium">Content Calendar</h4>
                        <p className="text-sm text-foreground/70">
                          Detailed content schedule and topics
                        </p>
                      </div>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => downloadReport('content_calendar.json', contentPlan)}
                      >
                        <Download className="w-4 h-4 mr-2" />
                        Download
                      </Button>
                    </div>
                  </div>
                </div>
              )}
            </Card>
          </div>
        )}

        {/* Video Generation Section */}
        {isVideoGenerating && (
          <div className="mb-8">
            <Card className="p-6 bg-card/50 backdrop-blur-sm border-border/50">
              <div className="flex items-center gap-3 mb-4">
                <Loader2 className="w-5 h-5 animate-spin text-primary" />
                <h3 className="text-xl font-semibold">Video Generation</h3>
                <Badge variant="secondary" className="text-xs">
                  In Progress
                </Badge>
              </div>
              <p className="text-foreground/70">
                Creating video content using AI video generation...
              </p>
            </Card>
          </div>
        )}

        {/* Video Generation Results */}
        {videoGenerated && (
          <div className="mb-8">
            <Card className="p-6 bg-card/50 backdrop-blur-sm border-border/50">
              <div className="flex items-center gap-3 mb-4">
                <Video className="w-5 h-5 text-primary" />
                <h3 className="text-xl font-semibold">Video Generated</h3>
                <Badge variant="default" className="text-xs">
                  Ready
                </Badge>
              </div>
              <p className="text-foreground/70 mb-4">
                Your video has been generated successfully. Access it through the InVideo AI workspace:
              </p>
              
              <div className="p-4 bg-background/30 rounded-lg border border-border/30">
                <div className="flex items-center justify-between">
                  <div>
                    <h4 className="font-medium mb-2">InVideo AI Workspace</h4>
                    <p className="text-sm text-foreground/70 mb-3">
                      Access your generated video content and make further edits
                    </p>
                    <div className="text-xs text-foreground/50 font-mono break-all mb-3">
                      https://ai.invideo.io/workspace/90f0d85e-edf5-47b3-8d2f-c7d23769d0ae/v40-copilot/81711fc8-5d3d-48fe-a2cd-1f7890e2c5f3
                    </div>
                  </div>
                </div>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => window.open('https://ai.invideo.io/workspace/90f0d85e-edf5-47b3-8d2f-c7d23769d0ae/v40-copilot/81711fc8-5d3d-48fe-a2cd-1f7890e2c5f3', '_blank')}
                  className="w-full"
                >
                  <ExternalLink className="w-4 h-4 mr-2" />
                  Open in InVideo AI
                </Button>
              </div>
            </Card>
          </div>
        )}

        {/* Podcast Generation Section */}
        {isPodcastGenerating && (
          <div className="mb-8">
            <Card className="p-6 bg-card/50 backdrop-blur-sm border-border/50">
              <div className="flex items-center gap-3 mb-4">
                <Loader2 className="w-5 h-5 animate-spin text-primary" />
                <h3 className="text-xl font-semibold">Podcast Generation</h3>
                <Badge variant="secondary" className="text-xs">
                  In Progress
                </Badge>
              </div>
              <p className="text-foreground/70">
                Creating podcast episode with AI narration...
              </p>
            </Card>
          </div>
        )}

        {/* Podcast Generation Results */}
        {podcastGenerated && (
          <div className="mb-8">
            <Card className="p-6 bg-card/50 backdrop-blur-sm border-border/50">
              <div className="flex items-center gap-3 mb-4">
                <Mic className="w-5 h-5 text-primary" />
                <h3 className="text-xl font-semibold">Podcast Episode</h3>
                <Badge variant="default" className="text-xs">
                  Ready
                </Badge>
              </div>
              <p className="text-foreground/70 mb-4">
                Your podcast episode is ready. Listen to the generated content:
              </p>
              
              <div className="p-4 bg-background/30 rounded-lg border border-border/30">
                <div className="mb-4">
                  <h4 className="font-medium mb-2">Episode Audio</h4>
                  <p className="text-sm text-foreground/70 mb-3">
                    AI-generated podcast episode based on your content plan
                  </p>
                </div>
                <audio 
                  controls 
                  className="w-full"
                  preload="metadata"
                >
                  <source src="/episode_audio.mp3" type="audio/mpeg" />
                  Your browser does not support the audio element.
                </audio>
              </div>
            </Card>
          </div>
        )}

        {/* Divider */}
        <div className="mb-8">
          <div className="flex items-center gap-4">
            <div className="flex-1 h-px bg-border/50"></div>
            <div className="text-sm text-foreground/50 font-medium">Pipeline Overview</div>
            <div className="flex-1 h-px bg-border/50"></div>
          </div>
        </div>

        {/* Pipeline Overview */}
        <div className="grid gap-6 mb-8">
          <Card className="p-6 bg-card/50 backdrop-blur-sm border-border/50">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-semibold">Active Pipeline</h2>
              <div className="flex gap-2">
                <TooltipProvider>
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <Button variant="glass" size="sm" disabled>
                        <Play className="w-4 h-4" />
                        Start
                      </Button>
                    </TooltipTrigger>
                    <TooltipContent>
                      <p>Coming Soon</p>
                    </TooltipContent>
                  </Tooltip>
                </TooltipProvider>
                <TooltipProvider>
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <Button variant="ghost" size="sm" disabled>
                        <Pause className="w-4 h-4" />
                        Pause
                      </Button>
                    </TooltipTrigger>
                    <TooltipContent>
                      <p>Coming Soon</p>
                    </TooltipContent>
                  </Tooltip>
                </TooltipProvider>
                <TooltipProvider>
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <Button variant="ghost" size="sm" disabled>
                        <Settings className="w-4 h-4" />
                      </Button>
                    </TooltipTrigger>
                    <TooltipContent>
                      <p>Coming Soon</p>
                    </TooltipContent>
                  </Tooltip>
                </TooltipProvider>
              </div>
            </div>
            
            <div className="grid gap-4">
              {pipelineSteps.map((step, index) => (
                <div key={index} className="flex items-center gap-4 p-4 rounded-lg bg-background/30 border border-border/30">
                  <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-primary flex items-center justify-center">
                    {step.status === "completed" ? (
                      <CheckCircle className="w-4 h-4 text-primary-foreground" />
                    ) : step.status === "in-progress" ? (
                      <div className="w-4 h-4 border-2 border-primary-foreground border-t-transparent rounded-full animate-spin" />
                    ) : (
                      <div className="w-4 h-4 rounded-full bg-muted" />
                    )}
                  </div>
                  
                  <div className="flex-grow">
                    <div className="flex items-center justify-between mb-1">
                      <span className="font-medium">{step.name}</span>
                      <Badge variant={
                        step.status === "completed" ? "default" : 
                        step.status === "in-progress" ? "secondary" : 
                        "outline"
                      }>
                        {step.status}
                      </Badge>
                    </div>
                    <Progress value={step.progress} className="h-2" />
                  </div>
                </div>
              ))}
            </div>
          </Card>
        </div>

        {/* Stats and Recent Content */}
        <div className="grid lg:grid-cols-3 gap-6">
          {/* Stats */}
          <div className="lg:col-span-1 space-y-4">
            <Card className="p-6 bg-card/50 backdrop-blur-sm border-border/50">
              <div className="flex items-center gap-3 mb-4">
                <BarChart3 className="w-5 h-5 text-primary" />
                <h3 className="font-semibold">This Month</h3>
                <TooltipProvider>
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <Badge variant="outline" className="ml-auto text-xs">
                        Preview
                      </Badge>
                    </TooltipTrigger>
                    <TooltipContent>
                      <p>Real analytics coming soon</p>
                    </TooltipContent>
                  </Tooltip>
                </TooltipProvider>
              </div>
              <div className="space-y-4">
                <div>
                  <div className="flex justify-between items-center mb-1">
                    <span className="text-sm text-foreground/70">Content Created</span>
                    <span className="font-bold">47</span>
                  </div>
                  <Progress value={78} className="h-2" />
                </div>
                <div>
                  <div className="flex justify-between items-center mb-1">
                    <span className="text-sm text-foreground/70">Published</span>
                    <span className="font-bold">32</span>
                  </div>
                  <Progress value={68} className="h-2" />
                </div>
                <div>
                  <div className="flex justify-between items-center mb-1">
                    <span className="text-sm text-foreground/70">Engagement</span>
                    <span className="font-bold">+24%</span>
                  </div>
                  <Progress value={85} className="h-2" />
                </div>
              </div>
            </Card>

            <Card className="p-6 bg-card/50 backdrop-blur-sm border-border/50">
              <div className="flex items-center gap-3 mb-4">
                <Calendar className="w-5 h-5 text-primary" />
                <h3 className="font-semibold">Quick Actions</h3>
              </div>
              <div className="space-y-3">
                <TooltipProvider>
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <Button variant="glass" className="w-full justify-start" disabled>
                        <Edit3 className="w-4 h-4" />
                        Create Content
                      </Button>
                    </TooltipTrigger>
                    <TooltipContent>
                      <p>Coming Soon</p>
                    </TooltipContent>
                  </Tooltip>
                </TooltipProvider>
                <TooltipProvider>
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <Button variant="glass" className="w-full justify-start" disabled>
                        <Globe className="w-4 h-4" />
                        Schedule Post
                      </Button>
                    </TooltipTrigger>
                    <TooltipContent>
                      <p>Coming Soon</p>
                    </TooltipContent>
                  </Tooltip>
                </TooltipProvider>
              </div>
            </Card>
          </div>

          {/* Recent Content */}
          <div className="lg:col-span-2">
            <Card className="p-6 bg-card/50 backdrop-blur-sm border-border/50">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-xl font-semibold">Recent Content</h3>
                <TooltipProvider>
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <Badge variant="outline" className="text-xs">
                        Preview
                      </Badge>
                    </TooltipTrigger>
                    <TooltipContent>
                      <p>Real content tracking coming soon</p>
                    </TooltipContent>
                  </Tooltip>
                </TooltipProvider>
              </div>
              <div className="space-y-4">
                {recentContent.map((content, index) => (
                  <div key={index} className="flex items-center justify-between p-4 rounded-lg bg-background/30 border border-border/30 hover:bg-background/40 transition-smooth">
                    <div>
                      <h4 className="font-medium mb-1">{content.title}</h4>
                      <div className="flex items-center gap-3 text-sm text-foreground/70">
                        <span>{content.type}</span>
                        <span>•</span>
                        <span>{content.date}</span>
                      </div>
                    </div>
                    <Badge variant={
                      content.status === "Published" ? "default" :
                      content.status === "In Review" ? "secondary" :
                      "outline"
                    }>
                      {content.status}
                    </Badge>
                  </div>
                ))}
              </div>
              <Button variant="ghost" className="w-full mt-4" disabled>
                <TooltipProvider>
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <span>View All Content</span>
                    </TooltipTrigger>
                    <TooltipContent>
                      <p>Coming Soon</p>
                    </TooltipContent>
                  </Tooltip>
                </TooltipProvider>
              </Button>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;