"use client";

import {
  AlertOutlined,
  CheckCircleOutlined,
  ClockCircleOutlined,
  DashboardOutlined,
  ExperimentOutlined,
  FieldTimeOutlined,
  SafetyCertificateOutlined,
} from "@ant-design/icons";
import { Card, Col, ConfigProvider, Layout, Progress, Row, Segmented, Space, Statistic, Table, Tag, Typography } from "antd";
import type { TableColumnsType } from "antd";
import type { EChartsOption } from "echarts";
import dynamic from "next/dynamic";
import { useState } from "react";

const ReactECharts = dynamic(() => import("echarts-for-react"), {
  ssr: false,
  loading: () => <div className="chart-loading">Loading chart</div>,
});

const { Header, Content } = Layout;
const { Text, Title } = Typography;

type ProductionRow = {
  key: string;
  line: string;
  batch: string;
  model: string;
  inspected: number;
  defects: number;
  topDefect: string;
  severity: "Critical" | "Major" | "Minor";
  status: "Clear" | "Rework" | "Quarantine";
};

const trendData = [
  { day: "Mon", inspected: 1180, defectRate: 2.4 },
  { day: "Tue", inspected: 1245, defectRate: 2.1 },
  { day: "Wed", inspected: 1310, defectRate: 2.8 },
  { day: "Thu", inspected: 1276, defectRate: 1.9 },
  { day: "Fri", inspected: 1395, defectRate: 2.6 },
  { day: "Sat", inspected: 884, defectRate: 3.2 },
  { day: "Sun", inspected: 760, defectRate: 2.2 },
];

const defectCategories = [
  { name: "Solder bridge", value: 42 },
  { name: "Missing component", value: 31 },
  { name: "Bent pin", value: 27 },
  { name: "Burn mark", value: 15 },
  { name: "Scratch", value: 22 },
  { name: "Misalignment", value: 18 },
];

const productionRows: ProductionRow[] = [
  {
    key: "L1-B2408-17",
    line: "Line 1",
    batch: "B2408-17",
    model: "AX-MB-410",
    inspected: 520,
    defects: 9,
    topDefect: "Solder bridge",
    severity: "Major",
    status: "Rework",
  },
  {
    key: "L2-B2408-18",
    line: "Line 2",
    batch: "B2408-18",
    model: "AX-MB-520",
    inspected: 486,
    defects: 4,
    topDefect: "Bent pin",
    severity: "Minor",
    status: "Clear",
  },
  {
    key: "L3-B2408-19",
    line: "Line 3",
    batch: "B2408-19",
    model: "AX-MB-520",
    inspected: 504,
    defects: 12,
    topDefect: "Missing component",
    severity: "Critical",
    status: "Quarantine",
  },
  {
    key: "L4-B2408-20",
    line: "Line 4",
    batch: "B2408-20",
    model: "AX-MB-610",
    inspected: 462,
    defects: 5,
    topDefect: "Misalignment",
    severity: "Minor",
    status: "Clear",
  },
];

const severityColor: Record<ProductionRow["severity"], string> = {
  Critical: "red",
  Major: "orange",
  Minor: "blue",
};

const statusColor: Record<ProductionRow["status"], string> = {
  Clear: "green",
  Rework: "gold",
  Quarantine: "volcano",
};

const columns: TableColumnsType<ProductionRow> = [
  {
    title: "Line",
    dataIndex: "line",
    key: "line",
    fixed: "left",
    width: 92,
  },
  {
    title: "Batch",
    dataIndex: "batch",
    key: "batch",
    width: 116,
  },
  {
    title: "Board Model",
    dataIndex: "model",
    key: "model",
    width: 132,
  },
  {
    title: "Inspected",
    dataIndex: "inspected",
    key: "inspected",
    align: "right",
    width: 110,
  },
  {
    title: "Defects",
    dataIndex: "defects",
    key: "defects",
    align: "right",
    width: 96,
  },
  {
    title: "Top Defect",
    dataIndex: "topDefect",
    key: "topDefect",
    width: 160,
  },
  {
    title: "Severity",
    dataIndex: "severity",
    key: "severity",
    width: 108,
    render: (severity: ProductionRow["severity"]) => <Tag color={severityColor[severity]}>{severity}</Tag>,
  },
  {
    title: "Status",
    dataIndex: "status",
    key: "status",
    width: 122,
    render: (status: ProductionRow["status"]) => <Tag color={statusColor[status]}>{status}</Tag>,
  },
];

