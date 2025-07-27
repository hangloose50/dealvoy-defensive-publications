import React from 'react'
import DashboardLayout from '../../components/DashboardLayout'
import AnalyticsOverview from '../../components/AnalyticsOverview'
import ScraperControl from '../../components/ScraperControl'

export default function DashboardPage() {
  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-semibold text-gray-900">Dashboard</h1>
          <p className="mt-1 text-sm text-gray-500">
            Welcome to your Dealvoy control center
          </p>
        </div>
        
        <AnalyticsOverview />
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <ScraperControl />
          
          <div className="bg-white shadow rounded-lg p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
              Quick Actions
            </h3>
            <div className="space-y-3">
              <button className="w-full text-left px-4 py-3 border border-gray-200 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-primary-500">
                <div className="font-medium text-gray-900">Start New Scraping Job</div>
                <div className="text-sm text-gray-500">Launch a new product discovery session</div>
              </button>
              
              <button className="w-full text-left px-4 py-3 border border-gray-200 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-primary-500">
                <div className="font-medium text-gray-900">Analyze Profit Opportunities</div>
                <div className="text-sm text-gray-500">Get AI-powered deal recommendations</div>
              </button>
              
              <button className="w-full text-left px-4 py-3 border border-gray-200 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-primary-500">
                <div className="font-medium text-gray-900">Check Ungating Status</div>
                <div className="text-sm text-gray-500">Review Amazon category approval predictions</div>
              </button>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  )
}
