import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/layout/Navbar";
import DashboardPage from "./pages/DashboardPage";
import ForecastPage from "./pages/ForecastPage";
import SegmentsPage from "./pages/SegmentsPage";
import AssistantPage from "./pages/AssistantPage";

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <main className="p-6">
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/forecast" element={<ForecastPage />} />
          <Route path="/segments" element={<SegmentsPage />} />
          <Route path="/assistant" element={<AssistantPage />} />
        </Routes>
      </main>
    </BrowserRouter>
  );
}

export default App;
