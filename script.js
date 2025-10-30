const targetDate = new Date('January 1, 2026 00:00:00');
const intervalDuration = 1000;

const daysEl = document.getElementById('days');
const hoursEl = document.getElementById('hours');
const minutesEl = document.getElementById('minutes');
const secondsEl = document.getElementById('seconds');
const messageEl = document.getElementById('message');

function formatNumber(value) {
  return String(value).padStart(2, '0');
}

function updateCountdown() {
  const now = new Date();
  const difference = targetDate.getTime() - now.getTime();

  if (difference <= 0) {
    clearInterval(timerId);
    daysEl.textContent = '00';
    hoursEl.textContent = '00';
    minutesEl.textContent = '00';
    secondsEl.textContent = '00';
    messageEl.textContent = 'È arrivato il momento!';
    messageEl.hidden = false;
    return;
  }

  const totalSeconds = Math.floor(difference / 1000);
  const days = Math.floor(totalSeconds / (24 * 60 * 60));
  const hours = Math.floor((totalSeconds % (24 * 60 * 60)) / (60 * 60));
  const minutes = Math.floor((totalSeconds % (60 * 60)) / 60);
  const seconds = totalSeconds % 60;

  daysEl.textContent = formatNumber(days);
  hoursEl.textContent = formatNumber(hours);
  minutesEl.textContent = formatNumber(minutes);
  secondsEl.textContent = formatNumber(seconds);
  messageEl.hidden = true;
}

const timerId = setInterval(updateCountdown, intervalDuration);
updateCountdown();
