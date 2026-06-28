import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import StatCard from "../components/StatCard";
import RevenueChart from "../components/RevenueChart";
import WhatsAppActivity from "../components/WhatsAppActivity";
import ExecutiveSummary from "../components/ExecutiveSummary";
import OneClickExecution from "../components/OneClickExecution";
function Dashboard() {
  return (
    <div className="flex min-h-screen bg-slate-950">

      <Sidebar />

      <main className="flex-1 p-10">

        <Navbar />
        

        <div className="grid grid-cols-4 gap-6 mt-10">

          <StatCard
            title="Revenue"
            value="₹2.35L"
            change="+18% this month"
          />

          <StatCard
            title="Profit"
            value="₹93K"
            change="+11% this month"
            color="text-green-400"
          />

          <StatCard
title="Business Health"
value="94%"
change="AI CEO Monitoring"
color="text-cyan-400"
/>
          <StatCard
            title="AI Confidence"
            value="97%"
            change="Decision Engine Active"
            color="text-purple-400"
          />

        </div>
        <div className="mt-8">
  <ExecutiveSummary />
</div>

<div className="mt-8"></div>

<div className="grid grid-cols-3 gap-6 mt-8">
  <div className="col-span-2">
    <OneClickExecution />
  </div>
  <div className="self-start">
    <WhatsAppActivity />
  </div>
</div>

<div className="grid grid-cols-3 gap-6 mt-8">
  <div className="col-span-2">
    <RevenueChart />
  </div>
</div>

</main>

    

    </div>
  );
}

export default Dashboard;