'use client'

import React, { useState, useEffect } from 'react'
import { 
  Play, 
  Pause, 
  RotateCcw, 
  Activity,
  AlertCircle,
  CheckCircle,
  Clock
} from 'lucide-react'

interface Scraper {
  id: string
  name: string
  status: 'running' | 'stopped' | 'error' | 'idle'
  lastRun: string
  itemsProcessed: number
  successRate: number
  source: string
}

const mockScrapers: Scraper[] = [
  {
    id: 'amazon-1',
    name: 'Amazon Product Scraper',
    status: 'running',
    lastRun: '2 minutes ago',
    itemsProcessed: 1247,
    successRate: 98.5,
    source: 'Amazon'
  },
  {
    id: 'walmart-1',
    name: 'Walmart Price Monitor',
    status: 'idle',
    lastRun: '15 minutes ago',
    itemsProcessed: 892,
    successRate: 95.2,
    source: 'Walmart'
  },
  {
    id: 'costco-1',
    name: 'Costco Inventory Tracker',
    status: 'error',
    lastRun: '1 hour ago',
    itemsProcessed: 234,
    successRate: 87.1,
    source: 'Costco'
  }
]

export default function ScraperControl() {
  const [scrapers, setScrapers] = useState<Scraper[]>(mockScrapers)
  const [selectedScraper, setSelectedScraper] = useState<string | null>(null)

  const getStatusIcon = (status: Scraper['status']) => {
    switch (status) {
      case 'running':
        return <Activity className="h-5 w-5 text-green-500 animate-pulse" />
      case 'stopped':
        return <Pause className="h-5 w-5 text-gray-500" />
      case 'error':
        return <AlertCircle className="h-5 w-5 text-red-500" />
      case 'idle':
        return <Clock className="h-5 w-5 text-yellow-500" />
      default:
        return <Clock className="h-5 w-5 text-gray-500" />
    }
  }

  const getStatusBadge = (status: Scraper['status']) => {
    const baseClasses = "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
    switch (status) {
      case 'running':
        return `${baseClasses} bg-green-100 text-green-800`
      case 'stopped':
        return `${baseClasses} bg-gray-100 text-gray-800`
      case 'error':
        return `${baseClasses} bg-red-100 text-red-800`
      case 'idle':
        return `${baseClasses} bg-yellow-100 text-yellow-800`
      default:
        return `${baseClasses} bg-gray-100 text-gray-800`
    }
  }

  const handleScraperAction = (scraperId: string, action: 'start' | 'stop' | 'restart') => {
    setScrapers(prev => prev.map(scraper => {
      if (scraper.id === scraperId) {
        let newStatus: Scraper['status'] = scraper.status
        switch (action) {
          case 'start':
            newStatus = 'running'
            break
          case 'stop':
            newStatus = 'stopped'
            break
          case 'restart':
            newStatus = 'running'
            break
        }
        return { ...scraper, status: newStatus, lastRun: 'Just now' }
      }
      return scraper
    }))
  }

  return (
    <div className="bg-white shadow rounded-lg">
      <div className="px-4 py-5 sm:p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg leading-6 font-medium text-gray-900">
            Scraper Control Panel
          </h3>
          <button className="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
            Add Scraper
          </button>
        </div>

        <div className="space-y-4">
          {scrapers.map((scraper) => (
            <div key={scraper.id} className="border border-gray-200 rounded-lg p-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  {getStatusIcon(scraper.status)}
                  <div>
                    <h4 className="text-sm font-medium text-gray-900">{scraper.name}</h4>
                    <p className="text-sm text-gray-500">{scraper.source}</p>
                  </div>
                </div>
                
                <div className="flex items-center space-x-4">
                  <span className={getStatusBadge(scraper.status)}>
                    {scraper.status.charAt(0).toUpperCase() + scraper.status.slice(1)}
                  </span>
                  
                  <div className="flex space-x-2">
                    {scraper.status !== 'running' && (
                      <button
                        onClick={() => handleScraperAction(scraper.id, 'start')}
                        className="inline-flex items-center p-1 border border-transparent rounded text-green-600 hover:bg-green-50"
                      >
                        <Play className="h-4 w-4" />
                      </button>
                    )}
                    
                    {scraper.status === 'running' && (
                      <button
                        onClick={() => handleScraperAction(scraper.id, 'stop')}
                        className="inline-flex items-center p-1 border border-transparent rounded text-red-600 hover:bg-red-50"
                      >
                        <Pause className="h-4 w-4" />
                      </button>
                    )}
                    
                    <button
                      onClick={() => handleScraperAction(scraper.id, 'restart')}
                      className="inline-flex items-center p-1 border border-transparent rounded text-blue-600 hover:bg-blue-50"
                    >
                      <RotateCcw className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              </div>
              
              <div className="mt-3 grid grid-cols-3 gap-4 text-sm">
                <div>
                  <span className="text-gray-500">Last Run:</span>
                  <p className="font-medium">{scraper.lastRun}</p>
                </div>
                <div>
                  <span className="text-gray-500">Items Processed:</span>
                  <p className="font-medium">{scraper.itemsProcessed.toLocaleString()}</p>
                </div>
                <div>
                  <span className="text-gray-500">Success Rate:</span>
                  <p className="font-medium">{scraper.successRate}%</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
