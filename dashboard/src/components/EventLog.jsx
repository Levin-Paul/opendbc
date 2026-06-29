import { Terminal } from 'lucide-react'
import { Panel } from './ui/Panel'

const LEVEL_COLOR = {
  green: 'text-green-400',
  red: 'text-red-400',
  yellow: 'text-yellow-400',
  blue: 'text-blue-400',
  info: 'text-gray-300',
}

export function EventLog({ events, privacyMode }) {
  return (
    <Panel title="Event Timeline" icon={Terminal}>
      {privacyMode ? (
        <p className="text-xs text-purple-400 font-mono">Logging disabled — privacy mode active</p>
      ) : (
        <div className="font-mono text-[11px] h-48 overflow-y-auto space-y-0.5 bg-[#0d0d0d] rounded p-2 border border-[#222]">
          {(events || []).slice().reverse().map((e, i) => (
            <p key={i} className={LEVEL_COLOR[e.level] || LEVEL_COLOR.info}>
              [{e.timestamp}] {e.message}
            </p>
          ))}
        </div>
      )}
    </Panel>
  )
}
