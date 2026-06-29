import { Radio } from 'lucide-react'
import { Panel } from './ui/Panel'

export function CanInspector({ frames, profileLabel }) {
  const latest = frames?.[frames.length - 1]

  return (
    <Panel title="CAN Packet Inspector (OpenDBC)" icon={Radio} accent="blue">
      <p className="text-xs text-gray-500 mb-2">Real DBC decode for {profileLabel}</p>
      {latest ? (
        <div className="font-mono text-xs space-y-2">
          <div className="bg-[#0d0d0d] rounded p-2 border border-[#333]">
            <p className="text-gray-500">RAW CAN MESSAGE</p>
            <p>ID: <span className="text-blue-400">{latest.address_hex}</span></p>
            <p>MSG: <span className="text-purple-400">{latest.message}</span></p>
            <p>DATA: <span className="text-yellow-300">{latest.data_hex}</span></p>
          </div>
          <div className="bg-[#0d0d0d] rounded p-2 border border-[#333]">
            <p className="text-gray-500 mb-1">DECODED</p>
            {(latest.decoded || []).map((d) => (
              <p key={d.signal}>
                <span className="text-green-400">{d.signal}</span>: {d.value} {d.unit}
              </p>
            ))}
            {(!latest.decoded || latest.decoded.length === 0) && (
              <p className="text-gray-600">No signals decoded (fallback telemetry active)</p>
            )}
          </div>
        </div>
      ) : (
        <p className="text-xs text-gray-600 font-mono">Waiting for CAN traffic…</p>
      )}
    </Panel>
  )
}
