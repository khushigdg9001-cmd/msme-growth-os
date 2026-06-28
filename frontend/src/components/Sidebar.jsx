import {
  LayoutDashboard,
  Package,
  IndianRupee,
  Users,
  ShieldCheck,
  Brain,
} from "lucide-react";

import { NavLink } from "react-router-dom";

function Sidebar() {
  const menu = [
    {
      icon: LayoutDashboard,
      label: "Dashboard",
      path: "/",
    },
    {
      icon: Package,
      label: "Inventory",
      path: "/inventory",
    },
    {
      icon: IndianRupee,
      label: "Finance",
      path: "/finance",
    },
    {
      icon: Users,
      label: "CRM",
      path: "/crm",
    },
    {
      icon: ShieldCheck,
      label: "Compliance",
      path: "/compliance",
    },
    {
      icon: Brain,
      label: "AI CEO",
      path: "/aiceo",
    },
  ];

  return (
    <aside className="w-72 min-h-screen bg-slate-900 border-r border-cyan-500/20 p-6">

      <h1 className="text-2xl font-bold text-cyan-400 mb-10">
        MSME Growth OS
      </h1>

      <div className="space-y-3">

        {menu.map((item) => {

          const Icon = item.icon;

          return (
            <NavLink
              key={item.label}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${
                  isActive
                    ? "bg-cyan-500 text-black font-semibold"
                    : "text-slate-300 hover:bg-cyan-500/20 hover:text-cyan-300"
                }`
              }
            >
              <Icon size={20} />
              {item.label}
            </NavLink>
          );
        })}
      </div>
    </aside>
  );
}

export default Sidebar;