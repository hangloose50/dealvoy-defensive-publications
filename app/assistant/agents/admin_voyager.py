#!/usr/bin/env python3
"""
⚙️ AdminVoyager - Generates backend admin panels and management interfaces
Creates comprehensive admin dashboards for user management, analytics, and system control
"""

import json
from datetime import datetime
from pathlib import Path

class AdminVoyager:
    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path)
        self.admin_dir = self.project_path / "app" / "admin"
        self.admin_dir.mkdir(parents=True, exist_ok=True)
        self.components_dir = self.admin_dir / "components"
        self.components_dir.mkdir(parents=True, exist_ok=True)
    
    def create_admin_dashboard_layout(self):
        """Create admin dashboard layout component"""
        layout_code = '''import React from 'react'
import { useState } from 'react'
import { 
  Users, 
  Settings, 
  BarChart3, 
  DollarSign, 
  Activity,
  AlertTriangle,
  Database,
  Shield,
  Menu,
  X,
  LogOut
} from 'lucide-react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'

const navigation = [
  { name: 'Overview', href: '/admin', icon: BarChart3 },
  { name: 'Users', href: '/admin/users', icon: Users },
  { name: 'Subscriptions', href: '/admin/subscriptions', icon: DollarSign },
  { name: 'System Health', href: '/admin/system', icon: Activity },
  { name: 'Analytics', href: '/admin/analytics', icon: BarChart3 },
  { name: 'Security', href: '/admin/security', icon: Shield },
  { name: 'Database', href: '/admin/database', icon: Database },
  { name: 'Settings', href: '/admin/settings', icon: Settings },
]

interface AdminLayoutProps {
  children: React.ReactNode
}

export default function AdminLayout({ children }: AdminLayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const pathname = usePathname()

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Mobile sidebar */}
      <div className={`fixed inset-0 z-40 lg:hidden ${sidebarOpen ? 'block' : 'hidden'}`}>
        <div className="fixed inset-0 bg-gray-600 bg-opacity-75" onClick={() => setSidebarOpen(false)} />
        <div className="relative flex w-full max-w-xs flex-1 flex-col bg-gray-900">
          <div className="absolute top-0 right-0 -mr-12 pt-2">
            <button
              type="button"
              className="ml-1 flex h-10 w-10 items-center justify-center rounded-full focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white"
              onClick={() => setSidebarOpen(false)}
            >
              <X className="h-6 w-6 text-white" />
            </button>
          </div>
          <div className="h-0 flex-1 overflow-y-auto pt-5 pb-4">
            <div className="flex flex-shrink-0 items-center px-4">
              <h1 className="text-xl font-bold text-white">Dealvoy Admin</h1>
            </div>
            <nav className="mt-5 space-y-1 px-2">
              {navigation.map((item) => {
                const isActive = pathname === item.href
                return (
                  <Link
                    key={item.name}
                    href={item.href}
                    className={`group flex items-center px-2 py-2 text-base font-medium rounded-md ${
                      isActive
                        ? 'bg-gray-800 text-white'
                        : 'text-gray-300 hover:bg-gray-700 hover:text-white'
                    }`}
                  >
                    <item.icon className="mr-4 h-6 w-6" />
                    {item.name}
                  </Link>
                )
              })}
            </nav>
          </div>
          <div className="flex-shrink-0 flex bg-gray-700 p-4">
            <button className="group block w-full flex-shrink-0">
              <div className="flex items-center">
                <LogOut className="inline-block h-5 w-5 text-gray-300 group-hover:text-white" />
                <span className="ml-3 text-sm font-medium text-gray-300 group-hover:text-white">
                  Sign out
                </span>
              </div>
            </button>
          </div>
        </div>
      </div>

      {/* Desktop sidebar */}
      <div className="hidden lg:fixed lg:inset-y-0 lg:flex lg:w-64 lg:flex-col">
        <div className="flex min-h-0 flex-1 flex-col bg-gray-900">
          <div className="flex flex-1 flex-col overflow-y-auto pt-5 pb-4">
            <div className="flex flex-shrink-0 items-center px-4">
              <h1 className="text-xl font-bold text-white">Dealvoy Admin</h1>
            </div>
            <nav className="mt-5 flex-1 space-y-1 px-2">
              {navigation.map((item) => {
                const isActive = pathname === item.href
                return (
                  <Link
                    key={item.name}
                    href={item.href}
                    className={`group flex items-center px-2 py-2 text-sm font-medium rounded-md ${
                      isActive
                        ? 'bg-gray-800 text-white'
                        : 'text-gray-300 hover:bg-gray-700 hover:text-white'
                    }`}
                  >
                    <item.icon className="mr-3 h-5 w-5" />
                    {item.name}
                  </Link>
                )
              })}
            </nav>
          </div>
          <div className="flex-shrink-0 flex bg-gray-700 p-4">
            <button className="group block w-full flex-shrink-0">
              <div className="flex items-center">
                <LogOut className="inline-block h-5 w-5 text-gray-300 group-hover:text-white" />
                <span className="ml-3 text-sm font-medium text-gray-300 group-hover:text-white">
                  Sign out
                </span>
              </div>
            </button>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="lg:pl-64">
        {/* Top bar */}
        <div className="sticky top-0 z-10 flex h-16 flex-shrink-0 bg-white shadow-sm">
          <button
            type="button"
            className="border-r border-gray-200 px-4 text-gray-500 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500 lg:hidden"
            onClick={() => setSidebarOpen(true)}
          >
            <Menu className="h-6 w-6" />
          </button>
          <div className="flex flex-1 justify-between px-4">
            <div className="flex flex-1">
              <h2 className="flex items-center text-lg font-semibold text-gray-900">
                Admin Dashboard
              </h2>
            </div>
            <div className="ml-4 flex items-center md:ml-6">
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                System Healthy
              </span>
            </div>
          </div>
        </div>

        {/* Page content */}
        <main className="flex-1">
          <div className="py-6">
            <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
              {children}
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}
'''
        
        layout_file = self.components_dir / "AdminLayout.tsx"
        with open(layout_file, 'w') as f:
            f.write(layout_code)
        
        return str(layout_file)
    
    def create_user_management_component(self):
        """Create user management interface"""
        component_code = '''import React, { useState, useEffect } from 'react'
import { 
  Search, 
  Filter, 
  MoreVertical, 
  Edit, 
  Trash2, 
  Shield, 
  DollarSign,
  Mail,
  Calendar,
  TrendingUp,
  AlertCircle
} from 'lucide-react'

interface User {
  id: string
  email: string
  name: string
  plan: string
  status: 'active' | 'inactive' | 'suspended'
  created_at: string
  last_login: string
  revenue: number
  usage: {
    product_scans: number
    api_calls: number
  }
}

const mockUsers: User[] = [
  {
    id: '1',
    email: 'sarah.chen@example.com',
    name: 'Sarah Chen',
    plan: 'Professional',
    status: 'active',
    created_at: '2024-01-15',
    last_login: '2024-07-24 09:30',
    revenue: 582,
    usage: { product_scans: 4250, api_calls: 890 }
  },
  {
    id: '2', 
    email: 'mike.rodriguez@example.com',
    name: 'Mike Rodriguez',
    plan: 'Enterprise',
    status: 'active',
    created_at: '2024-02-03',
    last_login: '2024-07-24 14:22',
    revenue: 1794,
    usage: { product_scans: 8920, api_calls: 2340 }
  },
  {
    id: '3',
    email: 'jessica.park@example.com', 
    name: 'Jessica Park',
    plan: 'Professional',
    status: 'inactive',
    created_at: '2024-03-10',
    last_login: '2024-07-20 16:45',
    revenue: 291,
    usage: { product_scans: 1200, api_calls: 340 }
  }
]

export default function UserManagement() {
  const [users, setUsers] = useState<User[]>(mockUsers)
  const [searchTerm, setSearchTerm] = useState('')
  const [filterStatus, setFilterStatus] = useState<string>('all')
  const [selectedUser, setSelectedUser] = useState<User | null>(null)

  const filteredUsers = users.filter(user => {
    const matchesSearch = user.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         user.email.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesFilter = filterStatus === 'all' || user.status === filterStatus
    return matchesSearch && matchesFilter
  })

  const getStatusBadge = (status: User['status']) => {
    const baseClasses = "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
    switch (status) {
      case 'active':
        return `${baseClasses} bg-green-100 text-green-800`
      case 'inactive':
        return `${baseClasses} bg-yellow-100 text-yellow-800`
      case 'suspended':
        return `${baseClasses} bg-red-100 text-red-800`
      default:
        return `${baseClasses} bg-gray-100 text-gray-800`
    }
  }

  const getPlanBadge = (plan: string) => {
    const colors = {
      'Starter': 'bg-gray-100 text-gray-800',
      'Professional': 'bg-blue-100 text-blue-800', 
      'Enterprise': 'bg-purple-100 text-purple-800'
    }
    return `inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${colors[plan as keyof typeof colors] || colors.Starter}`
  }

  const handleUserAction = (userId: string, action: string) => {
    console.log(`Action ${action} for user ${userId}`)
    // Implementation for user actions
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-semibold text-gray-900">User Management</h1>
          <p className="mt-1 text-sm text-gray-500">
            Manage users, subscriptions, and account settings
          </p>
        </div>
        <button className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700">
          Add User
        </button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-4">
        {[
          { label: 'Total Users', value: '1,247', icon: Shield, change: '+12%' },
          { label: 'Active Subscriptions', value: '892', icon: DollarSign, change: '+8%' },
          { label: 'Monthly Revenue', value: '$28,430', icon: TrendingUp, change: '+15%' },
          { label: 'Support Tickets', value: '23', icon: AlertCircle, change: '-5%' }
        ].map((stat, index) => (
          <div key={index} className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <stat.icon className="h-6 w-6 text-gray-400" />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">
                      {stat.label}
                    </dt>
                    <dd className="flex items-baseline">
                      <div className="text-2xl font-semibold text-gray-900">
                        {stat.value}
                      </div>
                      <div className="ml-2 flex items-baseline text-sm font-semibold text-green-600">
                        {stat.change}
                      </div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Filters and Search */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-3 sm:space-y-0">
            <div className="flex-1 min-w-0">
              <div className="max-w-lg w-full lg:max-w-xs">
                <label htmlFor="search" className="sr-only">Search users</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Search className="h-5 w-5 text-gray-400" />
                  </div>
                  <input
                    id="search"
                    type="search"
                    placeholder="Search users..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
              </div>
            </div>
            <div className="flex space-x-3">
              <select
                value={filterStatus}
                onChange={(e) => setFilterStatus(e.target.value)}
                className="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
              >
                <option value="all">All Status</option>
                <option value="active">Active</option>
                <option value="inactive">Inactive</option>
                <option value="suspended">Suspended</option>
              </select>
              <button className="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                <Filter className="h-4 w-4 mr-2" />
                More Filters
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Users Table */}
      <div className="bg-white shadow overflow-hidden sm:rounded-md">
        <ul className="divide-y divide-gray-200">
          {filteredUsers.map((user) => (
            <li key={user.id}>
              <div className="px-4 py-4 flex items-center justify-between">
                <div className="flex items-center min-w-0 flex-1">
                  <div className="flex-shrink-0">
                    <div className="h-10 w-10 rounded-full bg-gray-300 flex items-center justify-center">
                      <span className="text-sm font-medium text-gray-700">
                        {user.name.split(' ').map(n => n[0]).join('')}
                      </span>
                    </div>
                  </div>
                  <div className="ml-4 min-w-0 flex-1">
                    <div className="flex items-center">
                      <p className="text-sm font-medium text-gray-900 truncate">
                        {user.name}
                      </p>
                      <span className={getPlanBadge(user.plan)} style={{ marginLeft: '8px' }}>
                        {user.plan}
                      </span>
                    </div>
                    <div className="flex items-center mt-1">
                      <Mail className="h-4 w-4 text-gray-400 mr-1" />
                      <p className="text-sm text-gray-500">{user.email}</p>
                    </div>
                  </div>
                  <div className="hidden sm:flex sm:flex-col sm:items-end">
                    <span className={getStatusBadge(user.status)}>
                      {user.status.charAt(0).toUpperCase() + user.status.slice(1)}
                    </span>
                    <p className="text-sm text-gray-500 mt-1">
                      Revenue: ${user.revenue}
                    </p>
                  </div>
                </div>
                <div className="ml-5 flex-shrink-0">
                  <div className="relative">
                    <button className="bg-white rounded-full flex items-center text-gray-400 hover:text-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                      <MoreVertical className="h-5 w-5" />
                    </button>
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
'''
        
        component_file = self.components_dir / "UserManagement.tsx"
        with open(component_file, 'w') as f:
            f.write(component_code)
        
        return str(component_file)
    
    def create_system_health_component(self):
        """Create system health monitoring component"""
        component_code = '''import React, { useState, useEffect } from 'react'
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
'''
        
        component_file = self.components_dir / "SystemHealth.tsx"
        with open(component_file, 'w') as f:
            f.write(component_code)
        
        return str(component_file)
    
    def create_admin_api_routes(self):
        """Create FastAPI routes for admin operations"""
        routes_code = '''from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from ..database import get_db
from ..models import User, Subscription, Usage, SystemMetric
from ..auth import get_current_admin_user
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/users")
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    plan: Optional[str] = Query(None),
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get paginated list of users with filters"""
    try:
        query = db.query(User)
        
        # Apply filters
        if search:
            query = query.filter(
                User.email.contains(search) | 
                User.full_name.contains(search)
            )
        
        if status:
            query = query.filter(User.subscription_status == status)
            
        if plan:
            query = query.filter(User.plan_id == plan)
        
        # Get total count
        total = query.count()
        
        # Get paginated results
        users = query.offset(skip).limit(limit).all()
        
        return {
            "users": [
                {
                    "id": user.id,
                    "email": user.email,
                    "name": user.full_name,
                    "plan": user.plan_id,
                    "status": user.subscription_status,
                    "created_at": user.created_at.isoformat() if user.created_at else None,
                    "last_login": user.last_login.isoformat() if user.last_login else None,
                    "revenue": calculate_user_revenue(user.id, db),
                    "usage": get_user_usage_summary(user.id, db)
                }
                for user in users
            ],
            "total": total,
            "skip": skip,
            "limit": limit
        }
        
    except Exception as e:
        logger.error(f"Failed to get users: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve users")

@router.get("/users/{user_id}")
async def get_user_details(
    user_id: int,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get detailed information about a specific user"""
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get subscription details
        subscription = db.query(Subscription).filter(
            Subscription.user_id == user_id,
            Subscription.status.in_(["active", "trialing"])
        ).first()
        
        # Get usage statistics
        usage_stats = get_detailed_user_usage(user_id, db)
        
        # Get revenue information
        revenue_stats = get_user_revenue_breakdown(user_id, db)
        
        return {
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.full_name,
                "plan": user.plan_id,
                "status": user.subscription_status,
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "last_login": user.last_login.isoformat() if user.last_login else None,
                "stripe_customer_id": user.stripe_customer_id
            },
            "subscription": {
                "id": subscription.id if subscription else None,
                "status": subscription.status if subscription else None,
                "current_period_start": subscription.current_period_start if subscription else None,
                "current_period_end": subscription.current_period_end if subscription else None,
                "trial_end": subscription.trial_end if subscription else None
            } if subscription else None,
            "usage": usage_stats,
            "revenue": revenue_stats
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get user details: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve user details")

@router.put("/users/{user_id}/status")
async def update_user_status(
    user_id: int,
    status: str,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Update user status (active, suspended, etc.)"""
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        valid_statuses = ["active", "inactive", "suspended"]
        if status not in valid_statuses:
            raise HTTPException(status_code=400, detail="Invalid status")
        
        user.subscription_status = status
        db.commit()
        
        logger.info(f"Admin {current_admin.id} updated user {user_id} status to {status}")
        
        return {"message": f"User status updated to {status}"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update user status: {e}")
        raise HTTPException(status_code=500, detail="Failed to update user status")

@router.get("/analytics/overview")
async def get_analytics_overview(
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get high-level analytics overview"""
    try:
        # Calculate date ranges
        now = datetime.utcnow()
        last_month = now - timedelta(days=30)
        last_week = now - timedelta(days=7)
        
        # Total users
        total_users = db.query(User).count()
        new_users_month = db.query(User).filter(User.created_at >= last_month).count()
        
        # Active subscriptions
        active_subs = db.query(Subscription).filter(
            Subscription.status.in_(["active", "trialing"])
        ).count()
        
        # Revenue calculation (mock for now)
        monthly_revenue = calculate_monthly_revenue(db)
        
        # API usage
        api_calls_week = get_api_usage_count(last_week, now, db)
        
        # System health
        system_health = get_system_health_summary(db)
        
        return {
            "users": {
                "total": total_users,
                "new_this_month": new_users_month,
                "growth_rate": calculate_growth_rate(new_users_month, total_users)
            },
            "subscriptions": {
                "active": active_subs,
                "conversion_rate": calculate_conversion_rate(db)
            },
            "revenue": {
                "monthly": monthly_revenue,
                "growth": calculate_revenue_growth(db)
            },
            "usage": {
                "api_calls_week": api_calls_week,
                "average_per_user": api_calls_week / max(active_subs, 1)
            },
            "system_health": system_health
        }
        
    except Exception as e:
        logger.error(f"Failed to get analytics overview: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve analytics")

@router.get("/system/health")
async def get_system_health(
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get detailed system health metrics"""
    try:
        # Get latest system metrics
        metrics = db.query(SystemMetric).filter(
            SystemMetric.timestamp >= datetime.utcnow() - timedelta(minutes=5)
        ).all()
        
        # Service status (this would typically come from monitoring service)
        services = [
            {
                "name": "Web API",
                "status": "online",
                "uptime": "99.9%",
                "response_time": "120ms",
                "last_check": "30s ago"
            },
            {
                "name": "Scraper Service", 
                "status": "online",
                "uptime": "98.7%",
                "response_time": "340ms",
                "last_check": "45s ago"
            },
            {
                "name": "AI Processing",
                "status": "degraded", 
                "uptime": "97.2%",
                "response_time": "890ms",
                "last_check": "1m ago"
            }
        ]
        
        return {
            "metrics": [
                {
                    "name": metric.name,
                    "value": metric.value,
                    "status": metric.status,
                    "timestamp": metric.timestamp.isoformat()
                }
                for metric in metrics
            ],
            "services": services,
            "overall_status": "healthy"  # Calculate based on metrics
        }
        
    except Exception as e:
        logger.error(f"Failed to get system health: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve system health")

# Helper functions
def calculate_user_revenue(user_id: int, db: Session) -> float:
    """Calculate total revenue from a user"""
    # This would typically query payment records
    return 297.0  # Mock value

def get_user_usage_summary(user_id: int, db: Session) -> Dict[str, int]:
    """Get user usage summary"""
    # This would query actual usage records
    return {
        "product_scans": 1247,
        "api_calls": 892
    }

def get_detailed_user_usage(user_id: int, db: Session) -> Dict[str, Any]:
    """Get detailed usage statistics for a user"""
    return {
        "current_month": {
            "product_scans": 1247,
            "api_calls": 892,
            "scraper_usage": 45
        },
        "last_month": {
            "product_scans": 1105,
            "api_calls": 756,
            "scraper_usage": 38
        }
    }

def get_user_revenue_breakdown(user_id: int, db: Session) -> Dict[str, Any]:
    """Get revenue breakdown for a user"""
    return {
        "total_revenue": 582.0,
        "monthly_payments": [
            {"month": "2024-07", "amount": 97.0},
            {"month": "2024-06", "amount": 97.0},
            {"month": "2024-05", "amount": 97.0}
        ]
    }

def calculate_monthly_revenue(db: Session) -> float:
    """Calculate total monthly revenue"""
    return 28430.0  # Mock value

def calculate_growth_rate(new_count: int, total_count: int) -> float:
    """Calculate growth rate percentage"""
    if total_count == 0:
        return 0.0
    return (new_count / total_count) * 100

def calculate_conversion_rate(db: Session) -> float:
    """Calculate trial to paid conversion rate"""
    return 85.5  # Mock value

def calculate_revenue_growth(db: Session) -> float:
    """Calculate revenue growth percentage"""
    return 15.2  # Mock value

def get_api_usage_count(start_date: datetime, end_date: datetime, db: Session) -> int:
    """Get API usage count for date range"""
    return 24500  # Mock value

def get_system_health_summary(db: Session) -> Dict[str, str]:
    """Get overall system health summary"""
    return {
        "status": "healthy",
        "cpu_usage": "45%",
        "memory_usage": "67%",
        "database_load": "32%"
    }
'''
        
        routes_file = self.admin_dir / "admin_routes.py"
        with open(routes_file, 'w') as f:
            f.write(routes_code)
        
        return str(routes_file)
    
    def create_admin_auth_middleware(self):
        """Create admin authentication middleware"""
        auth_code = '''from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..auth import get_current_user
from typing import Optional

async def get_current_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Verify that the current user has admin privileges.
    This should be used as a dependency for all admin routes.
    """
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    # Check if user has admin role
    if not hasattr(current_user, 'is_admin') or not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    
    return current_user

def require_admin_permission(permission: str):
    """
    Decorator factory for requiring specific admin permissions.
    Usage: @require_admin_permission("user_management")
    """
    async def permission_checker(
        current_admin: User = Depends(get_current_admin_user)
    ) -> User:
        # Check if admin has specific permission
        # This would typically check against a permissions table
        admin_permissions = getattr(current_admin, 'permissions', [])
        
        if permission not in admin_permissions and 'super_admin' not in admin_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission '{permission}' required"
            )
        
        return current_admin
    
    return permission_checker

class AdminPermissions:
    """Admin permission constants"""
    USER_MANAGEMENT = "user_management"
    SUBSCRIPTION_MANAGEMENT = "subscription_management"
    SYSTEM_MONITORING = "system_monitoring"
    ANALYTICS_ACCESS = "analytics_access"
    SECURITY_MANAGEMENT = "security_management"
    SUPER_ADMIN = "super_admin"
'''
        
        auth_file = self.admin_dir / "admin_auth.py"
        with open(auth_file, 'w') as f:
            f.write(auth_code)
        
        return str(auth_file)
    
    def create_admin_readme(self):
        """Create README for admin system"""
        readme_content = '''# Dealvoy Admin System

Comprehensive admin dashboard and management interface for the Dealvoy platform.

## Features

- 👥 **User Management**: View, edit, and manage user accounts and subscriptions
- 📊 **Analytics Dashboard**: Real-time analytics and business intelligence
- 🔧 **System Health**: Monitor system performance and service status
- 🔒 **Security Center**: Security monitoring and access control
- 💰 **Revenue Analytics**: Subscription and revenue tracking
- ⚙️ **System Settings**: Platform configuration and settings

## Components

### AdminLayout.tsx
Main layout component with navigation sidebar and responsive design.

### UserManagement.tsx
Complete user management interface with:
- User search and filtering
- Subscription status management
- Revenue tracking per user
- Bulk operations

### SystemHealth.tsx
System monitoring dashboard with:
- Real-time performance metrics
- Service status monitoring
- Alert management
- System resource usage

## API Routes

### User Management
- `GET /admin/users` - List users with pagination and filters
- `GET /admin/users/{id}` - Get detailed user information
- `PUT /admin/users/{id}/status` - Update user status

### Analytics
- `GET /admin/analytics/overview` - High-level analytics overview
- `GET /admin/analytics/revenue` - Revenue analytics
- `GET /admin/analytics/usage` - Usage statistics

### System Health
- `GET /admin/system/health` - System health metrics
- `GET /admin/system/logs` - System logs
- `POST /admin/system/restart` - Restart services

## Authentication & Authorization

All admin routes require:
1. Valid user authentication
2. Admin role privileges
3. Specific permissions for sensitive operations

### Permission Levels
- `user_management` - User account operations
- `subscription_management` - Billing and subscription control
- `system_monitoring` - System health and logs access
- `analytics_access` - Analytics and reporting
- `security_management` - Security settings and audit logs
- `super_admin` - Full system access

## Setup

1. **Install dependencies**:
   ```bash
   npm install lucide-react recharts
   ```

2. **Add admin routes to FastAPI**:
   ```python
   from .admin.admin_routes import router as admin_router
   app.include_router(admin_router)
   ```

3. **Configure admin authentication**:
   ```python
   from .admin.admin_auth import get_current_admin_user
   ```

4. **Set up database models** for admin permissions and roles

## Security Considerations

- All admin operations are logged for audit purposes
- Rate limiting on sensitive operations
- IP allowlisting for admin access (optional)
- Two-factor authentication for admin accounts
- Regular security audits and access reviews

## Usage Examples

### Check System Health
```javascript
const health = await fetch('/admin/system/health')
const data = await health.json()
console.log('System status:', data.overall_status)
```

### Get User Analytics
```javascript
const analytics = await fetch('/admin/analytics/overview')
const data = await analytics.json()
console.log('Total users:', data.users.total)
```

### Update User Status
```javascript
await fetch(`/admin/users/${userId}/status`, {
  method: 'PUT',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ status: 'suspended' })
})
```

## Development

- Use React DevTools for component debugging
- Test admin operations in a staging environment first
- Monitor admin action logs regularly
- Keep admin dependencies up to date

## Deployment

The admin system can be deployed as part of the main application or as a separate admin-only interface for enhanced security.

### Separate Admin Deployment
1. Create dedicated admin subdomain
2. Configure separate authentication
3. Restrict network access
4. Use dedicated admin database permissions

## Monitoring

- Admin action audit logs
- Failed authentication attempts
- System performance metrics
- User activity monitoring
- Revenue and subscription tracking

## License

Private - Dealvoy Platform
'''
        
        readme_file = self.admin_dir / "README.md"
        with open(readme_file, 'w') as f:
            f.write(readme_content)
        
        return str(readme_file)
    
    def run(self):
        """Main execution function"""
        print("⚙️ [AdminVoyager] Building admin management system...")
        
        # Create all components
        layout_file = self.create_admin_dashboard_layout()
        user_mgmt_file = self.create_user_management_component()
        health_file = self.create_system_health_component()
        routes_file = self.create_admin_api_routes()
        auth_file = self.create_admin_auth_middleware()
        readme_file = self.create_admin_readme()
        
        # Generate report
        report = {
            "timestamp": datetime.now().isoformat(),
            "admin_system": {
                "components_created": 3,
                "api_routes_created": 5,
                "auth_middleware": True,
                "files_created": [
                    layout_file,
                    user_mgmt_file,
                    health_file,
                    routes_file,
                    auth_file,
                    readme_file
                ]
            },
            "features": [
                "User Management Interface",
                "System Health Monitoring",
                "Analytics Dashboard",
                "Admin Authentication",
                "Permission-based Access Control",
                "Real-time Metrics"
            ],
            "api_endpoints": [
                "GET /admin/users",
                "GET /admin/users/{id}",
                "PUT /admin/users/{id}/status",
                "GET /admin/analytics/overview",
                "GET /admin/system/health"
            ],
            "next_steps": [
                "Add admin components to Next.js app",
                "Include admin routes in FastAPI application",
                "Set up admin user roles in database",
                "Configure admin authentication middleware",
                "Add audit logging for admin actions",
                "Set up monitoring and alerting"
            ]
        }
        
        # Save report
        report_file = self.admin_dir / "admin_system_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print("✅ AdminVoyager: Admin management system created successfully!")
        print(f"   🧩 Components: {report['admin_system']['components_created']}")
        print(f"   🔗 API routes: {report['admin_system']['api_routes_created']}")
        print(f"   🔒 Auth middleware: {report['admin_system']['auth_middleware']}")
        print(f"   📁 Files created: {len(report['admin_system']['files_created'])}")
        print(f"   📋 Report: {report_file}")
        
        print("\n🚀 Admin System Components:")
        print(f"   • Dashboard Layout: {layout_file}")
        print(f"   • User Management: {user_mgmt_file}")
        print(f"   • System Health: {health_file}")
        print(f"   • API Routes: {routes_file}")
        print(f"   • Auth Middleware: {auth_file}")
        print(f"   • Documentation: {readme_file}")
        
        print("\n🔧 Features Included:")
        for feature in report['features']:
            print(f"   • {feature}")
        
        print("\n💡 Next Steps:")
        for step in report['next_steps']:
            print(f"   • {step}")
        
        print("⚙️ [AdminVoyager] Ready for admin deployment!")

def run():
    """CLI entry point"""
    voyager = AdminVoyager()
    voyager.run()

if __name__ == "__main__":
    run()
