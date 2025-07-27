import React, { useState, useEffect } from 'react'
import { 
  Activity, 
  Server, 
  Database, 
  Zap, 
  AlertTriangle, 
  CheckCircle, 
  RefreshCw,
  Clock,
  TrendingUp,
  TrendingDown
} from 'lucide-react'

interface SystemMetric {
  name: string
  value: string
  status: 'healthy' | 'warning' | 'critical'
  change: string
  changeType: 'increase' | 'decrease'
  lastUpdated: string
}

interface ServiceStatus {
  name: string
  status: 'online' | 'offline' | 'degraded'
  uptime: string
  responseTime: string
  lastCheck: string
}

const mockMetrics: SystemMetric[] = [
  {
    name: 'CPU Usage',
    value: '45%',
    status: 'healthy',
    change: '+2%',
    changeType: 'increase',
    lastUpdated: '1 min ago'
  },
  {
    name: 'Memory Usage',
    value: '67%',
    status: 'warning',
    change: '+5%',
    changeType: 'increase',
    lastUpdated: '1 min ago'
  },
  {
    name: 'Database Load',
    value: '32%',
    status: 'healthy',
    change: '-3%',
    changeType: 'decrease',
    lastUpdated: '1 min ago'
  },
  {
    name: 'API Response Time',
    value: '245ms',
    status: 'healthy',
    change: '-12ms',
    changeType: 'decrease',
    lastUpdated: '1 min ago'
  }
]

const mockServices: ServiceStatus[] = [
  {
    name: 'Web API',
    status: 'online',
    uptime: '99.9%',
    responseTime: '120ms',
    lastCheck: '30s ago'
  },
  {
    name: 'Scraper Service',
    status: 'online', 
    uptime: '98.7%',
    responseTime: '340ms',
    lastCheck: '45s ago'
  },
  {
    name: 'AI Processing',
    status: 'degraded',
    uptime: '97.2%',
    responseTime: '890ms',
    lastCheck: '1m ago'
  },
  {
    name: 'Database',
    status: 'online',
    uptime: '99.8%',
    responseTime: '15ms',
    lastCheck: '20s ago'
  },
  {
    name: 'Redis Cache',
    status: 'online',
    uptime: '99.9%',
    responseTime: '2ms',
    lastCheck: '25s ago'
  },
  {
    name: 'File Storage',
    status: 'online',
    uptime: '99.5%',
    responseTime: '65ms',
    lastCheck: '40s ago'
  }
]

