import { motion } from 'framer-motion'
import { Skull, Shield, Flame, Car } from 'lucide-react'
import { Panel } from './ui/Panel'

export function AttackMap({ flow }) {
  const blocked = flow === 'blocked' || flow === 'lockdown'
  const nodes = [
    { icon: Skull, label: 'Attacker', color: 'text-red-400' },
    { icon: Shield, label: 'Auth', color: 'text-yellow-400' },
    { icon: Shield, label: 'Gateway', color: 'text-blue-400' },
    { icon: Flame, label: 'Firewall', color: 'text-orange-400' },
    { icon: Car, label: 'Vehicle', color: 'text-green-400' },
  ]

  return (
    <Panel title="Attack Visualization" accent="red">
      <div className="flex items-center justify-center gap-1 py-4 flex-wrap">
        {nodes.map((n, i) => {
          const Icon = n.icon
          return (
            <div key={n.label} className="flex items-center">
              <div className="flex flex-col items-center px-2">
                <Icon className={`w-5 h-5 ${n.color}`} />
                <span className="text-[10px] text-gray-500">{n.label}</span>
              </div>
              {i < nodes.length - 1 && (
                <motion.div
                  className="w-8 h-1 bg-red-500/30 rounded relative overflow-hidden"
                  initial={false}
                >
                  <motion.div
                    className="absolute h-full w-2 bg-red-500 rounded"
                    animate={{ x: blocked ? [0, 24, 24] : [0, 32] }}
                    transition={{ repeat: Infinity, duration: 1, ease: 'linear' }}
                    style={{ opacity: blocked ? [1, 0.3, 0] : 1 }}
                  />
                </motion.div>
              )}
            </div>
          )
        })}
      </div>
      <p className="text-center text-[10px] text-gray-600">
        {blocked ? 'Attack packet stopped at gateway/firewall' : 'Red packets = attack traffic'}
      </p>
    </Panel>
  )
}
