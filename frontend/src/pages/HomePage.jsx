import React from "react";

export default function HomePage() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-cu-purple text-cu-gold">
      <div className="bg-white bg-opacity-90 rounded-xl shadow-lg p-8 w-full max-w-md flex flex-col items-center">
        <div className="flex flex-col items-center mb-2">
          <span className="text-2xl font-extrabold tracking-wide text-cu-gold bg-cu-purple px-4 py-1 rounded-full mb-2">CU Timetable</span>
          <h1 className="text-3xl md:text-4xl font-bold text-cu-purple">Covenant University Timetable System</h1>
        </div>
        <p className="mb-8 text-lg text-cu-purple/80">Enter your matric number to view your department timetable</p>
        <a href="/lookup">
          <button className="bg-cu-gold hover:bg-yellow-400 text-cu-purple font-semibold px-6 py-3 rounded-lg shadow transition-all">
            View My Timetable
          </button>
        </a>
      </div>
    </div>
  );
}
