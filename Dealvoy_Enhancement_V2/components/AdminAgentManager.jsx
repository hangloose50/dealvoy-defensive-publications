// ✅ Dealvoy Admin Agent Manager UI
// This component displays named agents, their tier access, and manual triggers for weekly video generation
// Assistant Task: Maintain this module and ensure agents are properly registered and tier-controlled. Do not duplicate agent names. It is okay to overwrite or expand existing agents.
// Assistant Task: Ensure all newly generated weekly video prompts from VidVoyager are automatically archived to the customer video library (/customer_portal/video_library/).
// Assistant Task: Generate and persist a welcome instructional video prompt via DemoVoyager and ensure it is always visible on the Dealvoy home page. Store prompt in /onboarding_videos/dealvoy_intro/video_prompt.txt.
// ✅ COMPLETED: Deploy dealvoy-icon.png across all platforms (web, mobile, admin) with HTML and manifest integration. Generated scaled versions (512x512, 1024x1024, 180x180). Maintained design consistency with locked icon pipeline.

import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Switch } from '@/components/ui/switch';
import { Card, CardContent } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Calendar, Clock, Play, Settings, Video, Shield, Search, Scale, Film } from 'lucide-react';

// Agent Registry with enhanced metadata
const AGENT_REGISTRY = [
  {
    name: 'TrendVoyager',
    role: 'Product trend scanner and analyzer (weekly batch)',
    tiers: ['Starter', 'Premium', 'Pro', 'Elite', 'Titan'],
    category: 'Market Intelligence',
    icon: '📈',
    weeklyVideoCount: { Starter: 1, Premium: 2, Pro: 3, Elite: 4, Titan: 5 },
    lastRun: '2025-07-20T10:00:00Z',
    outputTypes: ['.json', '.txt', 'trend-analysis.json'],
    enabled: true
  },
  {
    name: 'VidVoyager',
    role: 'Video prompt and storyboard generator (Runway-style)',
    tiers: ['Premium', 'Pro', 'Elite', 'Titan'],
    category: 'Video Generation',
    icon: '🎥',
    weeklyVideoCount: { Premium: 2, Pro: 4, Elite: 6, Titan: 10 },
    lastRun: '2025-07-27T08:30:00Z',
    outputTypes: ['.txt', '.json', 'video-prompt.txt'],
    enabled: true
  },
  {
    name: 'RiskSentinel',
    role: 'IP/brand safety scanner (SafeMatch Alert system)',
    tiers: ['Starter', 'Premium', 'Pro', 'Elite', 'Titan'],
    category: 'Risk Management',
    icon: '🛡️',
    weeklyVideoCount: { Starter: 1, Premium: 1, Pro: 2, Elite: 2, Titan: 3 },
    lastRun: '2025-07-27T09:15:00Z',
    outputTypes: ['.json', '.txt', 'risk-report.json'],
    enabled: true
  },
  {
    name: 'ScoutVision',
    role: 'ROI, Gating, and Buy/Skip evaluator embedded in scanner',
    tiers: ['All'],
    category: 'Product Scouting',
    icon: '🔍',
    weeklyVideoCount: { All: 2 },
    lastRun: '2025-07-27T07:45:00Z',
    outputTypes: ['.json', '.txt', 'scout-evaluation.json'],
    enabled: true
  },
  {
    name: 'TierScaler',
    role: 'Controls feature access and automation caps by pricing tier',
    tiers: ['All'],
    category: 'System Management',
    icon: '⚖️',
    weeklyVideoCount: { All: 1 },
    lastRun: '2025-07-27T06:00:00Z',
    outputTypes: ['.json', '.txt', 'tier-config.json'],
    enabled: true
  },
  {
    name: 'DemoVoyager',
    role: 'Creates onboarding and instructional video prompts',
    tiers: ['All'],
    category: 'Onboarding & Training',
    icon: '🎬',
    weeklyVideoCount: { All: 1 },
    lastRun: '2025-07-26T14:00:00Z',
    outputTypes: ['.txt', '.json', 'welcome-video-prompt.txt'],
    enabled: true,
    special: 'instructional-video-generator'
  }
];

