import React from "react";
import { Link, useLocation } from "react-router-dom";

const NAV_ITEMS = [
  { label: "Home", to: "/" },
  { label: "Lookup", to: "/lookup" },
  { label: "Timetable", to: "/timetable" },
  { label: "Evaluation", to: "/evaluation" },
];

export default function AppShell({ title, subtitle, children }) {
  const location = useLocation();

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <header className="bg-cu-purple text-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-xl md:text-2xl font-bold">CU Timetable Portal</h1>
            <p className="text-sm text-white/80">Covenant University schedule assistant</p>
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
