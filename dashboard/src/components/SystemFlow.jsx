import { motion } from 'framer-motion'
import { Smartphone, KeyRound, Shield, Flame, Car } from 'lucide-react'
import { Panel } from './ui/Panel'

const NODES = [
  { id: 'user', label: 'User Device', icon: Smartphone },
  { id: 'auth', label: 'Authentication', icon: KeyRound },
  { id: 'gateway', label: 'Security Gateway', icon: Shield },
  { id: 'firewall', label: 'CAN Firewall', icon: Flame },
  { id: 'vehicle', label: 'Virtual Vehicle', icon: Car },
]

function glow(flow) {
  if (flow === 'secure') return 'glow-green border-green-500/50'
  if (flow === 'blocked') return 'glow-red border-red-500/50'
  if (flow === 'suspicious') return 'glow-yellow border-yellow-500/50'
  return 'glow-blue border-blue-500/40'
}

export function SystemFlow({ flow, presentationMode }) {
  const flowMap = {
    idle: 'normal',
    normal: 'normal',
    secure: 'secure',
    suspicious: 'suspicious',
    blocked: 'blocked',
    lockdown: 'blocked',
  }
  const mode = flowMap[flow] || 'normal'
  const blocked = mode === 'blocked'

  return (
    <Panel title="System Flow" className={presentationMode ? 'col-span-full' : ''} accent="blue">
      <div className={`flex flex-wrap items-center justify-center gap-2 ${presentationMode ? 'py-8' : 'py-4'}`}>
        {NODES.map((node, i) => {
          const Icon = node.icon
          return (
            <div key={node.id} className="flex items-center">
              <motion.div
                className={`panel px-4 py-3 flex flex-col items-center min-w-[110px] border ${glow(mode)}`}
                animate={{ scale: mode === 'secure' ? [1, 1.02, 1] : 1 }}
                transition={{ repeat: mode === 'secure' ? Infinity : 0, duration: 2 }}
              >
                <Icon className="w-6 h-6 mb-1 text-blue-400" />
                <span className="text-xs font-semibold text-center">{node.label}</span>
                <span className="text-[10px] text-gray-500 mt-1 capitalize">{flow}</span>
              </motion.div>
              {i < NODES.length - 1 && (
                <div className="relative w-12 md:w-20 h-8 mx-1 overflow-hidden">
                  <motion.div
                    className={`absolute top-1/2 left-0 w-3 h-3 rounded-full -translate-y-1/2 ${blocked ? 'bg-red-500' : 'bg-blue-400'}`}
                    animate={{ x: blocked ? [0, 40, 40] : [0, 80] }}
                    transition={{ duration: blocked ? 0.8 : 1.4, repeat: Infinity, ease: 'linear' }}
                    style={{ opacity: blocked ? [1, 1, 0] : 1 }}
                  />
                  <div className="absolute top-1/2 left-0 right-0 h-px bg-gradient-to-r from-blue-500/50 to-transparent" />
                </div>
              )}
            </div>
          )
        })}
      </div>
      <p className="text-center text-xs text-gray-500 mt-2">
        Blue = communication · Green = authenticated · Red = blocked attack
      </p>
    </Panel>
  )
}
