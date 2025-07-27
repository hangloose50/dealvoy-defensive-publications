/**
 * Dealvoy Mobile App - Agent Manager Component
 * 
 * USPTO Patent Application #63/850,603
 * All rights reserved. Contains confidential and proprietary information.
 * 
 * Advanced interface for managing and monitoring 46 AI agents in real-time.
 */

import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  FlatList,
  TouchableOpacity,
  TextInput,
  RefreshControl,
  Alert,
  Switch,
  Modal,
} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';
import AgentViewModal from './AgentViewModal';

interface Agent {
  id: string;
  name: string;
  category: 'intelligence' | 'infrastructure' | 'optimization';
  status: 'active' | 'idle' | 'error' | 'maintenance';
  performance: number;
  lastRun: string;
  description: string;
  isEnabled: boolean;
  priority: 'high' | 'medium' | 'low';
  resourceUsage: number;
}

const AgentManager: React.FC = () => {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [filteredAgents, setFilteredAgents] = useState<Agent[]>([]);
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [refreshing, setRefreshing] = useState<boolean>(false);
  const [selectedAgent, setSelectedAgent] = useState<Agent | null>(null);
  const [modalVisible, setModalVisible] = useState<boolean>(false);

  useEffect(() => {
    loadAgents();
  }, []);

  useEffect(() => {
    filterAgents();
  }, [agents, searchQuery, selectedCategory]);

  const loadAgents = async () => {
    // Simulate loading all 46 agents
    const mockAgents: Agent[] = [
      {
        id: 'auto_optimizer_ai',
        name: 'Auto Optimizer AI',
        category: 'intelligence',
        status: 'active',
        performance: 94,
        lastRun: '2 min ago',
        description: 'AI-driven optimization with patent protection for automated performance enhancement',
        isEnabled: true,
        priority: 'high',
        resourceUsage: 75,
      },
      {
        id: 'category_ai',
        name: 'Category AI',
        category: 'intelligence',
        status: 'active',
        performance: 87,
        lastRun: '5 min ago',
        description: 'Product categorization with ML algorithms for intelligent taxonomy management',
        isEnabled: true,
        priority: 'high',
        resourceUsage: 62,
      },
      {
        id: 'cashflow_predictor_ai',
        name: 'Cash Flow Predictor',
        category: 'intelligence',
        status: 'active',
        performance: 92,
        lastRun: '1 min ago',
        description: 'Financial forecasting and cash flow analysis with predictive modeling',
        isEnabled: true,
        priority: 'high',
        resourceUsage: 68,
      },
      {
        id: 'claude_bridge_agent',
        name: 'Claude Bridge',
        category: 'intelligence',
        status: 'active',
        performance: 96,
        lastRun: '3 min ago',
        description: 'Claude AI integration for content generation and natural language processing',
        isEnabled: true,
        priority: 'high',
        resourceUsage: 82,
      },
      {
        id: 'api_gateway_monitor',
        name: 'API Gateway Monitor',
        category: 'infrastructure',
        status: 'active',
        performance: 89,
        lastRun: '1 min ago',
        description: 'API monitoring and health checks for system reliability',
        isEnabled: true,
        priority: 'medium',
        resourceUsage: 45,
      },
      {
        id: 'build_bot',
        name: 'Build Bot',
        category: 'infrastructure',
        status: 'idle',
        performance: 91,
        lastRun: '15 min ago',
        description: 'CI/CD automation with comprehensive testing and deployment',
        isEnabled: true,
        priority: 'medium',
        resourceUsage: 30,
      },
      {
        id: 'ab_price_tester',
        name: 'A/B Price Tester',
        category: 'optimization',
        status: 'active',
        performance: 85,
        lastRun: '4 min ago',
        description: 'A/B testing for pricing strategies with statistical analysis',
        isEnabled: true,
        priority: 'high',
        resourceUsage: 55,
      },
      {
        id: 'trend_ai',
        name: 'Trend AI',
        category: 'optimization',
        status: 'active',
        performance: 93,
        lastRun: '2 min ago',
        description: 'Trend analysis and prediction for market intelligence',
        isEnabled: true,
        priority: 'high',
        resourceUsage: 71,
      },
    ];

    setAgents(mockAgents);
  };

  const filterAgents = () => {
    let filtered = agents;

    if (selectedCategory !== 'all') {
      filtered = filtered.filter(agent => agent.category === selectedCategory);
    }

    if (searchQuery) {
      filtered = filtered.filter(agent =>
        agent.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        agent.description.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }

    setFilteredAgents(filtered);
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadAgents();
    setRefreshing(false);
  };

  const toggleAgent = (agentId: string) => {
    setAgents(prev => prev.map(agent =>
      agent.id === agentId ? { ...agent, isEnabled: !agent.isEnabled } : agent
    ));
  };

  const openAgentDetails = (agent: Agent) => {
    setSelectedAgent(agent);
    setModalVisible(true);
  };

  const getStatusColor = (status: string): string => {
    switch (status) {
      case 'active': return '#4CAF50';
      case 'idle': return '#FFC107';
      case 'error': return '#F44336';
      case 'maintenance': return '#9E9E9E';
      default: return '#9E9E9E';
    }
  };

  const getCategoryIcon = (category: string): string => {
    switch (category) {
      case 'intelligence': return 'psychology';
      case 'infrastructure': return 'storage';
      case 'optimization': return 'trending-up';
      default: return 'smart-toy';
    }
  };

  const renderAgentItem = ({ item }: { item: Agent }) => (
    <TouchableOpacity
      style={styles.agentCard}
      onPress={() => openAgentDetails(item)}
    >
      <View style={styles.agentHeader}>
        <View style={styles.agentTitleRow}>
          <Icon
            name={getCategoryIcon(item.category)}
            size={24}
            color="#0066cc"
            style={styles.categoryIcon}
          />
          <View style={styles.agentTitleContainer}>
            <Text style={styles.agentName}>{item.name}</Text>
            <Text style={styles.agentCategory}>{item.category}</Text>
          </View>
          <View style={styles.agentStatus}>
            <View style={[
              styles.statusDot,
              { backgroundColor: getStatusColor(item.status) }
            ]} />
            <Text style={styles.statusText}>{item.status}</Text>
          </View>
        </View>
        
        <View style={styles.agentControls}>
          <Switch
            value={item.isEnabled}
            onValueChange={() => toggleAgent(item.id)}
            trackColor={{ false: '#767577', true: '#81b0ff' }}
            thumbColor={item.isEnabled ? '#0066cc' : '#f4f3f4'}
          />
        </View>
      </View>

      <Text style={styles.agentDescription} numberOfLines={2}>
        {item.description}
      </Text>

      <View style={styles.agentMetrics}>
        <View style={styles.metricItem}>
          <Text style={styles.metricLabel}>Performance</Text>
          <Text style={styles.metricValue}>{item.performance}%</Text>
        </View>
        <View style={styles.metricItem}>
          <Text style={styles.metricLabel}>Resource Usage</Text>
          <Text style={styles.metricValue}>{item.resourceUsage}%</Text>
        </View>
        <View style={styles.metricItem}>
          <Text style={styles.metricLabel}>Last Run</Text>
          <Text style={styles.metricValue}>{item.lastRun}</Text>
        </View>
      </View>

      <View style={styles.progressBar}>
        <View
          style={[
            styles.progressFill,
            { width: `${item.performance}%` }
          ]}
        />
      </View>
    </TouchableOpacity>
  );

  const categories = [
    { key: 'all', label: 'All Agents' },
    { key: 'intelligence', label: 'Intelligence' },
    { key: 'infrastructure', label: 'Infrastructure' },
    { key: 'optimization', label: 'Optimization' },
  ];

  return (
    <SafeAreaView style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Agent Manager</Text>
        <Text style={styles.headerSubtitle}>
          {filteredAgents.length} of 46 agents
        </Text>
      </View>

      {/* Search and Filter */}
      <View style={styles.searchContainer}>
        <TextInput
          style={styles.searchInput}
          placeholder="Search agents..."
          value={searchQuery}
          onChangeText={setSearchQuery}
        />
        <Icon name="search" size={20} color="#666" style={styles.searchIcon} />
      </View>

      {/* Category Filter */}
      <View style={styles.categoryFilter}>
        {categories.map((category) => (
          <TouchableOpacity
            key={category.key}
            style={[
              styles.categoryButton,
              selectedCategory === category.key && styles.selectedCategoryButton
            ]}
            onPress={() => setSelectedCategory(category.key)}
          >
            <Text style={[
              styles.categoryButtonText,
              selectedCategory === category.key && styles.selectedCategoryButtonText
            ]}>
              {category.label}
            </Text>
          </TouchableOpacity>
        ))}
      </View>

      {/* Agent List */}
      <FlatList
        data={filteredAgents}
        renderItem={renderAgentItem}
        keyExtractor={(item) => item.id}
        style={styles.agentList}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
        showsVerticalScrollIndicator={false}
      />

      {/* Agent Details Modal */}
      {selectedAgent && (
        <AgentViewModal
          visible={modalVisible}
          agent={selectedAgent}
          onClose={() => setModalVisible(false)}
        />
      )}
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    padding: 20,
    backgroundColor: '#ffffff',
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
  },
  headerSubtitle: {
    fontSize: 14,
    color: '#666',
    marginTop: 4,
  },
  searchContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    margin: 16,
    backgroundColor: '#ffffff',
    borderRadius: 8,
    paddingHorizontal: 16,
    borderWidth: 1,
    borderColor: '#e0e0e0',
  },
  searchInput: {
    flex: 1,
    paddingVertical: 12,
    fontSize: 16,
    color: '#333',
  },
  searchIcon: {
    marginLeft: 8,
  },
  categoryFilter: {
    flexDirection: 'row',
    paddingHorizontal: 16,
    marginBottom: 16,
  },
  categoryButton: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
    backgroundColor: '#ffffff',
    marginRight: 8,
    borderWidth: 1,
    borderColor: '#e0e0e0',
  },
  selectedCategoryButton: {
    backgroundColor: '#0066cc',
    borderColor: '#0066cc',
  },
  categoryButtonText: {
    fontSize: 14,
    color: '#666',
    fontWeight: '500',
  },
  selectedCategoryButtonText: {
    color: '#ffffff',
  },
  agentList: {
    flex: 1,
    paddingHorizontal: 16,
  },
  agentCard: {
    backgroundColor: '#ffffff',
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  agentHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 12,
  },
  agentTitleRow: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  categoryIcon: {
    marginRight: 12,
  },
  agentTitleContainer: {
    flex: 1,
  },
  agentName: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
  },
  agentCategory: {
    fontSize: 12,
    color: '#666',
    textTransform: 'capitalize',
    marginTop: 2,
  },
  agentStatus: {
    flexDirection: 'row',
    alignItems: 'center',
    marginRight: 16,
  },
  statusDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    marginRight: 6,
  },
  statusText: {
    fontSize: 12,
    color: '#666',
    textTransform: 'capitalize',
  },
  agentControls: {
    alignItems: 'flex-end',
  },
  agentDescription: {
    fontSize: 14,
    color: '#666',
    lineHeight: 20,
    marginBottom: 16,
  },
  agentMetrics: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 12,
  },
  metricItem: {
    alignItems: 'center',
  },
  metricLabel: {
    fontSize: 12,
    color: '#666',
    marginBottom: 4,
  },
  metricValue: {
    fontSize: 14,
    fontWeight: '600',
    color: '#333',
  },
  progressBar: {
    height: 4,
    backgroundColor: '#e0e0e0',
    borderRadius: 2,
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    backgroundColor: '#4CAF50',
  },
});

export default AgentManager;
