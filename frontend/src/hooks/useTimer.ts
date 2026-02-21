import { useState, useRef, useCallback } from 'react';

interface UseTimerReturn {
    time: number;
    formattedTime: string;
    start: () => void;
    stop: () => void;
    reset: () => void;
    formatTime: (ms: number) => string;
}

export const useTimer = (): UseTimerReturn => {
    const [time, setTime] = useState<number>(0);
    const intervalRef = useRef<NodeJS.Timeout | null>(null);

    const start = useCallback((): void => {
        if (intervalRef.current) return;
        intervalRef.current = setInterval(() => {
            setTime(prev => prev + 10);
        }, 10);
    }, []);

    const stop = useCallback((): void => {
        if (intervalRef.current) {
            clearInterval(intervalRef.current);
            intervalRef.current = null;
        }
    }, []);

    const reset = useCallback((): void => {
        stop();
        setTime(0);
    }, [stop]);

    const formatTime = useCallback((ms: number): string => {
        const min = Math.floor(ms / 60000);
        const sec = Math.floor((ms % 60000) / 1000);
        const cs = Math.floor((ms % 1000) / 10);
        return `${min.toString().padStart(2, '0')}:${sec.toString().padStart(2, '0')}.${cs.toString().padStart(2, '0')}`;
    }, []);

    return {
        time,
        formattedTime: formatTime(time),
        start,
        stop,
        reset,
        formatTime
    };
};