const trendOptions: EChartsOption = {
  color: ["#1d7a8c", "#f09f38"],
  grid: { top: 34, right: 44, bottom: 36, left: 44 },
  tooltip: { trigger: "axis" },
  legend: { top: 0, right: 0, textStyle: { color: "#51606d" } },
  xAxis: {
    type: "category",
    data: trendData.map((item) => item.day),
    axisLine: { lineStyle: { color: "#d7dee6" } },
    axisLabel: { color: "#6a7683" },
  },
  yAxis: [
    {
      type: "value",
      name: "Boards",
      axisLabel: { color: "#6a7683" },
      splitLine: { lineStyle: { color: "#edf1f5" } },
    },
    {
      type: "value",
      name: "Defect %",
      min: 0,
      max: 5,
      axisLabel: { color: "#6a7683", formatter: "{value}%" },
      splitLine: { show: false },
    },
  ],
  series: [
    {
      name: "Inspected",
      type: "bar",
      data: trendData.map((item) => item.inspected),
      barWidth: 22,
      itemStyle: { borderRadius: [5, 5, 0, 0] },
    },
    {
      name: "Defect rate",
      type: "line",
      yAxisIndex: 1,
      smooth: true,
      symbolSize: 8,
      data: trendData.map((item) => item.defectRate),
    },
  ],
};

const categoryOptions: EChartsOption = {
  color: ["#c65332", "#1d7a8c", "#f0b43c", "#31475f", "#7a9650", "#8b6f4e"],
  tooltip: { trigger: "item" },
  legend: {
    bottom: 0,
    left: "center",
    itemWidth: 10,
    itemHeight: 10,
    textStyle: { color: "#51606d" },
  },
  series: [
    {
      name: "Defects",
      type: "pie",
      radius: ["46%", "70%"],
      center: ["50%", "44%"],
      avoidLabelOverlap: true,
      itemStyle: { borderColor: "#ffffff", borderWidth: 3, borderRadius: 6 },
      label: { color: "#40505f", formatter: "{b}\n{c}" },
      data: defectCategories,
    },
  ],
};

