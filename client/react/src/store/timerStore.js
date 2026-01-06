// store/timerStore.js
import { create } from "zustand";

export const useTimerStore = create((set, get) => ({
  seconds: 0,
  isRunning: false,
  intervalId: null,
  startTime: null,
  endTime: null,

  start: () => {
    if (get().intervalId) return;

    // ✅ set startTime only once
    if (!get().startTime) {
      const now = new Date();

      const formattedTime = now
        .toLocaleString('en-GB', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit',
          hourCycle: 'h23'
        })
        .replace(/\//g, '-')                         // 06-01-2026, 03:56:36
        .replace(/(\d{2})-(\d{2})-(\d{4})/, '$3-$2-$1') // 2026-01-06, 03:56:36
        .replace(', ', ' ');                         // remove comma
      console.log("⏱️ Session started at:", formattedTime);
      set({ startTime: formattedTime });
    }

    const id = setInterval(() => {
      set((state) => ({ seconds: state.seconds + 1 }));
    }, 1000);

    set({ intervalId: id, isRunning: true });
  },

  pause: () => {
    clearInterval(get().intervalId);
    set({ intervalId: null, isRunning: false });
  },

  reset: () => {
    clearInterval(get().intervalId);

    const endTime = new Date();
    const startTime = get().startTime;

    console.log("⏹️ Session ended at:", endTime.toLocaleString());
    set({ endTime: endTime })
    if (startTime) {
      const duration = Math.floor((endTime - startTime) / 1000);
      console.log("🕒 Total session duration:", duration, "seconds");
    }

    set({
      seconds: 0,
      intervalId: null,
      isRunning: false,
      startTime: null, // ✅ reset for next session
    });
  },
}));
