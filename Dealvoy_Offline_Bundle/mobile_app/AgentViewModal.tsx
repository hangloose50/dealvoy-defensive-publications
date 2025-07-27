/**
 * Dealvoy Mobile App - Agent View Modal Component
 * 
 * USPTO Patent Application #63/850,603
 * All rights reserved. Contains confidential and proprietary information.
 * 
 * Detailed modal view for individual AI agent monitoring and control.
 */

import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Modal,
  TouchableOpacity,
  ScrollView,
  Alert,
  Switch,
  ActivityIndicator,
  Dimensions,
} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';

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

interface LogEntry {
  id: string;
  timestamp: string;
  level: 'info' | 'warning' | 'error' | 'success';
  message: string;
}

interface AgentViewModalProps {
  visible: boolean;
  agent: Agent;
  onClose: () => void;
}

const { width } = Dimensions.get('window');

const AgentViewModal: React.FC<AgentViewModalProps> = ({ visible, agent, onClose }) => {
  const [activeTab, setActiveTab] = useState<'overview' | 'logs' | 'config'>('overview');
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [isRunning, setIsRunning] = useState<boolean>(false);
  const [agentState, setAgentState] = useState<Agent>(agent);

  useEffect(() => {
    if (visible) {
      setAgentState(agent);
      loadAgentLogs();
    }
  }, [visible, agent]);

  const loadAgentLogs = async () => {
    // Simulate loading agent logs
    const mockLogs: LogEntry[] = [
      {
        id: '1',
        timestamp: '2025-01-26 10:35:22',
        level: 'success',
        message: 'Agent optimization cycle completed successfully',
      },
      {
        id: '2',
        timestamp: '2025-01-26 10:32:15',
        level: 'info',
        message: 'Processing 1,247 product records',
      },
      {
        id: '3',
        timestamp: '2025-01-26 10:30:01',
        level: 'info',
        message: 'Agent started with high priority configuration',
      },
      {
        id: '4',
        timestamp: '2025-01-26 10:28:45',
        level: 'warning',
        message: 'Resource usage approaching 80% threshold',
      },
      {
        id: '5',
        timestamp: '2025-01-26 10:25:30',
        level: 'success',
        message: 'AI model training completed',
      },
    ];
    setLogs(mockLogs);
  };

  const runAgent = async () => {
    setIsRunning(true);
    try {
      // Simulate agent execution
      await new Promise(resolve => setTimeout(resolve, 3000));
      
      setAgentState(prev => ({
        ...prev,
        status: 'active',
        lastRun: 'Just now',
        performance: Math.min(100, prev.performance + Math.floor(Math.random() * 5)),
      }));

      Alert.alert('Success', `${agent.name} executed successfully`);
    } catch (error) {
      Alert.alert('Error', 'Failed to run agent');
    } finally {
      setIsRunning(false);
    }
  };

  const toggleAgent = () => {
    setAgentState(prev => ({ ...prev, isEnabled: !prev.isEnabled }));
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

  const getPriorityColor = (priority: string): string => {
    switch (priority) {
      case 'high': return '#F44336';
      case 'medium': return '#FFC107';
      case 'low': return '#4CAF50';
      default: return '#9E9E9E';
    }
  };

  const getLogLevelColor = (level: string): string => {
    switch (level) {
      case 'success': return '#4CAF50';
      case 'info': return '#2196F3';
      case 'warning': return '#FFC107';
      case 'error': return '#F44336';
      default: return '#9E9E9E';
    }
  };

  const renderOverviewTab = () => (
    <ScrollView style={styles.tabContent}>
      {/* Agent Status Card */}
      <View style={styles.statusCard}>
        <View style={styles.statusHeader}>
          <View style={styles.statusInfo}>
            <Text style={styles.statusTitle}>Current Status</Text>
            <View style={styles.statusRow}>
              <View style={[
                styles.statusDot,
                { backgroundColor: getStatusColor(agentState.status) }
              ]} />
              <Text style={styles.statusText}>{agentState.status.toUpperCase()}</Text>
            </View>
          </View>
          <Switch
            value={agentState.isEnabled}
            onValueChange={toggleAgent}
            trackColor={{ false: '#767577', true: '#81b0ff' }}
            thumbColor={agentState.isEnabled ? '#0066cc' : '#f4f3f4'}
          />
        </View>
      </View>

      {/* Performance Metrics */}
      <View style={styles.metricsCard}>
        <Text style={styles.cardTitle}>Performance Metrics</Text>
        
        <View style={styles.metricRow}>
          <View style={styles.metricItem}>
            <Text style={styles.metricLabel}>Performance</Text>
            <Text style={styles.metricValue}>{agentState.performance}%</Text>
            <View style={styles.progressBar}>
              <View style={[
                styles.progressFill,
                { width: `${agentState.performance}%`, backgroundColor: '#4CAF50' }
              ]} />
            </View>
          </View>
        </View>

        <View style={styles.metricRow}>
          <View style={styles.metricItem}>
            <Text style={styles.metricLabel}>Resource Usage</Text>
            <Text style={styles.metricValue}>{agentState.resourceUsage}%</Text>
            <View style={styles.progressBar}>
              <View style={[
                styles.progressFill,
                { 
                  width: `${agentState.resourceUsage}%`,
                  backgroundColor: agentState.resourceUsage > 80 ? '#F44336' : '#2196F3'
                }
              ]} />
            </View>
          </View>
        </View>

        <View style={styles.metricRow}>
          <View style={styles.metricItemHalf}>
            <Text style={styles.metricLabel}>Priority</Text>
            <View style={styles.priorityBadge}>
              <View style={[
                styles.priorityDot,
                { backgroundColor: getPriorityColor(agentState.priority) }
              ]} />
              <Text style={styles.priorityText}>{agentState.priority.toUpperCase()}</Text>
            </View>
          </View>
          <View style={styles.metricItemHalf}>
            <Text style={styles.metricLabel}>Last Run</Text>
            <Text style={styles.metricValue}>{agentState.lastRun}</Text>
          </View>
        </View>
      </View>

      {/* Agent Controls */}
      <View style={styles.controlsCard}>
        <Text style={styles.cardTitle}>Agent Controls</Text>
        
        <TouchableOpacity
          style={[styles.controlButton, styles.runButton]}
          onPress={runAgent}
          disabled={isRunning || !agentState.isEnabled}
        >
          {isRunning ? (
            <ActivityIndicator color="#ffffff" />
          ) : (
            <>
              <Icon name="play-arrow" size={20} color="#ffffff" />
              <Text style={styles.controlButtonText}>Run Agent</Text>
            </>
          )}
        </TouchableOpacity>

        <TouchableOpacity style={[styles.controlButton, styles.restartButton]}>
          <Icon name="refresh" size={20} color="#ffffff" />
          <Text style={styles.controlButtonText}>Restart Agent</Text>
        </TouchableOpacity>

        <TouchableOpacity style={[styles.controlButton, styles.stopButton]}>
          <Icon name="stop" size={20} color="#ffffff" />
          <Text style={styles.controlButtonText}>Stop Agent</Text>
        </TouchableOpacity>
      </View>

      {/* Agent Description */}
      <View style={styles.descriptionCard}>
        <Text style={styles.cardTitle}>Description</Text>
        <Text style={styles.descriptionText}>{agentState.description}</Text>
      </View>
    </ScrollView>
  );

  const renderLogsTab = () => (
    <ScrollView style={styles.tabContent}>
      <View style={styles.logsContainer}>
        <Text style={styles.cardTitle}>Recent Activity</Text>
        {logs.map((log) => (
          <View key={log.id} style={styles.logEntry}>
            <View style={styles.logHeader}>
              <View style={[
                styles.logLevelDot,
                { backgroundColor: getLogLevelColor(log.level) }
              ]} />
              <Text style={styles.logLevel}>{log.level.toUpperCase()}</Text>
              <Text style={styles.logTimestamp}>{log.timestamp}</Text>
            </View>
            <Text style={styles.logMessage}>{log.message}</Text>
          </View>
        ))}
      </View>
    </ScrollView>
  );

  const renderConfigTab = () => (
    <ScrollView style={styles.tabContent}>
      <View style={styles.configContainer}>
        <Text style={styles.cardTitle}>Configuration</Text>
        
        <View style={styles.configItem}>
          <Text style={styles.configLabel}>Agent ID</Text>
          <Text style={styles.configValue}>{agentState.id}</Text>
        </View>
        
        <View style={styles.configItem}>
          <Text style={styles.configLabel}>Category</Text>
          <Text style={styles.configValue}>{agentState.category}</Text>
        </View>
        
        <View style={styles.configItem}>
          <Text style={styles.configLabel}>Priority Level</Text>
          <Text style={styles.configValue}>{agentState.priority}</Text>
        </View>
        
        <View style={styles.configItem}>
          <Text style={styles.configLabel}>Auto-restart</Text>
          <Switch value={true} />
        </View>
        
        <View style={styles.configItem}>
          <Text style={styles.configLabel}>Resource Limit</Text>
          <Text style={styles.configValue}>85%</Text>
        </View>
        
        <View style={styles.configItem}>
          <Text style={styles.configLabel}>Patent Protection</Text>
          <Text style={styles.configValue}>USPTO #63/850,603</Text>
        </View>
      </View>
    </ScrollView>
  );

  return (
    <Modal
      visible={visible}
      animationType="slide"
      presentationStyle="pageSheet"
      onRequestClose={onClose}
    >
      <View style={styles.container}>
        {/* Header */}
        <View style={styles.header}>
          <TouchableOpacity style={styles.closeButton} onPress={onClose}>
            <Icon name="close" size={24} color="#333" />
          </TouchableOpacity>
          <Text style={styles.headerTitle}>{agentState.name}</Text>
          <View style={styles.headerRight} />
        </View>

        {/* Tab Navigation */}
        <View style={styles.tabNavigation}>
          {[
            { key: 'overview', label: 'Overview' },
            { key: 'logs', label: 'Logs' },
            { key: 'config', label: 'Config' },
          ].map((tab) => (
            <TouchableOpacity
              key={tab.key}
              style={[
                styles.tabButton,
                activeTab === tab.key && styles.activeTabButton
              ]}
              onPress={() => setActiveTab(tab.key as any)}
            >
              <Text style={[
                styles.tabButtonText,
                activeTab === tab.key && styles.activeTabButtonText
              ]}>
                {tab.label}
              </Text>
            </TouchableOpacity>
          ))}
        </View>

        {/* Tab Content */}
        {activeTab === 'overview' && renderOverviewTab()}
        {activeTab === 'logs' && renderLogsTab()}
        {activeTab === 'config' && renderConfigTab()}
      </View>
    </Modal>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: 16,
    backgroundColor: '#ffffff',
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  closeButton: {
    padding: 8,
  },
  headerTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
  },
  headerRight: {
    width: 40,
  },
  tabNavigation: {
    flexDirection: 'row',
    backgroundColor: '#ffffff',
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  tabButton: {
    flex: 1,
    paddingVertical: 16,
    alignItems: 'center',
  },
  activeTabButton: {
    borderBottomWidth: 2,
    borderBottomColor: '#0066cc',
  },
  tabButtonText: {
    fontSize: 14,
    color: '#666',
    fontWeight: '500',
  },
  activeTabButtonText: {
    color: '#0066cc',
    fontWeight: '600',
  },
  tabContent: {
    flex: 1,
    padding: 16,
  },
  statusCard: {
    backgroundColor: '#ffffff',
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
  },
  statusHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  statusInfo: {
    flex: 1,
  },
  statusTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginBottom: 8,
  },
  statusRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  statusDot: {
    width: 10,
    height: 10,
    borderRadius: 5,
    marginRight: 8,
  },
  statusText: {
    fontSize: 14,
    fontWeight: '500',
    color: '#333',
  },
  metricsCard: {
    backgroundColor: '#ffffff',
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
  },
  cardTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginBottom: 16,
  },
  metricRow: {
    marginBottom: 16,
  },
  metricItem: {
    flex: 1,
  },
  metricItemHalf: {
    flex: 0.5,
  },
  metricLabel: {
    fontSize: 12,
    color: '#666',
    marginBottom: 4,
  },
  metricValue: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
    marginBottom: 8,
  },
  progressBar: {
    height: 6,
    backgroundColor: '#e0e0e0',
    borderRadius: 3,
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
  },
  priorityBadge: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  priorityDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    marginRight: 6,
  },
  priorityText: {
    fontSize: 12,
    fontWeight: '600',
    color: '#333',
  },
  controlsCard: {
    backgroundColor: '#ffffff',
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
  },
  controlButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 12,
    borderRadius: 8,
    marginBottom: 8,
  },
  runButton: {
    backgroundColor: '#4CAF50',
  },
  restartButton: {
    backgroundColor: '#2196F3',
  },
  stopButton: {
    backgroundColor: '#F44336',
  },
  controlButtonText: {
    color: '#ffffff',
    fontSize: 14,
    fontWeight: '600',
    marginLeft: 8,
  },
  descriptionCard: {
    backgroundColor: '#ffffff',
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
  },
  descriptionText: {
    fontSize: 14,
    color: '#666',
    lineHeight: 20,
  },
  logsContainer: {
    backgroundColor: '#ffffff',
    borderRadius: 12,
    padding: 16,
  },
  logEntry: {
    marginBottom: 16,
    paddingBottom: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  logHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 4,
  },
  logLevelDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    marginRight: 8,
  },
  logLevel: {
    fontSize: 12,
    fontWeight: '600',
    color: '#333',
    marginRight: 8,
  },
  logTimestamp: {
    fontSize: 12,
    color: '#666',
    marginLeft: 'auto',
  },
  logMessage: {
    fontSize: 14,
    color: '#666',
    lineHeight: 18,
  },
  configContainer: {
    backgroundColor: '#ffffff',
    borderRadius: 12,
    padding: 16,
  },
  configItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  configLabel: {
    fontSize: 14,
    color: '#333',
    flex: 1,
  },
  configValue: {
    fontSize: 14,
    color: '#666',
    fontWeight: '500',
  },
});

export default AgentViewModal;
