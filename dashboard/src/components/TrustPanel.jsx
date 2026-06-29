import { Fingerprint } from 'lucide-react'
import { Panel } from './ui/Panel'

const TRUST = [
  'No cloud dependency',
  'User-owned cryptographic keys',
  'Offline-first authentication',
  'No continuous telemetry collection',
  'No manufacturer lock-in',
  'User-controlled privacy mode',
  'Local encrypted logs only',
  'No remote override by vendor',
]

export function TrustPanel() {
  return (
    <Panel title="Trust & Privacy Architecture" icon={Fingerprint} accent="green">
      <ul className="space-y-1.5 text-xs text-gray-300">
        {TRUST.map((t) => (
          <li key={t} className="flex gap-2">
            <span className="text-green-400">✓</span> {t}
          </li>
        ))}
      </ul>
      <p className="mt-4 text-sm font-semibold text-center text-green-400/90 italic">
        Trustless by design. User-controlled by default.
      </p>
    </Panel>
  )
}
