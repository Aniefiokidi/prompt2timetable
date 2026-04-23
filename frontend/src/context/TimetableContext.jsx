import React, { createContext, useState } from "react";

export const TimetableContext = createContext();

export function TimetableProvider({ children }) {
  const [timetable, setTimetable] = useState(null);
  const [view, setView] = useState("grid"); // grid or list

  return (
    <TimetableContext.Provider value={{ timetable, setTimetable, view, setView }}>
      {children}
    </TimetableContext.Provider>
  );
}
