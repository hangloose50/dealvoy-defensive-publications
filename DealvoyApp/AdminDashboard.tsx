/**
 * Dealvoy Mobile App - Admin Dashboard Component
 * 
 * USPTO Patent Application #63/850,603
 * All rights reserved. Contains confidential and proprietary information.
 * 
 * Comprehensive administrative control panel for the 46-agent AI system.
 */

import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  ScrollView,
  TouchableOpacity,
  Alert,
  Switch,
  RefreshControl,
  Dimensions,
} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';

interface SystemMetrics {
  totalAgents: number;
  activeAgents: number;
  avgPerformance: number;
  systemUptime: string;
  totalUsers: number;
  premiumUsers: number;
  resourceUsage: {
    cpu: number;
    memory: number;
    storage: number;
  };
}

interface AlertItem {
  id: string;
  type: 'error' | 'warning' | 'info';
  message: string;
  timestamp: string;
  resolved: boolean;
}

const { width } = Dimensions.get('window');

const AdminDashboard: React.FC = () => {
  const [metrics, setMetrics] = useState<SystemMetrics | null>(null);
  const [alerts, setAlerts] = useState<AlertItem[]>([]);
  const [refreshing, setRefreshing] = useState<boolean>(false);
  const [maintenanceMode, setMaintenanceMode] = useState<boolean>(false);
  const [autoScaling, setAutoScaling] = useState<boolean>(true);

  useEffect(() => {
    loadSystemMetrics();
    loadSystemAlerts();
  }, []);

  const loadSystemMetrics = async () => {
    // Simulate loading system metrics
    const mockMetrics: SystemMetrics = {
      totalAgents: 46,
      activeAgents: 43,
      avgPerformance: 91.7,
      systemUptime: '99.8%',
      totalUsers: 1247,
      premiumUsers: 342,
      resourceUsage: {
        cpu: 67,
        memory: 72,
        storage: 45,
      },
    };
    setMetrics(mockMetrics);
  };

  const loadSystemAlerts = async () => {
    const mockAlerts: AlertItem[] = [
      {
        id: '1',
        type: 'warning',
        message: 'Agent "Category AI" resource usage above 80%',
        timestamp: '2025-01-26 10:35:22',
        resolved: false,
      },
      {
        id: '2',
        type: 'info',
        message: 'System backup completed successfully',
        timestamp: '2025-01-26 09:15:00',
        resolved: true,
      },
      {
        id: '3',
        type: 'error',
        message: 'API rate limit exceeded for Walmart integration',
        timestamp: '2025-01-26 08:45:33',
        resolved: false,
      },
      {
        id: '4',
        type: 'info',
        message: '5 new premium subscriptions activated',
        timestamp: '2025-01-26 07:30:15',
        resolved: true,
      },
    ];
    setAlerts(mockAlerts);
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await Promise.all([loadSystemMetrics(), loadSystemAlerts()]);
    setRefreshing(false);
  };

  const handleEmergencyStop = () => {
    Alert.alert(
      'Emergency Stop',
      'This will immediately stop all 46 agents. Are you sure?',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Stop All',
          style: 'destructive',
          onPress: () => Alert.alert('Success', 'All agents have been stopped'),
        },
      ]
    );
  };

  const handleSystemRestart = () => {
    Alert.alert(
      'System Restart',
      'This will restart the entire Dealvoy system. Downtime: ~2 minutes.',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Restart',
          style: 'destructive',
          onPress: () => Alert.alert('Success', 'System restart initiated'),
        },
      ]
    );
  };

  const resolveAlert = (alertId: string) => {
    setAlerts(prev => prev.map(alert =>
      alert.id === alertId ? { ...alert, resolved: true } : alert
    ));
  };

  const getAlertColor = (type: string): string => {
    switch (type) {
      case 'error': return '#F44336';
      case 'warning': return '#FFC107';
      case 'info': return '#2196F3';
      default: return '#9E9E9E';
    }
  };

  const getAlertIcon = (type: string): string => {
    switch (type) {
      case 'error': return 'error';
      case 'warning': return 'warning';
      case 'info': return 'info';
      default: return 'notifications';
    }
  };

  if (!metrics) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.loadingContainer}>
          <Text>Loading admin dashboard...</Text>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView
        style={styles.scrollContainer}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
      >
        {/* Header */}
        <View style={styles.header}>
          <Text style={styles.headerTitle}>Admin Dashboard</Text>
          <Text style={styles.headerSubtitle}>System Control Center</Text>
        </View>

        {/* Quick Stats */}
        <View style={styles.statsContainer}>
          <View style={styles.statsRow}>
            <View style={styles.statCard}>
              <Icon name="smart-toy" size={24} color="#0066cc" />
              <Text style={styles.statNumber}>{metrics.activeAgents}/{metrics.totalAgents}</Text>
              <Text style={styles.statLabel}>Active Agents</Text>
            </View>
            <View style={styles.statCard}>
              <Icon name="trending-up" size={24} color="#4CAF50" />
              <Text style={styles.statNumber}>{metrics.avgPerformance}%</Text>
              <Text style={styles.statLabel}>Avg Performance</Text>
            </View>
          </View>
          <View style={styles.statsRow}>
            <View style={styles.statCard}>
              <Icon name="people" size={24} color="#2196F3" />
              <Text style={styles.statNumber}>{metrics.totalUsers}</Text>
              <Text style={styles.statLabel}>Total Users</Text>
            </View>
            <View style={styles.statCard}>
              <Icon name="schedule" size={24} color="#4CAF50" />
              <Text style={styles.statNumber}>{metrics.systemUptime}</Text>
              <Text style={styles.statLabel}>Uptime</Text>
            </View>
          </View>
        </View>

        {/* Resource Usage */}
        <View style={styles.resourceCard}>
          <Text style={styles.cardTitle}>System Resources</Text>
          
          <View style={styles.resourceItem}>
            <Text style={styles.resourceLabel}>CPU Usage</Text>
            <Text style={styles.resourceValue}>{metrics.resourceUsage.cpu}%</Text>
            <View style={styles.progressBar}>
              <View style={[
                styles.progressFill,
                { 
                  width: `${metrics.resourceUsage.cpu}%`,
                  backgroundColor: metrics.resourceUsage.cpu > 80 ? '#F44336' : '#4CAF50'
                }
              ]} />
            </View>
          </View>

          <View style={styles.resourceItem}>
            <Text style={styles.resourceLabel}>Memory Usage</Text>
            <Text style={styles.resourceValue}>{metrics.resourceUsage.memory}%</Text>
            <View style={styles.progressBar}>
              <View style={[
                styles.progressFill,
                { 
                  width: `${metrics.resourceUsage.memory}%`,
                  backgroundColor: metrics.resourceUsage.memory > 80 ? '#F44336' : '#4CAF50'
                }
              ]} />
            </View>
          </View>

          <View style={styles.resourceItem}>
            <Text style={styles.resourceLabel}>Storage Usage</Text>
            <Text style={styles.resourceValue}>{metrics.resourceUsage.storage}%</Text>
            <View style={styles.progressBar}>
              <View style={[
                styles.progressFill,
                { 
                  width: `${metrics.resourceUsage.storage}%`,
                  backgroundColor: '#4CAF50'
                }
              ]} />
            </View>
          </View>
        </View>

        {/* System Controls */}
        <View style={styles.controlsCard}>
          <Text style={styles.cardTitle}>System Controls</Text>
          
          <View style={styles.controlRow}>
            <Text style={styles.controlLabel}>Maintenance Mode</Text>
            <Switch
              value={maintenanceMode}
              onValueChange={setMaintenanceMode}
              trackColor={{ false: '#767577', true: '#81b0ff' }}
              thumbColor={maintenanceMode ? '#0066cc' : '#f4f3f4'}
            />
          </View>

          <View style={styles.controlRow}>
            <Text style={styles.controlLabel}>Auto Scaling</Text>
            <Switch
              value={autoScaling}
              onValueChange={setAutoScaling}
              trackColor={{ false: '#767577', true: '#81b0ff' }}
              thumbColor={autoScaling ? '#0066cc' : '#f4f3f4'}
            />
          </View>

          <TouchableOpacity style={styles.emergencyButton} onPress={handleEmergencyStop}>
            <Icon name="stop" size={20} color="#ffffff" />
            <Text style={styles.emergencyButtonText}>Emergency Stop All Agents</Text>
          </TouchableOpacity>

          <TouchableOpacity style={styles.restartButton} onPress={handleSystemRestart}>
            <Icon name="refresh" size={20} color="#ffffff" />
            <Text style={styles.restartButtonText}>Restart System</Text>
          </TouchableOpacity>
        </View>

        {/* System Alerts */}
        <View style={styles.alertsCard}>
          <Text style={styles.cardTitle}>System Alerts</Text>
          {alerts.map((alert) => (
            <View key={alert.id} style={[
              styles.alertItem,
              alert.resolved && styles.resolvedAlert
            ]}>
              <View style={styles.alertHeader}>
                <Icon
                  name={getAlertIcon(alert.type)}
                  size={20}
                  color={getAlertColor(alert.type)}
                />
                <Text style={styles.alertType}>{alert.type.toUpperCase()}</Text>
                <Text style={styles.alertTimestamp}>{alert.timestamp}</Text>
              </View>
              <Text style={styles.alertMessage}>{alert.message}</Text>
              {!alert.resolved && (
                <TouchableOpacity
                  style={styles.resolveButton}
                  onPress={() => resolveAlert(alert.id)}
                >
                  <Text style={styles.resolveButtonText}>Mark Resolved</Text>
                </TouchableOpacity>
              )}
            </View>
          ))}
        </View>

        {/* User Statistics */}
        <View style={styles.userStatsCard}>
          <Text style={styles.cardTitle}>User Statistics</Text>
          
          <View style={styles.userStatsRow}>
            <View style={styles.userStatItem}>
              <Text style={styles.userStatNumber}>{metrics.totalUsers}</Text>
              <Text style={styles.userStatLabel}>Total Users</Text>
            </View>
            <View style={styles.userStatItem}>
              <Text style={styles.userStatNumber}>{metrics.premiumUsers}</Text>
              <Text style={styles.userStatLabel}>Premium Users</Text>
            </View>
            <View style={styles.userStatItem}>
              <Text style={styles.userStatNumber}>
                {Math.round((metrics.premiumUsers / metrics.totalUsers) * 100)}%
              </Text>
              <Text style={styles.userStatLabel}>Conversion Rate</Text>
            </View>
          </View>
        </View>

        {/* Patent Information */}
        <View style={styles.patentCard}>
          <Text style={styles.cardTitle}>System Protection</Text>
          <View style={styles.patentInfo}>
            <Icon name="security" size={24} color="#0066cc" />
            <View style={styles.patentText}>
              <Text style={styles.patentTitle}>USPTO Patent Application</Text>
              <Text style={styles.patentNumber}>#63/850,603</Text>
              <Text style={styles.patentDescription}>
                All 46 AI agents protected under intellectual property law
              </Text>
            </View>
          </View>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  scrollContainer: {
    flex: 1,
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
  statsContainer: {
    padding: 16,
  },
  statsRow: {
    flexDirection: 'row',
    marginBottom: 12,
  },
  statCard: {
    flex: 1,
    backgroundColor: '#ffffff',
    padding: 16,
    borderRadius: 12,
    alignItems: 'center',
    marginHorizontal: 6,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  statNumber: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333',
    marginTop: 8,
  },
  statLabel: {
    fontSize: 12,
    color: '#666',
    marginTop: 4,
    textAlign: 'center',
  },
  resourceCard: {
    backgroundColor: '#ffffff',
    margin: 16,
    borderRadius: 12,
    padding: 16,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
    marginBottom: 16,
  },
  resourceItem: {
    marginBottom: 16,
  },
  resourceLabel: {
    fontSize: 14,
    color: '#666',
    marginBottom: 4,
  },
  resourceValue: {
    fontSize: 16,
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
  controlsCard: {
    backgroundColor: '#ffffff',
    margin: 16,
    borderRadius: 12,
    padding: 16,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  controlRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  controlLabel: {
    fontSize: 16,
    color: '#333',
  },
  emergencyButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#F44336',
    padding: 12,
    borderRadius: 8,
    marginTop: 16,
  },
  emergencyButtonText: {
    color: '#ffffff',
    fontSize: 14,
    fontWeight: '600',
    marginLeft: 8,
  },
  restartButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#2196F3',
    padding: 12,
    borderRadius: 8,
    marginTop: 8,
  },
  restartButtonText: {
    color: '#ffffff',
    fontSize: 14,
    fontWeight: '600',
    marginLeft: 8,
  },
  alertsCard: {
    backgroundColor: '#ffffff',
    margin: 16,
    borderRadius: 12,
    padding: 16,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  alertItem: {
    marginBottom: 16,
    paddingBottom: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  resolvedAlert: {
    opacity: 0.6,
  },
  alertHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  alertType: {
    fontSize: 12,
    fontWeight: '600',
    color: '#333',
    marginLeft: 8,
  },
  alertTimestamp: {
    fontSize: 12,
    color: '#666',
    marginLeft: 'auto',
  },
  alertMessage: {
    fontSize: 14,
    color: '#666',
    lineHeight: 18,
    marginBottom: 8,
  },
  resolveButton: {
    alignSelf: 'flex-start',
    backgroundColor: '#4CAF50',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 4,
  },
  resolveButtonText: {
    color: '#ffffff',
    fontSize: 12,
    fontWeight: '600',
  },
  userStatsCard: {
    backgroundColor: '#ffffff',
    margin: 16,
    borderRadius: 12,
    padding: 16,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  userStatsRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  userStatItem: {
    alignItems: 'center',
    flex: 1,
  },
  userStatNumber: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#0066cc',
  },
  userStatLabel: {
    fontSize: 12,
    color: '#666',
    marginTop: 4,
    textAlign: 'center',
  },
  patentCard: {
    backgroundColor: '#ffffff',
    margin: 16,
    borderRadius: 12,
    padding: 16,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    marginBottom: 32,
  },
  patentInfo: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  patentText: {
    marginLeft: 16,
    flex: 1,
  },
  patentTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#333',
  },
  patentNumber: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#0066cc',
    marginTop: 2,
  },
  patentDescription: {
    fontSize: 12,
    color: '#666',
    marginTop: 4,
  },
});

export default AdminDashboard;
