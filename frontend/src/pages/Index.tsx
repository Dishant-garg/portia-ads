import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Link } from "react-router-dom";
import heroImage from "@/assets/hero-image.jpg";
import { 
  Search, 
  Edit3, 
  CheckCircle, 
  Globe, 
  BarChart3, 
  Zap,
  ArrowRight,
  Users,
  Clock,
  TrendingUp,
  Mic,
  Video,
  Newspaper
} from "lucide-react";

const Index = () => {
  const features = [
    {
      icon: Search,
      title: "AI Research Agent",
      description: "Automated market research and trend analysis from multiple sources",
      color: "from-blue-500 to-cyan-500"
    },
    {
      icon: Edit3,
      title: "Content Planner",
      description: "Strategic editorial calendar creation with content optimization",
      color: "from-purple-500 to-pink-500"
    },
    {
      icon: CheckCircle,
      title: "Quality Assurance",
      description: "Fact-checking and accuracy verification before publishing",
      color: "from-green-500 to-emerald-500"
    },
    {
      icon: Globe,
      title: "Multi-Platform Publishing",
      description: "Seamless distribution across all your digital channels",
      color: "from-orange-500 to-red-500"
    }
  ];

  const pipelineSteps = [
    { name: "Research Agent", description: "Market research and trend analysis" },
    { name: "Content Planner", description: "Editorial calendar and content strategy" },
    { name: "Writer Agent", description: "Draft generation and editing" },
    { name: "Fact Checker", description: "Accuracy verification" },
    { name: "SEO Optimizer", description: "Search optimization" },
    { name: "Publisher Agent", description: "Multi-platform distribution" }
  ];

  const stats = [
    { label: "Content Pieces", value: "10,000+", icon: Newspaper },
    { label: "Active Users", value: "2,500+", icon: Users },
    { label: "Time Saved", value: "80%", icon: Clock },
    { label: "Engagement Boost", value: "45%", icon: TrendingUp }
  ];

  return (
    <div className="min-h-screen bg-gradient-hero">
      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4">
        <div className="container mx-auto text-center">
          <Badge variant="secondary" className="mb-6 bg-primary/10 text-primary border-primary/20">
            <Zap className="w-4 h-4 mr-2" />
            Powered by Advanced AI
          </Badge>
          
          <h1 className="text-5xl md:text-7xl font-bold mb-6 bg-gradient-primary bg-clip-text text-transparent leading-tight">
            AI Content Production
            <br />
            Pipeline
          </h1>
          
          <p className="text-xl md:text-2xl text-foreground/70 mb-8 max-w-3xl mx-auto leading-relaxed">
            End-to-end content creation with quality gates, human oversight, and multi-platform distribution. 
            Transform your content strategy with intelligent automation.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-16">
            <Button variant="hero" size="lg" asChild>
              <Link to="/dashboard">
                Start Free Trial
                <ArrowRight className="w-5 h-5" />
              </Link>
            </Button>
            <Button variant="glass" size="lg">
              Watch Demo
              <Video className="w-5 h-5" />
            </Button>
          </div>
          
          <div className="relative max-w-5xl mx-auto">
            <img 
              src={heroImage} 
              alt="AI Content Production Pipeline" 
              className="w-full rounded-2xl shadow-elegant border border-border/20"
            />
            <div className="absolute inset-0 bg-gradient-primary/10 rounded-2xl"></div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 px-4">
        <div className="container mx-auto">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <div key={index} className="text-center">
                <div className="w-12 h-12 mx-auto mb-4 bg-gradient-primary rounded-xl flex items-center justify-center">
                  <stat.icon className="w-6 h-6 text-primary-foreground" />
                </div>
                <div className="text-3xl font-bold mb-2">{stat.value}</div>
                <div className="text-foreground/70">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4">
        <div className="container mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              Intelligent Content Creation
            </h2>
            <p className="text-xl text-foreground/70 max-w-2xl mx-auto">
              Our AI agents work together to create, verify, and distribute high-quality content at scale
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <Card key={index} className="p-6 bg-card/50 backdrop-blur-sm border-border/50 hover:shadow-glow hover:scale-105 transition-bounce group">
                <div className={`w-12 h-12 rounded-xl bg-gradient-to-r ${feature.color} flex items-center justify-center mb-4 group-hover:shadow-glow transition-smooth`}>
                  <feature.icon className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-xl font-semibold mb-3">{feature.title}</h3>
                <p className="text-foreground/70">{feature.description}</p>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Pipeline Visualization */}
      <section className="py-20 px-4 bg-background/30">
        <div className="container mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              Your Content Production Pipeline
            </h2>
            <p className="text-xl text-foreground/70 max-w-2xl mx-auto">
              Six intelligent agents working in perfect harmony to deliver exceptional content
            </p>
          </div>
          
          <div className="max-w-4xl mx-auto">
            <div className="grid gap-4">
              {pipelineSteps.map((step, index) => (
                <div key={index} className="flex items-center gap-6 p-6 rounded-2xl bg-card/50 backdrop-blur-sm border border-border/50 hover:bg-card/70 transition-smooth group">
                  <div className="flex-shrink-0 w-12 h-12 rounded-full bg-gradient-primary flex items-center justify-center text-primary-foreground font-bold text-lg group-hover:shadow-glow transition-smooth">
                    {index + 1}
                  </div>
                  <div className="flex-grow">
                    <h3 className="text-xl font-semibold mb-2">{step.name}</h3>
                    <p className="text-foreground/70">{step.description}</p>
                  </div>
                  {index < pipelineSteps.length - 1 && (
                    <ArrowRight className="w-6 h-6 text-primary opacity-50 group-hover:opacity-100 transition-smooth" />
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Enhanced Features */}
      <section className="py-20 px-4">
        <div className="container mx-auto">
          <div className="grid lg:grid-cols-2 gap-16 items-center">
            <div>
              <Badge variant="secondary" className="mb-6 bg-primary/10 text-primary border-primary/20">
                <Mic className="w-4 h-4 mr-2" />
                Enhanced AI Production
              </Badge>
              <h2 className="text-4xl font-bold mb-6">
                Podcast & Video Creation
              </h2>
              <p className="text-lg text-foreground/70 mb-8">
                Transform your content into engaging podcasts and videos with our enhanced AI production assistant. 
                From script generation to voice synthesis and automated editing.
              </p>
              
              <div className="space-y-4 mb-8">
                <div className="flex items-center gap-3">
                  <CheckCircle className="w-5 h-5 text-primary" />
                  <span>Multi-source content aggregation</span>
                </div>
                <div className="flex items-center gap-3">
                  <CheckCircle className="w-5 h-5 text-primary" />
                  <span>Script generation with human review</span>
                </div>
                <div className="flex items-center gap-3">
                  <CheckCircle className="w-5 h-5 text-primary" />
                  <span>Voice synthesis and video editing automation</span>
                </div>
                <div className="flex items-center gap-3">
                  <CheckCircle className="w-5 h-5 text-primary" />
                  <span>Multi-platform publishing with scheduling</span>
                </div>
              </div>
              
              <Button variant="gradient" size="lg">
                Explore AI Production
                <ArrowRight className="w-5 h-5" />
              </Button>
            </div>
            
            <div className="relative">
              <div className="bg-gradient-secondary rounded-2xl p-8 shadow-glow">
                <div className="bg-background/20 backdrop-blur-sm rounded-xl p-6 border border-border/20">
                  <h3 className="text-xl font-semibold mb-4 text-primary-foreground">Production Workflow</h3>
                  <div className="space-y-3">
                    <div className="flex items-center gap-3 text-primary-foreground/80">
                      <div className="w-2 h-2 rounded-full bg-primary-glow"></div>
                      <span>Content Aggregation</span>
                    </div>
                    <div className="flex items-center gap-3 text-primary-foreground/80">
                      <div className="w-2 h-2 rounded-full bg-primary-glow"></div>
                      <span>Script Generation</span>
                    </div>
                    <div className="flex items-center gap-3 text-primary-foreground/80">
                      <div className="w-2 h-2 rounded-full bg-primary-glow"></div>
                      <span>Voice & Video Synthesis</span>
                    </div>
                    <div className="flex items-center gap-3 text-primary-foreground/80">
                      <div className="w-2 h-2 rounded-full bg-primary-glow"></div>
                      <span>Multi-Platform Distribution</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 bg-gradient-primary">
        <div className="container mx-auto text-center">
          <h2 className="text-4xl md:text-5xl font-bold mb-6 text-primary-foreground">
            Ready to Transform Your Content Strategy?
          </h2>
          <p className="text-xl text-primary-foreground/80 mb-8 max-w-2xl mx-auto">
            Join thousands of content creators who have automated their workflow and scaled their impact
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button variant="secondary" size="lg" asChild>
              <Link to="/dashboard">
                Start Your Free Trial
                <ArrowRight className="w-5 h-5" />
              </Link>
            </Button>
            <Button variant="glass" size="lg" className="text-primary-foreground border-primary-foreground/20 hover:bg-primary-foreground/10">
              Schedule Demo
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Index;