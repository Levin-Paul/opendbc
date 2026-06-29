import { Shield, Wifi, WifiOff, Eye, Presentation, Play } from 'lucide-react'
import { Badge, Btn } from './ui/Panel'

export function TopNav({
  state,
  profiles,
  connected,
  onProfile,
  onSettings,
  onRunDemo,
  presentationMode,
  privacyMode,
}) {
  const status = state?.system_status || 'STANDBY'
  const statusColor =
    status === 'SECURE' ? 'green' : status === 'LOCKDOWN' ? 'red' : status === 'STANDBY' ? 'gray' : 'yellow'

  return (
    <header className="panel px-5 py-3 flex flex-wrap items-center gap-4 justify-between sticky top-0 z-40 backdrop-blur-md bg-[#0a0a0a]/90">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-blue-500/20 flex items-center justify-center glow-blue">
          <Shield className="w-6 h-6 text-blue-400" />
        </div>
        <div>
          <h1 className="text-lg font-bold tracking-tight">Vehicle Cybersecurity Gateway</h1>
          <p className="text-xs text-gray-500">Secure CAN · Offline-first · OpenDBC simulation</p>
        </div>
      </div>

      <div className="flex flex-wrap items-center gap-2">
        <Badge color={statusColor}>{status}</Badge>
        <Badge color={state?.vehicle_online ? 'green' : 'red'}>
          {state?.vehicle_online ? 'Vehicle Online' : 'Vehicle Offline'}
        </Badge>
        <Badge color={state?.session_active ? 'green' : 'gray'}>
          {state?.session_active ? `Session ${state.session_remaining_s}s` : 'No Session'}
        </Badge>
        <Badge color={connected ? 'blue' : 'gray'}>
          {connected ? <><Wifi className="w-3 h-3 inline" /> Live</> : <><WifiOff className="w-3 h-3 inline" /> WS</>}
        </Badge>
        {privacyMode && <Badge color="purple">PRIVACY MODE</Badge>}
      </div>

      <div className="flex flex-wrap items-center gap-2">
        <label className="text-xs text-gray-500">Profile</label>
        <select
          className="bg-[#1e1e1e] border border-[#333] rounded-lg text-xs px-2 py-1.5"
          value={state?.vehicle?.profile_id || ''}
          onChange={(e) => onProfile(e.target.value)}
        >
          {profiles.map((p) => (
            <option key={p.id} value={p.id}>{p.label}</option>
          ))}
        </select>
        <Btn variant="ghost" onClick={() => onSettings({ privacy_mode: !privacyMode })}>
          <Eye className="w-3 h-3 inline mr-1" /> Privacy
        </Btn>
        <Btn variant="ghost" onClick={() => onSettings({ presentation_mode: !presentationMode })}>
          <Presentation className="w-3 h-3 inline mr-1" /> Present
        </Btn>
        <Btn variant="purple" onClick={onRunDemo}>
          <Play className="w-3 h-3 inline mr-1" /> Demo Mode
        </Btn>
      </div>
    </header>
  )
}
