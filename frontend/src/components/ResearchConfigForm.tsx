import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Search, Settings } from "lucide-react";
import { useState } from "react";

const formSchema = z.object({
  topic: z.string().min(1, "Research topic is required"),
  target_audience: z.string().min(1, "Target audience is required"),
  competitor_domains: z.string().optional(),
  research_depth: z.enum(["basic", "standard", "comprehensive"]),
});

type FormData = z.infer<typeof formSchema>;

interface ResearchConfigFormProps {
  onSubmit: (data: {
    topic: string;
    target_audience: string;
    competitor_domains: string[];
    research_depth: "basic" | "standard" | "comprehensive";
  }) => void;
  trigger?: React.ReactNode;
}

const ResearchConfigForm = ({ onSubmit, trigger }: ResearchConfigFormProps) => {
  const [open, setOpen] = useState(false);
  
  const form = useForm<FormData>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      topic: "",
      target_audience: "",
      competitor_domains: "",
      research_depth: "standard",
    },
  });

  const handleSubmit = (data: FormData) => {
    // Transform the data to match your API format
    const transformedData = {
      topic: data.topic,
      target_audience: data.target_audience,
      competitor_domains: data.competitor_domains 
        ? data.competitor_domains.split(',').map(domain => domain.trim()).filter(domain => domain.length > 0)
        : [],
      research_depth: data.research_depth
    };
    onSubmit(transformedData);
    setOpen(false);
    form.reset();
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        {trigger || (
          <Button variant="glass" className="w-full justify-start">
            <Search className="w-4 h-4" />
            Configure Research
          </Button>
        )}
      </DialogTrigger>
      <DialogContent className="sm:max-w-[600px] bg-card/95 backdrop-blur-sm border-border/50">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Settings className="w-5 h-5 text-primary" />
            Research Configuration
          </DialogTitle>
        </DialogHeader>
        
        <Form {...form}>
          <form onSubmit={form.handleSubmit(handleSubmit)} className="space-y-6">
            <FormField
              control={form.control}
              name="topic"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Research Topic</FormLabel>
                  <FormControl>
                    <Input 
                      placeholder="e.g., AI_in_Healthcare, Sustainable_Fashion_Trends"
                      {...field}
                      className="bg-background/50 border-border/50"
                    />
                  </FormControl>
                  <FormDescription>
                    The main subject area you want to research and create content about
                  </FormDescription>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="target_audience"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Target Audience</FormLabel>
                  <FormControl>
                    <Input 
                      placeholder="Healthcare professionals, hospital administrators, medical researchers"
                      {...field}
                      className="bg-background/50 border-border/50"
                    />
                  </FormControl>
                  <FormDescription>
                    Who is your primary audience for this content?
                  </FormDescription>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="competitor_domains"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Competitor Domains (Optional)</FormLabel>
                  <FormControl>
                    <Textarea 
                      placeholder="healthitnews.com, medicalfuturist.com, healthcare-it-times.com"
                      {...field}
                      className="bg-background/50 border-border/50 min-h-[80px]"
                    />
                  </FormControl>
                  <FormDescription>
                    Enter competitor websites (comma separated) to analyze their content strategy
                  </FormDescription>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="research_depth"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Research Depth</FormLabel>
                  <Select onValueChange={field.onChange} defaultValue={field.value}>
                    <FormControl>
                      <SelectTrigger className="bg-background/50 border-border/50">
                        <SelectValue placeholder="Select research depth" />
                      </SelectTrigger>
                    </FormControl>
                    <SelectContent className="bg-popover/95 backdrop-blur-sm border-border/50">
                      <SelectItem value="basic">Basic - Quick overview and key trends</SelectItem>
                      <SelectItem value="standard">Standard - Comprehensive analysis with market insights</SelectItem>
                      <SelectItem value="comprehensive">Comprehensive - Deep dive with competitor analysis</SelectItem>
                    </SelectContent>
                  </Select>
                  <FormDescription>
                    How thorough should the research be?
                  </FormDescription>
                  <FormMessage />
                </FormItem>
              )}
            />

            <div className="flex gap-3 pt-4">
              <Button 
                type="button" 
                variant="glass" 
                onClick={() => setOpen(false)}
                className="flex-1"
              >
                Cancel
              </Button>
              <Button 
                type="submit" 
                variant="hero" 
                className="flex-1"
              >
                Start Research Pipeline
              </Button>
            </div>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
};

export default ResearchConfigForm;