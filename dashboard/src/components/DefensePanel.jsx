import { motion } from 'framer-motion'
import { ShieldCheck } from 'lucide-react'
import { Panel } from './ui/Panel'

export function DefensePanel({ defense }) {
  const items = defense?.length ? defense : [
    { action: 'Monitoring CAN bus', color: 'blue' },
  ]

  return (
    <Panel title="Defense Response" icon={ShieldCheck} accent="green">
      <div className="space-y-2">
        {items.map((d, i) => (
          <motion.div
            key={`${d.action}-${i}`}
            initial={{ opacity: 0, y: 6 }}
            animate={{ opacity: 1, y: 0 }}
            className={`text-xs px-3 py-2 rounded-lg border ${
              d.color === 'red' ? 'border-red-500/40 bg-red-500/10 text-red-300' :
              d.color === 'yellow' ? 'border-yellow-500/40 bg-yellow-500/10 text-yellow-200' :
              'border-green-500/40 bg-green-500/10 text-green-300'
            }`}
          >
            {d.action}
          </motion.div>
        ))}
      </div>
    </Panel>
  )
}
