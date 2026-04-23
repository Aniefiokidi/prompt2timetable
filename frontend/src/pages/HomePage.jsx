import React from "react";
import { Link } from "react-router-dom";

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-cu-purple to-purple-900 p-4 flex items-center justify-center">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-3xl p-8 md:p-10">
        <span className="inline-block text-sm font-semibold tracking-wide text-cu-gold bg-cu-purple px-3 py-1 rounded-full mb-4">
          CU Timetable
        </span>
        <h1 className="text-3xl md:text-4xl font-bold text-cu-purple mb-3">Covenant University Timetable System</h1>
        <p className="text-slate-600 mb-8">
          Generate and review department timetables in clean grid and list views, with export options for sharing.
        </p>
        <div className="flex flex-wrap gap-3">
          <Link to="/lookup" className="bg-cu-purple hover:bg-purple-900 text-cu-gold font-semibold px-6 py-3 rounded-lg shadow transition-all">
            Start Timetable Lookup
          </Link>
          <Link to="/evaluation" className="border border-cu-purple text-cu-purple hover:bg-cu-purple hover:text-white font-semibold px-6 py-3 rounded-lg transition-all">
            View Evaluation
          </Link>
        </div>
      </div>
    </div>
  );
}