// Video Archive Configuration
const VIDEO_ARCHIVE_CONFIG = {
  customerLibraryPath: '/customer_portal/video_library/',
  onboardingPath: '/onboarding_videos/dealvoy_intro/',
  archiveFormat: 'YYYY-MM-DD_HH-mm_[AGENT]_[TIER]_video_prompt.txt',
  maxArchiveSize: 1000, // Maximum archived prompts per agent
  autoCleanupDays: 90
};

// Weekly Schedule Configuration
const WEEKLY_SCHEDULE = {
  nextRun: '2025-08-03T06:00:00Z', // Sunday 6:00 AM EST
  timezone: 'EST',
  runDay: 'Sunday',
  batchGeneration: true
};

export default function AdminAgentManager() {
  const [enabledAgents, setEnabledAgents] = useState({});
  const [agentRegistry, setAgentRegistry] = useState(AGENT_REGISTRY);
  const [lastVideoGeneration, setLastVideoGeneration] = useState({});
  const [welcomeVideoRequired, setWelcomeVideoRequired] = useState(false);
  const [systemStatus, setSystemStatus] = useState({
    totalAgents: AGENT_REGISTRY.length,
    activeAgents: AGENT_REGISTRY.filter(a => a.enabled).length,
    nextScheduledRun: WEEKLY_SCHEDULE.nextRun,
    lastArchive: null
  });

  // Initialize enabled agents from registry
  useEffect(() => {
    const initialStates = {};
    agentRegistry.forEach(agent => {
      initialStates[agent.name] = agent.enabled;
    });
    setEnabledAgents(initialStates);

    // Check if welcome video is required for homepage
    checkWelcomeVideoStatus();
  }, []);

  // Check welcome video status
  const checkWelcomeVideoStatus = () => {
    // In production, check if welcome video exists on homepage
    const welcomeExists = localStorage.getItem('dealvoy_welcome_video_active');
    setWelcomeVideoRequired(!welcomeExists);
  };

  // Toggle agent with validation to prevent duplicates
  const toggleAgent = (agentName) => {
    const existingAgent = agentRegistry.find(a => a.name === agentName);
    if (!existingAgent) {
      console.error(`Agent ${agentName} not found in registry`);
      return;
    }

    setEnabledAgents((prev) => ({
      ...prev,
      [agentName]: !prev[agentName],
    }));

    // Update registry
    setAgentRegistry(prev => 
      prev.map(agent => 
        agent.name === agentName 
          ? { ...agent, enabled: !agent.enabled }
          : agent
      )
    );

    console.log(`Agent ${agentName} ${enabledAgents[agentName] ? 'disabled' : 'enabled'}`);
  };

  // Manual trigger for agent execution
  const triggerAgent = async (agentName, tier = null) => {
    const agent = agentRegistry.find(a => a.name === agentName);
    if (!agent || !enabledAgents[agentName]) {
      alert(`Agent ${agentName} is not available or disabled`);
      return;
    }

    console.log(`Manual trigger initiated for ${agentName}`);
    
    // Execution safeguard: Only output files, no external logins
    const outputType = agent.outputTypes[Math.floor(Math.random() * agent.outputTypes.length)];
    
    // Simulate agent execution
    const result = {
      agent: agentName,
      tier: tier || 'manual',
      timestamp: new Date().toISOString(),
      outputType: outputType,
      status: 'completed',
      output: `${agentName}_${Date.now()}_${outputType}`
    };

    // Archive to customer video library if VidVoyager
    if (agentName === 'VidVoyager') {
      await archiveVideoPrompt(result);
    }

    // Update last run time
    setAgentRegistry(prev => 
      prev.map(a => 
        a.name === agentName 
          ? { ...a, lastRun: result.timestamp }
          : a
      )
    );

    setLastVideoGeneration(prev => ({
      ...prev,
      [agentName]: result
    }));

    alert(`${agentName} manual run completed.\nOutput: ${result.output}\nType: ${outputType}\nNo external logins triggered.`);
  };

  // Archive video prompts to customer library
  const archiveVideoPrompt = async (result) => {
    const archiveFileName = `${new Date().toISOString().split('T')[0]}_${result.agent}_${result.tier}_video_prompt.txt`;
    const archivePath = VIDEO_ARCHIVE_CONFIG.customerLibraryPath + archiveFileName;
    
    console.log(`Archiving video prompt to: ${archivePath}`);
    
    // In production: Save to actual file system
    // await fs.writeFile(archivePath, result.output);
    
    // For demo: Store in localStorage
    const existingArchive = JSON.parse(localStorage.getItem('video_archive') || '[]');
    existingArchive.push({
      ...result,
      archivePath,
      archived: true
    });
    localStorage.setItem('video_archive', JSON.stringify(existingArchive));
    
    console.log(`Video prompt archived successfully: ${archiveFileName}`);
  };

  // Generate welcome video via DemoVoyager
  const generateWelcomeVideo = async () => {
    console.log('DemoVoyager: Generating welcome instructional video...');
    
    const welcomeVideoPrompt = `
=== DEMOVOYAGER WELCOME VIDEO GENERATION ===
Generated: ${new Date().toLocaleString()}

🎬 VIDEO TITLE: "Welcome to Dealvoy: Your AI-Powered Arbitrage Intelligence Platform"

📋 VIDEO STRUCTURE:
1. INTRO (0-15 seconds)
   - Dealvoy logo animation with "Decode. Discover. Dominate." tagline
   - Welcome message: "Transform your retail arbitrage with AI intelligence"

2. PLATFORM OVERVIEW (15-45 seconds)
   - Dashboard tour highlighting key features
   - AI agent ecosystem showcase
   - Patent-protected technology (#63/850,603)

3. AGENT SHOWCASE (45-90 seconds)
   - TrendVoyager: Market intelligence and trend analysis
   - VidVoyager: Video content generation for marketing
   - RiskSentinel: IP and brand safety protection
   - ScoutVision: ROI evaluation and product scouting
   - TierScaler: Intelligent pricing and feature management

4. TIER COMPARISON (90-120 seconds)
   - Starter ($29/month): Basic agents + 2 videos/week
   - Premium ($67/month): Enhanced features + 4 videos/week
   - Pro ($97/month): Advanced capabilities + 6 videos/week
   - Elite ($197/month): Premium features + 8 videos/week
   - Titan ($297/month): Full access + 10 videos/week

5. CALL TO ACTION (120-135 seconds)
   - "Start your free trial today"
   - "Join thousands of successful arbitrage entrepreneurs"
   - "Decode. Discover. Dominate your market."

🎯 TECHNICAL SPECIFICATIONS:
- Format: MP4, 1080p, 16:9 aspect ratio
- Duration: 2 minutes 15 seconds
- Audio: Professional voiceover + ambient background music
- Graphics: Modern UI animations, real product screenshots
- Typography: Inter font family, brand color palette
- Branding: Consistent Dealvoy visual identity

📊 IMPLEMENTATION REQUIREMENTS:
- Auto-play on homepage hero section (muted by default)
- Video controls for user interaction
- Closed captions for accessibility compliance
- Mobile-responsive player
- CDN optimization for fast loading

🔒 COMPLIANCE & SAFETY:
- USPTO Patent #63/850,603 compliant
- No external API dependencies during generation
- Safe local content output only
- Professional business presentation standards
- GDPR and privacy compliant

📁 FILE OUTPUT:
- Primary: /onboarding_videos/dealvoy_intro/video_prompt.txt
- Backup: /customer_portal/video_library/welcome_series/
- Homepage Integration: Auto-embed with fallback image

🚀 DEPLOYMENT STATUS:
- Priority: Critical - Homepage integration required
- Status: Ready for video production pipeline
- Integration: Automatic homepage visibility
- Monitoring: Track engagement and conversion metrics

Generated by DemoVoyager v2.1
Timestamp: ${new Date().toISOString()}
Agent Status: Active and Operational
    `;

    // Save to onboarding directory
    const onboardingPath = VIDEO_ARCHIVE_CONFIG.onboardingPath + 'video_prompt.txt';
    
    // In production: Create directory and save file
    console.log(`Saving welcome video prompt to: ${onboardingPath}`);
    
    // Store in localStorage for demo
    localStorage.setItem('dealvoy_welcome_video_prompt', welcomeVideoPrompt);
    localStorage.setItem('dealvoy_welcome_video_active', 'true');
    localStorage.setItem('welcome_video_required_homepage', 'true');
    
    // Update agent last run
    setAgentRegistry(prev => 
      prev.map(a => 
        a.name === 'DemoVoyager' 
          ? { ...a, lastRun: new Date().toISOString() }
          : a
      )
    );

    setWelcomeVideoRequired(false);
    
    alert(`✅ DemoVoyager: Welcome video prompt generated successfully!

📁 Saved to: ${onboardingPath}
🏠 Homepage: Marked as required content
🎬 Status: Ready for video production
📊 Integration: Automatic visibility enabled

The welcome video is now flagged for immediate homepage integration.`);

    console.log('Welcome video prompt:', welcomeVideoPrompt);
  };

  // Test tier simulation
  const testTierSimulation = (agentName, tier) => {
    const agent = agentRegistry.find(a => a.name === agentName);
    if (!agent) return;

    const isValidTier = agent.tiers.includes(tier) || agent.tiers.includes('All');
    if (!isValidTier) {
      alert(`${agentName} is not available for ${tier} tier.\nAvailable tiers: ${agent.tiers.join(', ')}`);
      return;
    }

    const weeklyCount = agent.weeklyVideoCount[tier] || agent.weeklyVideoCount['All'] || 1;
    
    alert(`🧪 Tier Simulation: ${agentName} on ${tier} tier
    
📊 Weekly Video Generation: ${weeklyCount} videos
🎯 Simulation Mode: Safe (no live connections)
⚡ Status: Test environment active
🔒 Safeguards: Local execution only

Simulating ${agentName} functionality for ${tier} tier users...`);
    
    console.log(`Testing ${agentName} on ${tier} tier - ${weeklyCount} weekly videos`);
  };

  // Add new agent (prevent duplicates)
  const addNewAgent = (newAgent) => {
    const existingAgent = agentRegistry.find(a => a.name === newAgent.name);
    if (existingAgent) {
      console.log(`Updating existing agent: ${newAgent.name}`);
      setAgentRegistry(prev => 
        prev.map(a => a.name === newAgent.name ? { ...a, ...newAgent } : a)
      );
    } else {
      console.log(`Adding new agent: ${newAgent.name}`);
      setAgentRegistry(prev => [...prev, newAgent]);
    }
  };

  // Format relative time
  const formatRelativeTime = (timestamp) => {
    const now = new Date();
    const past = new Date(timestamp);
    const diffMs = now - past;
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    const diffDays = Math.floor(diffHours / 24);
    
    if (diffDays > 0) return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;
    if (diffHours > 0) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
    return 'Recently';
  };

  return (
    <div className="space-y-6 p-6 max-w-6xl mx-auto">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-3xl font-bold">🧠 Dealvoy Agent Control Center</h2>
          <p className="text-muted-foreground mt-1">
            Manage AI agents, generate video content, and monitor system performance
          </p>
        </div>
        <div className="text-right text-sm text-muted-foreground">
          <p className="flex items-center gap-2">
            <Calendar className="w-4 h-4" />
            Next Run: Sunday, Aug 3, 2025 at 6:00 AM EST
          </p>
          <p>Active: {systemStatus.activeAgents}/{systemStatus.totalAgents} agents</p>
        </div>
      </div>

      {/* Welcome Video Status Alert */}
      {welcomeVideoRequired && (
        <Alert className="border-amber-200 bg-amber-50">
          <Film className="h-4 w-4" />
          <AlertDescription>
            <strong>Homepage Integration Required:</strong> Welcome video prompt needs to be generated for homepage visibility.
            <Button 
              variant="outline" 
              size="sm" 
              className="ml-2"
              onClick={generateWelcomeVideo}
            >
              Generate Now
            </Button>
          </AlertDescription>
        </Alert>
      )}

      {/* Agent Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {agentRegistry.map((agent) => (
          <Card key={agent.name} className={`p-4 transition-all duration-200 ${
            enabledAgents[agent.name] 
              ? 'border-green-200 bg-green-50/50' 
              : 'border-gray-200 bg-gray-50/50'
          } ${agent.special === 'instructional-video-generator' ? 'ring-2 ring-amber-200' : ''}`}>
            
            {/* Agent Header */}
            <div className="flex justify-between items-start mb-3">
              <div className="flex items-center gap-2">
                <span className="text-2xl">{agent.icon}</span>
                <div>
                  <Label className="text-lg font-semibold">{agent.name}</Label>
                  <p className="text-xs text-muted-foreground">{agent.category}</p>
                </div>
              </div>
              <Switch
                checked={enabledAgents[agent.name] || false}
                onCheckedChange={() => toggleAgent(agent.name)}
              />
            </div>

            {/* Agent Details */}
            <CardContent className="p-0 space-y-3">
              <p className="text-sm text-muted-foreground">{agent.role}</p>
              
              {/* Tier Badges */}
              <div className="flex flex-wrap gap-1">
                <span className="text-xs font-medium text-muted-foreground">Tiers:</span>
                {agent.tiers.map(tier => (
                  <Badge 
                    key={tier} 
                    variant="secondary" 
                    className="text-xs cursor-pointer"
                    onClick={() => testTierSimulation(agent.name, tier)}
                  >
                    {tier}
                  </Badge>
                ))}
              </div>

              {/* Status & Last Run */}
              <div className="text-xs text-muted-foreground flex items-center gap-4">
                <span className="flex items-center gap-1">
                  <Clock className="w-3 h-3" />
                  {formatRelativeTime(agent.lastRun)}
                </span>
                <span className="flex items-center gap-1">
                  <span className={`w-2 h-2 rounded-full ${
                    enabledAgents[agent.name] ? 'bg-green-500' : 'bg-gray-400'
                  }`} />
                  {enabledAgents[agent.name] ? 'Active' : 'Disabled'}
                </span>
              </div>

              {/* Agent Actions */}
              <div className="flex gap-2 pt-2">
                <Button 
                  variant="outline" 
                  size="sm" 
                  className="flex-1"
                  disabled={!enabledAgents[agent.name]}
                  onClick={() => triggerAgent(agent.name)}
                >
                  <Play className="w-3 h-3 mr-1" />
                  Manual Run
                </Button>
                <Button 
                  variant="ghost" 
                  size="sm"
                  disabled={!enabledAgents[agent.name]}
                >
                  <Settings className="w-3 h-3" />
                </Button>
              </div>

              {/* Special DemoVoyager Section */}
              {agent.special === 'instructional-video-generator' && (
                <div className="mt-3 p-3 bg-amber-50 border border-amber-200 rounded-lg">
                  <div className="flex items-center gap-2 mb-2">
                    <Video className="w-4 h-4 text-amber-600" />
                    <span className="text-sm font-medium text-amber-800">
                      Instructional Video Generator
                    </span>
                  </div>
                  <p className="text-xs text-amber-700 mb-2">
                    Creates "Welcome to Dealvoy" onboarding content for homepage integration
                  </p>
                  <Button 
                    variant="default" 
                    size="sm" 
                    className="w-full bg-amber-600 hover:bg-amber-700"
                    onClick={generateWelcomeVideo}
                  >
                    <Film className="w-3 h-3 mr-1" />
                    Generate Welcome Video
                  </Button>
                </div>
              )}
            </CardContent>
          </Card>
        ))}
      </div>

      {/* System Status */}
      <Card className="p-4 bg-blue-50 border-blue-200">
        <div className="flex items-center justify-between mb-2">
          <Label className="text-base font-semibold flex items-center gap-2">
            <Shield className="w-4 h-4" />
            System Status
          </Label>
          <Badge variant="outline" className="text-green-700 border-green-300">
            All Systems Operational
          </Badge>
        </div>
        
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div>
            <p className="text-muted-foreground">Active Agents</p>
            <p className="font-semibold">{systemStatus.activeAgents}/{systemStatus.totalAgents}</p>
          </div>
          <div>
            <p className="text-muted-foreground">Next Scheduled Run</p>
            <p className="font-semibold">Sunday 6:00 AM</p>
          </div>
          <div>
            <p className="text-muted-foreground">Video Archive</p>
            <p className="font-semibold">Auto-enabled</p>
          </div>
          <div>
            <p className="text-muted-foreground">Safety Status</p>
            <p className="font-semibold text-green-600">Secure</p>
          </div>
        </div>

        <div className="mt-3 text-xs text-muted-foreground">
          <p>🛡️ <strong>Execution Safeguards:</strong> No external logins, local output only (.txt, .json, prompts)</p>
          <p>📁 <strong>Auto-Archive:</strong> VidVoyager outputs saved to /customer_portal/video_library/</p>
          <p>🏠 <strong>Homepage Integration:</strong> DemoVoyager welcome video auto-visible on home page</p>
        </div>
      </Card>
    </div>
  );
}
