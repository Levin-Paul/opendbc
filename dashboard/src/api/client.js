const API = '/api'

async function post(path, body = {}) {
  const res = await fetch(`${API}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  return res.json()
}

export const api = {
  getState: () => fetch(`${API}/state`).then((r) => r.json()),
  getProfiles: () => fetch(`${API}/profiles`).then((r) => r.json()),
  setProfile: (profile_id) => post('/profile', { profile_id }),
  connect: () => post('/auth/connect'),
  challenge: () => post('/auth/challenge'),
  sign: () => post('/auth/sign'),
  disconnect: () => post('/auth/disconnect'),
  revoke: () => post('/auth/revoke'),
  enableControls: () => post('/controls/enable'),
  request: (operation) => post('/request', { operation }),
  attack: (type) => post(`/attack/${type}`),
  ignition: (on) => post('/vehicle/ignition', { on }),
  doors: (open) => post('/vehicle/doors', { open }),
  ecuOffline: (ecu) => post('/vehicle/ecu-offline', { ecu }),
  batteryDrop: () => post('/vehicle/battery-drop'),
  settings: (body) => post('/settings', body),
  runDemo: () => post('/demo/run'),
  resetDemo: () => post('/demo/reset'),
}
