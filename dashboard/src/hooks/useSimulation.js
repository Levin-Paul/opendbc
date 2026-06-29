import { useCallback, useEffect, useState } from 'react'
import { api } from '../api/client'

const WS_URL = `${window.location.protocol === 'https:' ? 'wss' : 'ws'}://${window.location.host}/ws`

export function useSimulation() {
  const [state, setState] = useState(null)
  const [profiles, setProfiles] = useState([])
  const [connected, setConnected] = useState(false)
  const [alert, setAlert] = useState(null)
  const [demoStep, setDemoStep] = useState(null)
  const [shake, setShake] = useState(false)

  const refresh = useCallback(async () => {
    const [s, p] = await Promise.all([api.getState(), api.getProfiles()])
    setState(s)
    setProfiles(p)
  }, [])

  useEffect(() => {
    refresh()
    const ws = new WebSocket(WS_URL)
    ws.onopen = () => setConnected(true)
    ws.onclose = () => setConnected(false)
    ws.onmessage = (ev) => {
      const msg = JSON.parse(ev.data)
      if (msg.type === 'state') setState(msg.payload)
      if (msg.type === 'attack' && msg.payload?.alert) {
        setAlert(msg.payload)
        if (msg.payload.shake) {
          setShake(true)
          setTimeout(() => setShake(false), 600)
        }
        if (msg.payload.fullscreen) {
          setTimeout(() => setAlert(null), 5000)
        } else {
          setTimeout(() => setAlert(null), 4000)
        }
      }
      if (msg.type === 'demo_step') setDemoStep(msg.payload)
    }
    return () => ws.close()
  }, [refresh])

  const runAttack = async (type) => {
    const r = await api.attack(type)
    if (r.alert) setAlert(r)
    if (r.shake) {
      setShake(true)
      setTimeout(() => setShake(false), 600)
    }
    return r
  }

  return {
    state,
    profiles,
    connected,
    alert,
    demoStep,
    shake,
    api,
    refresh,
    runAttack,
    setAlert,
  }
}
