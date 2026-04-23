
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import StudentInputPage from "./pages/StudentInputPage";
import TimetablePage from "./pages/TimetablePage";
import EvaluationPage from "./pages/EvaluationPage";
import { TimetableProvider } from "./context/TimetableContext";

export default function App() {
  return (
    <TimetableProvider>
      <Router>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/lookup" element={<StudentInputPage />} />
          <Route path="/timetable" element={<TimetablePage />} />
          <Route path="/evaluation" element={<EvaluationPage />} />
          <Route path="*" element={<div className="min-h-screen flex items-center justify-center text-2xl text-cu-purple">404 - Page Not Found</div>} />
        </Routes>
      </Router>
    </TimetableProvider>
  );
}
