import React from "react";
import { Link, useLocation } from "react-router-dom";
import covenantLogo from "../assets/covenant-logo.svg";

const OFFICIAL_CU_LOGO_URL =
  "https://www.covenantuniversity.edu.ng/images/logos/covenant-university-logo-desktop.png";

const NAV_ITEMS = [
  { label: "Dashboard", to: "/" },
  { label: "Upload Data", to: "/upload" },
  { label: "Generate Timetable", to: "/assistant" },
  { label: "View Timetable", to: "/timetable" },
  { label: "Lookup", to: "/lookup" },
  { label: "Evaluation", to: "/evaluation" },
];

export default function AppShell({ title, subtitle, children }) {
  const location = useLocation();

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <header className="bg-white border-b border-slate-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-3 md:py-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <img
              src={OFFICIAL_CU_LOGO_URL}
              alt="Covenant University logo"
              onError={(e) => {
                e.currentTarget.onerror = null;
                e.currentTarget.src = covenantLogo;
              }}
              className="h-12 md:h-14 w-auto object-contain"
            />
            <div>
            <h1 className="text-lg md:text-2xl font-bold text-cu-purple leading-tight">CU Sched</h1>
            <p className="text-xs md:text-sm text-slate-600">Covenant University Timetable</p>
            </div>
          </div>
          <div className="hidden md:block text-right">
            <p className="text-xs uppercase tracking-wide text-slate-500">Academic Session Tool</p>
            <p className="text-sm font-medium text-slate-700">Fast lookup • Clean export</p>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 py-6 grid grid-cols-1 md:grid-cols-[230px,1fr] gap-6">
        <aside className="bg-white rounded-xl shadow-sm border border-slate-200 p-3 h-fit">
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-500 px-2 mb-2">Navigation</p>
          <nav className="space-y-1">
            {NAV_ITEMS.map((item) => {
              const active = location.pathname === item.to;
              return (
                <Link
                  key={item.to}
                  to={item.to}
                  className={`block rounded-lg px-3 py-2 text-sm font-medium transition ${
                    active ? "bg-cu-purple text-cu-gold" : "text-slate-700 hover:bg-slate-100"
                  }`}
                >
                  {item.label}
                </Link>
              );
            })}
          </nav>
        </aside>

        <main className="space-y-4">
          {(title || subtitle) && (
            <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5">
              {title && <h2 className="text-2xl font-bold text-cu-purple">{title}</h2>}
              {subtitle && <p className="text-sm text-slate-600 mt-1">{subtitle}</p>}
            </div>
          )}
          <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-4 md:p-6">{children}</div>
        </main>
      </div>
    </div>
  );
}
