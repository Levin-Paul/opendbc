import { ShieldAlert } from 'lucide-react'
import { motion } from 'framer-motion'
import { Panel, Badge } from './ui/Panel'

export function FirewallPanel({ firewall, onRead }) {
  const active = firewall?.active_rule
  const allowed = firewall?.rules?.filter((r) => r.action === 'allow') || []
  const blocked = firewall?.rules?.filter((r) => r.action === 'block') || []

  return (
    <Panel title="CAN Firewall" icon={ShieldAlert} accent="green">
      <div className="flex flex-wrap gap-2 mb-3 text-[10px]">
        {firewall?.replay_detection && <Badge color="blue">Replay detection</Badge>}
        {firewall?.rate_limited && <Badge color="yellow">Rate limited</Badge>}
        {firewall?.session_validation && <Badge color="green">Session valid</Badge>}
      </div>
      <div className="grid grid-cols-2 gap-3 text-xs">
        <div>
          <p className="text-green-400 font-semibold mb-1">ALLOWED</p>
          <ul className="space-y-1">
            {allowed.map((r) => (
              <motion.li
                key={r.id}
                className={`font-mono ${active === r.id ? 'text-green-300 glow-green px-1 rounded' : 'text-gray-400'}`}
                animate={active === r.id ? { scale: [1, 1.05, 1] } : {}}
                onClick={() => onRead(r.id)}
              >
                ✓ {r.id.replace(/_/g, ' ')}
              </motion.li>
            ))}
          </ul>
        </div>
        <div>
          <p className="text-red-400 font-semibold mb-1">BLOCKED</p>
          <ul className="space-y-1">
            {blocked.map((r) => (
              <motion.li
                key={r.id}
                className={`font-mono ${active === r.id ? 'text-red-300 glow-red px-1 rounded' : 'text-gray-500'}`}
                animate={active === r.id ? { scale: [1, 1.05, 1] } : {}}
              >
                ✗ {r.id.replace(/_/g, ' ')}
              </motion.li>
            ))}
          </ul>
        </div>
      </div>
    </Panel>
  )
}
