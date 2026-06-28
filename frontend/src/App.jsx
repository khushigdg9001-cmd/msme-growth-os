import { useState } from "react";
import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

import Landing from "./pages/Landing";
import Dashboard from "./pages/Dashboard";
import Inventory from "./pages/Inventory";
import Finance from "./pages/Finance";
import CRM from "./pages/CRM";
import Compliance from "./pages/Compliance";
import AICEO from "./pages/AICEO";

function App() {
  const [launched, setLaunched] = useState(false);

  if (!launched) {
    return <Landing onLaunch={() => setLaunched(true)} />;
  }

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/inventory" element={<Inventory />} />
        <Route path="/finance" element={<Finance />} />
        <Route path="/crm" element={<CRM />} />
        <Route path="/compliance" element={<Compliance />} />
        <Route path="/aiceo" element={<AICEO />} />
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;