export default function SystemHealth() {
  const [metrics, setMetrics] = useState<SystemMetric[]>(mockMetrics)
  const [services, setServices] = useState<ServiceStatus[]>(mockServices)
  const [isRefreshing, setIsRefreshing] = useState(false)

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'healthy':
      case 'online':
        return <CheckCircle className="h-5 w-5 text-green-500" />
      case 'warning':
      case 'degraded':
        return <AlertTriangle className="h-5 w-5 text-yellow-500" />
      case 'critical':
      case 'offline':
        return <AlertTriangle className="h-5 w-5 text-red-500" />
      default:
        return <Activity className="h-5 w-5 text-gray-500" />
    }
  }

  const getStatusBadge = (status: string) => {
    const baseClasses = "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
    switch (status) {
      case 'healthy':
      case 'online':
        return `${baseClasses} bg-green-100 text-green-800`
      case 'warning':
      case 'degraded':
        return `${baseClasses} bg-yellow-100 text-yellow-800`
      case 'critical':
      case 'offline':
        return `${baseClasses} bg-red-100 text-red-800`
      default:
        return `${baseClasses} bg-gray-100 text-gray-800`
    }
  }

  const handleRefresh = async () => {
    setIsRefreshing(true)
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000))
    setIsRefreshing(false)
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-semibold text-gray-900">System Health</h1>
          <p className="mt-1 text-sm text-gray-500">
            Real-time monitoring of system performance and service status
          </p>
        </div>
        <button
          onClick={handleRefresh}
          disabled={isRefreshing}
          className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50"
        >
          <RefreshCw className={`h-4 w-4 mr-2 ${isRefreshing ? 'animate-spin' : ''}`} />
          Refresh
        </button>
      </div>

      {/* System Metrics */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {metrics.map((metric, index) => (
          <div key={index} className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  {getStatusIcon(metric.status)}
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">
                      {metric.name}
                    </dt>
                    <dd className="flex items-baseline">
                      <div className="text-2xl font-semibold text-gray-900">
                        {metric.value}
                      </div>
                      <div className={`ml-2 flex items-baseline text-sm font-semibold ${
                        metric.changeType === 'decrease' ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {metric.changeType === 'increase' ? (
                          <TrendingUp className="self-center flex-shrink-0 h-4 w-4" />
                        ) : (
                          <TrendingDown className="self-center flex-shrink-0 h-4 w-4" />
                        )}
                        <span className="ml-1">{metric.change}</span>
                      </div>
                    </dd>
                  </dl>
                </div>
              </div>
              <div className="mt-3">
                <div className="flex items-center text-sm text-gray-500">
                  <Clock className="h-4 w-4 mr-1" />
                  {metric.lastUpdated}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Service Status */}
      <div className="bg-white shadow overflow-hidden sm:rounded-md">
        <div className="px-4 py-5 sm:px-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900">
            Service Status
          </h3>
          <p className="mt-1 max-w-2xl text-sm text-gray-500">
            Current status of all system services and components
          </p>
        </div>
        <ul className="divide-y divide-gray-200">
          {services.map((service, index) => (
            <li key={index}>
              <div className="px-4 py-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    {getStatusIcon(service.status)}
                    <div className="ml-4">
                      <div className="flex items-center">
                        <p className="text-sm font-medium text-gray-900">
                          {service.name}
                        </p>
                        <span className={getStatusBadge(service.status)} style={{ marginLeft: '8px' }}>
                          {service.status.charAt(0).toUpperCase() + service.status.slice(1)}
                        </span>
                      </div>
                      <div className="flex items-center mt-1 space-x-4">
                        <span className="text-sm text-gray-500">
                          Uptime: {service.uptime}
                        </span>
                        <span className="text-sm text-gray-500">
                          Response: {service.responseTime}
                        </span>
                        <span className="text-sm text-gray-500">
                          Last check: {service.lastCheck}
                        </span>
                      </div>
                    </div>
                  </div>
                  <div className="flex space-x-2">
                    <button className="text-blue-600 hover:text-blue-900 text-sm font-medium">
                      View Logs
                    </button>
                    <button className="text-gray-600 hover:text-gray-900 text-sm font-medium">
                      Restart
                    </button>
                  </div>
                </div>
              </div>
            </li>
          ))}
        </ul>
      </div>

      {/* Recent Alerts */}
      <div className="bg-white shadow overflow-hidden sm:rounded-md">
        <div className="px-4 py-5 sm:px-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900">
            Recent Alerts
          </h3>
        </div>
        <ul className="divide-y divide-gray-200">
          {[
            {
              type: 'warning',
              message: 'Memory usage above 65% threshold',
              time: '5 minutes ago',
              resolved: false
            },
            {
              type: 'info',
              message: 'Scheduled maintenance completed successfully',
              time: '2 hours ago',
              resolved: true
            },
            {
              type: 'error',
              message: 'AI Processing service temporary slowdown',
              time: '4 hours ago',
              resolved: true
            }
          ].map((alert, index) => (
            <li key={index}>
              <div className="px-4 py-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    {alert.type === 'error' && <AlertTriangle className="h-5 w-5 text-red-500" />}
                    {alert.type === 'warning' && <AlertTriangle className="h-5 w-5 text-yellow-500" />}
                    {alert.type === 'info' && <CheckCircle className="h-5 w-5 text-blue-500" />}
                    <div className="ml-4">
                      <p className="text-sm font-medium text-gray-900">
                        {alert.message}
                      </p>
                      <p className="text-sm text-gray-500">{alert.time}</p>
                    </div>
                  </div>
                  <div>
                    {alert.resolved ? (
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                        Resolved
                      </span>
                    ) : (
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                        Active
                      </span>
                    )}
                  </div>
                </div>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}
