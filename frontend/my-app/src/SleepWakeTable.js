import React from 'react';

export default function SleepWakeTable({ currentBedtimes, currentWaketimes, onBedtimeChange, onWaketimeChange }) {
    const weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

    const handleBedtimeChange = (event, index) => {
        onBedtimeChange(index, parseInt(event.target.value));
    };

    const handleWaketimeChange = (event, index) => {
        onWaketimeChange(index, parseInt(event.target.value));
    };

    const renderRows = () => {
        return weekdays.map((day, index) => (
            <tr key={index}>
                <td>{day}</td>
                <td>
                    <input
                        type="number"
                        value={currentBedtimes[index]}
                        onChange={(event) => handleBedtimeChange(event, index)}
                    />
                </td>
                <td>
                    <input
                        type="number"
                        value={currentWaketimes[index]}
                        onChange={(event) => handleWaketimeChange(event, index)}
                    />
                </td>
            </tr>
        ));
    };

    return (
        <div>
            <h2>Sleep-Wake Times</h2>
            <table>
                <thead>
                    <tr>
                        <th>Weekday</th>
                        <th>Bedtime</th>
                        <th>Waketime</th>
                    </tr>
                </thead>
                <tbody>
                    {renderRows()}
                </tbody>
            </table>
        </div>
    );
}
