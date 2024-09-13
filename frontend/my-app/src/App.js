import React, { useState, useEffect } from 'react';
import { Inject, ScheduleComponent, Day, Week, Month, Agenda, EventSettingsModel} from '@syncfusion/ej2-react-schedule';
import {registerLicense} from "@syncfusion/ej2-base";
import hypnogramImage from './Hypnogram.png';
registerLicense("Ngo9BigBOggjHTQxAR8/V1NBaF5cXmZCe0x0WmFZfVpgfF9CYlZTQWYuP1ZhSXxXdkFhXH9WdHZXQ2VeUkA");
function App() {
  //Data for information storage
  const [schedule_data, setScheduleData] = useState([]);
  
  const [schedule, setSchedule] = useState({
    Monday: { bedtime: '12:00 AM', waketime: '10:00 AM' },
    Tuesday: { bedtime: '1:00 AM', waketime: '11:00 AM' },
    Wednesday: { bedtime: '12:00 AM', waketime: '10:00 AM' },
    Thursday: { bedtime: '11:00 PM', waketime: '12:00 AM' },
    Friday: { bedtime: '12:00 AM', waketime: '10:00 AM' }
  });
  const [adjustedSchedule, setAdjustedSchedule] = useState(null);

  const [hypnogramUrl, setHypnogramUrl] = useState('');
  
  const onload = async (e) => {
    try {
      // const response = await fetch('/get_hypnogram_image', {
      //   method: 'POST',
      //   headers: {
      //     'Content-Type': 'application/json',
      //   },
      //   body: JSON.stringify(schedule),
      // });
      // const data = await response.json();
  
      // Set the image URL from the response
      // setHypnogramUrl("Hypnogram.png");
      console.log("Welcome to Circadia")
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const reorderSchedule = (schedule) => {
    const orderedDays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"];
    const newSchedule = {};

    orderedDays.forEach((day) => {
      if (schedule[day]) {
        newSchedule[day] = schedule[day];
      }
    });

    return newSchedule;
  };

  const convertToEvents = (adjustedSchedule) => {
    const scheduleData = [];
    const weekdays = {
      Monday: 1,
      Tuesday: 2,
      Wednesday: 3,
      Thursday: 4,
      Friday: 5,
    };
  
    Object.entries(adjustedSchedule).forEach(([day, times]) => {
      const dayIndex = weekdays[day];
      if (times.bedtime) {
        const bedtimeParts = times.bedtime.match(/(\d+):(\d+)\s*(AM|PM)/);
        const bedtimeHour = parseInt(bedtimeParts[1], 10);
        const bedtimeMinute = parseInt(bedtimeParts[2], 10);
        const isPM = bedtimeParts[3] === 'PM';
        const startTime = new Date(2024, 3, 28 + dayIndex, isPM ? bedtimeHour + 12 : bedtimeHour, bedtimeMinute);
  
        scheduleData.push({
          Id: scheduleData.length + 1,
          Subject: `Sleep on ${day}`,
          StartTime: startTime,
          EndTime: new Date(startTime.getTime() + 60 * 60 * 1000), // 1-hour duration
          IsAllDay: false,
        });
      }
  
      if (times.waketime) {
        const waketimeParts = times.waketime.match(/(\d+):(\d+)\s*(AM|PM)/);
        const waketimeHour = parseInt(waketimeParts[1], 10);
        const waketimeMinute = parseInt(waketimeParts[2], 10);
        const isPM = waketimeParts[3] === 'PM';
        const startTime = new Date(2024, 3, 28 + dayIndex, isPM ? waketimeHour + 12 : waketimeHour, waketimeMinute);
  
        scheduleData.push({
          Id: scheduleData.length + 1,
          Subject: `Wake up on ${day}`,
          StartTime: startTime,
          EndTime: new Date(startTime.getTime() + 60 * 60 * 1000), // 1-hour duration
          IsAllDay: false,
        });
      }
    });
  
    return scheduleData;
  };
  
  

  // Update the state with the ordered schedule

  const handleChange = (e, day, field) => {
    const { value } = e.target;
    setSchedule(prevSchedule => ({
      ...prevSchedule,
      [day]: {
        ...prevSchedule[day],
        [field]: value
      }
    }));
  };

  
  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("Should create a new schedule")
    try {
      console.log("Attempting to submit")
      const response = await fetch('/get_schedule', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(schedule)
      });
      console.log("Made it here")
      const data = await response.json();
      console.log(data)
      const orderedSchedule = reorderSchedule(data);
      setAdjustedSchedule(orderedSchedule);
      const event_list = convertToEvents(orderedSchedule);
      setScheduleData((prevData) => [...prevData, ...event_list]);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  useEffect(() => {
    // Trigger the function when the component mounts
    onload(null); // Pass null since there's no event object
  }, []); 

  return (
    <div className="app">
      <header className="header">
        <h1 style={{ color: '#A9E5DE', fontSize: '100px' }}>Good Morning!</h1>
        <h2 style={{ color: '#A9E5DE' }}>Let's get the day started:</h2>
      </header>

      <h2 style={{ color: '#A9E5DE' }}>Sleep</h2>
        <div className="container">
          <h1 style={{color: 'white'}}>Sleep Score:</h1>
          <h1 style={{ color: 'white', fontSize: '90px' }}>29</h1>
          <p>Chart data</p>
          <img src={hypnogramImage} alt="Hypnogram" style={{ maxWidth: '100%' }} />
      </div>

      <div className="flex-container">
        <h2 style={{ color: '#A9E5DE' }}>Productivity</h2>
        <div className="container">
          <div className="fullscreen-center" style={{ border: '2px solid #A9E5DE', padding: '50px', borderRadius: '10px', textAlign: 'center' }}>
            <ScheduleComponent 
              width={800}
              height={500}
              eventSettings = {{
                dataSource: schedule_data
              }}
            > 
              <Inject services={[Day, Week, Month, Agenda]} />
            </ScheduleComponent>
          </div>
        </div>
        <br></br>
        <div>
        <h2 style={{ color: '#A9E5DE' }}>Share Your Current Sleep With Us Here!</h2>
        <form onSubmit={handleSubmit}>
          {Object.entries(schedule).map(([day, { bedtime, waketime }]) => (
            <div key={day}>
              <h3>{day}</h3>
              <label>
                Bedtime:
                <input
                  type="text"
                  value={bedtime}
                  onChange={(e) => handleChange(e, day, 'bedtime')}
                />
              </label>
              <label>
                Waketime:
                <input
                  type="text"
                  value={waketime}
                  onChange={(e) => handleChange(e, day, 'waketime')}
                />
              </label>
            </div>
          ))}
          <br></br>
          <button style={{backgroundColor: "#A9E5DE", width: "100px", height: "50px"}} type="submit">Submit</button>
       
          </form>

      </div> 
      
        {adjustedSchedule && (
          <div>
            <h2>Adjusted Schedule</h2>
            <ul>
              {Object.entries(adjustedSchedule).map(([day, times]) => (
                <li key={day}>
                  {day}: Bedtime - {times.bedtime}, Waketime - {times.waketime}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