export default function Home() {
  const [selectedWindow, setSelectedWindow] = useState("7 days");

  return (
    <ConfigProvider
      theme={{
        token: {
          colorPrimary: "#1d7a8c",
          borderRadius: 8,
          fontFamily: "var(--font-dashboard)",
        },
        components: {
          Card: { headerBg: "transparent" },
          Table: { headerBg: "#f4f7f9" },
        },
      }}
    >
      <Layout className="dashboard-shell">
        <Header className="dashboard-header">
          <Space size={14} align="center" className="brand-group">
            <span className="brand-mark"><ExperimentOutlined /></span>
            <div>
              <Text className="eyebrow">Axion Quality Ops</Text>
              <Title level={1}>Motherboard Defect Monitoring</Title>
            </div>
          </Space>
          <Space className="header-actions" size={12} wrap>
            <Tag color="cyan">AOI Line Feed</Tag>
            <Segmented
              value={selectedWindow}
              options={["Shift", "24 hours", "7 days"]}
              onChange={(value) => setSelectedWindow(String(value))}
            />
          </Space>
        </Header>

        <Content className="dashboard-content">
          <section className="overview-panel">
            <div>
              <Text className="eyebrow">Current window: {selectedWindow}</Text>
              <Title level={2}>Inspection statistics from motherboard visual checks</Title>
            </div>
            <div className="health-score">
              <Progress type="circle" percent={97.6} size={96} strokeColor="#1d7a8c" format={() => "97.6%"} />
              <div>
                <Text strong>Pass yield</Text>
                <Text type="secondary">Stable, with Line 3 under review</Text>
              </div>
            </div>
          </section>

          <Row gutter={[16, 16]}>
            <Col xs={24} sm={12} lg={8} xl={4}>
              <Card className="metric-card">
                <Statistic title="Inspected Boards" value={7350} prefix={<DashboardOutlined />} />
                <Text type="secondary">+8.4% vs prior window</Text>
              </Card>
            </Col>
            <Col xs={24} sm={12} lg={8} xl={4}>
              <Card className="metric-card warning-card">
                <Statistic title="Defective Boards" value={176} prefix={<AlertOutlined />} />
                <Text type="secondary">2.4% defect rate</Text>
              </Card>
            </Col>
            <Col xs={24} sm={12} lg={8} xl={4}>
              <Card className="metric-card">
                <Statistic title="Pass Rate" value={97.6} suffix="%" prefix={<CheckCircleOutlined />} />
                <Text type="secondary">Target 97.0%</Text>
              </Card>
            </Col>
            <Col xs={24} sm={12} lg={8} xl={4}>
              <Card className="metric-card critical-card">
                <Statistic title="Critical Defects" value={15} prefix={<SafetyCertificateOutlined />} />
                <Text type="secondary">8.5% of defects</Text>
              </Card>
            </Col>
            <Col xs={24} sm={12} lg={8} xl={4}>
              <Card className="metric-card">
                <Statistic title="Avg. Inspection" value={4.8} suffix="s" prefix={<ClockCircleOutlined />} />
                <Text type="secondary">Camera to decision</Text>
              </Card>
            </Col>
            <Col xs={24} sm={12} lg={8} xl={4}>
              <Card className="metric-card">
                <Statistic title="Rework Queue" value={43} prefix={<FieldTimeOutlined />} />
                <Text type="secondary">12 quarantined</Text>
              </Card>
            </Col>
          </Row>

          <Row gutter={[16, 16]} className="chart-row">
            <Col xs={24} xl={15}>
              <Card title="Inspection Volume and Defect Rate" className="panel-card">
                <ReactECharts option={trendOptions} className="chart chart-wide" />
              </Card>
            </Col>
            <Col xs={24} xl={9}>
              <Card title="Defect Category Mix" className="panel-card">
                <ReactECharts option={categoryOptions} className="chart chart-donut" />
              </Card>
            </Col>
          </Row>

          <Row gutter={[16, 16]}>
            <Col xs={24} lg={8}>
              <Card title="Severity Snapshot" className="panel-card status-card">
                <Space direction="vertical" size={18} className="status-list">
                  <div>
                    <div className="status-line"><Text>Critical</Text><Text strong>15</Text></div>
                    <Progress percent={8.5} strokeColor="#c65332" showInfo={false} />
                  </div>
                  <div>
                    <div className="status-line"><Text>Major</Text><Text strong>74</Text></div>
                    <Progress percent={42} strokeColor="#f0b43c" showInfo={false} />
                  </div>
                  <div>
                    <div className="status-line"><Text>Minor</Text><Text strong>87</Text></div>
                    <Progress percent={49.5} strokeColor="#1d7a8c" showInfo={false} />
                  </div>
                </Space>
              </Card>
            </Col>
            <Col xs={24} lg={16}>
              <Card title="Line and Batch Watchlist" className="panel-card table-card">
                <Table
                  columns={columns}
                  dataSource={productionRows}
                  pagination={false}
                  size="middle"
                  scroll={{ x: 940 }}
                />
              </Card>
            </Col>
          </Row>
        </Content>
      </Layout>
    </ConfigProvider>
  );
}
