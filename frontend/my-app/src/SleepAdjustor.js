import React from "react";

export class Sleeper {
    constructor(current_bedtime, current_waketime, score) {
        this.bedtime = current_bedtime;
        this.waketime = current_waketime;
        this.sleepscore = score;
    }

    adjustSleep(target_bedtimes, target_waketimes) {
        const days = Math.min(target_bedtimes.length, target_waketimes.length);
        const bedtime_adjustment = [];
        const waketime_adjustment = [];
        for (let i = 0; i < days; i++) {
            const target_bedtime = target_bedtimes[i];
            const target_waketime = target_waketimes[i];
            const bedtime = this.bedtime + (i / (days - 1)) * (target_bedtime - this.bedtime);
            const waketime = this.waketime + (i / (days - 1)) * (target_waketime - this.waketime);
            bedtime_adjustment.push(bedtime);
            waketime_adjustment.push(waketime);
        }
        return [bedtime_adjustment, waketime_adjustment];
    }
}

export class Event {
    constructor(label, start_time, end_time, event_type = 'static', priority = 0) {
        this.label = label;
        this.priority = priority;
        this.event_type = event_type;
        this.duration = null;
        if (typeof start_time === 'string' && start_time.includes(':')) {
            this.start_time = this.timeToDecimal(start_time);
        } else {
            this.start_time = null;
        }
        if (typeof end_time === 'string' && end_time.includes(':')) {
            this.end_time = this.timeToDecimal(end_time);
        } else {
            const parsedEnd = parseFloat(end_time);
            if (!isNaN(parsedEnd)) {
                this.duration = parsedEnd;
            }
            this.end_time = null;
        }
    }

    timeToDecimal(timeStr) {
        const [hours, minutes] = timeStr.split(':').map(Number);
        return hours + minutes / 60;
    }

    formatTime(timeDecimal) {
        const hours = Math.floor(timeDecimal);
        const minutes = Math.round((timeDecimal % 1) * 60);
        return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`;
    }

    toString() {
        const startDisplay = this.start_time !== null ? this.formatTime(this.start_time) : "Flexible";
        const endDisplay = this.end_time !== null ? this.formatTime(this.end_time) : `${this.duration} hours`;
        return `${this.label}: ${startDisplay} - ${endDisplay} (${this.event_type}, Priority: ${this.priority})`;
    }
}

export class CalendarLogic {
    constructor() {
        this.days = {};
        for (let i = 0; i < 7; i++) {
            this.days[`Day ${i + 1}`] = [];
        }
    }

    addEvent(day, event) {
        this.days[day].push(event);
        this.resolveConflicts(day);
    }

    resolveConflicts(day) {
        const events = this.days[day].sort((a, b) => {
            if (a.start_time !== null && b.start_time !== null) {
                return a.start_time - b.start_time;
            }
            return 0;
        });
        for (let i = 0; i < events.length - 1; i++) {
            const current = events[i];
            const nextEvent = events[i + 1];
            if (current.end_time !== null && nextEvent.start_time !== null && current.end_time > nextEvent.start_time) {
                if (current.priority > nextEvent.priority) {
                    nextEvent.start_time = current.end_time;
                    if (nextEvent.duration !== null) {
                        nextEvent.end_time = nextEvent.start_time + nextEvent.duration;
                    }
                } else {
                    current.end_time = nextEvent.start_time;
                }
            }
        }
    }

    findFreeSlots(day) {
        const freeSlots = [];
        let endOfLastEvent = 0;
        const events = this.days[day].sort((a, b) => {
            if (a.start_time !== null && b.start_time !== null) {
                return a.start_time - b.start_time;
            }
            return 0;
        });
        for (const event of events) {
            if (event.start_time !== null && event.start_time > endOfLastEvent) {
                freeSlots.push([endOfLastEvent, event.start_time]);
            }
            if (event.end_time !== null) {
                endOfLastEvent = Math.max(endOfLastEvent, event.end_time);
            }
        }
        if (endOfLastEvent < 24) {
            freeSlots.push([endOfLastEvent, 24]);
        }
        return freeSlots;
    }

    placeDynamicEvents() {
        for (const day in this.days) {
            const freeSlots = this.findFreeSlots(day);
            for (const event of this.days[day]) {
                if (event.event_type === 'dynamic' && event.start_time === null) {
                    for (const [start, end] of freeSlots) {
                        if (end - start >= event.duration) {
                            event.start_time = start;
                            event.end_time = start + event.duration;
                            break;
                        }
                    }
                }
            }
        }
    }

    displayWeek() {
        for (const day in this.days) {
            console.log(`Events on ${day}:`);
            for (const event of this.days[day]) {
                console.log(event.toString());
            }
        }
    }
}

export class SleepAdjustor extends React.Component {
    render() {
        const { currentBedtimes, currentWaketimes } = this.props;

        // Parse currentBedtimes and currentWaketimes as numbers
        const parsedBedtimes = currentBedtimes.map(time => parseInt(time, 10));
        const parsedWaketimes = currentWaketimes.map(time => parseInt(time, 10));

        const mySleeper = new Sleeper(parsedBedtimes, parsedWaketimes, 87);

        const target_bedtimes = [22, 22, 22, 22, 22, 22, 22];
        const target_waketimes = [7, 7, 7, 7, 7, 7, 7];

        const modCurrBed = mySleeper.adjustSleep(target_bedtimes, target_waketimes)[0];
        const modCurrWake = mySleeper.adjustSleep(target_bedtimes, target_waketimes)[1];

        const daysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

        return (
            <div>
                <h2>Adjusted Sleep and Wake Times</h2>
                <table>
                    <thead>
                        <tr>
                            <th></th>
                            {daysOfWeek.map((day, index) => (
                                <th key={index}>{day}</th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Sleep Time</td>
                            {modCurrBed.map((time, index) => (
                                <td key={index}>{time}</td>
                            ))}
                        </tr>
                        <tr>
                            <td>Wake Time</td>
                            {modCurrWake.map((time, index) => (
                                <td key={index}>{time}</td>
                            ))}
                        </tr>
                    </tbody>
                </table>
            </div>
        );
    }
}


// // Usage example
// const calendar = new Calendar();
// const sleeper = new Sleeper(1, 12); // Current bedtime and wake time
// const [bedtimes, waketimes] = sleeper.adjustSleep(23, 8, 7);

// for (let i = 0; i < 7; i++) {
//     const bedtime = `${Math.floor(bedtimes[i])}:${Math.round((bedtimes[i] % 1) * 60).toString().padStart(2, '0')}`;
//     const waketime = `${Math.floor(waketimes[i])}:${Math.round((waketimes[i] % 1) * 60).toString().padStart(2, '0')}`;
//     calendar.addEvent(`Day ${i + 1}`, new Event('Sleep', bedtime, waketime, 'static', 10));
// }

// // Add more complex event scenarios including dynamic events without specified times
// calendar.addEvent('Day 1', new Event('Work', '09:00', '17:00', 'static', 1));
// calendar.addEvent('Day 1', new Event('Meeting', '10:00', '11:00', 'static', 5));

// calendar.addEvent('Day 1', new Event('Study Time', null, '2', 'dynamic', 3)); // 2 hours needed, no start time set

// calendar.placeDynamicEvents(); // Place dynamic events in free slots
// calendar.displayWeek();
