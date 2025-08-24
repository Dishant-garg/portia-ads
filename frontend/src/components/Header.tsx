import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";
import { Zap, Menu } from "lucide-react";

export const Header = () => {
  return (
    <header className="fixed top-0 w-full z-50 bg-background/80 backdrop-blur-sm border-b border-border">
      <div className="container mx-auto px-4 h-16 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2 hover:opacity-80 transition-smooth">
          <div className="w-8 h-8 bg-gradient-primary rounded-lg flex items-center justify-center">
            <Zap className="w-5 h-5 text-primary-foreground" />
          </div>
          <span className="text-xl font-bold bg-gradient-primary bg-clip-text text-transparent">
            ContentFlow AI
          </span>
        </Link>
        
        <nav className="hidden md:flex items-center gap-8">
          <Link to="/" className="text-foreground/80 hover:text-foreground transition-smooth">
            Home
          </Link>
          <Link to="/dashboard" className="text-foreground/80 hover:text-foreground transition-smooth">
            Dashboard
          </Link>
        </nav>
        
        <div className="flex items-center gap-4">
          <Button variant="ghost" className="hidden md:flex">
            Sign In
          </Button>
          <Button variant="hero" asChild>
            <Link to="/dashboard">Get Started</Link>
          </Button>
          <Button variant="ghost" size="icon" className="md:hidden">
            <Menu className="w-5 h-5" />
          </Button>
        </div>
      </div>
    </header>
  );
};