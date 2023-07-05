import { io } from 'socket.io-client'
import { useMemo, useState } from 'react';

export default function useServer(opts?: { port?: number | string | null }) {
    let [connected, setConnected] = useState(false);

    let port = opts?.port ?? new URL(window.location.href).searchParams.get('socketio_port')
    const socket = useMemo(() => io(`http://localhost:${port}`), [port]);

    socket.on('connect', () => setConnected(true));
    socket.on('disconnect', () => setConnected(false));

    return { server: socket, connected };
}