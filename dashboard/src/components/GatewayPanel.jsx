import { Server } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { Panel, Badge } from './ui/Panel'

export function GatewayPanel({ gateway, lockdown }) {
  const queue = gateway?.queue || []

  return (
    <Panel title="Security Gateway (ESP32)" icon={Server} accent={lockdown ? 'red' : 'blue'}>
      <div className="flex gap-2 mb-3">
        <Badge color={gateway?.controls_allowed ? 'green' : 'gray'}>
          Controls {gateway?.controls_allowed ? 'Allowed' : 'Denied'}
        </Badge>
        {lockdown && <Badge color="red">LOCKDOWN</Badge>}
      </div>
      <p className="text-xs text-gray-500 mb-2">Incoming request queue</p>
      <div className="space-y-2 max-h-40 overflow-y-auto">
        <AnimatePresence>
          {queue.length === 0 && (
            <p className="text-xs text-gray-600 font-mono">Awaiting requests…</p>
          )}
          {queue.slice().reverse().map((req, i) => (
            <motion.div
              key={`${req.ts}-${i}`}
              initial={{ opacity: 0, x: -12 }}
              animate={{ opacity: 1, x: 0 }}
              className="text-xs font-mono bg-[#1a1a1a] rounded px-2 py-1.5 border border-[#2a2a2a] flex justify-between"
            >
              <span>{req.operation}</span>
              <Badge color={req.status === 'allowed' ? 'green' : req.status === 'blocked' ? 'red' : 'yellow'}>
                {req.status}
              </Badge>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
      <div className="mt-3 text-[10px] text-gray-600 space-y-1">
        <p>READ_RPM → allowed (authenticated)</p>
        <p>ENGINE_SHUTDOWN → blocked</p>
      </div>
    </Panel>
  )
}
