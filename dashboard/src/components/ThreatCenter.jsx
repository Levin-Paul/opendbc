import { Swords } from 'lucide-react'
import { Panel, Btn } from './ui/Panel'

const ATTACKS = [
  { id: 'unauthorized', label: 'Unauthorized Device Connection' },
  { id: 'replay', label: 'Replay Attack' },
  { id: 'can_injection', label: 'Rogue CAN Injection' },
  { id: 'ecu_flash', label: 'ECU Flash Attempt' },
  { id: 'dos', label: 'Denial of Service' },
  { id: 'spoofing', label: 'Device Spoofing' },
  { id: 'tampering', label: 'Physical Tampering' },
  { id: 'obd_bypass', label: 'OBD Port Bypass' },
  { id: 'power_cut', label: 'Gateway Power Cut' },
  { id: 'mitm', label: 'MITM Interception' },
]

export function ThreatCenter({ onAttack }) {
  return (
    <Panel title="Threat Simulation Center" icon={Swords} accent="red" className="border-red-900/30">
      <p className="text-xs text-gray-500 mb-3">Conceptual simulation only — no real offensive tooling</p>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
        {ATTACKS.map((a) => (
          <Btn key={a.id} variant="danger" className="text-left !text-[11px]" onClick={() => onAttack(a.id)}>
            {a.label}
          </Btn>
        ))}
      </div>
    </Panel>
  )
}
