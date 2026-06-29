import { Gauge, Car } from 'lucide-react'
import { Panel, Btn } from './ui/Panel'

function GaugeArc({ label, value, unit, max = 120 }) {
  const pct = Math.min(100, (value / max) * 100)
  return (
    <div className="flex flex-col items-center">
      <div className="relative w-20 h-20">
        <svg viewBox="0 0 100 100" className="w-full h-full -rotate-90">
          <circle cx="50" cy="50" r="42" fill="none" stroke="#2a2a2a" strokeWidth="8" />
          <circle
            cx="50" cy="50" r="42" fill="none" stroke="#3b82f6" strokeWidth="8"
            strokeDasharray={`${pct * 2.64} 264`}
            strokeLinecap="round"
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-lg font-bold">{value}</span>
          <span className="text-[9px] text-gray-500">{unit}</span>
        </div>
      </div>
      <span className="text-[10px] text-gray-500 mt-1">{label}</span>
    </div>
  )
}

export function VehiclePanel({ vehicle, api }) {
  if (!vehicle) return null
  const doors = vehicle.doors || {}
  const openDoors = Object.entries(doors).filter(([, v]) => v).map(([k]) => k)

  return (
    <Panel title="Virtual Vehicle" icon={Car} accent="blue">
      <p className="text-xs text-purple-400 mb-2">{vehicle.profile_label} · DBC: {vehicle.dbc}</p>
      <div className="flex justify-around mb-4">
        <GaugeArc label="RPM" value={vehicle.rpm} unit="rpm" max={7000} />
        <GaugeArc label="Speed" value={vehicle.speed_kph} unit="km/h" max={120} />
      </div>
      <div className="grid grid-cols-2 gap-2 text-xs font-mono mb-3">
        <div className="bg-[#1a1a1a] rounded p-2">Battery: <span className="text-green-400">{vehicle.battery_v}V</span></div>
        <div className="bg-[#1a1a1a] rounded p-2">Ignition: <span className={vehicle.ignition ? 'text-green-400' : 'text-gray-500'}>{vehicle.ignition ? 'ON' : 'OFF'}</span></div>
        <div className="bg-[#1a1a1a] rounded p-2">Steer: {vehicle.steering_angle}°</div>
        <div className="bg-[#1a1a1a] rounded p-2">Brake: {vehicle.brake_pressed ? 'YES' : 'NO'}</div>
        <div className="bg-[#1a1a1a] rounded p-2 col-span-2">Doors: {openDoors.length ? openDoors.join(', ') : 'All closed'}</div>
        <div className="bg-[#1a1a1a] rounded p-2 col-span-2">
          ECUs: {Object.entries(vehicle.ecus || {}).filter(([, v]) => v).map(([k]) => k.toUpperCase()).join(' · ') || 'None'}
        </div>
        {vehicle.tamper && <div className="col-span-2 text-red-400 animate-pulse">⚠ Tamper / Vibration detected</div>}
      </div>
      <div className="flex flex-wrap gap-2">
        <Btn onClick={() => api.ignition(!vehicle.ignition)}>Toggle Ignition</Btn>
        <Btn onClick={() => api.doors(true)}>Open Doors</Btn>
        <Btn onClick={() => api.doors(false)}>Close Doors</Btn>
        <Btn onClick={() => api.ecuOffline('eps')}>Disconnect EPS</Btn>
        <Btn onClick={() => api.batteryDrop()}>Battery Drop</Btn>
      </div>
    </Panel>
  )
}
