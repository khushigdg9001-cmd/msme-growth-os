import { Bell, Search, UserCircle } from "lucide-react";

function Navbar() {
  return (
    <header className="flex items-center justify-between mb-10">
      <div>
        <div className="space-y-2">

<p className="text-cyan-400 text-lg font-semibold tracking-wide">
WELCOME, URBAN THREADS PVT. LTD.
</p>

<h1 className="text-5xl font-bold text-white">
AI CEO Dashboard
</h1>

<p className="text-slate-400 text-xl">
AI Agents are autonomously monitoring your business.
</p>

<div className="flex items-center gap-2 mt-3">

<div className="w-2.5 h-2.5 rounded-full bg-green-400 animate-pulse"></div>

<p className="text-sm text-slate-500">
Last Sync • {new Date().toLocaleTimeString("en-IN", {
hour: "2-digit",
minute: "2-digit",
hour12: true,
timeZone: "Asia/Kolkata"
})} IST
</p>

</div>

</div>
      </div>

      <div className="flex items-center gap-5">
        <button className="p-3 rounded-xl bg-slate-900 hover:bg-slate-800 transition">
          <Search className="text-white" />
        </button>

        <button className="p-3 rounded-xl bg-slate-900 hover:bg-slate-800 transition relative">
          <Bell className="text-white" />

          <span className="absolute top-2 right-2 w-2 h-2 bg-cyan-400 rounded-full"></span>
        </button>

        <UserCircle
          size={42}
          className="text-cyan-400 cursor-pointer"
        />
      </div>
    </header>
  );
}

export default Navbar;
