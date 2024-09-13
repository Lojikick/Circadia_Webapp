import React, { useState } from 'react';
function App() {
  const [schedule, setSchedule] = useState({
    Monday: { bedtime: '', waketime: '' },
    Tuesday: { bedtime: '', waketime: '' },
    Wednesday: { bedtime: '', waketime: '' },
    Thursday: { bedtime: '', waketime: '' },
    Friday: { bedtime: '', waketime: '' }
  });
  const [adjustedSchedule, setAdjustedSchedule] = useState(null);
  const [hypnogramUrl, setHypnogramUrl] = useState('');
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
    try {
      const response = await fetch('/generate_hypnogram', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(schedule)
      });
      const data = await response.json();
      setAdjustedSchedule(data.adjustedSchedule); // Assuming the backend also sends adjusted sleep schedule
      setHypnogramUrl(`data:image/png;base64,${data.image}`);
    } catch (error) {
      console.error('Error:', error);
    }
  };
  return (
    <div className="app">
      <header className="header">
        <h1 style={{ color: '#A9E5DE', fontSize: '100px' }}>Good Morning!</h1>
        <h2 style={{ color: '#A9E5DE' }}>Let's get the day started:</h2>
      </header>
      <div className="flex-container">
        <div className="container">
          <h1 style={{color: 'white'}}>Sleep Score:</h1>
          <h1 style={{ color: 'white', fontSize: '90px' }}>77</h1>
          {hypnogramUrl && <img src={hypnogramUrl} alt="Hypnogram" />}
        </div>
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
          <button style={{backgroundColor: "#A9E5DE", width: "100px", height: "50px"}} type="submit">Submit</button>
        </form>
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