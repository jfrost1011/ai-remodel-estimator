# User Flow Diagram
**AI Remodel & Home Extension Cost Predictor 6-Hour MVP**

```mermaid
flowchart TD
  A[Landing Page\nVC Dashboard] --> B{Start Estimator?}
  B -->|Yes| C[Step 1:\nZIP Code]
  B -->|No| Z[Exit]
  
  C --> D[Step 2:\nProject Type]
  D --> E[Step 3:\nSquare Footage]
  
  %% Real-time cost preview updates on each step
  E -.-> CP[Cost Preview Card\nUpdates in Real-time]
  
  E --> F[Step 4:\nMaterial Grade]
  F --> G[Step 5:\nTimeline]
  
  G --> H{Process\nEstimate}
  H -->|Processing| I[Mini-Loading\n1.8s Max]
  
  I --> J[Results Display]
  
  %% Three main results components
  J --> K[Cost Breakdown]
  J --> L[Download PDF]
  J --> M[Pro Features\nUpsell]
  
  %% Certification-specific flows
  J -.-> N[Certification Panel:\nRAGAS Metrics]
  J -.-> O[Fine-tuning\nComparison]
  
  %% VC-focused components
  K -.-> VC1[ROI Calculator]
  L -.-> VC2[Market Size\nContext]
  M -.-> VC3[Subscription\nModel]
  
  %% Actions from results
  K --> P{New Estimate?}
  L --> P
  M --> P
  
  %% Optional paths
  N -.-> P
  O -.-> P
  
  P -->|Yes| C
  P -->|No| Z
  
  %% Styling for different node types
  style A fill:#f5f5f5,stroke:#333
  style J fill:#e6f3ff,stroke:#4a90e2
  style CP fill:#e6ffe6,stroke:#4CAF50
  style N fill:#fff0e6,stroke:#ff9800
  style O fill:#fff0e6,stroke:#ff9800
  style VC1 fill:#ffe6e6,stroke:#f44336,stroke-dasharray: 5 5
  style VC2 fill:#ffe6e6,stroke:#f44336,stroke-dasharray: 5 5
  style VC3 fill:#ffe6e6,stroke:#f44336,stroke-dasharray: 5 5
```

## Flow Description

This flowchart illustrates the streamlined user journey for the 6-Hour MVP, optimized for both certification compliance and VC impressions.

### Key Components:

1. **Entry Point with VC Dashboard**
   - Prominently displays market metrics and performance indicators
   - Immediate start button to begin the estimation process

2. **5-Step Express Form**
   - Simplified input collection with real-time cost preview
   - Each step designed for minimum input friction
   - Progressive disclosure of complexity

3. **Results With Triple Focus**
   - User value: Detailed cost breakdown
   - Certification requirements: RAGAS metrics and fine-tuning comparison
   - VC appeal: Market context and subscription upsell

4. **Real-Time Elements**
   - Cost preview updates continuously as inputs change
   - Minimal loading time (max 1.8s) for processing
   - Instant PDF generation

### Special Features:

- **Certification-Specific Components** (orange nodes)
  - RAGAS metrics panel showing all required measurements
  - Fine-tuning comparison demonstrating embedding improvements
  - These sections can be expanded for evaluators but minimized for regular users

- **VC-Focused Elements** (red dashed nodes)
  - ROI calculator showing value proposition
  - Market size context highlighting opportunity
  - Subscription model preview showing growth potential

This user flow is specifically designed to complete certification requirements with minimal development time while creating an impression of a mature, market-ready product for potential investors.