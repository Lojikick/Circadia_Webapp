import React, { useState } from 'react';
import './Calendar.css';

const CalendarEntry = ({ startTime, endTime, date }) => {
  return (
    <div className="calendar-entry">
      <p>{date}</p>
      <p>{startTime} - {endTime}</p>
    </div>
  );
};

const Calendar = () => {
  const [entries, setEntries] = useState([
    { startTime: "08:00", endTime: "10:00", date: "2024-04-14" },
    { startTime: "13:30", endTime: "15:30", date: "2024-04-15" },
  ]);

  return (
    <div className="calendar">
      {entries.map((entry, index) => (
        <CalendarEntry key={index} startTime={entry.startTime} endTime={entry.endTime} date={entry.date} />
      ))}
    </div>
  );
};

export default Calendar;
