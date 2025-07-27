'use client'

import React from 'react'
import { 
  TrendingUp, 
  TrendingDown, 
  DollarSign, 
  ShoppingCart,
  Users,
  Activity
} from 'lucide-react'
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  BarChart,
  Bar
} from 'recharts'

const mockData = [
  { name: 'Jan', revenue: 4000, deals: 240, users: 100 },
  { name: 'Feb', revenue: 3000, deals: 198, users: 120 },
  { name: 'Mar', revenue: 5000, deals: 340, users: 150 },
  { name: 'Apr', revenue: 4500, deals: 290, users: 180 },
  { name: 'May', revenue: 6000, deals: 420, users: 220 },
  { name: 'Jun', revenue: 5500, deals: 380, users: 250 },
]

const stats = [
  {
    name: 'Total Revenue',
    value: '$28,000',
    change: '+12.5%',
    changeType: 'increase',
    icon: DollarSign,
  },
  {
    name: 'Active Deals',
    value: '1,870',
    change: '+8.2%',
    changeType: 'increase',
    icon: ShoppingCart,
  },
  {
    name: 'Active Users',
    value: '920',
    change: '+3.1%',
    changeType: 'increase',
    icon: Users,
  },
  {
    name: 'API Calls',
    value: '24.5K',
    change: '-2.4%',
    changeType: 'decrease',
    icon: Activity,
  },
]

export default function AnalyticsOverview() {
  return (
    <div className="space-y-6">
      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => {
          const Icon = stat.icon
          return (
            <div key={stat.name} className="bg-white overflow-hidden shadow rounded-lg">
              <div className="p-5">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <Icon className="h-6 w-6 text-gray-400" />
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">
                        {stat.name}
                      </dt>
                      <dd className="flex items-baseline">
                        <div className="text-2xl font-semibold text-gray-900">
                          {stat.value}
                        </div>
                        <div className={`ml-2 flex items-baseline text-sm font-semibold ${
                          stat.changeType === 'increase' 
                            ? 'text-green-600' 
                            : 'text-red-600'
                        }`}>
                          {stat.changeType === 'increase' ? (
                            <TrendingUp className="self-center flex-shrink-0 h-4 w-4" />
                          ) : (
                            <TrendingDown className="self-center flex-shrink-0 h-4 w-4" />
                          )}
                          <span className="ml-1">{stat.change}</span>
                        </div>
                      </dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>
          )
        })}
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Revenue Chart */}
        <div className="bg-white shadow rounded-lg p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
            Revenue Trend
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={mockData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Line 
                type="monotone" 
                dataKey="revenue" 
                stroke="#3b82f6" 
                strokeWidth={2}
                dot={{ fill: '#3b82f6', strokeWidth: 2, r: 4 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Deals Chart */}
        <div className="bg-white shadow rounded-lg p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
            Monthly Deals
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={mockData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="deals" fill="#10b981" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
            Recent Activity
          </h3>
          <div className="flow-root">
            <ul className="-mb-8">
              {[
                {
                  id: 1,
                  content: 'New user signed up for Pro plan',
                  time: '2 minutes ago',
                  type: 'user'
                },
                {
                  id: 2,
                  content: 'Amazon scraper processed 245 new products',
                  time: '5 minutes ago',
                  type: 'scraper'
                },
                {
                  id: 3,
                  content: 'Monthly revenue goal reached',
                  time: '1 hour ago',
                  type: 'revenue'
                },
                {
                  id: 4,
                  content: 'System backup completed successfully',
                  time: '2 hours ago',
                  type: 'system'
                }
              ].map((item, itemIdx, items) => (
                <li key={item.id}>
                  <div className="relative pb-8">
                    {itemIdx !== items.length - 1 ? (
                      <span
                        className="absolute top-4 left-4 -ml-px h-full w-0.5 bg-gray-200"
                        aria-hidden="true"
                      />
                    ) : null}
                    <div className="relative flex space-x-3">
                      <div>
                        <span className="h-8 w-8 rounded-full bg-primary-500 flex items-center justify-center ring-8 ring-white">
                          <Activity className="h-4 w-4 text-white" />
                        </span>
                      </div>
                      <div className="min-w-0 flex-1 pt-1.5 flex justify-between space-x-4">
                        <div>
                          <p className="text-sm text-gray-500">{item.content}</p>
                        </div>
                        <div className="text-right text-sm whitespace-nowrap text-gray-500">
                          <time>{item.time}</time>
                        </div>
                      </div>
                    </div>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}
