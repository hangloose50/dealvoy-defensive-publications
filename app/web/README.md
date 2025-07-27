# Dealvoy Web Dashboard

A modern Next.js dashboard for the Dealvoy e-commerce intelligence platform.

## Features

- 🎯 **Real-time Analytics**: Track revenue, deals, and user activity
- 🤖 **Scraper Control**: Manage and monitor web scrapers
- 💳 **Billing Integration**: Stripe-powered subscription management
- 🔐 **Authentication**: Secure auth with Supabase
- 📱 **Responsive Design**: Works on desktop and mobile
- ⚡ **Fast Performance**: Built with Next.js 14 and optimized components

## Tech Stack

- **Framework**: Next.js 14 with App Router
- **Styling**: Tailwind CSS
- **Authentication**: Supabase Auth
- **Database**: PostgreSQL (via Supabase)
- **Payments**: Stripe
- **Charts**: Recharts
- **Icons**: Lucide React
- **State Management**: Zustand
- **API**: tRPC with TypeScript

## Getting Started

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Set up environment variables**:
   ```bash
   cp .env.example .env.local
   # Fill in your configuration values
   ```

3. **Run the development server**:
   ```bash
   npm run dev
   ```

4. **Open your browser**:
   Navigate to [http://localhost:3000](http://localhost:3000)

## Project Structure

```
app/web/
├── components/           # Reusable UI components
│   ├── DashboardLayout.tsx
│   ├── ScraperControl.tsx
│   └── AnalyticsOverview.tsx
├── pages/               # Next.js pages
│   └── dashboard/       # Dashboard routes
├── package.json         # Dependencies
├── tailwind.config.js   # Tailwind configuration
└── next.config.js       # Next.js configuration
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript compiler

## Configuration

### Supabase Setup

1. Create a new Supabase project
2. Set up authentication providers
3. Create database tables for users, subscriptions, and analytics
4. Add environment variables

### Stripe Setup

1. Create Stripe account and get API keys
2. Set up webhook endpoints
3. Configure subscription products and prices
4. Add environment variables

## Deployment

The dashboard can be deployed to Vercel, Netlify, or any platform that supports Next.js.

### Vercel Deployment

1. Connect your repository to Vercel
2. Add environment variables in Vercel dashboard
3. Deploy automatically on each push

## API Integration

The dashboard integrates with the Dealvoy backend API for:

- Scraper management and monitoring
- User analytics and metrics
- Product data and insights
- Subscription and billing management

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

Private - Dealvoy Platform
